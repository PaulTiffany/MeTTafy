"""Typed Hyperon execution and state-liveness witnesses.

This layer is deliberately sibling to ``runtime_trace.check_emitted_provenance``:
the artifact checker proves that expected provenance survived serialization;
this module records what a MeTTa engine actually observed. Neither channel is
allowed to silently stand in for source-to-target semantic faithfulness.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .ir import ProvenanceEdge


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class MettaAtomWitness:
    atom: str
    metatype: str


@dataclass(frozen=True)
class MettaStep:
    form: str
    results: tuple[str, ...]
    added: tuple[str, ...]
    removed: tuple[str, ...]


@dataclass(frozen=True)
class HyperonExecutionTrace:
    trace_id: str
    artifact_id: str
    artifact_sha256: str
    engine: str
    engine_version: str
    ok: bool
    results: tuple[tuple[str, ...], ...]
    atoms: tuple[MettaAtomWitness, ...]
    steps: tuple[MettaStep, ...]
    error: str


class LivenessDecision(str, Enum):
    LIVE = "live"
    NOT_DEMONSTRATED = "not_demonstrated"
    INCONSISTENT = "inconsistent"
    INSUFFICIENT = "insufficient"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class StateLivenessProbe:
    """A caller-justified perturbation over one witnessed execution.

    Query indices address ``HyperonExecutionTrace.results``. Because every
    ``!`` evaluation contributes a result entry, state-mutating evaluations
    such as ``!(add-atom ...)`` also occupy indices.

    Step indices address ``HyperonExecutionTrace.steps``; the standalone ``!``
    parser marker is not itself a step.
    """

    dependency_id: str
    baseline_query_index: int
    perturbed_query_index: int
    restored_query_index: int
    mutation_step_index: int
    restoration_step_index: int


@dataclass(frozen=True)
class StateLivenessAssessment:
    dependency_id: str
    decision: LivenessDecision
    reason: str


def trace_from_record(
    emitted_metta: str,
    record: dict[str, Any],
    *,
    artifact_id: str = "artifact:semantic-metta",
) -> HyperonExecutionTrace:
    """Convert a driver record to a typed trace, failing closed on malformed data."""
    digest = _sha256(emitted_metta)
    trace_id = f"hyperon:{digest[:16]}"
    try:
        ok = record["ok"]
        engine = record["engine"]
        engine_version = record["engine_version"]
        error = record["error"]
        if not isinstance(ok, bool):
            raise TypeError("ok must be bool")
        if not all(isinstance(item, str) for item in (engine, engine_version, error)):
            raise TypeError("engine, engine_version, and error must be strings")

        raw_results = record["results"]
        raw_atoms = record["atoms"]
        raw_steps = record["steps"]
        if not all(isinstance(item, list) for item in (raw_results, raw_atoms, raw_steps)):
            raise TypeError("results, atoms, and steps must be lists")

        results = tuple(_string_tuple(result, "query result") for result in raw_results)
        atoms = tuple(_atom_witness(item) for item in raw_atoms)
        steps = tuple(_step_witness(item) for item in raw_steps)
    except (KeyError, TypeError, ValueError) as exc:
        return HyperonExecutionTrace(
            trace_id=trace_id,
            artifact_id=artifact_id,
            artifact_sha256=digest,
            engine="hyperon",
            engine_version="unknown",
            ok=False,
            results=(),
            atoms=(),
            steps=(),
            error=f"MalformedWitnessRecord: {exc}",
        )

    return HyperonExecutionTrace(
        trace_id=trace_id,
        artifact_id=artifact_id,
        artifact_sha256=digest,
        engine=engine,
        engine_version=engine_version,
        ok=ok,
        results=results,
        atoms=atoms,
        steps=steps,
        error=error,
    )


def run_hyperon_witness(
    emitted_metta: str,
    *,
    artifact_id: str = "artifact:semantic-metta",
    timeout_seconds: float = 10.0,
) -> HyperonExecutionTrace:
    """Run the shipped driver in a fresh isolated Python process.

    ``python -I`` keeps the witness process from inheriting user-site/PYTHONPATH
    state. It is process isolation, not a hostile-code sandbox.
    """
    driver = Path(__file__).with_name("hyperon_driver.py")
    with tempfile.TemporaryDirectory(prefix="mettafy-hyperon-") as tmp:
        root = Path(tmp)
        source_path = root / "artifact.metta"
        output_path = root / "witness.json"
        source_path.write_text(emitted_metta, encoding="utf-8")
        command = [
            sys.executable,
            "-I",
            str(driver),
            str(source_path),
            str(output_path),
        ]
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            record = _failure_record(
                f"TimeoutExpired: Hyperon witness exceeded {timeout_seconds:g}s"
            )
            return trace_from_record(emitted_metta, record, artifact_id=artifact_id)

        if not output_path.exists():
            detail = completed.stderr.strip() or completed.stdout.strip()
            record = _failure_record(
                f"DriverExit: code={completed.returncode}"
                + (f"; {detail}" if detail else "")
            )
            return trace_from_record(emitted_metta, record, artifact_id=artifact_id)

        try:
            loaded = json.loads(output_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            loaded = _failure_record(f"WitnessReadError: {type(exc).__name__}: {exc}")

    if not isinstance(loaded, dict):
        loaded = _failure_record("WitnessReadError: top-level record must be an object")
    return trace_from_record(emitted_metta, loaded, artifact_id=artifact_id)


def execution_links(trace: HyperonExecutionTrace) -> list[ProvenanceEdge]:
    """Link the artifact to an execution trace only when execution was observed."""
    if not trace.ok:
        return []
    return [
        ProvenanceEdge(
            relation="executed_as",
            source_id=trace.artifact_id,
            target_id=trace.trace_id,
        )
    ]


def assess_state_liveness(
    trace: HyperonExecutionTrace,
    probe: StateLivenessProbe,
) -> StateLivenessAssessment:
    """Assess whether a declared dependency is observably coupled to MeTTa state.

    ``not_demonstrated`` is intentionally not a "dead semantics" verdict: a
    chosen perturbation can be irrelevant, redundant, or absorbed by a robust
    strategy. Faithfulness is outside this function's authority.
    """
    if not trace.ok:
        return StateLivenessAssessment(
            dependency_id=probe.dependency_id,
            decision=LivenessDecision.UNAVAILABLE,
            reason=f"execution witness unavailable: {trace.error or 'unknown error'}",
        )

    try:
        baseline = trace.results[probe.baseline_query_index]
        perturbed = trace.results[probe.perturbed_query_index]
        restored = trace.results[probe.restored_query_index]
        mutation = trace.steps[probe.mutation_step_index]
        restoration = trace.steps[probe.restoration_step_index]
    except IndexError:
        return StateLivenessAssessment(
            dependency_id=probe.dependency_id,
            decision=LivenessDecision.INSUFFICIENT,
            reason="probe references a query or step outside the witnessed trace",
        )

    if not _step_changed(mutation) or not _step_changed(restoration):
        return StateLivenessAssessment(
            dependency_id=probe.dependency_id,
            decision=LivenessDecision.INSUFFICIENT,
            reason="declared perturbation/restoration did not both produce witnessed state deltas",
        )

    if _same_result_multiset(baseline, perturbed):
        return StateLivenessAssessment(
            dependency_id=probe.dependency_id,
            decision=LivenessDecision.NOT_DEMONSTRATED,
            reason="witnessed state changed, but the selected query result did not",
        )

    if not _same_result_multiset(baseline, restored):
        return StateLivenessAssessment(
            dependency_id=probe.dependency_id,
            decision=LivenessDecision.INCONSISTENT,
            reason="query changed under perturbation but did not return to baseline after restoration",
        )

    return StateLivenessAssessment(
        dependency_id=probe.dependency_id,
        decision=LivenessDecision.LIVE,
        reason="query changed under witnessed state perturbation and returned after restoration",
    )


def _atom_witness(value: Any) -> MettaAtomWitness:
    if not isinstance(value, dict):
        raise TypeError("atom witness must be an object")
    atom = value.get("atom")
    metatype = value.get("metatype")
    if not isinstance(atom, str) or not isinstance(metatype, str):
        raise TypeError("atom witness fields must be strings")
    return MettaAtomWitness(atom=atom, metatype=metatype)


def _step_witness(value: Any) -> MettaStep:
    if not isinstance(value, dict):
        raise TypeError("step witness must be an object")
    form = value.get("form")
    if not isinstance(form, str):
        raise TypeError("step form must be a string")
    return MettaStep(
        form=form,
        results=_string_tuple(value.get("results"), "step results"),
        added=_string_tuple(value.get("added"), "step added"),
        removed=_string_tuple(value.get("removed"), "step removed"),
    )


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{field} must be a list of strings")
    return tuple(value)


def _same_result_multiset(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return Counter(left) == Counter(right)


def _step_changed(step: MettaStep) -> bool:
    return bool(step.added or step.removed)


def _failure_record(error: str) -> dict[str, Any]:
    return {
        "ok": False,
        "engine": "hyperon",
        "engine_version": "unknown",
        "results": [],
        "atoms": [],
        "steps": [],
        "error": error,
    }

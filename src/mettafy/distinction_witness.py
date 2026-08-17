"""Observe whether a bounded recovered distinction survives source -> target runtime.

This module instruments emitted MeTTa with a read-only query for one recovered
provenance dependency and compares three executions: baseline, source-perturbed,
and restored.  It is intentionally narrower than semantic equivalence: the
result says only whether one selected distinction was preserved through the
observable compilation/runtime path.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from enum import Enum

from .derived_probe import ProbeJustification
from .hyperon_witness import HyperonExecutionTrace


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _dependency_atom(justification: ProbeJustification) -> str:
    edge = justification.dependency
    return (
        f"(Provenance {_quote(edge.relation)} "
        f"{_quote(edge.source_id)} {_quote(edge.target_id)})"
    )


def _query_count(emitted_metta: str) -> int:
    return sum(
        1
        for line in emitted_metta.splitlines()
        if line.lstrip().startswith("!")
    )


@dataclass(frozen=True)
class DependencyObservationProgram:
    canonical_artifact_id: str
    canonical_artifact_sha256: str
    instrumented_artifact_id: str
    instrumented_artifact_sha256: str
    instrumented_metta: str
    dependency_id: str
    query_index: int


class DistinctionDecision(str, Enum):
    PRESERVED = "preserved"
    COLLAPSED = "collapsed"
    INCONSISTENT = "inconsistent"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class DistinctionAssessment:
    dependency_id: str
    decision: DistinctionDecision
    reason: str
    baseline: tuple[str, ...]
    perturbed: tuple[str, ...]
    restored: tuple[str, ...]


def instrument_dependency_observation(
    emitted_metta: str,
    justification: ProbeJustification,
    *,
    canonical_artifact_id: str,
) -> DependencyObservationProgram:
    """Append one read-only exact-dependency query to an emitted artifact."""
    query_index = _query_count(emitted_metta)
    atom = _dependency_atom(justification)
    instrumented = emitted_metta + f"!(match &self {atom} Present)\n"
    canonical_digest = _sha256(emitted_metta)
    instrumented_digest = _sha256(instrumented)
    return DependencyObservationProgram(
        canonical_artifact_id=canonical_artifact_id,
        canonical_artifact_sha256=canonical_digest,
        instrumented_artifact_id=(
            f"{canonical_artifact_id}:observe:{instrumented_digest[:16]}"
        ),
        instrumented_artifact_sha256=instrumented_digest,
        instrumented_metta=instrumented,
        dependency_id=justification.dependency_id,
        query_index=query_index,
    )


def assess_distinction_preservation(
    baseline_trace: HyperonExecutionTrace,
    baseline_program: DependencyObservationProgram,
    perturbed_trace: HyperonExecutionTrace,
    perturbed_program: DependencyObservationProgram,
    restored_trace: HyperonExecutionTrace,
    restored_program: DependencyObservationProgram,
) -> DistinctionAssessment:
    """Assess a baseline -> perturb -> restore target observation triple."""
    traces = (baseline_trace, perturbed_trace, restored_trace)
    if any(not trace.ok for trace in traces):
        detail = "; ".join(trace.error or "unknown error" for trace in traces if not trace.ok)
        return DistinctionAssessment(
            dependency_id=baseline_program.dependency_id,
            decision=DistinctionDecision.UNAVAILABLE,
            reason=f"one or more target execution witnesses are unavailable: {detail}",
            baseline=(),
            perturbed=(),
            restored=(),
        )

    try:
        baseline = baseline_trace.results[baseline_program.query_index]
        perturbed = perturbed_trace.results[perturbed_program.query_index]
        restored = restored_trace.results[restored_program.query_index]
    except IndexError:
        return DistinctionAssessment(
            dependency_id=baseline_program.dependency_id,
            decision=DistinctionDecision.UNAVAILABLE,
            reason="one or more observation queries are outside the witnessed trace",
            baseline=(),
            perturbed=(),
            restored=(),
        )

    if baseline_program.dependency_id != perturbed_program.dependency_id or (
        baseline_program.dependency_id != restored_program.dependency_id
    ):
        return DistinctionAssessment(
            dependency_id=baseline_program.dependency_id,
            decision=DistinctionDecision.INCONSISTENT,
            reason="the three observations do not address the same recovered dependency",
            baseline=baseline,
            perturbed=perturbed,
            restored=restored,
        )

    if Counter(baseline) != Counter(restored):
        return DistinctionAssessment(
            dependency_id=baseline_program.dependency_id,
            decision=DistinctionDecision.INCONSISTENT,
            reason="restoration did not recover the baseline target observation",
            baseline=baseline,
            perturbed=perturbed,
            restored=restored,
        )

    if Counter(baseline) == Counter(perturbed):
        return DistinctionAssessment(
            dependency_id=baseline_program.dependency_id,
            decision=DistinctionDecision.COLLAPSED,
            reason="source perturbation did not change the selected target observation",
            baseline=baseline,
            perturbed=perturbed,
            restored=restored,
        )

    return DistinctionAssessment(
        dependency_id=baseline_program.dependency_id,
        decision=DistinctionDecision.PRESERVED,
        reason=(
            "selected target observation changed under source perturbation and "
            "returned after source restoration"
        ),
        baseline=baseline,
        perturbed=perturbed,
        restored=restored,
    )

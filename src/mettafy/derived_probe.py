"""Derive target-state liveness probes from recovered MeTTafy provenance.

The probe generator does not invent domain semantics.  It selects a provenance
dependency that MeTTafy's blind recognizer already promoted, verifies that the
exact dependency atom survived emission, and appends a reversible query /
remove / restore experiment to an *instrumented derivative* of the canonical
artifact.

This demonstrates that a recovered dependency participates in target runtime
state.  It does not establish source-to-target semantic faithfulness.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .hyperon_witness import HyperonExecutionTrace, StateLivenessProbe, execution_links
from .ir import ProvenanceEdge
from .recognition import RecognitionResult, RuleTrace


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _dependency_atom(edge: ProvenanceEdge) -> str:
    return (
        f"(Provenance {_quote(edge.relation)} "
        f"{_quote(edge.source_id)} {_quote(edge.target_id)})"
    )


def _dependency_id(edge: ProvenanceEdge) -> str:
    material = f"{edge.relation}\0{edge.source_id}\0{edge.target_id}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
    return f"dependency:{digest}"


def _top_level_form_count(emitted_metta: str) -> int:
    """Count the current emitter's one-form-per-line descriptive artifact."""
    return sum(
        1
        for line in emitted_metta.splitlines()
        if line.strip() and not line.lstrip().startswith(";")
    )


def _query_count(emitted_metta: str) -> int:
    return sum(
        1
        for line in emitted_metta.splitlines()
        if line.lstrip().startswith("!")
    )


@dataclass(frozen=True)
class ProbeJustification:
    dependency: ProvenanceEdge
    dependency_id: str
    rule_trace_id: str
    rule_id: str
    unit_id: str
    strategy_id: str
    observed_required_features: tuple[str, ...]


@dataclass(frozen=True)
class DerivedLivenessProgram:
    canonical_artifact_id: str
    canonical_artifact_sha256: str
    instrumented_artifact_id: str
    instrumented_artifact_sha256: str
    instrumented_metta: str
    justification: ProbeJustification
    probe: StateLivenessProbe


def derive_authorized_by_liveness_program(
    emitted_metta: str,
    result: RecognitionResult,
    *,
    canonical_artifact_id: str = "artifact:semantic-metta",
) -> DerivedLivenessProgram | None:
    """Instrument one promoted ``authorized_by`` dependency for a live probe.

    Selection is deterministic.  Only edges backed by a promoted rule trace and
    an emitted strategy are eligible.  If recognition produced no such edge,
    ``None`` is returned rather than manufacturing a dependency.
    """
    strategies = {strategy.id for strategy in result.strategies}
    promoted_traces = {
        trace.trace_id: trace for trace in result.rule_traces if trace.decision == "promote"
    }
    eligible: list[tuple[ProvenanceEdge, RuleTrace]] = []
    for edge in result.provenance_edges:
        trace = promoted_traces.get(edge.source_id)
        if (
            edge.relation == "authorized_by"
            and trace is not None
            and edge.target_id in strategies
        ):
            eligible.append((edge, trace))

    if not eligible:
        return None

    edge, trace = min(
        eligible,
        key=lambda item: (
            item[0].source_id,
            item[0].target_id,
            item[0].relation,
        ),
    )
    atom = _dependency_atom(edge)
    if atom not in emitted_metta.splitlines():
        raise ValueError(
            "eligible recovered dependency is absent from the emitted MeTTa artifact"
        )

    existing_queries = _query_count(emitted_metta)
    existing_steps = _top_level_form_count(emitted_metta)
    dependency_id = _dependency_id(edge)

    suffix = "\n".join(
        (
            f"!(match &self {atom} Present)",
            f"!(remove-atom &self {atom})",
            f"!(match &self {atom} Present)",
            f"!(add-atom &self {atom})",
            f"!(match &self {atom} Present)",
        )
    )
    instrumented = emitted_metta + suffix + "\n"
    canonical_digest = _sha256(emitted_metta)
    instrumented_digest = _sha256(instrumented)
    instrumented_id = (
        f"{canonical_artifact_id}:liveness-probe:{instrumented_digest[:16]}"
    )

    return DerivedLivenessProgram(
        canonical_artifact_id=canonical_artifact_id,
        canonical_artifact_sha256=canonical_digest,
        instrumented_artifact_id=instrumented_id,
        instrumented_artifact_sha256=instrumented_digest,
        instrumented_metta=instrumented,
        justification=ProbeJustification(
            dependency=edge,
            dependency_id=dependency_id,
            rule_trace_id=trace.trace_id,
            rule_id=trace.rule_id,
            unit_id=trace.local_id,
            strategy_id=edge.target_id,
            observed_required_features=trace.observed_required_features,
        ),
        probe=StateLivenessProbe(
            dependency_id=dependency_id,
            baseline_query_index=existing_queries,
            perturbed_query_index=existing_queries + 2,
            restored_query_index=existing_queries + 4,
            mutation_step_index=existing_steps + 1,
            restoration_step_index=existing_steps + 3,
        ),
    )


def derived_probe_links(
    program: DerivedLivenessProgram,
    trace: HyperonExecutionTrace,
) -> list[ProvenanceEdge]:
    """Link canonical artifact -> instrumented probe -> observed execution."""
    links = [
        ProvenanceEdge(
            relation="instrumented_as",
            source_id=program.canonical_artifact_id,
            target_id=program.instrumented_artifact_id,
        )
    ]
    if (
        trace.artifact_id == program.instrumented_artifact_id
        and trace.artifact_sha256 == program.instrumented_artifact_sha256
    ):
        links.extend(execution_links(trace))
    return links

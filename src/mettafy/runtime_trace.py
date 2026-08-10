from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .ir import ProvenanceEdge


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RuntimeTrace:
    """Deterministic trace for checking one emitted semantic artifact."""

    trace_id: str
    artifact_id: str
    artifact_sha256: str
    checker: str
    expected_edges: int
    verified_edges: int
    decision: str


@dataclass(frozen=True)
class WitnessRecord:
    """Certification record produced from a completed runtime trace."""

    witness_id: str
    runtime_trace_id: str
    decision: str
    artifact_sha256: str


def check_emitted_provenance(
    emitted_metta: str,
    *,
    provenance_edges: list[ProvenanceEdge],
    artifact_id: str = "artifact:semantic-metta",
) -> tuple[RuntimeTrace, WitnessRecord, list[ProvenanceEdge]]:
    """Check the emitted provenance graph and return typed certification linkage.

    This is an artifact checker, not a MeTTa evaluator. It verifies that every
    expected typed provenance edge survived deterministic serialization.
    """
    verified = 0
    for edge in provenance_edges:
        atom = (
            f'(Provenance "{edge.relation}" "{edge.source_id}" '
            f'"{edge.target_id}")'
        )
        if atom in emitted_metta:
            verified += 1

    digest = _sha256(emitted_metta)
    decision = "pass" if verified == len(provenance_edges) else "fail"
    trace_id = f"runtime:{digest[:16]}"
    witness_id = f"witness:{digest[:16]}"

    trace = RuntimeTrace(
        trace_id=trace_id,
        artifact_id=artifact_id,
        artifact_sha256=digest,
        checker="mettafy.runtime_trace.check_emitted_provenance.v1",
        expected_edges=len(provenance_edges),
        verified_edges=verified,
        decision=decision,
    )
    witness = WitnessRecord(
        witness_id=witness_id,
        runtime_trace_id=trace_id,
        decision=decision,
        artifact_sha256=digest,
    )
    links = [
        ProvenanceEdge(
            relation="checked_as",
            source_id=artifact_id,
            target_id=trace_id,
        ),
        ProvenanceEdge(
            relation="certified_by",
            source_id=trace_id,
            target_id=witness_id,
        ),
    ]
    return trace, witness, links

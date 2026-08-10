from __future__ import annotations

from dataclasses import dataclass

from .ir import ProvenanceEdge


@dataclass(frozen=True)
class ReductionState:
    """Source-neutral state summary at one side of a candidate reduction."""

    state_id: str
    boundary_sha256: str
    obstruction_measure: int

    def __post_init__(self) -> None:
        if self.obstruction_measure < 0:
            raise ValueError("obstruction_measure must be nonnegative")
        if len(self.boundary_sha256) != 64:
            raise ValueError("boundary_sha256 must be a SHA-256 hex digest")
        try:
            int(self.boundary_sha256, 16)
        except ValueError as exc:
            raise ValueError("boundary_sha256 must be hexadecimal") from exc


@dataclass(frozen=True)
class ReducibilityTrace:
    """White-box decision trace for one candidate structural reduction."""

    trace_id: str
    before_id: str
    after_id: str
    boundary_preserved: bool
    obstruction_before: int
    obstruction_after: int
    obstruction_decreased: bool
    decision: str
    reason: str


@dataclass(frozen=True)
class ReducibilityCertificate:
    """Certificate emitted only when both reducibility guards hold."""

    certificate_id: str
    trace_id: str
    before_id: str
    after_id: str
    boundary_sha256: str
    obstruction_before: int
    obstruction_after: int


def evaluate_reducibility(
    before: ReductionState,
    after: ReductionState,
) -> tuple[ReducibilityTrace, ReducibilityCertificate | None, list[ProvenanceEdge]]:
    """Certify a reduction iff the observable boundary is preserved and obstruction strictly decreases."""

    boundary_preserved = before.boundary_sha256 == after.boundary_sha256
    obstruction_decreased = after.obstruction_measure < before.obstruction_measure
    trace_id = f"reducibility:{before.state_id}:{after.state_id}"

    if not boundary_preserved:
        decision = "reject"
        reason = "observable boundary changed"
    elif not obstruction_decreased:
        decision = "reject"
        reason = "obstruction measure did not strictly decrease"
    else:
        decision = "certify"
        reason = "boundary preserved and obstruction measure strictly decreased"

    trace = ReducibilityTrace(
        trace_id=trace_id,
        before_id=before.state_id,
        after_id=after.state_id,
        boundary_preserved=boundary_preserved,
        obstruction_before=before.obstruction_measure,
        obstruction_after=after.obstruction_measure,
        obstruction_decreased=obstruction_decreased,
        decision=decision,
        reason=reason,
    )

    if decision != "certify":
        return trace, None, []

    certificate_id = f"certificate:{trace_id}"
    certificate = ReducibilityCertificate(
        certificate_id=certificate_id,
        trace_id=trace_id,
        before_id=before.state_id,
        after_id=after.state_id,
        boundary_sha256=before.boundary_sha256,
        obstruction_before=before.obstruction_measure,
        obstruction_after=after.obstruction_measure,
    )
    provenance = [
        ProvenanceEdge(
            relation="reduced_to",
            source_id=before.state_id,
            target_id=after.state_id,
        ),
        ProvenanceEdge(
            relation="justified_by",
            source_id=trace_id,
            target_id=certificate_id,
        ),
    ]
    return trace, certificate, provenance

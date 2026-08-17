from __future__ import annotations

from dataclasses import dataclass

from .ir import ProvenanceEdge, Strategy, StrategyKind


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
class LiftWitness:
    """Mechanical evidence that a reduced solution extends to the source state."""

    witness_id: str
    verified: bool


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
    lift_witness_id: str
    lift_verified: bool
    decision: str
    reason: str


@dataclass(frozen=True)
class ReducibilityCertificate:
    """Certificate emitted only when all reducibility guards hold."""

    certificate_id: str
    trace_id: str
    before_id: str
    after_id: str
    boundary_sha256: str
    obstruction_before: int
    obstruction_after: int
    lift_witness_id: str


def evaluate_reducibility(
    before: ReductionState,
    after: ReductionState,
    *,
    lift_witness: LiftWitness,
) -> tuple[ReducibilityTrace, ReducibilityCertificate | None, list[ProvenanceEdge]]:
    """Certify iff boundary is preserved, obstruction descends, and lift is verified."""

    boundary_preserved = before.boundary_sha256 == after.boundary_sha256
    obstruction_decreased = after.obstruction_measure < before.obstruction_measure
    trace_id = f"reducibility:{before.state_id}:{after.state_id}"

    if not boundary_preserved:
        decision = "reject"
        reason = "observable boundary changed"
    elif not obstruction_decreased:
        decision = "reject"
        reason = "obstruction measure did not strictly decrease"
    elif not lift_witness.verified:
        decision = "reject"
        reason = "reduced witness is not verified to lift to the source state"
    else:
        decision = "certify"
        reason = (
            "boundary preserved, obstruction measure strictly decreased, "
            "and reduced witness lifts to source"
        )

    trace = ReducibilityTrace(
        trace_id=trace_id,
        before_id=before.state_id,
        after_id=after.state_id,
        boundary_preserved=boundary_preserved,
        obstruction_before=before.obstruction_measure,
        obstruction_after=after.obstruction_measure,
        obstruction_decreased=obstruction_decreased,
        lift_witness_id=lift_witness.witness_id,
        lift_verified=lift_witness.verified,
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
        lift_witness_id=lift_witness.witness_id,
    )
    provenance = [
        ProvenanceEdge("reduced_to", before.state_id, after.state_id),
        ProvenanceEdge("lifts_via", after.state_id, lift_witness.witness_id),
        ProvenanceEdge("certified_reducible_by", before.state_id, certificate_id),
    ]
    return trace, certificate, provenance


def strategy_from_certificate(
    certificate: ReducibilityCertificate,
) -> tuple[Strategy, ProvenanceEdge]:
    """Promote only a mechanically certified reduction into Strategy IR."""

    strategy_id = f"certified:{certificate.before_id}:{certificate.after_id}:reduction"
    strategy = Strategy(id=strategy_id, kind=StrategyKind.REDUCTION, confidence=1.0)
    authorization = ProvenanceEdge(
        relation="authorized_by",
        source_id=certificate.certificate_id,
        target_id=strategy_id,
    )
    return strategy, authorization

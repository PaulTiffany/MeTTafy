from __future__ import annotations

from dataclasses import dataclass

from .ir import ProvenanceEdge, Strategy, StrategyKind


@dataclass(frozen=True)
class ReducibilityCertificate:
    """Source-neutral certificate for one boundary-preserving strict descent."""

    certificate_id: str
    local_id: str
    boundary_before: tuple[str, ...]
    boundary_after: tuple[str, ...]
    obstruction_before: int
    obstruction_after: int

    @property
    def boundary_preserved(self) -> bool:
        return self.boundary_before == self.boundary_after

    @property
    def strict_descent(self) -> bool:
        return self.obstruction_after < self.obstruction_before

    @property
    def valid(self) -> bool:
        return self.boundary_preserved and self.strict_descent


def certify_reducibility(
    certificate: ReducibilityCertificate,
) -> tuple[Strategy | None, list[ProvenanceEdge]]:
    """Promote Reducibility iff the explicit mechanical certificate is valid."""
    if certificate.obstruction_before < 0 or certificate.obstruction_after < 0:
        raise ValueError("obstruction measures must be non-negative")
    if not certificate.valid:
        return None, []

    strategy_id = f"cert:{certificate.local_id}:reducibility"
    strategy = Strategy(
        id=strategy_id,
        kind=StrategyKind.REDUCTION,
        confidence=1.0,
    )
    provenance = [
        ProvenanceEdge(
            relation="authorized_by",
            source_id=certificate.certificate_id,
            target_id=strategy_id,
        ),
        ProvenanceEdge(
            relation="preserves_boundary",
            source_id=certificate.certificate_id,
            target_id=strategy_id,
        ),
        ProvenanceEdge(
            relation="strictly_decreases",
            source_id=certificate.certificate_id,
            target_id=strategy_id,
        ),
    ]
    return strategy, provenance

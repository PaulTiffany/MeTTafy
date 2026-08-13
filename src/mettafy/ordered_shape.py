from __future__ import annotations

from dataclasses import dataclass

from mettafy.sequential_frontier import CleanFrontierTurn

Edge = tuple[str, str]


def _canonical_edge(left: str, right: str) -> Edge:
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True)
class PhysicalComponentShape:
    """Orientation-free physical fact learned by one complete clean turn.

    The graph is fixed, so the component carrier plus its induced edges, color
    pair, and frontier contact describe the resolved component independently of
    which direction the two colors were swapped.
    """

    color_pair: frozenset[int]
    vertices: frozenset[str]
    edges: frozenset[Edge]
    frontier_hits: frozenset[str]


def resolved_component_shape(turn: CleanFrontierTurn) -> PhysicalComponentShape:
    """Derive the retained physical shape fact from an exact current turn."""

    if not turn.valid:
        raise ValueError("ordered shape requires a valid clean frontier turn")

    seed_color = turn.before.coloring[turn.move.seed]
    color_pair = frozenset({seed_color, turn.move.other_color})
    edges: set[Edge] = set()
    for left in turn.component:
        for right in turn.before.graph[left]:
            if right in turn.component and left != right:
                edges.add(_canonical_edge(left, right))

    return PhysicalComponentShape(
        color_pair=color_pair,
        vertices=turn.component,
        edges=frozenset(edges),
        frontier_hits=turn.boundary_hits,
    )


@dataclass(frozen=True)
class OrderedShapeLedger:
    """Retained component-shape facts already resolved by the construction."""

    resolved: frozenset[PhysicalComponentShape] = frozenset()


@dataclass(frozen=True)
class ShapeProgressCertificate:
    """Certify one *new* resolved physical shape as genuine ordered progress.

    This certificate does not prove that every saturated planar construction
    always has fresh progress.  It only enforces the proof's distinction between
    a legal reversible graph symmetry and a genuinely new construction event.
    """

    before: OrderedShapeLedger
    turn: CleanFrontierTurn
    shape: PhysicalComponentShape

    @property
    def derived_shape_matches(self) -> bool:
        return self.turn.valid and self.shape == resolved_component_shape(self.turn)

    @property
    def fresh(self) -> bool:
        return self.shape not in self.before.resolved

    @property
    def valid(self) -> bool:
        return self.derived_shape_matches and self.fresh

    def commit(self) -> OrderedShapeLedger:
        if not self.valid:
            raise ValueError("resolved component replay is not fresh ordered progress")
        return OrderedShapeLedger(
            self.before.resolved | frozenset({self.shape})
        )


def certify_shape_progress(
    ledger: OrderedShapeLedger,
    turn: CleanFrontierTurn,
) -> ShapeProgressCertificate:
    return ShapeProgressCertificate(
        before=ledger,
        turn=turn,
        shape=resolved_component_shape(turn),
    )

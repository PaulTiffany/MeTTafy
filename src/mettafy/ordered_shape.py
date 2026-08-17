from __future__ import annotations

from dataclasses import dataclass

from mettafy.sequential_frontier import CleanFrontierTurn

Edge = tuple[str, str]
Lineage = tuple[frozenset[int], frozenset[str]]


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

    @property
    def lineage(self) -> Lineage:
        """Identity coordinates that survive an orientation/relabeling swap."""

        return (self.color_pair, self.frontier_hits)

    def same_lineage(self, earlier: PhysicalComponentShape) -> bool:
        return self.lineage == earlier.lineage

    def retains(self, earlier: PhysicalComponentShape) -> bool:
        """Whether this shape preserves every resolved fact in an earlier lineage state."""

        return (
            self.same_lineage(earlier)
            and earlier.vertices <= self.vertices
            and earlier.edges <= self.edges
        )

    def strictly_refines(self, earlier: PhysicalComponentShape) -> bool:
        """Theseus order: same lineage, all old structure retained, something added."""

        return self.retains(earlier) and self != earlier


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

    def lineage_shapes(
        self,
        shape: PhysicalComponentShape,
    ) -> frozenset[PhysicalComponentShape]:
        return frozenset(
            earlier for earlier in self.resolved if earlier.lineage == shape.lineage
        )


@dataclass(frozen=True)
class ShapeProgressCertificate:
    """Certify a consequential physical move modulo inconsequential labels.

    Equality in the orientation-free physical representation is replay, not
    progress.  A first observation of a lineage is new structure.  A revisit
    of an existing lineage counts only when it strictly refines every retained
    version of that lineage; an incompatible rewrite is not allowed to erase
    resolved constructional knowledge.

    This certificate does not prove that every saturated planar construction
    always has fresh progress.  It mechanically enforces the identity/refinement
    contract used by the ordered proof.
    """

    before: OrderedShapeLedger
    turn: CleanFrontierTurn
    shape: PhysicalComponentShape

    @property
    def derived_shape_matches(self) -> bool:
        return self.turn.valid and self.shape == resolved_component_shape(self.turn)

    @property
    def prior_lineage_shapes(self) -> frozenset[PhysicalComponentShape]:
        return self.before.lineage_shapes(self.shape)

    @property
    def equivalent_replay(self) -> bool:
        return self.shape in self.before.resolved

    @property
    def new_lineage(self) -> bool:
        return not self.prior_lineage_shapes

    @property
    def retains_prior_lineage(self) -> bool:
        return all(self.shape.retains(earlier) for earlier in self.prior_lineage_shapes)

    @property
    def strict_refinement(self) -> bool:
        prior = self.prior_lineage_shapes
        return (
            bool(prior)
            and self.retains_prior_lineage
            and any(self.shape.strictly_refines(earlier) for earlier in prior)
        )

    @property
    def consequential(self) -> bool:
        """A move adds a new lineage or strictly refines retained structure."""

        return self.new_lineage or self.strict_refinement

    @property
    def fresh(self) -> bool:
        return not self.equivalent_replay

    @property
    def valid(self) -> bool:
        return (
            self.derived_shape_matches
            and self.fresh
            and self.retains_prior_lineage
            and self.consequential
        )

    def commit(self) -> OrderedShapeLedger:
        if not self.valid:
            raise ValueError(
                "label-only replay or non-retentive rewrite is not ordered progress"
            )
        return OrderedShapeLedger(self.before.resolved | frozenset({self.shape}))


def certify_shape_progress(
    ledger: OrderedShapeLedger,
    turn: CleanFrontierTurn,
) -> ShapeProgressCertificate:
    return ShapeProgressCertificate(
        before=ledger,
        turn=turn,
        shape=resolved_component_shape(turn),
    )

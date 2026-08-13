from __future__ import annotations

from dataclasses import dataclass

from mettafy.color_construction import ConstructionState


@dataclass(frozen=True, order=True)
class RealizedStateIdentity:
    """Public identity of one realized construction state.

    ``color`` is part of the realized state identity.  This object does not
    model a vertex choosing a color; it records the state that actually exists
    at the verification boundary.
    """

    vertex: str
    color: int


def realized_state_identities(state: ConstructionState) -> frozenset[RealizedStateIdentity]:
    """Project a construction into the realized state identities visible publicly."""

    return frozenset(
        RealizedStateIdentity(vertex=vertex, color=color)
        for vertex, color in state.coloring.items()
    )


@dataclass(frozen=True)
class PublicRewriteObservation:
    """Judge one realized state rewrite without access to the chooser's policy.

    The public verifier receives only the state before, the carrier declared as
    transformed, and the realized successor.  Search heuristics, decision
    trees, and future routes are intentionally absent from this interface.

    This certificate establishes an exact observable rewrite, not fresh
    constructional progress.  A lawful inverse may therefore be valid here and
    still be rejected by the ordered-shape ledger as replay.
    """

    before: ConstructionState
    declared_carrier: frozenset[str]
    after: ConstructionState

    @property
    def same_graph(self) -> bool:
        return dict(self.before.graph) == dict(self.after.graph)

    @property
    def same_realized_carriers(self) -> bool:
        return set(self.before.coloring) == set(self.after.coloring)

    @property
    def changed_vertices(self) -> frozenset[str]:
        if not self.same_realized_carriers:
            return frozenset()
        return frozenset(
            vertex
            for vertex in self.before.coloring
            if self.before.coloring[vertex] != self.after.coloring[vertex]
        )

    @property
    def declared_carrier_is_exact(self) -> bool:
        return bool(self.declared_carrier) and self.declared_carrier == self.changed_vertices

    @property
    def untouched_identities_preserved(self) -> bool:
        if not self.same_realized_carriers:
            return False
        return all(
            self.before.coloring[vertex] == self.after.coloring[vertex]
            for vertex in self.before.coloring
            if vertex not in self.declared_carrier
        )

    @property
    def valid(self) -> bool:
        return (
            self.same_graph
            and self.same_realized_carriers
            and self.declared_carrier_is_exact
            and self.untouched_identities_preserved
            and self.before.committed_edges_valid
            and self.after.committed_edges_valid
        )

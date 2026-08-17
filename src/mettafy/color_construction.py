from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Mapping

from mettafy.four_color_ontology import FOUR_COLOR_SURFACE_GENUS, FOUR_COLOR_SURFACE_NAME

PALETTE4 = frozenset({0, 1, 2, 3})
Graph = Mapping[str, tuple[str, ...]]
Coloring = Mapping[str, int]


def _edge_set(graph: Graph) -> frozenset[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor not in graph:
                raise ValueError(f"unknown neighbor {neighbor!r}")
            edge = (vertex, neighbor) if vertex < neighbor else (neighbor, vertex)
            if edge[0] != edge[1]:
                edges.add(edge)
    return frozenset(edges)


@dataclass(frozen=True)
class ConstructionState:
    """A partial construction state in the fixed Four Color surface species.

    The surface species is fixed at genus zero and is intentionally not a state
    parameter. ``coloring`` contains only assignments already committed by the
    construction. Every committed edge obligation is exact.
    """

    surface_name: ClassVar[str] = FOUR_COLOR_SURFACE_NAME
    surface_genus: ClassVar[int] = FOUR_COLOR_SURFACE_GENUS

    graph: Graph
    coloring: Coloring

    def __post_init__(self) -> None:
        graph = {vertex: tuple(neighbors) for vertex, neighbors in self.graph.items()}
        coloring = dict(self.coloring)
        object.__setattr__(self, "graph", MappingProxyType(graph))
        object.__setattr__(self, "coloring", MappingProxyType(coloring))

        _edge_set(graph)
        unknown = set(coloring) - set(graph)
        if unknown:
            raise ValueError(f"coloring contains unknown vertices: {sorted(unknown)}")
        if any(color not in PALETTE4 for color in coloring.values()):
            raise ValueError("construction uses a terminal color outside Q4")
        if not self.committed_edges_valid:
            raise ValueError("construction violates an already committed edge")

    @property
    def committed_edges_valid(self) -> bool:
        return all(
            self.coloring[u] != self.coloring[v]
            for u, v in _edge_set(self.graph)
            if u in self.coloring and v in self.coloring
        )

    @property
    def complete(self) -> bool:
        return len(self.coloring) == len(self.graph)

    def neighbor_color_image(self, vertex: str) -> frozenset[int]:
        if vertex not in self.graph:
            raise ValueError(f"unknown vertex {vertex!r}")
        return frozenset(
            self.coloring[neighbor]
            for neighbor in self.graph[vertex]
            if neighbor in self.coloring
        )

    def admissible_colors(self, vertex: str) -> frozenset[int]:
        """The exact construction observable A(v) = Q4 minus c(N(v))."""

        return PALETTE4 - self.neighbor_color_image(vertex)

    def commit(self, vertex: str, color: int) -> ConstructionState:
        if vertex in self.coloring:
            raise ValueError("vertex is already committed")
        if color not in self.admissible_colors(vertex):
            raise ValueError("color is not admissible under current adjacency")
        updated = dict(self.coloring)
        updated[vertex] = color
        return ConstructionState(self.graph, updated)


@dataclass(frozen=True)
class BrownObservation:
    """A deliberately coarse bounded-observer projection."""

    terminal_support: frozenset[int]
    committed_vertices: int
    unresolved_vertices: int
    brown: bool


def brown_projection(state: ConstructionState) -> BrownObservation:
    unresolved = len(state.graph) - len(state.coloring)
    return BrownObservation(
        terminal_support=frozenset(state.coloring.values()),
        committed_vertices=len(state.coloring),
        unresolved_vertices=unresolved,
        brown=unresolved > 0,
    )


def terminal_decode(state: ConstructionState) -> dict[str, int]:
    """Return the four-color map only after every vertex is committed."""

    if not state.complete:
        raise ValueError("terminal decode requires a completed construction")
    if not state.committed_edges_valid:
        raise AssertionError("completed construction has an invalid edge ledger")
    return dict(state.coloring)


@dataclass(frozen=True)
class TraversalRewriteCertificate:
    """A graph-level construction rewrite certified by exact observables."""

    before: ConstructionState
    after: ConstructionState
    focus: str

    @property
    def same_graph(self) -> bool:
        return dict(self.before.graph) == dict(self.after.graph)

    @property
    def same_committed_vertices(self) -> bool:
        return set(self.before.coloring) == set(self.after.coloring)

    @property
    def focus_uncommitted(self) -> bool:
        return self.focus not in self.before.coloring and self.focus not in self.after.coloring

    @property
    def source_has_zero_focus_slack(self) -> bool:
        return not self.before.admissible_colors(self.focus)

    @property
    def target_has_focus_slack(self) -> bool:
        return bool(self.after.admissible_colors(self.focus))

    @property
    def valid(self) -> bool:
        return (
            self.same_graph
            and self.same_committed_vertices
            and self.focus_uncommitted
            and self.before.committed_edges_valid
            and self.after.committed_edges_valid
            and self.source_has_zero_focus_slack
            and self.target_has_focus_slack
        )

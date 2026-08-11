from __future__ import annotations

from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.color_construction import ConstructionState

BoundaryVertices5 = tuple[str, str, str, str, str]


@dataclass(frozen=True)
class AlternatingConnection:
    """A retained simple exterior path in one two-color subgraph."""

    path: tuple[str, ...]
    color_pair: frozenset[int]

    def valid_in(self, state: ConstructionState) -> bool:
        if len(self.path) < 2 or len(set(self.path)) != len(self.path):
            return False
        if len(self.color_pair) != 2:
            return False
        if any(vertex not in state.coloring for vertex in self.path):
            return False
        if any(state.coloring[vertex] not in self.color_pair for vertex in self.path):
            return False
        return all(
            right in state.graph[left]
            for left, right in zip(self.path, self.path[1:])
        )


@dataclass(frozen=True)
class LockedC5Witness:
    """The exterior information that makes a saturated C5 one-step locked.

    For the canonical boundary roles A-B-A-C-D, both B-C and B-D alternating
    continuations are retained explicitly.  This object deliberately expands
    beyond the pentagon instead of projecting the lock back to local data.
    """

    state: ConstructionState
    focus: str
    boundary: BoundaryVertices5
    pivot_to_first_flank: AlternatingConnection
    pivot_to_second_flank: AlternatingConnection

    @property
    def boundary_colors(self) -> tuple[int, int, int, int, int]:
        colors = tuple(self.state.coloring[vertex] for vertex in self.boundary)
        return (colors[0], colors[1], colors[2], colors[3], colors[4])

    @property
    def defects(self) -> C5DefectState:
        return C5DefectState(self.boundary_colors)

    @property
    def witness_vertices(self) -> frozenset[str]:
        return frozenset(
            self.boundary
            + self.pivot_to_first_flank.path
            + self.pivot_to_second_flank.path
        )

    @property
    def expansion_size(self) -> int:
        """Finite retained witness size; not yet the descent quantity."""

        return len(self.witness_vertices)

    @property
    def valid(self) -> bool:
        if self.focus in self.state.coloring:
            return False
        if len(set(self.boundary)) != 5:
            return False
        if any(vertex not in self.state.coloring for vertex in self.boundary):
            return False
        if any(
            self.boundary[(index + 1) % 5] not in self.state.graph[vertex]
            for index, vertex in enumerate(self.boundary)
        ):
            return False
        if any(self.focus not in self.state.graph[vertex] for vertex in self.boundary):
            return False

        defects = self.defects
        if not defects.is_saturated_four_color_boundary:
            return False
        roles = defects.saturated_roles
        pivot_vertex = self.boundary[roles.pivot_index]
        flank_vertices = tuple(self.boundary[index] for index in roles.flank_indices)
        flank_colors = roles.flank_colors

        expected_pairs = (
            frozenset({roles.pivot_color, flank_colors[0]}),
            frozenset({roles.pivot_color, flank_colors[1]}),
        )
        connections = (
            self.pivot_to_first_flank,
            self.pivot_to_second_flank,
        )
        for connection, flank_vertex, expected_pair in zip(
            connections, flank_vertices, expected_pairs
        ):
            if not connection.valid_in(self.state):
                return False
            if connection.color_pair != expected_pair:
                return False
            if connection.path[0] != pivot_vertex or connection.path[-1] != flank_vertex:
                return False

        return True

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TypeAlias

from mettafy.color_construction import ConstructionState
from mettafy.plane_dual_pairing import DegreeFiveDualPairing, Pair, toggle_cut_endpoints
from mettafy.plane_parameterization import (
    COLOR_TO_V4,
    V4,
    color_difference,
    frontier_modes,
    v4_add,
)
from mettafy.zero_point_correspondence import (
    DUAL_DEFECT_FAMILY,
    ControlParameterization,
    same_construction_state,
)

Edge: TypeAlias = tuple[str, str]
Face: TypeAlias = tuple[str, str, str]
BoundaryVertices5: TypeAlias = tuple[str, str, str, str, str]
DualNode: TypeAlias = str

V4_TO_COLOR = {mode: color for color, mode in COLOR_TO_V4.items()}


def canonical_edge(left: str, right: str) -> Edge:
    if left == right:
        raise ValueError("self-loop is outside the simple planar carrier")
    return (left, right) if left < right else (right, left)


def _graph_edges(state: ConstructionState) -> frozenset[Edge]:
    return frozenset(
        canonical_edge(vertex, neighbor)
        for vertex, neighbors in state.graph.items()
        for neighbor in neighbors
        if vertex != neighbor
    )


@dataclass(frozen=True)
class DegreeFiveTriangulatedEmbedding:
    """Retained spherical embedding witness around one uncommitted degree-five focus.

    Removing the five focus triangles leaves a triangulated disk whose cyclic
    boundary is exactly ``boundary``.  This is witness data, not a mutable
    surface parameter of the Four Color construction state.
    """

    state: ConstructionState
    focus: str
    boundary: BoundaryVertices5
    faces: tuple[Face, ...]

    @property
    def boundary_colors(self) -> tuple[int, int, int, int, int]:
        colors = tuple(self.state.coloring[vertex] for vertex in self.boundary)
        return (colors[0], colors[1], colors[2], colors[3], colors[4])

    @property
    def disk_faces(self) -> tuple[Face, ...]:
        if not self.valid:
            raise ValueError("embedding witness is not valid")
        return tuple(face for face in self.faces if self.focus not in face)

    @property
    def valid(self) -> bool:
        if self.state.surface_genus != 0 or not self.state.committed_edges_valid:
            return False
        if self.focus in self.state.coloring or self.focus not in self.state.graph:
            return False
        if tuple(self.state.graph[self.focus]) != self.boundary:
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
        if any(len(set(face)) != 3 for face in self.faces):
            return False

        graph_edges = _graph_edges(self.state)
        face_edge_counts: Counter[Edge] = Counter()
        for face in self.faces:
            if any(vertex not in self.state.graph for vertex in face):
                return False
            for left, right in zip(face, face[1:] + face[:1]):
                edge = canonical_edge(left, right)
                if edge not in graph_edges:
                    return False
                face_edge_counts[edge] += 1

        if set(face_edge_counts) != set(graph_edges):
            return False
        if any(count != 2 for count in face_edge_counts.values()):
            return False
        if len(self.state.graph) - len(graph_edges) + len(self.faces) != 2:
            return False

        expected_focus_faces = {
            frozenset(
                {
                    self.focus,
                    self.boundary[index],
                    self.boundary[(index + 1) % 5],
                }
            )
            for index in range(5)
        }
        actual_focus_faces = {
            frozenset(face) for face in self.faces if self.focus in face
        }
        if actual_focus_faces != expected_focus_faces:
            return False

        committed = set(self.state.coloring)
        disk_faces = tuple(face for face in self.faces if self.focus not in face)
        if any(any(vertex not in committed for vertex in face) for face in disk_faces):
            return False
        if any(
            len({self.state.coloring[vertex] for vertex in face}) != 3
            for face in disk_faces
        ):
            return False
        return _committed_subgraph_connected(self.state)


@dataclass(frozen=True)
class DualContinuationPath:
    """One actual selected-mode path in the embedded dual disk."""

    terminal_edges: Pair
    crossed_edges: tuple[Edge, ...]

    @property
    def valid(self) -> bool:
        left, right = self.terminal_edges
        return (
            left != right
            and left in range(5)
            and right in range(5)
            and bool(self.crossed_edges)
            and len(set(self.crossed_edges)) == len(self.crossed_edges)
        )


@dataclass(frozen=True)
class EmbeddedDualContinuation:
    """Graph-derived dual continuation network for one singleton V4 mode."""

    embedding: DegreeFiveTriangulatedEmbedding
    translation_mode: V4
    paths: tuple[DualContinuationPath, DualContinuationPath]

    @property
    def terminal_pairing(self) -> tuple[Pair, Pair]:
        return (self.paths[0].terminal_edges, self.paths[1].terminal_edges)

    @property
    def valid(self) -> bool:
        if not self.embedding.valid:
            return False
        if any(not path.valid for path in self.paths):
            return False
        try:
            pairing = DegreeFiveDualPairing(
                self.embedding.boundary_colors,
                self.translation_mode,
            )
        except ValueError:
            return False
        observed_terminals = frozenset(
            terminal
            for path in self.paths
            for terminal in path.terminal_edges
        )
        if observed_terminals != frozenset(pairing.terminal_edges):
            return False
        return self.terminal_pairing in pairing.pairing_options


@dataclass(frozen=True)
class DualDomainParameter:
    """Nonzero V4 domain-translation parameter anchored at one exact z0."""

    chart: ControlParameterization
    continuation: EmbeddedDualContinuation
    path: DualContinuationPath
    translated_vertices: frozenset[str]

    @property
    def translation_mode(self) -> V4:
        return self.continuation.translation_mode

    @property
    def valid(self) -> bool:
        if self.chart.family != DUAL_DEFECT_FAMILY or not self.chart.valid:
            return False
        if not self.continuation.valid or self.path not in self.continuation.paths:
            return False
        embedding = self.continuation.embedding
        if not same_construction_state(self.chart.base, embedding.state):
            return False
        components = _cut_components(self.chart.base, frozenset(self.path.crossed_edges))
        if len(components) != 2 or self.translated_vertices not in components:
            return False
        if not self.translated_vertices or set(self.translated_vertices) == set(
            self.chart.base.coloring
        ):
            return False
        return all(
            color_difference(
                self.chart.base.coloring[left],
                self.chart.base.coloring[right],
            )
            != self.translation_mode
            for left, right in self.path.crossed_edges
        )


@dataclass(frozen=True)
class DualDomainNonzeroCertificate:
    """Exact graph-level realization of an embedding-derived nonzero dual parameter."""

    parameter: DualDomainParameter
    after: ConstructionState

    @property
    def target_has_focus_slack(self) -> bool:
        focus = self.parameter.continuation.embedding.focus
        return bool(self.after.admissible_colors(focus))

    @property
    def valid(self) -> bool:
        if not self.parameter.valid:
            return False
        before = self.parameter.chart.base
        replayed = _translate_state(
            before,
            self.parameter.translated_vertices,
            self.parameter.translation_mode,
        )
        if not same_construction_state(replayed, self.after):
            return False
        if same_construction_state(before, self.after):
            return False

        embedding = self.parameter.continuation.embedding
        before_modes = _mode_word5(frontier_modes(embedding.boundary_colors))
        expected_modes = toggle_cut_endpoints(
            before_modes,
            self.parameter.translation_mode,
            self.parameter.path.terminal_edges,
        )
        after_boundary = tuple(
            self.after.coloring[vertex] for vertex in embedding.boundary
        )
        after_modes = _mode_word5(frontier_modes(after_boundary))
        return expected_modes == after_modes


def derive_embedded_dual_continuation(
    embedding: DegreeFiveTriangulatedEmbedding,
    translation_mode: V4,
) -> EmbeddedDualContinuation:
    """Derive the actual boundary-terminal pairing from the retained embedding."""

    if not embedding.valid:
        raise ValueError("a valid triangulated embedding witness is required")

    pairing = DegreeFiveDualPairing(embedding.boundary_colors, translation_mode)
    boundary_edges = {
        canonical_edge(
            embedding.boundary[index],
            embedding.boundary[(index + 1) % 5],
        ): index
        for index in range(5)
    }

    edge_faces: dict[Edge, list[int]] = {}
    for face_index, face in enumerate(embedding.disk_faces):
        for left, right in zip(face, face[1:] + face[:1]):
            edge_faces.setdefault(canonical_edge(left, right), []).append(face_index)

    adjacency: dict[DualNode, list[tuple[DualNode, Edge]]] = {}
    for edge, incident_faces in edge_faces.items():
        left, right = edge
        mode = color_difference(
            embedding.state.coloring[left],
            embedding.state.coloring[right],
        )
        if mode == translation_mode:
            continue

        if edge in boundary_edges:
            if len(incident_faces) != 1:
                raise AssertionError("disk boundary edge must meet one disk face")
            terminal = _terminal_node(boundary_edges[edge])
            face_node = _face_node(incident_faces[0])
            _add_dual_edge(adjacency, terminal, face_node, edge)
        else:
            if len(incident_faces) != 2:
                raise AssertionError("interior disk edge must meet two disk faces")
            first = _face_node(incident_faces[0])
            second = _face_node(incident_faces[1])
            _add_dual_edge(adjacency, first, second, edge)

    for face_index in range(len(embedding.disk_faces)):
        if len(adjacency.get(_face_node(face_index), [])) != 2:
            raise AssertionError(
                "selected-mode dual degree must equal two at every disk triangle"
            )
    for terminal_index in pairing.terminal_edges:
        if len(adjacency.get(_terminal_node(terminal_index), [])) != 1:
            raise AssertionError("selected boundary terminal must have dual degree one")

    paths = _terminal_paths(adjacency, pairing.terminal_edges)
    continuation = EmbeddedDualContinuation(
        embedding=embedding,
        translation_mode=translation_mode,
        paths=(paths[0], paths[1]),
    )
    if not continuation.valid:
        raise AssertionError("embedding-derived dual continuation failed certification")
    return continuation


def derive_dual_domain_parameters(
    chart: ControlParameterization,
    embedding: DegreeFiveTriangulatedEmbedding,
    translation_mode: V4,
) -> tuple[DualDomainParameter, DualDomainParameter]:
    """Expose the two actual nonzero path controls based at the chart's shared z0."""

    if chart.family != DUAL_DEFECT_FAMILY or not chart.valid:
        raise ValueError("parameterization is not a valid V4 dual-defect chart")
    if not same_construction_state(chart.base, embedding.state):
        raise ValueError("dual chart and embedding witness must share the same zero-point")

    continuation = derive_embedded_dual_continuation(embedding, translation_mode)
    parameters: list[DualDomainParameter] = []
    for path in continuation.paths:
        components = _cut_components(chart.base, frozenset(path.crossed_edges))
        if len(components) != 2:
            raise AssertionError("embedded dual path did not produce a two-sided primal cut")
        side = min(
            components,
            key=lambda component: (len(component), tuple(sorted(component))),
        )
        parameter = DualDomainParameter(
            chart=chart,
            continuation=continuation,
            path=path,
            translated_vertices=side,
        )
        if not parameter.valid:
            raise AssertionError("embedding-derived nonzero dual parameter is invalid")
        parameters.append(parameter)
    return (parameters[0], parameters[1])


def apply_dual_nonzero_parameter(
    parameter: DualDomainParameter,
) -> DualDomainNonzeroCertificate:
    """Realize one embedding-derived domain translation from its exact zero-point."""

    if not parameter.valid:
        raise ValueError("nonzero dual parameter is not valid at its zero-point")
    after = _translate_state(
        parameter.chart.base,
        parameter.translated_vertices,
        parameter.translation_mode,
    )
    certificate = DualDomainNonzeroCertificate(parameter, after)
    if not certificate.valid:
        raise AssertionError("nonzero dual parameter failed exact graph certification")
    return certificate


def _translate_state(
    state: ConstructionState,
    vertices: frozenset[str],
    translation_mode: V4,
) -> ConstructionState:
    updated = dict(state.coloring)
    for vertex in vertices:
        current_mode = COLOR_TO_V4[updated[vertex]]
        updated[vertex] = V4_TO_COLOR[v4_add(current_mode, translation_mode)]
    return ConstructionState(state.graph, updated)


def _cut_components(
    state: ConstructionState,
    crossed_edges: frozenset[Edge],
) -> tuple[frozenset[str], ...]:
    remaining = set(state.coloring)
    components: list[frozenset[str]] = []
    while remaining:
        seed = min(remaining)
        seen = {seed}
        frontier = [seed]
        while frontier:
            vertex = frontier.pop()
            for neighbor in state.graph[vertex]:
                if neighbor not in state.coloring or neighbor in seen:
                    continue
                if canonical_edge(vertex, neighbor) in crossed_edges:
                    continue
                seen.add(neighbor)
                frontier.append(neighbor)
        remaining.difference_update(seen)
        components.append(frozenset(seen))
    return tuple(components)


def _committed_subgraph_connected(state: ConstructionState) -> bool:
    if not state.coloring:
        return False
    return len(_cut_components(state, frozenset())) == 1


def _add_dual_edge(
    adjacency: dict[DualNode, list[tuple[DualNode, Edge]]],
    left: DualNode,
    right: DualNode,
    primal_edge: Edge,
) -> None:
    adjacency.setdefault(left, []).append((right, primal_edge))
    adjacency.setdefault(right, []).append((left, primal_edge))


def _terminal_paths(
    adjacency: dict[DualNode, list[tuple[DualNode, Edge]]],
    terminals: tuple[int, int, int, int],
) -> tuple[DualContinuationPath, DualContinuationPath]:
    paths: list[DualContinuationPath] = []
    consumed: set[int] = set()
    for start_index in sorted(terminals):
        if start_index in consumed:
            continue
        start = _terminal_node(start_index)
        previous: DualNode | None = None
        current = start
        crossed: list[Edge] = []
        seen: set[DualNode] = set()

        while True:
            if current in seen:
                raise AssertionError("terminal continuation entered a dual cycle")
            seen.add(current)
            if current.startswith("t:") and current != start:
                end_index = int(current.split(":", 1)[1])
                break
            choices = [
                (neighbor, edge)
                for neighbor, edge in adjacency[current]
                if neighbor != previous
            ]
            if len(choices) != 1:
                raise AssertionError("selected-mode continuation is not a simple dual path")
            next_node, primal_edge = choices[0]
            crossed.append(primal_edge)
            previous, current = current, next_node

        consumed.update({start_index, end_index})
        pair = (start_index, end_index)
        if pair[0] > pair[1]:
            pair = (pair[1], pair[0])
        paths.append(DualContinuationPath(pair, tuple(crossed)))

    if len(paths) != 2:
        raise AssertionError("four selected boundary terminals must yield two dual paths")
    paths.sort(key=lambda path: path.terminal_edges)
    return (paths[0], paths[1])


def _face_node(index: int) -> DualNode:
    return f"f:{index}"


def _terminal_node(index: int) -> DualNode:
    return f"t:{index}"


def _mode_word5(modes: tuple[V4, ...]) -> tuple[V4, V4, V4, V4, V4]:
    if len(modes) != 5:
        raise ValueError("degree-five boundary must have five derivative modes")
    return (modes[0], modes[1], modes[2], modes[3], modes[4])

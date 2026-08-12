from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TypeAlias

from mettafy.dual_path_switching import (
    certify_alternating_path_switch,
    disk_primal_edges,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    Edge,
    canonical_edge,
)
from mettafy.plane_parameterization import NONZERO_MODES, V4, color_difference

DualNode: TypeAlias = tuple[str, int]


@dataclass(frozen=True)
class ModeMatching:
    """One exact V4-mode matching in the trivalent disk dual.

    Every properly colored disk triangle has exactly one primal edge of each
    nonzero V4 mode.  In the dual, each mode is therefore a matching on face
    nodes, with boundary edges terminating at boundary half-edge nodes.
    """

    mode: V4
    primal_edges: frozenset[Edge]

    @property
    def valid(self) -> bool:
        return self.mode in NONZERO_MODES and bool(self.primal_edges)


@dataclass(frozen=True)
class AlternatingComponent:
    """One path or cycle in the union of two mode matchings."""

    excluded_mode: V4
    terminals: tuple[int, ...]
    primal_edges: frozenset[Edge]
    face_indices: frozenset[int]

    @property
    def is_cycle(self) -> bool:
        return not self.terminals

    @property
    def valid(self) -> bool:
        return (
            self.excluded_mode in NONZERO_MODES
            and len(self.terminals) in (0, 2)
            and len(set(self.terminals)) == len(self.terminals)
            and all(index in range(5) for index in self.terminals)
            and bool(self.primal_edges)
            and bool(self.face_indices)
        )


@dataclass(frozen=True)
class TrivalentDualSpliceSignature:
    """Full three-matching connectivity retained by the colored disk dual.

    Boundary terminal pairings alone forget internal alternating cycles and the
    physical way the three V4 matchings splice through common triangle nodes.
    This signature keeps the three content-addressed physical matchings and
    derives every two-mode path/cycle component from the retained embedding.
    """

    embedding: DegreeFiveTriangulatedEmbedding
    matchings: tuple[ModeMatching, ModeMatching, ModeMatching]

    @property
    def valid(self) -> bool:
        if not self.embedding.valid:
            return False
        if tuple(matching.mode for matching in self.matchings) != NONZERO_MODES:
            return False
        if any(not matching.valid for matching in self.matchings):
            return False

        disk_edges = disk_primal_edges(self.embedding)
        carriers = tuple(matching.primal_edges for matching in self.matchings)
        if frozenset().union(*carriers) != disk_edges:
            return False
        if any(
            carriers[left].intersection(carriers[right])
            for left in range(3)
            for right in range(left + 1, 3)
        ):
            return False

        for face in self.embedding.disk_faces:
            face_edges = frozenset(
                canonical_edge(face[index], face[(index + 1) % 3])
                for index in range(3)
            )
            if any(len(face_edges.intersection(carrier)) != 1 for carrier in carriers):
                return False

        return all(
            component.valid
            for mode in NONZERO_MODES
            for component in self.components(mode)
        )

    def matching_edges(self, mode: V4) -> frozenset[Edge]:
        if mode not in NONZERO_MODES:
            raise ValueError("matching mode must be nonzero in V4")
        for matching in self.matchings:
            if matching.mode == mode:
                return matching.primal_edges
        raise AssertionError("valid splice signature lost a V4 matching")

    def components(self, excluded_mode: V4) -> tuple[AlternatingComponent, ...]:
        """All terminal paths and internal cycles of the other two matchings."""

        return _alternating_components(self.embedding, excluded_mode)

    def terminal_pairing(self, excluded_mode: V4) -> tuple[tuple[int, int], ...]:
        return tuple(
            (component.terminals[0], component.terminals[1])
            for component in self.components(excluded_mode)
            if len(component.terminals) == 2
        )

    def cycle_carriers(self, excluded_mode: V4) -> tuple[frozenset[Edge], ...]:
        return tuple(
            component.primal_edges
            for component in self.components(excluded_mode)
            if component.is_cycle
        )

    @property
    def total_alternating_cycles(self) -> int:
        return sum(len(self.cycle_carriers(mode)) for mode in NONZERO_MODES)


def trivalent_dual_splice_signature(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> TrivalentDualSpliceSignature:
    """Derive the exact three-edge-colored trivalent dual splice state."""

    if not embedding.valid:
        raise ValueError("a valid retained triangulated embedding is required")
    disk_edges = disk_primal_edges(embedding)
    matchings = tuple(
        ModeMatching(
            mode=mode,
            primal_edges=frozenset(
                edge
                for edge in disk_edges
                if color_difference(
                    embedding.state.coloring[edge[0]],
                    embedding.state.coloring[edge[1]],
                )
                == mode
            ),
        )
        for mode in NONZERO_MODES
    )
    signature = TrivalentDualSpliceSignature(
        embedding=embedding,
        matchings=(matchings[0], matchings[1], matchings[2]),
    )
    if not signature.valid:
        raise AssertionError("trivalent dual splice signature failed certification")
    return signature


@dataclass(frozen=True)
class MatchingPathSwitchCertificate:
    """Exact Kempe-style switch of the two complementary dual matchings."""

    parameter: DualDomainParameter
    before: TrivalentDualSpliceSignature
    after: TrivalentDualSpliceSignature
    path_edges: frozenset[Edge]

    @property
    def valid(self) -> bool:
        if not self.parameter.valid or not self.before.valid or not self.after.valid:
            return False
        if self.parameter.continuation.embedding != self.before.embedding:
            return False
        sigma = self.parameter.translation_mode
        if self.path_edges != frozenset(self.parameter.path.crossed_edges):
            return False
        if self.before.matching_edges(sigma) != self.after.matching_edges(sigma):
            return False
        for mode in NONZERO_MODES:
            if mode == sigma:
                continue
            if self.after.matching_edges(mode) != self.before.matching_edges(
                mode
            ).symmetric_difference(self.path_edges):
                return False
        return True


def certify_matching_path_switch(
    parameter: DualDomainParameter,
) -> MatchingPathSwitchCertificate:
    """Lift a certified domain translation to the three dual matchings."""

    switch = certify_alternating_path_switch(parameter)
    before = trivalent_dual_splice_signature(parameter.continuation.embedding)
    after = trivalent_dual_splice_signature(switch.after_embedding)
    certificate = MatchingPathSwitchCertificate(
        parameter=parameter,
        before=before,
        after=after,
        path_edges=frozenset(parameter.path.crossed_edges),
    )
    if not certificate.valid:
        raise AssertionError("dual matching path switch failed exact certification")
    return certificate


def _alternating_components(
    embedding: DegreeFiveTriangulatedEmbedding,
    excluded_mode: V4,
) -> tuple[AlternatingComponent, ...]:
    if excluded_mode not in NONZERO_MODES:
        raise ValueError("excluded mode must be nonzero in V4")

    boundary_edges = {
        canonical_edge(
            embedding.boundary[index],
            embedding.boundary[(index + 1) % 5],
        ): index
        for index in range(5)
    }
    edge_faces: dict[Edge, list[int]] = defaultdict(list)
    for face_index, face in enumerate(embedding.disk_faces):
        for index in range(3):
            edge_faces[
                canonical_edge(face[index], face[(index + 1) % 3])
            ].append(face_index)

    adjacency: dict[DualNode, list[tuple[DualNode, Edge]]] = defaultdict(list)
    for edge, incident_faces in edge_faces.items():
        if color_difference(
            embedding.state.coloring[edge[0]],
            embedding.state.coloring[edge[1]],
        ) == excluded_mode:
            continue
        if edge in boundary_edges:
            if len(incident_faces) != 1:
                raise AssertionError("disk boundary edge must meet exactly one disk face")
            left = ("t", boundary_edges[edge])
            right = ("f", incident_faces[0])
        else:
            if len(incident_faces) != 2:
                raise AssertionError("interior disk edge must meet exactly two disk faces")
            left = ("f", incident_faces[0])
            right = ("f", incident_faces[1])
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))

    for face_index in range(len(embedding.disk_faces)):
        if len(adjacency[("f", face_index)]) != 2:
            raise AssertionError("two-mode dual degree must be two at every disk triangle")
    for node, neighbors in adjacency.items():
        if node[0] == "t" and len(neighbors) != 1:
            raise AssertionError("selected boundary terminal must have degree one")

    unseen = set(adjacency)
    components: list[AlternatingComponent] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        nodes: set[DualNode] = {seed}
        edges: set[Edge] = set()
        while stack:
            node = stack.pop()
            for neighbor, primal_edge in adjacency[node]:
                edges.add(primal_edge)
                if neighbor not in nodes:
                    nodes.add(neighbor)
                    stack.append(neighbor)
        unseen.difference_update(nodes)
        terminals = tuple(sorted(node[1] for node in nodes if node[0] == "t"))
        component = AlternatingComponent(
            excluded_mode=excluded_mode,
            terminals=terminals,
            primal_edges=frozenset(edges),
            face_indices=frozenset(node[1] for node in nodes if node[0] == "f"),
        )
        if not component.valid:
            raise AssertionError("alternating dual component failed certification")
        components.append(component)

    return tuple(
        sorted(
            components,
            key=lambda component: (
                component.terminals,
                tuple(sorted(component.primal_edges)),
            ),
        )
    )

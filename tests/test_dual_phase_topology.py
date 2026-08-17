from __future__ import annotations

from collections import Counter, defaultdict, deque
from typing import TypeAlias

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_control_topology_delta import certify_dual_control_topology_delta
from mettafy.dual_path_switching import dual_pairing_signature
from mettafy.dual_phase_topology import certify_phase_topology
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    Edge,
    canonical_edge,
)

Face: TypeAlias = tuple[str, str, str]
DiskFaces: TypeAlias = tuple[Face, ...]

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"
DISK_FACES: DiskFaces = (
    ("b", "x0", "x1"),
    ("x1", "x2", "x0"),
    ("e", "x2", "d"),
    ("a", "x0", "b"),
    ("x1", "d", "x2"),
    ("e", "x0", "a"),
    ("e", "x0", "x2"),
    ("c", "x1", "b"),
    ("c", "x1", "d"),
)
COLORING = {
    "a": 0,
    "b": 1,
    "c": 0,
    "d": 2,
    "e": 3,
    "x0": 2,
    "x1": 3,
    "x2": 1,
}


def _add_edge(adjacency: dict[str, set[str]], left: str, right: str) -> None:
    adjacency[left].add(right)
    adjacency[right].add(left)


def _face_key(faces: DiskFaces) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(sorted(face)) for face in faces))


def _disk_embedding(faces: DiskFaces) -> DegreeFiveTriangulatedEmbedding:
    vertices = {FOCUS, *BOUNDARY, *COLORING}
    adjacency = {vertex: set() for vertex in vertices}
    for index, vertex in enumerate(BOUNDARY):
        _add_edge(adjacency, FOCUS, vertex)
        _add_edge(adjacency, vertex, BOUNDARY[(index + 1) % 5])
    for face in faces:
        for index, vertex in enumerate(face):
            _add_edge(adjacency, vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    focus_faces = tuple(
        (FOCUS, BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    embedding = DegreeFiveTriangulatedEmbedding(
        state=ConstructionState(graph, COLORING),
        focus=FOCUS,
        boundary=BOUNDARY,
        faces=focus_faces + faces,
    )
    assert embedding.valid
    return embedding


def _proper_color_preserving_flips(faces: DiskFaces) -> tuple[DiskFaces, ...]:
    edge_faces: dict[Edge, list[int]] = defaultdict(list)
    for face_index, face in enumerate(faces):
        for index in range(3):
            edge_faces[
                canonical_edge(face[index], face[(index + 1) % 3])
            ].append(face_index)

    boundary_edges = frozenset(
        canonical_edge(BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    all_edges = frozenset(edge_faces)
    generated: dict[tuple[tuple[str, ...], ...], DiskFaces] = {}

    for diagonal, incident_faces in edge_faces.items():
        if diagonal in boundary_edges or len(incident_faces) != 2:
            continue
        first_index, second_index = incident_faces
        first_face = faces[first_index]
        second_face = faces[second_index]
        first_opposite = next(vertex for vertex in first_face if vertex not in diagonal)
        second_opposite = next(vertex for vertex in second_face if vertex not in diagonal)
        if first_opposite == second_opposite:
            continue

        replacement = canonical_edge(first_opposite, second_opposite)
        if replacement in all_edges:
            continue
        if COLORING[first_opposite] == COLORING[second_opposite]:
            continue

        left, right = diagonal
        updated = [
            face
            for index, face in enumerate(faces)
            if index not in (first_index, second_index)
        ]
        updated.extend(
            (
                (first_opposite, second_opposite, left),
                (first_opposite, second_opposite, right),
            )
        )
        candidate = tuple(sorted(updated, key=lambda face: tuple(sorted(face))))
        generated[_face_key(candidate)] = candidate

    return tuple(generated[key] for key in sorted(generated))


def _flip_family() -> tuple[DiskFaces, ...]:
    queue: deque[DiskFaces] = deque([DISK_FACES])
    seen = {_face_key(DISK_FACES)}
    family: list[DiskFaces] = []
    while queue:
        faces = queue.popleft()
        family.append(faces)
        for candidate in _proper_color_preserving_flips(faces):
            key = _face_key(candidate)
            if key in seen:
                continue
            seen.add(key)
            queue.append(candidate)
    return tuple(family)


def test_phase_rank_has_exact_path_cycle_short_circuit_accounting() -> None:
    certificate = certify_phase_topology(_disk_embedding(DISK_FACES))

    assert certificate.valid
    assert certificate.boundary_terminal_incidence_count == 10
    assert certificate.terminal_path_count == 5
    assert certificate.alternating_cycle_count == 1
    assert certificate.two_edge_terminal_path_count == 0
    assert certificate.phase.phase_fragment_rank == 12
    assert certificate.degree_five_phase_rank == 12


def test_topological_identity_survives_complete_flip_family() -> None:
    family = _flip_family()
    assert len(family) == 154

    rank_counts: Counter[int] = Counter()
    saw_cycle = False
    saw_short_circuit = False

    for faces in family:
        certificate = certify_phase_topology(_disk_embedding(faces))
        assert certificate.valid
        assert certificate.boundary_terminal_incidence_count == 10
        assert certificate.terminal_path_count == 5
        assert certificate.phase.phase_fragment_rank == (
            10
            + 2 * certificate.alternating_cycle_count
            - certificate.two_edge_terminal_path_count
        )
        rank_counts[certificate.phase.phase_fragment_rank] += 1
        saw_cycle = saw_cycle or certificate.alternating_cycle_count > 0
        saw_short_circuit = (
            saw_short_circuit or certificate.two_edge_terminal_path_count > 0
        )

    # Both correction terms are realized by actual retained planar carriers;
    # neither is decorative bookkeeping in the identity.
    assert saw_cycle
    assert saw_short_circuit
    assert sum(rank_counts.values()) == 154


def test_all_flip_family_pivot_controls_have_exact_present_delta() -> None:
    family = _flip_family()
    pivot_sources = 0
    certified_controls = 0
    realized_deltas: set[tuple[int, int, int]] = set()

    for faces in family:
        embedding = _disk_embedding(faces)
        if dual_pairing_signature(embedding).regime != "pivot":
            continue
        pivot_sources += 1

        outcomes: list[tuple[str, int]] = []
        parameters = current_dual_parameters(embedding)
        assert len(parameters) == 4
        for parameter in parameters:
            certificate = certify_dual_control_topology_delta(parameter)
            assert certificate.valid
            certified_controls += 1
            realized_deltas.add(
                (
                    certificate.delta_cycles,
                    certificate.delta_two_edge_terminal_paths,
                    certificate.delta_phase_rank,
                )
            )
            outcomes.append(
                (
                    dual_pairing_signature(certificate.after.embedding).regime,
                    certificate.delta_phase_rank,
                )
            )

        # Reachability is represented by the controls that are applicable now.
        # Across this falsifier family, every pivot source has a present choice
        # that either exposes direct geometry or lowers the exact topological
        # phase account; no future-route coordinate participates in the test.
        assert any(
            regime == "direct" or delta_phase < 0
            for regime, delta_phase in outcomes
        )

    assert pivot_sources == 26
    assert certified_controls == 104
    assert len(realized_deltas) > 1

from __future__ import annotations

from collections import Counter, defaultdict, deque
from typing import TypeAlias

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_involution_phase import dual_involution_phase_signature
from mettafy.dual_path_switching import (
    certify_alternating_path_switch,
    dual_pairing_signature,
)
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
    if not embedding.valid:
        raise AssertionError("flip-family member lost its planar embedding certificate")
    return embedding


def _proper_color_preserving_flips(faces: DiskFaces) -> tuple[DiskFaces, ...]:
    """Generate alternate theorem instances, never construction controls."""

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
        first_opposite = next(
            vertex for vertex in first_face if vertex not in diagonal
        )
        second_opposite = next(
            vertex for vertex in second_face if vertex not in diagonal
        )
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
        candidate = tuple(
            sorted(updated, key=lambda face: tuple(sorted(face)))
        )
        key = _face_key(candidate)
        generated[key] = candidate

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


def test_phase_descent_candidate_survives_full_flip_family() -> None:
    # This is a falsifier family of distinct planar theorem instances. Diagonal
    # flips are used only to generate embeddings; they are not admitted as
    # coloration construction controls.
    family = _flip_family()
    assert len(family) == 154

    regimes: Counter[str] = Counter()
    pivot_ranks: Counter[int] = Counter()

    for faces in family:
        embedding = _disk_embedding(faces)
        source_regime = dual_pairing_signature(embedding).regime
        regimes[source_regime] += 1
        if source_regime != "pivot":
            continue

        source_rank = dual_involution_phase_signature(
            embedding
        ).phase_fragment_rank
        pivot_ranks[source_rank] += 1

        parameters = current_dual_parameters(embedding)
        assert len(parameters) == 4
        outcomes: list[tuple[str, int]] = []
        for parameter in parameters:
            successor = certify_alternating_path_switch(
                parameter
            ).after_embedding
            successor_regime = dual_pairing_signature(successor).regime
            successor_rank = dual_involution_phase_signature(
                successor
            ).phase_fragment_rank
            outcomes.append((successor_regime, successor_rank))

        assert any(
            regime == "direct" or rank < source_rank
            for regime, rank in outcomes
        )

    assert regimes == Counter({"direct": 128, "pivot": 26})
    assert pivot_ranks == Counter({9: 12, 11: 6, 12: 3, 13: 2, 10: 2, 14: 1})

from __future__ import annotations

from collections.abc import Iterable
from itertools import product

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_path_switching import (
    certify_alternating_path_switch,
    dual_pairing_signature,
    selected_dual_primal_edges,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.plane_parameterization import NONZERO_MODES, proper_cycle

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"
Face = tuple[str, str, str]

PENTAGON_TRIANGULATIONS: tuple[tuple[Face, Face, Face], ...] = (
    (("a", "b", "c"), ("a", "c", "d"), ("a", "d", "e")),
    (("a", "b", "c"), ("a", "c", "e"), ("c", "d", "e")),
    (("a", "b", "d"), ("b", "c", "d"), ("a", "d", "e")),
    (("b", "c", "d"), ("b", "d", "e"), ("a", "b", "e")),
    (("a", "b", "e"), ("b", "c", "e"), ("c", "d", "e")),
)


def _add_edge(adjacency: dict[str, set[str]], left: str, right: str) -> None:
    adjacency[left].add(right)
    adjacency[right].add(left)


def _boundary_colors_fit_triangulation(
    disk_faces: tuple[Face, Face, Face],
    boundary_colors: tuple[int, int, int, int, int],
) -> bool:
    coloring = dict(zip(BOUNDARY, boundary_colors))
    return all(
        coloring[vertex] != coloring[face[(index + 1) % 3]]
        for face in disk_faces
        for index, vertex in enumerate(face)
    )


def pentagon_embedding(
    disk_faces: tuple[Face, Face, Face],
    boundary_colors: tuple[int, int, int, int, int],
) -> DegreeFiveTriangulatedEmbedding:
    adjacency = {vertex: set() for vertex in (FOCUS,) + BOUNDARY}
    for index, vertex in enumerate(BOUNDARY):
        _add_edge(adjacency, FOCUS, vertex)
        _add_edge(adjacency, vertex, BOUNDARY[(index + 1) % 5])
    for face in disk_faces:
        for index, vertex in enumerate(face):
            _add_edge(adjacency, vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    state = ConstructionState(graph, dict(zip(BOUNDARY, boundary_colors)))
    focus_faces = tuple(
        (FOCUS, BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    return DegreeFiveTriangulatedEmbedding(
        state=state,
        focus=FOCUS,
        boundary=BOUNDARY,
        faces=focus_faces + disk_faces,
    )


def saturated_boundary_words() -> Iterable[tuple[int, int, int, int, int]]:
    for word in product(range(4), repeat=5):
        if proper_cycle(word) and len(set(word)) == 4:
            yield (word[0], word[1], word[2], word[3], word[4])


def compatible_boundary_only_embeddings() -> Iterable[DegreeFiveTriangulatedEmbedding]:
    for disk_faces in PENTAGON_TRIANGULATIONS:
        for boundary_colors in saturated_boundary_words():
            if _boundary_colors_fit_triangulation(disk_faces, boundary_colors):
                embedding = pentagon_embedding(disk_faces, boundary_colors)
                assert embedding.valid
                yield embedding


def test_every_boundary_only_dual_stage_is_an_exact_alternating_path_switch() -> None:
    configurations = 0
    switches = 0

    for embedding in compatible_boundary_only_embeddings():
        configurations += 1
        for parameter in current_dual_parameters(embedding):
            certificate = certify_alternating_path_switch(parameter)
            assert certificate.valid
            switches += 1

            sigma = certificate.translation_mode
            before = parameter.continuation.embedding
            after = certificate.after_embedding
            assert selected_dual_primal_edges(before, sigma) == selected_dual_primal_edges(
                after,
                sigma,
            )
            for mode in NONZERO_MODES:
                if mode == sigma:
                    continue
                assert selected_dual_primal_edges(
                    after,
                    mode,
                ) == selected_dual_primal_edges(before, mode).symmetric_difference(
                    certificate.path_edges
                )

    assert configurations == 360
    assert switches == 1440


def test_every_boundary_only_pivot_stage_switches_to_direct_geometry() -> None:
    direct = 0
    pivot = 0
    pivot_switches = 0

    for embedding in compatible_boundary_only_embeddings():
        signature = dual_pairing_signature(embedding)
        assert signature.valid
        if signature.regime == "direct":
            direct += 1
            continue

        pivot += 1
        for parameter in current_dual_parameters(embedding):
            switch = certify_alternating_path_switch(parameter)
            assert switch.valid
            successor = dual_pairing_signature(switch.after_embedding)
            assert successor.valid
            assert successor.regime == "direct"
            pivot_switches += 1

    assert direct == 240
    assert pivot == 120
    assert pivot_switches == 480


def test_persistent_pairing_signature_is_pivot_and_any_stage_makes_it_direct() -> None:
    embedding = pentagon_embedding(
        PENTAGON_TRIANGULATIONS[3],
        (0, 1, 0, 2, 3),
    )
    signature = dual_pairing_signature(embedding)
    assert signature.valid
    assert signature.regime == "pivot"
    assert all(pairing.kind == "pivot" for pairing in signature.pairings)

    for parameter in current_dual_parameters(embedding):
        switch = certify_alternating_path_switch(parameter)
        successor = dual_pairing_signature(switch.after_embedding)
        assert successor.regime == "direct"

from __future__ import annotations

from collections.abc import Iterable
from itertools import product

from mettafy.cacophony_router import (
    OneStageFocusSlackRoute,
    TwoStageFocusSlackRoute,
    current_dual_parameters,
    route_focus_slack_within_two_stages,
    routing_regime,
)
from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    apply_graph_native_dual_stage,
    graph_native_witness_state,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.plane_parameterization import proper_cycle

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"
Face = tuple[str, str, str]

# The five Catalan triangulations of a pentagonal disk with no interior vertex.
# Each is a fan from one boundary vertex; keeping all five labelled versions
# makes the finite theorem witness independent of dihedral quotienting.
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
    # The focus-neighbor order is theorem witness data, not a mutable surface
    # coordinate. Preserve the declared cyclic boundary exactly.
    graph[FOCUS] = BOUNDARY

    state = ConstructionState(
        graph,
        dict(zip(BOUNDARY, boundary_colors)),
    )
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


def test_boundary_only_triangulated_disks_route_in_at_most_two_stages() -> None:
    compatible = 0
    direct = 0
    pivot = 0

    for disk_faces in PENTAGON_TRIANGULATIONS:
        for boundary_colors in saturated_boundary_words():
            # A saturated C5 word need not satisfy the two diagonals of this
            # particular triangulation. Reject it before ConstructionState so
            # the exact edge-ledger invariant remains fail-fast everywhere.
            if not _boundary_colors_fit_triangulation(disk_faces, boundary_colors):
                continue

            embedding = pentagon_embedding(disk_faces, boundary_colors)
            assert embedding.valid
            compatible += 1
            history = graph_native_witness_state(embedding.state)
            route = route_focus_slack_within_two_stages(embedding, history)

            assert route is not None
            assert route.valid
            assert route.final_state.admissible_colors(FOCUS)
            if isinstance(route, OneStageFocusSlackRoute):
                direct += 1
                assert route.extra_stage_cost == 0
            else:
                assert isinstance(route, TwoStageFocusSlackRoute)
                pivot += 1
                assert route.extra_stage_cost == 1

    # Exact labelled finite theorem witness: five triangulations times their
    # compatible saturated colorings split into two staged control regimes.
    assert compatible == 360
    assert direct == 240
    assert pivot == 120


def test_persistent_double_lock_is_a_pivot_to_direct_transition() -> None:
    disk_faces = PENTAGON_TRIANGULATIONS[3]
    embedding = pentagon_embedding(disk_faces, (0, 1, 0, 2, 3))
    assert embedding.valid
    history = graph_native_witness_state(embedding.state)

    assert routing_regime(embedding, history) == "pivot"
    route = route_focus_slack_within_two_stages(embedding, history)
    assert isinstance(route, TwoStageFocusSlackRoute)
    assert route.valid
    assert not route.first.target_has_focus_slack
    assert routing_regime(route.rebased.embedding, route.first.after_history) == "direct"
    assert route.second.target_has_focus_slack
    assert route.final_state.admissible_colors(FOCUS)


def test_freshness_alone_is_not_the_router() -> None:
    # This exact direct-regime carrier has both useful-now and zero-slack fresh
    # controls. The staged controller must inspect current consequence rather
    # than treating every unused physical stage as interchangeable progress.
    embedding = pentagon_embedding(
        PENTAGON_TRIANGULATIONS[0],
        (0, 1, 2, 1, 3),
    )
    assert embedding.valid
    history = graph_native_witness_state(embedding.state)
    parameters = current_dual_parameters(embedding)
    stages = tuple(
        apply_graph_native_dual_stage(parameter, history)
        for parameter in parameters
    )

    assert any(stage.target_has_focus_slack for stage in stages)
    assert any(not stage.target_has_focus_slack for stage in stages)
    assert routing_regime(embedding, history) == "direct"

    route = route_focus_slack_within_two_stages(embedding, history)
    assert isinstance(route, OneStageFocusSlackRoute)
    assert route.valid
    assert route.final_state.admissible_colors(FOCUS)

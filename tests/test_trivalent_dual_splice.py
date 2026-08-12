from __future__ import annotations

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_path_switching import dual_pairing_signature
from mettafy.graph_native_staging import graph_native_witness_state
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.plane_parameterization import NONZERO_MODES
from mettafy.staged_cacophony_search import route_focus_slack_bounded
from mettafy.trivalent_dual_splice import (
    certify_matching_path_switch,
    trivalent_dual_splice_signature,
)

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"
DISK_FACES = (
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


def interior_pivot_witness() -> DegreeFiveTriangulatedEmbedding:
    vertices = {FOCUS, *BOUNDARY, *COLORING}
    adjacency = {vertex: set() for vertex in vertices}
    for index, vertex in enumerate(BOUNDARY):
        _add_edge(adjacency, FOCUS, vertex)
        _add_edge(adjacency, vertex, BOUNDARY[(index + 1) % 5])
    for face in DISK_FACES:
        for index, vertex in enumerate(face):
            _add_edge(adjacency, vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    state = ConstructionState(graph, COLORING)
    focus_faces = tuple(
        (FOCUS, BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    embedding = DegreeFiveTriangulatedEmbedding(
        state=state,
        focus=FOCUS,
        boundary=BOUNDARY,
        faces=focus_faces + DISK_FACES,
    )
    assert embedding.valid
    return embedding


def test_trivalent_signature_exposes_cycle_hidden_by_boundary_pairing() -> None:
    embedding = interior_pivot_witness()
    signature = trivalent_dual_splice_signature(embedding)

    assert signature.valid
    assert tuple(matching.mode for matching in signature.matchings) == NONZERO_MODES
    assert signature.total_alternating_cycles == 1
    assert len(signature.cycle_carriers((1, 0))) == 1
    assert signature.terminal_pairing((1, 0)) == ((2, 4),)
    assert signature.terminal_pairing((0, 1)) == ((0, 4), (1, 3))
    assert signature.terminal_pairing((1, 1)) == ((0, 3), (1, 2))


def test_every_first_pivot_is_exact_matching_switch_but_cycle_rank_is_not_enough() -> None:
    embedding = interior_pivot_witness()
    assert dual_pairing_signature(embedding).regime == "pivot"

    parameters = current_dual_parameters(embedding)
    assert len(parameters) == 4
    switches = tuple(certify_matching_path_switch(parameter) for parameter in parameters)

    assert all(switch.valid for switch in switches)
    assert all(switch.before.total_alternating_cycles == 1 for switch in switches)
    assert all(switch.after.total_alternating_cycles == 0 for switch in switches)
    assert all(
        dual_pairing_signature(switch.after.embedding).regime == "pivot"
        for switch in switches
    )


def test_zero_cycle_pivot_can_require_another_geometry_changing_stage() -> None:
    embedding = interior_pivot_witness()
    history = graph_native_witness_state(embedding.state)
    route = route_focus_slack_bounded(embedding, history, max_stages=3)

    assert route is not None
    assert route.valid
    assert route.stage_count == 3
    assert len(route.rebased_points) == 2

    source = trivalent_dual_splice_signature(embedding)
    first = trivalent_dual_splice_signature(route.rebased_points[0].embedding)
    second = trivalent_dual_splice_signature(route.rebased_points[1].embedding)

    assert source.total_alternating_cycles == 1
    assert first.total_alternating_cycles == 0
    assert second.total_alternating_cycles == 0
    assert dual_pairing_signature(first.embedding).regime == "pivot"
    assert dual_pairing_signature(second.embedding).regime == "direct"

from __future__ import annotations

from mettafy.cacophony_router import (
    current_dual_parameters,
    route_focus_slack_within_two_stages,
)
from mettafy.color_construction import ConstructionState
from mettafy.dual_jordan_surgery import (
    ModeNetworkTriangleCertificate,
    certify_jordan_mod2_surgery,
)
from mettafy.dual_path_switching import dual_pairing_signature
from mettafy.graph_native_staging import graph_native_witness_state
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.staged_cacophony_search import route_focus_slack_bounded

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"

# Three-interior-vertex triangulated pentagonal disk.  It is an exact kill
# witness for the conjecture that one pivot dual stage must expose direct
# geometry.  The boundary is the familiar saturated word (0,1,0,2,3), but all
# four immediate embedding-derived dual stages remain pivot-type.
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


def test_shared_edge_mode_network_triangle_is_exact() -> None:
    embedding = interior_pivot_witness()
    certificate = ModeNetworkTriangleCertificate(embedding)
    assert certificate.valid


def test_universal_one_pivot_to_direct_conjecture_is_killed() -> None:
    embedding = interior_pivot_witness()
    signature = dual_pairing_signature(embedding)
    assert signature.valid
    assert signature.regime == "pivot"

    parameters = current_dual_parameters(embedding)
    assert len(parameters) == 4
    surgeries = tuple(certify_jordan_mod2_surgery(parameter) for parameter in parameters)

    # Every immediate stage obeys the exact shared-edge-aware F2/Jordan surgery
    # laws, yet every successor is still pivot.  This kills both the strong
    # "any path" and the weaker "some one-stage pivot" conjectures.
    assert all(certificate.valid for certificate in surgeries)
    assert {certificate.case for certificate in surgeries} == {
        "endpoint_slide",
        "interlaced_pair",
    }
    assert all(certificate.successor_regime == "pivot" for certificate in surgeries)
    assert all(not certificate.target_pairing_is_direct for certificate in surgeries)


def test_cacophony_witness_requires_three_certified_stages() -> None:
    embedding = interior_pivot_witness()
    history = graph_native_witness_state(embedding.state)

    # The old two-stage router now serves as a falsifier for its own range.
    assert route_focus_slack_within_two_stages(embedding, history) is None
    assert route_focus_slack_bounded(embedding, history, max_stages=2) is None

    route = route_focus_slack_bounded(embedding, history, max_stages=3)
    assert route is not None
    assert route.valid
    assert route.stage_count == 3
    assert route.extra_stage_cost == 2
    assert len(set(route.stage_ids)) == 3
    assert route.final_state.admissible_colors(FOCUS)

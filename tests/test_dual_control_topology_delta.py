from __future__ import annotations

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_control_topology_delta import certify_dual_control_topology_delta
from mettafy.dual_path_switching import dual_pairing_signature
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding

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
    focus_faces = tuple(
        (FOCUS, BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    embedding = DegreeFiveTriangulatedEmbedding(
        state=ConstructionState(graph, COLORING),
        focus=FOCUS,
        boundary=BOUNDARY,
        faces=focus_faces + DISK_FACES,
    )
    assert embedding.valid
    return embedding


def test_every_first_control_has_exact_cycle_to_phase_delta() -> None:
    embedding = interior_pivot_witness()
    parameters = current_dual_parameters(embedding)
    assert len(parameters) == 4

    certificates = tuple(
        certify_dual_control_topology_delta(parameter) for parameter in parameters
    )
    assert all(certificate.valid for certificate in certificates)

    # All four current pivot controls remove the witness's one internal
    # alternating cycle, create no two-edge terminal short circuit, and hence
    # realize the exact local accounting 2*(-1) - 0 = -2.
    assert {certificate.delta_cycles for certificate in certificates} == {-1}
    assert {
        certificate.delta_two_edge_terminal_paths for certificate in certificates
    } == {0}
    assert {certificate.delta_phase_rank for certificate in certificates} == {-2}


def test_same_current_state_exposes_distinct_topological_consequences() -> None:
    embedding = interior_pivot_witness()
    first_parameter = current_dual_parameters(embedding)[0]
    first = certify_dual_control_topology_delta(first_parameter)
    successor = first.after.embedding

    assert dual_pairing_signature(successor).regime == "pivot"
    assert first.after.phase.phase_fragment_rank == 10

    outcomes: list[tuple[str, int, int, int]] = []
    for parameter in current_dual_parameters(successor):
        certificate = certify_dual_control_topology_delta(parameter)
        outcomes.append(
            (
                dual_pairing_signature(certificate.after.embedding).regime,
                certificate.delta_cycles,
                certificate.delta_two_edge_terminal_paths,
                certificate.delta_phase_rank,
            )
        )

    # One currently applicable control can restore the higher pivot phase,
    # while another can expose direct geometry without changing Phi.  Thus
    # applicability is always present, but the controls are not equivalent.
    assert any(regime == "pivot" and delta_phase > 0 for regime, _, _, delta_phase in outcomes)
    assert any(regime == "direct" and delta_phase == 0 for regime, _, _, delta_phase in outcomes)
    assert all(delta_phase == 2 * delta_cycles - delta_short for _, delta_cycles, delta_short, delta_phase in outcomes)

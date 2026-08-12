from __future__ import annotations

from mettafy.cacophony_router import current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.dual_involution_phase import dual_involution_phase_signature
from mettafy.dual_path_switching import dual_pairing_signature
from mettafy.graph_native_staging import (
    apply_graph_native_dual_stage,
    fresh_dual_parameters_at_zero,
    graph_native_witness_state,
    rebase_zero_after_dual_stage,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.staged_cacophony_search import route_focus_slack_bounded
from mettafy.trivalent_dual_splice import trivalent_dual_splice_signature

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


def test_three_mode_matchings_are_exact_partial_involutions() -> None:
    embedding = interior_pivot_witness()
    phase = dual_involution_phase_signature(embedding)

    assert phase.valid
    assert phase.phase_fragment_rank == 12
    assert tuple(len(involution.domain) for involution in phase.involutions) == (
        12,
        10,
        10,
    )

    products = phase.ordered_products
    assert len(products) == 6
    assert all(product.valid for product in products)
    assert all(len(product.steps) == len(DISK_FACES) for product in products)
    for product in products:
        reverse = phase.product(product.right_mode, product.left_mode)
        assert product.inverse_relation == reverse.relation


def test_ordered_phase_survives_when_cycle_count_has_lost_signal() -> None:
    embedding = interior_pivot_witness()
    history = graph_native_witness_state(embedding.state)
    route = route_focus_slack_bounded(embedding, history, max_stages=3)

    assert route is not None
    assert route.valid
    assert route.stage_count == 3
    assert len(route.rebased_points) == 2

    embeddings = (
        embedding,
        route.rebased_points[0].embedding,
        route.rebased_points[1].embedding,
    )
    phases = tuple(dual_involution_phase_signature(point) for point in embeddings)
    splices = tuple(trivalent_dual_splice_signature(point) for point in embeddings)
    regimes = tuple(dual_pairing_signature(point).regime for point in embeddings)

    assert regimes == ("pivot", "pivot", "direct")
    assert tuple(splice.total_alternating_cycles for splice in splices) == (1, 0, 0)
    assert tuple(phase.phase_fragment_rank for phase in phases) == (12, 10, 10)
    assert len({phase.phase_relation_key for phase in phases}) == 3

    # The scalar rank decreases exactly on the pivot-to-pivot stage of this
    # shortest certificate. Once direct geometry is reached, strict descent is
    # no longer the obligation; the next current control yields focus slack.
    assert phases[1].phase_fragment_rank < phases[0].phase_fragment_rank
    assert phases[2].phase_fragment_rank == phases[1].phase_fragment_rank


def test_phase_fragment_candidate_survives_every_first_pivot_control() -> None:
    embedding = interior_pivot_witness()
    history = graph_native_witness_state(embedding.state)
    initial_phase = dual_involution_phase_signature(embedding)

    assert dual_pairing_signature(embedding).regime == "pivot"
    assert initial_phase.phase_fragment_rank == 12

    first_parameters = current_dual_parameters(embedding)
    assert len(first_parameters) == 4

    for parameter in first_parameters:
        first = apply_graph_native_dual_stage(parameter, history)
        assert not first.target_has_focus_slack
        point = rebase_zero_after_dual_stage(first)
        assert point is not None
        assert point.valid

        successor = point.embedding
        successor_phase = dual_involution_phase_signature(successor)
        assert dual_pairing_signature(successor).regime == "pivot"
        assert successor_phase.phase_fragment_rank == 10
        assert (
            successor_phase.phase_fragment_rank
            < initial_phase.phase_fragment_rank
        )

        fresh = fresh_dual_parameters_at_zero(point, first.after_history)
        assert len(fresh) == 3
        next_outcomes: list[tuple[str, int]] = []
        for second_parameter in fresh:
            second = apply_graph_native_dual_stage(
                second_parameter,
                first.after_history,
            )
            assert not second.target_has_focus_slack
            second_point = rebase_zero_after_dual_stage(second)
            assert second_point is not None
            regime = dual_pairing_signature(second_point.embedding).regime
            rank = dual_involution_phase_signature(
                second_point.embedding
            ).phase_fragment_rank
            next_outcomes.append((regime, rank))

        # Freshness alone is not a router. Each first successor still exposes a
        # lawful pivot choice that increases the scalar, but also exposes direct
        # choices. The surviving candidate is existential:
        #
        #   pivot => exists fresh T: direct(Tz) or Phi(Tz) < Phi(z).
        assert ("pivot", 12) in next_outcomes
        assert ("direct", 10) in next_outcomes
        assert any(
            regime == "direct" or rank < successor_phase.phase_fragment_rank
            for regime, rank in next_outcomes
        )

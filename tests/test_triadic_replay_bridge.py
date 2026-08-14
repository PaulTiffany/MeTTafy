from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.evitability import TurnActionSignature
from mettafy.sequential_frontier import clean_frontier_turns
from mettafy.triadic_evitability import triadic_ordered_evitability
from mettafy.triadic_replay_bridge import (
    apply_clean_turn_epoch,
    certify_triadic_inverse_replay,
    history_from_construction,
)

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"


def three_interior_lock_state() -> ConstructionState:
    disk_faces = (
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
    coloring = {
        "a": 0,
        "b": 1,
        "c": 0,
        "d": 2,
        "e": 3,
        "x0": 2,
        "x1": 3,
        "x2": 1,
    }
    vertices = {FOCUS, *BOUNDARY, *coloring}
    adjacency = {vertex: set() for vertex in vertices}

    def add_edge(left: str, right: str) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    for index, vertex in enumerate(BOUNDARY):
        add_edge(FOCUS, vertex)
        add_edge(vertex, BOUNDARY[(index + 1) % 5])
    for face in disk_faces:
        for index, vertex in enumerate(face):
            add_edge(vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    return ConstructionState(graph, coloring)


def _clean_turn(state: ConstructionState, seed: str, other_color: int):
    matches = tuple(
        turn
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
        if turn.move.seed == seed and turn.move.other_color == other_color
    )
    assert len(matches) == 1
    return matches[0]


def _action(seed: str, source: int, target: int) -> TurnActionSignature:
    return TurnActionSignature(
        seed=seed,
        source_color=source,
        target_color=target,
        component=frozenset({seed}),
        boundary_hits=frozenset({seed}),
        restoration_colors_after=frozenset(),
    )


def test_whole_component_turn_creates_one_shared_realization_epoch() -> None:
    state = three_interior_lock_state()
    turn = _clean_turn(state, "a", 2)
    history0 = history_from_construction(state)
    history1 = apply_clean_turn_epoch(history0, turn)

    component_states = {
        current.lineage: current
        for current in history1.current_states
        if current.lineage in turn.component
    }

    assert turn.component == frozenset({"a", "x0"})
    assert set(component_states) == set(turn.component)
    assert {current.born_at for current in component_states.values()} == {
        max(current.born_at for current in history1.current_states)
    }
    assert {current.generation for current in component_states.values()} == {1}
    assert history1.current_state_birth_tiers[-1] == turn.component

    # Serialization inside the atomic component action cannot fabricate an
    # actor order between simultaneously realized successor identities.
    ordered = triadic_ordered_evitability(
        {
            _action("a", turn.after.coloring["a"], 0),
            _action("x0", turn.after.coloring["x0"], 2),
        },
        history1,
    )
    assert ordered.current_state_order.first_actors == turn.component
    assert ordered.current_state_order.first_actor is None


def test_c6_physical_replay_is_triadic_historical_nonreturn() -> None:
    state = three_interior_lock_state()
    first = _clean_turn(state, "a", 2)
    inverse = _clean_turn(first.after, "a", 0)

    certificate = certify_triadic_inverse_replay(first, inverse)

    assert certificate.valid
    assert certificate.physical_shape_replay
    assert certificate.inverse_shape.equivalent_replay
    assert not certificate.inverse_shape.fresh
    assert not certificate.inverse_shape.consequential

    # The public graph/coloring snapshot returns exactly.
    assert certificate.extensional_return
    assert (
        certificate.initial.extensional_projection
        == certificate.after_inverse.extensional_projection
    )

    # Persistent lineage history also remains the same.
    assert certificate.lineage_order_return

    # But the two public actions created successor identities in new epochs.
    assert certificate.held_difference_changed
    assert not certificate.triadic_return
    assert (
        certificate.initial.difference.current_state_birth_tiers
        != certificate.after_inverse.difference.current_state_birth_tiers
    )
    assert (
        certificate.after_inverse.difference.current_state_birth_tiers[-1]
        == first.component
    )

    generations = dict(certificate.after_inverse.difference.generations)
    assert generations["a"] == 2
    assert generations["x0"] == 2


def test_quotienting_history_recovers_the_c6_replay_view() -> None:
    state = three_interior_lock_state()
    first = _clean_turn(state, "a", 2)
    inverse = _clean_turn(first.after, "a", 0)
    certificate = certify_triadic_inverse_replay(first, inverse)

    # If Delta is deliberately forgotten, the initial and returned worlds
    # become identical again. C6's physical-shape replay is therefore a
    # legitimate quotient, not a claim that constructional history rewound.
    assert (
        certificate.initial.extensional_projection
        == certificate.after_inverse.extensional_projection
    )
    assert certificate.first_shape.shape == certificate.inverse_shape.shape
    assert certificate.initial != certificate.after_inverse

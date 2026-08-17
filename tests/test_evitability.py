from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.evitability import (
    extensional_evitability,
    retained_evitability,
    turn_action_signature,
)
from mettafy.ordered_shape import OrderedShapeLedger, certify_shape_progress
from mettafy.sequential_frontier import clean_frontier_turns

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"


def _state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e", "x"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
        "x": ("a",),
    }
    coloring = {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3, "x": 2}
    return ConstructionState(graph, coloring)


def _turn(state: ConstructionState, *, seed: str, other_color: int):
    matches = tuple(
        turn
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
        if turn.move.seed == seed and turn.move.other_color == other_color
    )
    assert len(matches) == 1
    return matches[0]


def test_clean_action_can_transform_zero_restoration_into_forced_restoration() -> None:
    state = _state()
    before = extensional_evitability(state, FOCUS, BOUNDARY)
    assert before.restoration_colors == frozenset()
    assert not before.restoration_forced

    finishing = tuple(
        turn
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
        if turn.after.admissible_colors(FOCUS)
    )
    assert finishing
    turn = sorted(finishing, key=lambda item: (item.move.seed, item.move.other_color))[0]
    after = extensional_evitability(turn.after, FOCUS, BOUNDARY)

    assert len(after.restoration_colors) == 1
    assert after.restoration_forced
    assert before != after
    assert turn_action_signature(turn).restoration_colors_after == after.restoration_colors


def test_exact_inverse_restores_extensional_but_not_retained_evitability() -> None:
    state = _state()
    empty = OrderedShapeLedger()
    initial_extensional = extensional_evitability(state, FOCUS, BOUNDARY)
    initial_retained = retained_evitability(state, FOCUS, BOUNDARY, empty)

    first = _turn(state, seed="a", other_color=2)
    first_signature = turn_action_signature(first)
    first_progress = certify_shape_progress(empty, first)
    assert first_progress.valid
    ledger = first_progress.commit()

    inverse = _turn(first.after, seed="a", other_color=0)
    assert inverse.after == state

    returned_extensional = extensional_evitability(inverse.after, FOCUS, BOUNDARY)
    returned_retained = retained_evitability(
        inverse.after,
        FOCUS,
        BOUNDARY,
        ledger,
    )

    # State-only future action structure is exactly reversible with the state.
    assert returned_extensional == initial_extensional

    # Retained resolution changes what counts as a consequential continuation.
    assert first_signature in initial_retained.consequential_turns
    assert first_signature not in returned_retained.consequential_turns
    assert first_signature in returned_retained.replay_turns
    assert returned_retained != initial_retained


def test_retained_evitability_never_invents_a_nonlawful_turn() -> None:
    state = _state()
    first = _turn(state, seed="a", other_color=2)
    ledger = certify_shape_progress(OrderedShapeLedger(), first).commit()
    snapshot = retained_evitability(first.after, FOCUS, BOUNDARY, ledger)

    classified = (
        snapshot.consequential_turns
        | snapshot.replay_turns
        | snapshot.blocked_turns
    )
    assert classified == snapshot.extensional.turns
    assert not (
        snapshot.consequential_turns & snapshot.replay_turns
        or snapshot.consequential_turns & snapshot.blocked_turns
        or snapshot.replay_turns & snapshot.blocked_turns
    )

from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.ordered_shape import OrderedShapeLedger, certify_shape_progress
from mettafy.sequential_frontier import clean_frontier_turns
from mettafy.state_transition_boundary import (
    PublicRewriteObservation,
    RealizedStateIdentity,
    realized_state_identities,
)

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


def _turn(state: ConstructionState, other_color: int):
    matches = tuple(
        turn
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
        if turn.move.seed == "a" and turn.move.other_color == other_color
    )
    assert len(matches) == 1
    return matches[0]


def test_realized_identity_includes_current_color() -> None:
    identities = realized_state_identities(_state())
    assert RealizedStateIdentity("a", 0) in identities
    assert RealizedStateIdentity("b", 1) in identities
    assert RealizedStateIdentity("x", 2) in identities


def test_public_rewrite_checks_exact_changed_carrier() -> None:
    turn = _turn(_state(), 2)
    observation = PublicRewriteObservation(turn.before, turn.component, turn.after)
    assert observation.valid
    assert observation.changed_vertices == frozenset({"a", "x"})
    assert observation.untouched_identities_preserved

    bad = PublicRewriteObservation(turn.before, frozenset({"a"}), turn.after)
    assert not bad.valid


def test_valid_inverse_rewrite_is_not_fresh_ordered_progress() -> None:
    state = _state()
    first = _turn(state, 2)
    assert PublicRewriteObservation(first.before, first.component, first.after).valid

    first_progress = certify_shape_progress(OrderedShapeLedger(), first)
    assert first_progress.valid
    ledger = first_progress.commit()

    inverse = _turn(first.after, 0)
    inverse_public = PublicRewriteObservation(inverse.before, inverse.component, inverse.after)
    inverse_progress = certify_shape_progress(ledger, inverse)

    assert inverse_public.valid
    assert inverse.after == state
    assert inverse_progress.equivalent_replay
    assert not inverse_progress.fresh
    assert not inverse_progress.consequential
    assert not inverse_progress.valid

from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    KempeTraversalCertificate,
    apply_kempe_move,
    opening_single_moves,
    single_move_locked,
)


def locked_planar_state() -> ConstructionState:
    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e", "x"),
        "b": ("v", "a", "c", "x", "y"),
        "c": ("v", "b", "d", "y", "z"),
        "d": ("v", "c", "e", "z"),
        "e": ("v", "d", "a"),
        "x": ("a", "b", "y"),
        "y": ("b", "c", "x", "z"),
        "z": ("c", "d", "y"),
    }
    return ConstructionState(
        graph,
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
            "x": 2,
            "y": 3,
            "z": 1,
        },
    )


def test_saturated_focus_can_be_single_move_locked() -> None:
    state = locked_planar_state()
    assert state.admissible_colors("v") == frozenset()
    assert opening_single_moves(state, "v") == ()
    assert single_move_locked(state, "v")


def test_two_exact_component_moves_open_a_terminal_color() -> None:
    state = locked_planar_state()
    first = KempeMove(seed="a", other_color=2)
    after_first = apply_kempe_move(state, first)
    assert after_first.admissible_colors("v") == frozenset()

    second = KempeMove(seed="b", other_color=3)
    certificate = KempeTraversalCertificate(
        initial=state,
        focus="v",
        moves=(first, second),
    )
    assert certificate.valid
    assert certificate.final.admissible_colors("v")


def test_component_swap_preserves_every_committed_edge() -> None:
    state = locked_planar_state()
    for move in (
        KempeMove(seed="a", other_color=2),
        KempeMove(seed="b", other_color=3),
    ):
        state = apply_kempe_move(state, move)
        assert state.committed_edges_valid

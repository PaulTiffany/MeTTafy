from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    KempeTraversalCertificate,
    apply_kempe_move,
    opening_single_moves,
    single_move_locked,
)


def locked_planar_c5_state() -> ConstructionState:
    """Explicit planar saturated C5 that is locked against every single move."""

    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "x", "p"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "y"),
        "e": ("v", "d", "a", "q"),
        "x": ("b", "y"),
        "y": ("x", "d"),
        "p": ("b", "q"),
        "q": ("p", "e"),
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
            "y": 1,
            "p": 3,
            "q": 1,
        },
    )


def boundary_word(state: ConstructionState) -> tuple[int, int, int, int, int]:
    return tuple(state.coloring[name] for name in ("a", "b", "c", "d", "e"))  # type: ignore[return-value]


def test_single_move_lock_is_not_multistage_lock() -> None:
    """The retained negative witness opens after two exact component stages.

    This promotes a concrete compelled-staging fact and prevents the historical
    single-move lock witness from being misread as evidence of global closure.
    """

    state = locked_planar_c5_state()
    assert boundary_word(state) == (0, 1, 0, 2, 3)
    assert state.admissible_colors("v") == frozenset()
    assert single_move_locked(state, "v")

    # Stage 1: the canonical A/B component contains a-b-c.  Swapping it retains
    # every committed edge obligation but keeps the center saturated.
    first = KempeMove(seed="a", other_color=1)
    after_first = apply_kempe_move(state, first)
    assert after_first.committed_edges_valid
    assert boundary_word(after_first) == (1, 0, 1, 2, 3)
    assert after_first.admissible_colors("v") == frozenset()

    # Stage 2: in the new representation the b-containing 0/2 component is
    # disconnected from d.  Its exact swap desaturates the original boundary.
    second = KempeMove(seed="b", other_color=2)
    after_second = apply_kempe_move(after_first, second)
    assert after_second.committed_edges_valid
    assert boundary_word(after_second) == (1, 2, 1, 2, 3)
    assert after_second.admissible_colors("v") == frozenset({0})

    certificate = KempeTraversalCertificate(
        initial=state,
        focus="v",
        moves=(first, second),
    )
    assert certificate.valid


def test_post_stage_disconnect_is_visible_to_existing_opening_search() -> None:
    state = locked_planar_c5_state()
    after_first = apply_kempe_move(state, KempeMove(seed="a", other_color=1))

    openings = opening_single_moves(after_first, "v")
    assert openings
    assert any(move.seed == "b" and move.other_color == 2 for move in openings)

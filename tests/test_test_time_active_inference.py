from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import (
    ColorationControlSurface,
    state_key,
)


def locked_planar_c5_state() -> ConstructionState:
    """Retained saturated planar C5 used by the staged-control witnesses."""

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


def test_test_time_control_reobserves_hard_successor() -> None:
    """One current control may remain hard; the successor is then re-observed."""

    state = locked_planar_c5_state()
    surface = ColorationControlSurface(state, "v")

    assert state.admissible_colors("v") == frozenset()
    assert boundary_word(state) == (0, 1, 0, 2, 3)

    first = surface.immediate_access(state)
    assert first is not None and first.valid
    assert first.before is state
    assert first.after.admissible_colors("v") == frozenset()
    assert boundary_word(first.after) == (1, 0, 1, 2, 3)

    # The next permission is derived from the actual successor, not stored in
    # the first certificate or inherited from a counterfactual route.
    second = surface.immediate_access(first.after)
    assert second is not None and second.valid
    assert second.before == first.after


def test_current_actionability_does_not_imply_no_trap() -> None:
    """The deterministic current-control policy can legally replay a hard state.

    This is a negative witness for the exact proof boundary:

        current actionability != progress != global closure.

    The test does not say every policy loops. It says a no-trap theorem must be
    proved from more than the existence of one current legal action.
    """

    state = locked_planar_c5_state()
    surface = ColorationControlSurface(state, "v")

    first = surface.immediate_access(state)
    assert first is not None and first.valid
    assert first.after.admissible_colors("v") == frozenset()

    second = surface.immediate_access(first.after)
    assert second is not None and second.valid

    # `immediate_access` is intentionally myopic. On this witness its next
    # deterministic choice is the exact inverse, returning to the original hard
    # coloring. Receding-horizon legality therefore cannot itself be promoted
    # into a closure theorem.
    assert state_key(second.after) == state_key(state)
    assert second.after.admissible_colors("v") == frozenset()

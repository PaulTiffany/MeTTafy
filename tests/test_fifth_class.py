from __future__ import annotations

from fractions import Fraction

import pytest

from mettafy.fifth_class import ChannelStabilityWindow, window_nonempty


def test_four_stable_five_routes_interval_is_exact() -> None:
    floor = Fraction(1, 4)
    lower = Fraction(3, 16)
    upper = Fraction(1, 4)

    at_lower = ChannelStabilityWindow(lower, floor)
    inside = ChannelStabilityWindow(Fraction(1, 5), floor)
    at_upper = ChannelStabilityWindow(upper, floor)

    assert at_lower.four_five_window_lower == lower
    assert at_lower.four_five_window_upper == upper
    assert at_lower.four_stable_five_routes
    assert inside.four_stable_five_routes
    assert not at_upper.four_stable_five_routes


def test_interval_membership_and_stability_behavior_are_equivalent_on_grid() -> None:
    for floor_num in range(1, 12):
        floor = Fraction(floor_num, 12)
        for rho_num in range(0, 25):
            state = ChannelStabilityWindow(Fraction(rho_num, 48), floor)
            assert state.separation_equivalence


def test_fifth_channel_soft_mode_is_strictly_lower_than_fourth_for_positive_conflict() -> None:
    state = ChannelStabilityWindow(Fraction(1, 5), Fraction(1, 4))
    assert state.soft_mode(5) < state.soft_mode(4)


def test_window_is_nonempty_for_every_admissible_observer_floor() -> None:
    for numerator in range(1, 100):
        assert window_nonempty(Fraction(numerator, 100))


def test_reference_case_separates_four_and_five() -> None:
    state = ChannelStabilityWindow(Fraction(1, 5), Fraction(1, 4))
    assert state.soft_mode(4) == Fraction(2, 5)
    assert state.soft_mode(5) == Fraction(1, 5)
    assert state.stable(4)
    assert state.routes(5)
    assert state.separation_equivalence


def test_invalid_domains_fail_closed() -> None:
    with pytest.raises(ValueError, match="observer_soft_floor"):
        ChannelStabilityWindow(Fraction(1, 5), Fraction(1))
    with pytest.raises(ValueError, match="rho"):
        ChannelStabilityWindow(Fraction(-1, 5), Fraction(1, 4))
    with pytest.raises(ValueError, match="channels"):
        ChannelStabilityWindow(Fraction(1, 5), Fraction(1, 4)).soft_mode(1)

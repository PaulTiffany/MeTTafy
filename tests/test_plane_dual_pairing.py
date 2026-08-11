from __future__ import annotations

from itertools import product

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.plane_dual_pairing import (
    DegreeFiveDualPairing,
    selected_two_mode_degree,
    singleton_edges_adjacent,
    toggle_cut_endpoints,
    triangle_modes,
)
from mettafy.plane_parameterization import NONZERO_MODES, proper_cycle


def saturated_boundaries() -> tuple[tuple[int, int, int, int, int], ...]:
    boundaries = []
    for word in product(range(4), repeat=5):
        if proper_cycle(word) and len(set(word)) == 4:
            boundaries.append((word[0], word[1], word[2], word[3], word[4]))
    return tuple(boundaries)


def test_proper_triangle_carries_each_nonzero_v4_mode_once() -> None:
    for colors in product(range(4), repeat=3):
        if len(set(colors)) != 3:
            continue
        modes = triangle_modes((colors[0], colors[1], colors[2]))
        assert set(modes) == set(NONZERO_MODES)
        for excluded in NONZERO_MODES:
            assert selected_two_mode_degree((colors[0], colors[1], colors[2]), excluded) == 2


def test_every_saturated_c5_has_exactly_one_opening_and_one_locked_pairing_type() -> None:
    boundaries = saturated_boundaries()
    assert len(boundaries) == 120

    for boundary in boundaries:
        defects = C5DefectState(boundary)
        singleton_modes = tuple(
            mode for mode, count in defects.mode_counts.items() if count == 1
        )
        assert len(singleton_modes) == 2

        for translation_mode in singleton_modes:
            pairing = DegreeFiveDualPairing(boundary, translation_mode)
            assert pairing.opening_pairing != pairing.locked_pairing
            assert all(pairing.pair_opens(pair) for pair in pairing.opening_pairing)
            assert not any(pairing.pair_opens(pair) for pair in pairing.locked_pairing)


def test_locked_boundary_translation_is_reversible_not_a_descent_measure() -> None:
    boundary = (0, 1, 0, 2, 3)
    pairing = DegreeFiveDualPairing(boundary, (0, 1))
    modes = pairing.modes
    locked_pair = pairing.locked_pairing[0]

    after = toggle_cut_endpoints(modes, pairing.translation_mode, locked_pair)
    assert not singleton_edges_adjacent(after)
    assert after != modes

    restored = toggle_cut_endpoints(after, pairing.translation_mode, locked_pair)
    assert restored == modes


def test_cut_translation_rejects_crossing_its_own_mode() -> None:
    boundary = (0, 1, 0, 2, 3)
    pairing = DegreeFiveDualPairing(boundary, (0, 1))
    forbidden_edge = pairing.modes.index(pairing.translation_mode)

    try:
        toggle_cut_endpoints(
            pairing.modes,
            pairing.translation_mode,
            (forbidden_edge, (forbidden_edge + 1) % 5),
        )
    except ValueError as exc:
        assert "forbidden translation mode" in str(exc)
    else:
        raise AssertionError("cut crossing its own translation mode must be rejected")

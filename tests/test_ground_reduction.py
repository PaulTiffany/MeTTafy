from __future__ import annotations

from itertools import product

import pytest

from mettafy.color_construction import PALETTE4
from mettafy.ground_reduction import (
    SATURATED_BOUNDARY_NORMAL_FORM,
    immediate_restoration_color,
    saturated_boundary_normal_form,
)


def test_immediate_restoration_is_exhaustive_through_degree_three() -> None:
    checked = 0
    for degree in range(4):
        for neighbor_colors in product(sorted(PALETTE4), repeat=degree):
            restored = immediate_restoration_color(neighbor_colors)
            assert restored in PALETTE4
            assert restored not in neighbor_colors
            checked += 1

    assert checked == 1 + 4 + 16 + 64


def test_c0_degree_four_all_colors_refutes_immediate_missing_color_step() -> None:
    neighbor_colors = (0, 1, 2, 3)

    assert PALETTE4 - frozenset(neighbor_colors) == frozenset()
    with pytest.raises(ValueError, match="degree <= 3"):
        immediate_restoration_color(neighbor_colors)


def test_c1_all_proper_saturated_q4_five_cycles_have_one_normal_form() -> None:
    accepted = []
    for colors in product(sorted(PALETTE4), repeat=5):
        try:
            normal_form = saturated_boundary_normal_form(colors)
        except ValueError:
            continue
        accepted.append(colors)
        assert normal_form == SATURATED_BOUNDARY_NORMAL_FORM

    assert len(accepted) == 120


def test_m1_rejects_nonproper_or_nonsaturated_boundary() -> None:
    with pytest.raises(ValueError, match="proper saturated"):
        saturated_boundary_normal_form((0, 0, 1, 2, 3))

    with pytest.raises(ValueError, match="proper saturated"):
        saturated_boundary_normal_form((0, 1, 0, 1, 2))

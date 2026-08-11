from __future__ import annotations

from itertools import product

from mettafy.plane_parameterization import (
    FixedRegionFrontier,
    ZERO,
    frontier_closure,
    proper_cycle,
    same_parity_mode_counts,
)


def test_closed_frontier_telescopes_to_zero_in_v4() -> None:
    boundary = (1, 2, 1, 3, 2)
    assert proper_cycle(boundary)
    assert frontier_closure(boundary) == ZERO
    assert same_parity_mode_counts(boundary)


def test_fixed_region_reduces_absolute_palette_to_three_nonzero_modes() -> None:
    frontier = FixedRegionFrontier(center_color=0, boundary=(1, 2, 1, 3, 2))
    assert len(set(frontier.radial_modes)) == 3
    assert ZERO not in frontier.radial_modes
    assert frontier.parity_closed


def test_every_proper_degree_five_three_color_frontier_has_311_mode_signature() -> None:
    signatures: set[tuple[int, int, int]] = set()
    for boundary in product((1, 2, 3), repeat=5):
        if not proper_cycle(boundary):
            continue
        frontier = FixedRegionFrontier(center_color=0, boundary=boundary)
        signatures.add(frontier.degree_five_signature)
        assert frontier.parity_closed
    assert signatures == {(3, 1, 1)}


def test_forbidden_degree_five_mode_splits_do_not_occur() -> None:
    forbidden = {(5, 0, 0), (4, 1, 0), (3, 2, 0), (2, 2, 1)}
    observed: set[tuple[int, int, int]] = set()
    for boundary in product((1, 2, 3), repeat=5):
        if proper_cycle(boundary):
            observed.add(
                FixedRegionFrontier(
                    center_color=0,
                    boundary=boundary,
                ).degree_five_signature
            )
    assert observed.isdisjoint(forbidden)

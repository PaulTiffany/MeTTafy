from __future__ import annotations

from itertools import product

import mettafy.c5_defect_calculus as defects
import mettafy.plane_parameterization as plane


def test_every_proper_c5_has_311_derivative_signature() -> None:
    signatures: set[tuple[int, int, int]] = set()
    for boundary in product(range(4), repeat=5):
        if not plane.proper_cycle(boundary):
            continue
        state = defects.C5DefectState(boundary)
        signatures.add(state.signature)
    assert signatures == {(3, 1, 1)}


def test_defect_adjacency_exactly_classifies_three_vs_four_color_c5() -> None:
    observed: set[tuple[int, bool]] = set()
    for boundary in product(range(4), repeat=5):
        if not plane.proper_cycle(boundary):
            continue
        state = defects.C5DefectState(boundary)
        observed.add((state.color_count, state.singleton_edges_adjacent))
        assert state.adjacency_class_matches_color_count
    assert observed == {(3, True), (4, False)}


def test_saturated_roles_recover_abacd_structure() -> None:
    state = defects.C5DefectState((0, 1, 0, 2, 3))
    roles = state.saturated_roles
    assert roles.repeated_color == 0
    assert roles.repeated_indices == (0, 2)
    assert roles.pivot_index == 1
    assert roles.pivot_color == 1
    assert roles.flank_indices == (3, 4)
    assert roles.flank_colors == (2, 3)
    assert state.candidate_opening_color_pairs == (
        frozenset({1, 2}),
        frozenset({1, 3}),
    )

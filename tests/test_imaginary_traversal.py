from __future__ import annotations

from mettafy.imaginary_traversal import (
    G0,
    X3_REP,
    X4_REP,
    conjugate_subgroup,
    group_elements,
    imaginary_square,
    j_inv_map,
    j_map,
    orbit,
    sheet,
    stabilizer,
)


def test_group_order_and_sheet_orbits_are_algebraic_halves() -> None:
    group = group_elements()
    x3_orbit = orbit(X3_REP)
    x4_orbit = orbit(X4_REP)
    assert len(group) == 240
    assert len(stabilizer(X3_REP)) == 2
    assert len(stabilizer(X4_REP)) == 2
    assert len(x3_orbit) == 120
    assert len(x4_orbit) == 120
    assert x3_orbit.isdisjoint(x4_orbit)
    assert all(sheet(word) == 3 for word in x3_orbit)
    assert all(sheet(word) == 4 for word in x4_orbit)


def test_stabilizers_are_conjugate() -> None:
    assert conjugate_subgroup(stabilizer(X3_REP), G0) == stabilizer(X4_REP)


def test_sheet_switch_is_bijective() -> None:
    for word in orbit(X3_REP):
        assert j_inv_map(j_map(word)) == word
    for word in orbit(X4_REP):
        assert j_map(j_inv_map(word)) == word


def test_imaginary_traversal_squares_to_minus_identity() -> None:
    for word in orbit(X3_REP):
        returned, scalar = imaginary_square(word)
        assert returned == word
        assert scalar == -1


def test_traversal_changes_sheet_without_creating_terminal_rank() -> None:
    for word in orbit(X3_REP):
        paired = j_map(word)
        assert sheet(word) == 3
        assert sheet(paired) == 4
        assert set(word) <= {0, 1, 2, 3}
        assert set(paired) <= {0, 1, 2, 3}

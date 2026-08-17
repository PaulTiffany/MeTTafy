from __future__ import annotations

from mettafy.imaginary_traversal import (
    G0,
    X3_REP,
    X4_REP,
    LinearSheetState,
    conjugate_subgroup,
    frozen_exterior_lift_preserves_edges,
    group_elements,
    imaginary_square,
    imaginary_traversal,
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


def test_sheet_and_module_sign_are_independent_coordinates() -> None:
    state = LinearSheetState(X3_REP, 1)
    first = imaginary_traversal(state)
    second = imaginary_traversal(first)
    assert state.sheet_index == 3
    assert first.sheet_index == 4
    assert first.coefficient == 1
    assert second.word == state.word
    assert second.sheet_index == 3
    assert second.coefficient == -1


def test_traversal_changes_sheet_without_creating_terminal_rank() -> None:
    for word in orbit(X3_REP):
        paired = j_map(word)
        assert sheet(word) == 3
        assert sheet(paired) == 4
        assert set(word) <= {0, 1, 2, 3}
        assert set(paired) <= {0, 1, 2, 3}


def test_local_sheet_switch_does_not_lift_by_identity_over_arbitrary_exterior() -> None:
    """A concrete planar off-boundary edge blocks the naive local J lift.

    X4_REP is a proper C5 coloring.  Its paired X3 word changes position 0 to
    color 3.  Attach one exterior leaf of color 3 to that boundary vertex.
    The source coloring is valid at that edge (0 != 3), but the frozen-exterior
    J^-1 image collides (3 == 3).  Therefore local sheet conjugacy alone is not
    a graph-level lift theorem.
    """
    after = j_inv_map(X4_REP)
    assert X4_REP[0] != 3
    assert after[0] == 3
    assert not frozen_exterior_lift_preserves_edges(X4_REP, after, ((0, 3),))


def test_frozen_exterior_lift_can_succeed_when_constraints_are_compatible() -> None:
    after = j_inv_map(X4_REP)
    assert frozen_exterior_lift_preserves_edges(X4_REP, after, ((0, 1),))

from __future__ import annotations

from mettafy.c5_lock_witness import AlternatingConnection, LockedC5Witness
from tests.test_locked_planar_c5 import locked_planar_c5_state


def test_locked_c5_witness_retains_both_exterior_connections() -> None:
    state = locked_planar_c5_state()
    witness = LockedC5Witness(
        state=state,
        focus="v",
        boundary=("a", "b", "c", "d", "e"),
        pivot_to_first_flank=AlternatingConnection(
            path=("b", "x", "y", "d"),
            color_pair=frozenset({1, 2}),
        ),
        pivot_to_second_flank=AlternatingConnection(
            path=("b", "p", "q", "e"),
            color_pair=frozenset({1, 3}),
        ),
    )

    assert witness.valid
    assert witness.defects.is_saturated_four_color_boundary
    assert not witness.defects.singleton_edges_adjacent
    assert witness.expansion_size == 9
    assert witness.witness_vertices == frozenset(
        {"a", "b", "c", "d", "e", "x", "y", "p", "q"}
    )


def test_lock_witness_fails_closed_when_a_connection_is_not_retained() -> None:
    state = locked_planar_c5_state()
    witness = LockedC5Witness(
        state=state,
        focus="v",
        boundary=("a", "b", "c", "d", "e"),
        pivot_to_first_flank=AlternatingConnection(
            path=("b", "x", "y", "d"),
            color_pair=frozenset({1, 2}),
        ),
        pivot_to_second_flank=AlternatingConnection(
            path=(),
            color_pair=frozenset({1, 3}),
        ),
    )

    assert not witness.valid

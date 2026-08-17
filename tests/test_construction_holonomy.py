from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import KempeMove, apply_kempe_move

BOUNDARY = ("a", "b", "c", "d", "e")


def persistent_double_lock_state() -> ConstructionState:
    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    return ConstructionState(
        graph,
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
        },
    )


def boundary_word(state: ConstructionState) -> tuple[int, int, int, int, int]:
    colors = tuple(state.coloring[vertex] for vertex in BOUNDARY)
    return (colors[0], colors[1], colors[2], colors[3], colors[4])


def replay(state: ConstructionState, moves: tuple[KempeMove, ...]) -> ConstructionState:
    current = state
    for move in moves:
        current = apply_kempe_move(current, move)
        assert current.committed_edges_valid
    return current


def test_two_legal_stage_orders_need_not_commute() -> None:
    """Exact discrete-curvature witness on the persistent-lock carrier.

    Both orderings use legal component swaps and preserve every committed edge,
    yet they land in different construction states.  This is a path-ordering
    fact, not a knot claim: it justifies retaining stage history instead of
    collapsing the construction to a static boundary potential.
    """

    state = persistent_double_lock_state()
    t_ab = KempeMove(seed="a", other_color=1)
    t_bc = KempeMove(seed="b", other_color=2)

    ab_then_bc = replay(state, (t_ab, t_bc))
    bc_then_ab = replay(state, (t_bc, t_ab))

    assert boundary_word(ab_then_bc) == (1, 2, 1, 0, 3)
    assert boundary_word(bc_then_ab) == (1, 2, 0, 1, 3)
    assert dict(ab_then_bc.coloring) != dict(bc_then_ab.coloring)
    assert ab_then_bc.admissible_colors("v") == frozenset()
    assert bc_then_ab.admissible_colors("v") == frozenset()


def test_order_defect_is_an_exact_residual_component_transport() -> None:
    """The noncommuting square leaves a concrete, reversible residue.

    The two orderings differ exactly by swapping the 0/1 component {c,d}.
    Thus the path-order defect is carried by an ordinary graph-native Kempe
    component rather than by an observer projection or invented scalar phase.
    """

    state = persistent_double_lock_state()
    t_ab = KempeMove(seed="a", other_color=1)
    t_bc = KempeMove(seed="b", other_color=2)

    ab_then_bc = replay(state, (t_ab, t_bc))
    bc_then_ab = replay(state, (t_bc, t_ab))

    residue_forward = KempeMove(seed="c", other_color=1)
    residue_backward = KempeMove(seed="c", other_color=0)

    assert dict(apply_kempe_move(bc_then_ab, residue_forward).coloring) == dict(
        ab_then_bc.coloring
    )
    assert dict(apply_kempe_move(ab_then_bc, residue_backward).coloring) == dict(
        bc_then_ab.coloring
    )


def test_some_compelled_opening_stages_do_commute() -> None:
    """Control: path dependence is structural, not asserted for every pair.

    The two singleton stages that open this witness commute and reach the same
    terminally open construction.  A future holonomy invariant must therefore
    distinguish commuting from noncommuting staging rather than declaring all
    stage order significant by fiat.
    """

    state = persistent_double_lock_state()
    t_ac = KempeMove(seed="a", other_color=2)
    t_ad = KempeMove(seed="c", other_color=3)

    ac_then_ad = replay(state, (t_ac, t_ad))
    ad_then_ac = replay(state, (t_ad, t_ac))

    assert dict(ac_then_ad.coloring) == dict(ad_then_ac.coloring)
    assert boundary_word(ac_then_ad) == (2, 1, 3, 2, 3)
    assert ac_then_ad.admissible_colors("v") == frozenset({0})

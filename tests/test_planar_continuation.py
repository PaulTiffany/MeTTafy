from __future__ import annotations

import pytest

from mettafy.planar_continuation import ContinuationPair, endpoints_alternate


def test_alternating_endpoint_pairs_force_intersection() -> None:
    assert endpoints_alternate((0, 2), (1, 3), 4)
    pair = ContinuationPair(boundary_size=4, first=(0, 2), second=(1, 3))
    assert pair.forced_intersection
    assert not pair.bounded_planar_coexistence_not_refuted


def test_non_alternating_pairs_are_not_forced_to_cross_by_cyclic_order() -> None:
    assert not endpoints_alternate((0, 1), (2, 3), 4)
    assert not endpoints_alternate((0, 3), (1, 2), 4)


def test_cyclic_order_obstruction_is_rotation_invariant() -> None:
    assert endpoints_alternate((1, 3), (2, 4), 5)
    assert endpoints_alternate((3, 0), (4, 1), 5)


def test_pairs_must_have_disjoint_endpoints() -> None:
    with pytest.raises(ValueError, match="disjoint endpoints"):
        endpoints_alternate((0, 2), (2, 3), 4)

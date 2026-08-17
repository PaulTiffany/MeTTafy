from __future__ import annotations

from itertools import product

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import state_key
from mettafy.kempe_traversal import all_component_moves
from mettafy.plane_parameterization import proper_cycle
from mettafy.zero_point_correspondence import (
    ZERO_PARAMETER,
    apply_kempe_nonzero_parameter,
    dual_defect_parameterization,
    kempe_parameterization,
    realize_kempe_parameter,
    reparameterize_at_zero,
    zero_point_correspondence,
)

BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary: tuple[int, int, int, int, int]) -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(graph, dict(zip(BOUNDARY, boundary)))


def persistent_double_lock_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )


def saturated_boundaries() -> tuple[tuple[int, int, int, int, int], ...]:
    return tuple(
        (word[0], word[1], word[2], word[3], word[4])
        for word in product(range(4), repeat=5)
        if proper_cycle(word) and len(set(word)) == 4
    )


def test_kempe_zero_parameter_is_exact_identity() -> None:
    state = persistent_double_lock_state()
    chart = kempe_parameterization(state)
    realized = realize_kempe_parameter(chart, ZERO_PARAMETER)

    assert realized is state
    assert state_key(realized) == state_key(state)
    assert dict(realized.graph) == dict(state.graph)


def test_kempe_and_dual_parameterizations_share_z0_on_all_saturated_c5() -> None:
    boundaries = saturated_boundaries()
    assert len(boundaries) == 120

    for boundary in boundaries:
        state = wheel_state(boundary)
        kempe = kempe_parameterization(state)
        dual = dual_defect_parameterization(state, "v")
        correspondence = zero_point_correspondence(kempe, dual)

        assert correspondence.valid
        assert correspondence.left.family != correspondence.right.family
        assert state_key(correspondence.shared_zero) == state_key(state)
        assert dict(correspondence.shared_zero.graph) == dict(state.graph)


def test_reparameterization_at_z0_is_not_a_construction_transition() -> None:
    state = persistent_double_lock_state()
    correspondence = zero_point_correspondence(
        kempe_parameterization(state),
        dual_defect_parameterization(state, "v"),
    )

    realized = reparameterize_at_zero(correspondence)
    assert state_key(realized) == state_key(state)
    assert dict(realized.coloring) == dict(state.coloring)
    assert realized.committed_edges_valid


def test_nonzero_kempe_parameter_requires_family_specific_certificate() -> None:
    state = persistent_double_lock_state()
    chart = kempe_parameterization(state)
    move = all_component_moves(state)[0]

    certificate = apply_kempe_nonzero_parameter(chart, move)
    assert certificate.valid
    assert state_key(certificate.after) != state_key(state)
    assert dict(certificate.after.graph) == dict(state.graph)
    assert certificate.after.surface_genus == 0
    assert certificate.after.committed_edges_valid


def test_nonzero_parameter_must_be_available_at_its_own_zero_point() -> None:
    state = persistent_double_lock_state()
    chart = kempe_parameterization(state)
    move = all_component_moves(state)[0]
    after = apply_kempe_nonzero_parameter(chart, move).after

    next_chart = kempe_parameterization(after)
    stale_only = next(
        candidate
        for candidate in all_component_moves(state)
        if candidate not in all_component_moves(after)
    )
    with pytest.raises(ValueError, match="not available at this zero-point"):
        realize_kempe_parameter(next_chart, stale_only)


def test_distinct_construction_points_do_not_correspond_at_zero() -> None:
    state = persistent_double_lock_state()
    chart = kempe_parameterization(state)
    after = apply_kempe_nonzero_parameter(chart, all_component_moves(state)[0]).after

    with pytest.raises(ValueError, match="not based at the same construction state"):
        zero_point_correspondence(
            kempe_parameterization(state),
            kempe_parameterization(after),
        )

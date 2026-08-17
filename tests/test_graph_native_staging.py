from __future__ import annotations

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    apply_graph_native_dual_stage,
    fresh_dual_parameters_at_zero,
    graph_native_witness_state,
    rebase_zero_after_dual_stage,
    stage_id_for_dual_parameter,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    apply_dual_nonzero_parameter,
    canonical_edge,
    derive_dual_domain_parameters,
)
from mettafy.witness_expansion import GraphNativeStageId
from mettafy.zero_point_correspondence import (
    dual_defect_parameterization,
    same_construction_state,
)

BOUNDARY = ("a", "b", "c", "d", "e")
SIGMA_01 = (0, 1)
SIGMA_11 = (1, 1)


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


def persistent_embedding() -> DegreeFiveTriangulatedEmbedding:
    return DegreeFiveTriangulatedEmbedding(
        state=persistent_double_lock_state(),
        focus="v",
        boundary=BOUNDARY,
        faces=(
            ("v", "b", "a"),
            ("v", "c", "b"),
            ("v", "d", "c"),
            ("v", "e", "d"),
            ("v", "a", "e"),
            ("a", "b", "e"),
            ("b", "c", "d"),
            ("b", "d", "e"),
        ),
    )


def test_stage_identity_depends_on_mode_and_physical_cut_not_path_orientation() -> None:
    left = GraphNativeStageId(
        translation_mode=SIGMA_01,
        crossed_edges=(("e", "a"), ("b", "a")),
    )
    right = GraphNativeStageId(
        translation_mode=SIGMA_01,
        crossed_edges=(("a", "b"), ("a", "e")),
    )

    assert left == right
    assert left.crossed_edges == (("a", "b"), ("a", "e"))
    assert left.token == "dual:01:a--b,a--e"


def test_persistent_carrier_rebases_and_exposes_a_fresh_second_stage() -> None:
    embedding = persistent_embedding()
    assert embedding.valid
    history = graph_native_witness_state(embedding.state)
    assert len(history.carrier_edges) == 7
    assert history.stage_capacity_upper_bound == 3 * ((1 << 7) - 1)

    initial_chart = dual_defect_parameterization(embedding.state, "v")
    initial_parameters = derive_dual_domain_parameters(
        initial_chart,
        embedding,
        SIGMA_01,
    )
    first_parameter = next(
        parameter
        for parameter in initial_parameters
        if parameter.path.terminal_edges == (0, 4)
    )

    first = apply_graph_native_dual_stage(first_parameter, history)
    assert first.valid
    assert not first.target_has_focus_slack
    assert first.dual_certificate.after.admissible_colors("v") == frozenset()
    assert first.stage_id.crossed_edges == (
        canonical_edge("a", "b"),
        canonical_edge("a", "e"),
    )
    assert first.after_history.stage_history == (first.stage_id,)
    assert first.after_history.retained_carrier_edges == frozenset(
        {canonical_edge("a", "b"), canonical_edge("a", "e")}
    )
    assert first.after_history.remaining_stage_capacity == (
        history.remaining_stage_capacity - 1
    )

    rebased = rebase_zero_after_dual_stage(first)
    assert rebased is not None
    assert rebased.valid
    assert rebased.correspondence.shared_zero is first.dual_certificate.after

    same_mode_parameters = derive_dual_domain_parameters(
        rebased.dual_chart,
        rebased.embedding,
        SIGMA_01,
    )
    inverse_parameter = next(
        parameter
        for parameter in same_mode_parameters
        if stage_id_for_dual_parameter(parameter) == first.stage_id
    )

    # The inverse remains a legal graph symmetry.
    inverse = apply_dual_nonzero_parameter(inverse_parameter)
    assert inverse.valid
    assert same_construction_state(inverse.after, embedding.state)

    # But the same physical cut/mode cannot be counted twice as proof progress.
    with pytest.raises(ValueError, match="already been consumed as proof progress"):
        apply_graph_native_dual_stage(inverse_parameter, first.after_history)

    fresh = fresh_dual_parameters_at_zero(rebased, first.after_history)
    assert fresh
    assert all(
        stage_id_for_dual_parameter(parameter) not in first.after_history.stage_history
        for parameter in fresh
    )

    second_parameter = next(
        parameter
        for parameter in fresh
        if parameter.translation_mode == SIGMA_11
        and parameter.path.terminal_edges == (1, 2)
    )
    second = apply_graph_native_dual_stage(
        second_parameter,
        first.after_history,
    )

    assert second.valid
    assert second.target_has_focus_slack
    assert second.dual_certificate.after.admissible_colors("v") == frozenset({0})
    assert second.stage_id.crossed_edges == (
        canonical_edge("b", "c"),
        canonical_edge("c", "d"),
    )
    assert second.after_history.stage_history == (first.stage_id, second.stage_id)
    assert second.after_history.retained_carrier_edges == frozenset(
        {
            canonical_edge("a", "b"),
            canonical_edge("a", "e"),
            canonical_edge("b", "c"),
            canonical_edge("c", "d"),
        }
    )
    assert second.after_history.remaining_stage_capacity == (
        history.remaining_stage_capacity - 2
    )
    assert rebase_zero_after_dual_stage(second) is None

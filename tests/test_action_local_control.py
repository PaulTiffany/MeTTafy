from __future__ import annotations

from dataclasses import fields

import pytest

from mettafy.action_local_control import (
    ChangeDirectionAction,
    StopAction,
    realize_change_direction,
    realize_stop,
)
from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    fresh_dual_parameters_at_zero,
    graph_native_witness_state,
    rebase_zero_after_dual_stage,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    derive_dual_domain_parameters,
)
from mettafy.zero_point_correspondence import dual_defect_parameterization

BOUNDARY = ("a", "b", "c", "d", "e")
SIGMA_01 = (0, 1)
SIGMA_11 = (1, 1)


def persistent_embedding() -> DegreeFiveTriangulatedEmbedding:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    state = ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )
    embedding = DegreeFiveTriangulatedEmbedding(
        state=state,
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
    assert embedding.valid
    return embedding


def first_current_choice(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> DualDomainParameter:
    chart = dual_defect_parameterization(embedding.state, embedding.focus)
    parameters = derive_dual_domain_parameters(chart, embedding, SIGMA_01)
    return next(
        parameter
        for parameter in parameters
        if parameter.path.terminal_edges == (0, 4)
    )


def test_action_certificates_have_one_affected_state_and_no_sibling_coordinates() -> None:
    assert tuple(field.name for field in fields(ChangeDirectionAction)) == (
        "parameter",
        "before_history",
        "stage",
    )
    assert tuple(field.name for field in fields(StopAction)) == (
        "before",
        "focus",
        "color",
        "after",
    )

    forbidden = {
        "alternatives",
        "candidates",
        "future",
        "outcomes",
        "route",
        "routes",
        "targets",
    }
    assert forbidden.isdisjoint(field.name for field in fields(ChangeDirectionAction))
    assert forbidden.isdisjoint(field.name for field in fields(StopAction))


def test_one_chosen_direction_change_realizes_exactly_one_successor() -> None:
    embedding = persistent_embedding()
    history = graph_native_witness_state(embedding.state)
    parameter = first_current_choice(embedding)

    action = realize_change_direction(parameter, history)

    assert action.valid
    assert action.decision == "change_direction"
    assert action.affected_state_count == 1
    assert action.affected_state is action.after
    assert action.before is embedding.state
    assert action.after.admissible_colors("v") == frozenset()
    assert 0 < action.displacement <= action.finite_displacement_budget
    assert action.after.committed_edges_valid


def test_successor_rederives_its_own_choice_then_can_stop() -> None:
    embedding = persistent_embedding()
    history = graph_native_witness_state(embedding.state)
    first = realize_change_direction(first_current_choice(embedding), history)

    point = rebase_zero_after_dual_stage(first.stage)
    assert point is not None
    assert point.valid
    assert point.embedding.state is first.after

    fresh = fresh_dual_parameters_at_zero(point, first.stage.after_history)
    second_parameter = next(
        parameter
        for parameter in fresh
        if parameter.translation_mode == SIGMA_11
        and parameter.path.terminal_edges == (1, 2)
    )
    second = realize_change_direction(second_parameter, first.stage.after_history)

    assert second.valid
    assert second.before is first.after
    assert second.affected_state_count == 1
    assert second.after.admissible_colors("v") == frozenset({0})

    stop = realize_stop(second.after, "v", 0)
    assert stop.valid
    assert stop.decision == "stop"
    assert stop.affected_state_count == 1
    assert stop.affected_state is stop.after
    assert stop.displacement == 1
    assert stop.after.complete
    assert stop.after.committed_edges_valid


def test_stop_is_not_available_at_zero_focus_slack() -> None:
    embedding = persistent_embedding()
    assert embedding.state.admissible_colors("v") == frozenset()

    with pytest.raises(ValueError, match="not currently admissible"):
        realize_stop(embedding.state, "v", 0)

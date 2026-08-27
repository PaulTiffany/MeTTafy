from __future__ import annotations

from dataclasses import fields

import pytest

from mettafy.action_local_control import (
    CommitFocusAction,
    CounterfactualDirectionChange,
    imagine_change_direction,
    realize_focus_commit,
)
from mettafy.active_inference_boundary import (
    CertifiedInstantiation,
    ImaginedState,
    InferenceEpisode,
    amortize,
    void_count,
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


def open_wheel_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 1, "e": 2},
    )


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


def test_inference_and_realized_certificates_have_distinct_payloads() -> None:
    """INFERENCE/BRIDGE: imagined stages and realized authority are different types."""

    assert tuple(field.name for field in fields(CounterfactualDirectionChange)) == (
        "parameter",
        "before_history",
        "stage",
    )
    assert tuple(field.name for field in fields(CertifiedInstantiation)) == (
        "realized",
        "focus",
        "color",
    )
    assert tuple(field.name for field in fields(CommitFocusAction)) == (
        "certificate",
        "after",
    )


def test_one_chosen_direction_change_is_counterfactual_only() -> None:
    """INFERENCE: a dual-stage response is an imagined state, not construction history."""

    embedding = persistent_embedding()
    history = graph_native_witness_state(embedding.state)
    parameter = first_current_choice(embedding)

    change = imagine_change_direction(parameter, history)

    assert change.valid
    assert change.decision == "counterfactual_change_direction"
    assert change.imagined_state_count == 1
    assert change.before is embedding.state
    assert change.after.admissible_colors("v") == frozenset()
    assert 0 < change.displacement <= change.finite_displacement_budget
    assert change.after.committed_edges_valid
    assert embedding.state.admissible_colors("v") == frozenset()
    assert "v" not in embedding.state.coloring


def test_sequential_dual_imagination_cannot_self_promote_to_authority() -> None:
    """NEGATIVE/BRIDGE: imagined opening is rechecked against the unchanged map."""

    embedding = persistent_embedding()
    realized = embedding.state
    history = graph_native_witness_state(realized)
    first = imagine_change_direction(first_current_choice(embedding), history)

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
    second = imagine_change_direction(second_parameter, first.stage.after_history)

    assert second.valid
    assert second.before is first.after
    assert second.after.admissible_colors("v") == frozenset({0})
    assert realized.admissible_colors("v") == frozenset()

    episode = InferenceEpisode(
        realized=realized,
        focus="v",
        imagined=(
            ImaginedState(realized),
            ImaginedState(first.after),
            ImaginedState(second.after),
        ),
    )
    with pytest.raises(ValueError, match="admissible state on the realized map"):
        amortize(episode, 0)

    assert "v" not in realized.coloring


def test_realized_focus_commit_requires_certified_instantiation() -> None:
    """BRIDGE/REALIZED: focus execution consumes only an authority certificate."""

    realized = open_wheel_state()
    assert realized.admissible_colors("v") == frozenset({3})

    episode = InferenceEpisode(
        realized=realized,
        focus="v",
        imagined=(ImaginedState(realized),),
    )
    certificate = amortize(episode, 3)
    commit = realize_focus_commit(certificate)

    assert commit.valid
    assert commit.certificate is certificate
    assert commit.decision == "commit_focus"
    assert commit.before is realized
    assert commit.focus == "v"
    assert commit.color == 3
    assert commit.affected_state_count == 1
    assert commit.displacement == 1
    assert void_count(commit.after) == void_count(realized) - 1
    assert commit.after.complete
    assert commit.after.committed_edges_valid
    assert "v" not in realized.coloring


def test_blocked_actual_focus_cannot_forge_execution_by_color_choice() -> None:
    """NEGATIVE: a color plus blocked map is not a valid construction certificate."""

    realized = persistent_embedding().state
    invalid = CertifiedInstantiation(realized=realized, focus="v", color=0)
    assert not invalid.valid

    with pytest.raises(ValueError, match="invalid certified instantiation"):
        realize_focus_commit(invalid)

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    GraphNativeDualStageCertificate,
    RebasedZeroPoint,
    apply_graph_native_dual_stage,
    committed_carrier_edges,
    fresh_dual_parameters_at_zero,
    rebase_zero_after_dual_stage,
    stage_id_for_dual_parameter,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    apply_dual_nonzero_parameter,
    derive_dual_domain_parameters,
)
from mettafy.witness_expansion import GraphNativeWitnessExpansionState
from mettafy.zero_point_correspondence import (
    dual_defect_parameterization,
    same_construction_state,
)

RoutingRegime: TypeAlias = Literal["direct", "pivot", "unavailable"]


@dataclass(frozen=True)
class OneStageFocusSlackRoute:
    """A current graph-native dual control that immediately yields focus slack."""

    embedding: DegreeFiveTriangulatedEmbedding
    before_history: GraphNativeWitnessExpansionState
    stage: GraphNativeDualStageCertificate

    @property
    def stage_count(self) -> int:
        return 1

    @property
    def extra_stage_cost(self) -> int:
        return 0

    @property
    def final_state(self) -> ConstructionState:
        return self.stage.dual_certificate.after

    @property
    def valid(self) -> bool:
        if not self.embedding.valid or not self.stage.valid:
            return False
        if self.stage.before_history != self.before_history:
            return False
        if self.before_history.carrier_edges != committed_carrier_edges(
            self.embedding.state
        ):
            return False
        if not same_construction_state(
            self.embedding.state,
            self.stage.dual_certificate.parameter.chart.base,
        ):
            return False
        return self.stage.target_has_focus_slack


@dataclass(frozen=True)
class TwoStageFocusSlackRoute:
    """A pivot stage followed by a freshly derived direct stage at the new z0."""

    embedding: DegreeFiveTriangulatedEmbedding
    before_history: GraphNativeWitnessExpansionState
    first: GraphNativeDualStageCertificate
    rebased: RebasedZeroPoint
    second: GraphNativeDualStageCertificate

    @property
    def stage_count(self) -> int:
        return 2

    @property
    def extra_stage_cost(self) -> int:
        """One extra stage beyond the direct one-stage regime."""

        return 1

    @property
    def final_state(self) -> ConstructionState:
        return self.second.dual_certificate.after

    @property
    def valid(self) -> bool:
        if not self.embedding.valid or not self.first.valid or not self.second.valid:
            return False
        if self.first.before_history != self.before_history:
            return False
        if self.first.target_has_focus_slack:
            return False
        if not same_construction_state(
            self.embedding.state,
            self.first.dual_certificate.parameter.chart.base,
        ):
            return False

        expected_rebased = rebase_zero_after_dual_stage(self.first)
        if expected_rebased is None or not expected_rebased.valid or not self.rebased.valid:
            return False
        if not same_construction_state(
            expected_rebased.embedding.state,
            self.rebased.embedding.state,
        ):
            return False
        if self.second.before_history != self.first.after_history:
            return False
        if not same_construction_state(
            self.rebased.embedding.state,
            self.second.dual_certificate.parameter.chart.base,
        ):
            return False
        if self.first.stage_id == self.second.stage_id:
            return False
        return self.second.target_has_focus_slack


FocusSlackRoute: TypeAlias = OneStageFocusSlackRoute | TwoStageFocusSlackRoute


def current_dual_parameters(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> tuple[DualDomainParameter, ...]:
    """Derive every current singleton-mode dual control from one exact embedding."""

    if not embedding.valid:
        raise ValueError("a valid retained degree-five embedding is required")
    if embedding.state.admissible_colors(embedding.focus):
        return ()

    defects = C5DefectState(embedding.boundary_colors)
    if not defects.is_saturated_four_color_boundary:
        raise ValueError("zero focus slack requires a saturated proper C5 boundary")

    chart = dual_defect_parameterization(embedding.state, embedding.focus)
    singleton_modes = tuple(
        sorted(mode for mode, count in defects.mode_counts.items() if count == 1)
    )
    if len(singleton_modes) != 2:
        raise AssertionError("saturated degree-five boundary must have two singleton modes")

    parameters: list[DualDomainParameter] = []
    for mode in singleton_modes:
        parameters.extend(derive_dual_domain_parameters(chart, embedding, mode))
    return tuple(sorted(parameters, key=_parameter_key))


def fresh_current_dual_parameters(
    embedding: DegreeFiveTriangulatedEmbedding,
    history: GraphNativeWitnessExpansionState,
) -> tuple[DualDomainParameter, ...]:
    """Current embedding-derived controls not already consumed as proof progress."""

    if history.carrier_edges != committed_carrier_edges(embedding.state):
        raise ValueError("routing history does not share the retained physical carrier")
    consumed = frozenset(history.stage_history)
    return tuple(
        parameter
        for parameter in current_dual_parameters(embedding)
        if stage_id_for_dual_parameter(parameter) not in consumed
    )


def direct_focus_slack_parameters(
    embedding: DegreeFiveTriangulatedEmbedding,
    history: GraphNativeWitnessExpansionState,
) -> tuple[DualDomainParameter, ...]:
    """Fresh controls whose exact current realization already gives A(focus) != empty."""

    return tuple(
        parameter
        for parameter in fresh_current_dual_parameters(embedding, history)
        if apply_dual_nonzero_parameter(parameter).target_has_focus_slack
    )


def routing_regime(
    embedding: DegreeFiveTriangulatedEmbedding,
    history: GraphNativeWitnessExpansionState,
) -> RoutingRegime:
    """Classify current access without encoding theorem status into ConstructionState."""

    fresh = fresh_current_dual_parameters(embedding, history)
    if not fresh:
        return "unavailable"
    if any(
        apply_dual_nonzero_parameter(parameter).target_has_focus_slack
        for parameter in fresh
    ):
        return "direct"
    return "pivot"


def route_focus_slack_within_two_stages(
    embedding: DegreeFiveTriangulatedEmbedding,
    history: GraphNativeWitnessExpansionState,
) -> FocusSlackRoute | None:
    """Exact two-stage receding-horizon router for the current dual control layer.

    The router first prefers any *current* fresh control that yields positive
    focus palette slack.  Only when no such direct control exists does it try a
    current pivot, rebase the shared zero-point to the exact successor, derive
    the successor controls afresh, and ask for one fresh direct stage there.

    Returning ``None`` is evidence only that this certified two-stage control
    layer did not supply a route.  It is not a Four Color theorem status.
    """

    if not embedding.valid:
        raise ValueError("a valid retained degree-five embedding is required")
    if embedding.state.admissible_colors(embedding.focus):
        raise ValueError("two-stage routing is only defined for zero focus slack")

    current = fresh_current_dual_parameters(embedding, history)

    # Smooth/direct regime: do not pay a staging cost when the current geometry
    # already exposes a certified focus-slack control.
    for parameter in current:
        stage = apply_graph_native_dual_stage(parameter, history)
        if stage.target_has_focus_slack:
            direct_route = OneStageFocusSlackRoute(embedding, history, stage)
            if not direct_route.valid:
                raise AssertionError("direct focus-slack route failed certification")
            return direct_route

    # Pivot regime: current controls are lawful but none directly changes the
    # focus observable.  Execute only one simulated/current pivot at a time,
    # rebase to its exact successor, then derive the next access from that z0.
    for parameter in current:
        first = apply_graph_native_dual_stage(parameter, history)
        if first.target_has_focus_slack:
            raise AssertionError("direct route was missed before pivot routing")
        rebased = rebase_zero_after_dual_stage(first)
        if rebased is None:
            raise AssertionError("zero-slack pivot did not produce a successor zero-point")

        second_parameters = tuple(
            sorted(
                fresh_dual_parameters_at_zero(rebased, first.after_history),
                key=_parameter_key,
            )
        )
        for second_parameter in second_parameters:
            second = apply_graph_native_dual_stage(
                second_parameter,
                first.after_history,
            )
            if not second.target_has_focus_slack:
                continue
            staged_route = TwoStageFocusSlackRoute(
                embedding=embedding,
                before_history=history,
                first=first,
                rebased=rebased,
                second=second,
            )
            if not staged_route.valid:
                raise AssertionError("two-stage focus-slack route failed certification")
            return staged_route

    return None


def _parameter_key(parameter: DualDomainParameter) -> str:
    return stage_id_for_dual_parameter(parameter).token

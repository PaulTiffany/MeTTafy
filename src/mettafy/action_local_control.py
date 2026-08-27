from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.active_inference_boundary import CertifiedInstantiation, instantiate
from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    GraphNativeDualStageCertificate,
    apply_graph_native_dual_stage,
)
from mettafy.plane_dual_control import DualDomainParameter
from mettafy.witness_expansion import GraphNativeWitnessExpansionState

DecisionKind: TypeAlias = Literal["counterfactual_change_direction", "commit_focus"]


def coloring_hamming_distance(
    before: ConstructionState,
    after: ConstructionState,
) -> int:
    """INFERENCE: count changed assignments on one fixed coloring carrier."""

    if dict(before.graph) != dict(after.graph):
        raise ValueError("coloring distance requires one fixed graph carrier")
    missing = object()
    return sum(
        before.coloring.get(vertex, missing) != after.coloring.get(vertex, missing)
        for vertex in before.graph
    )


# Historical name retained for archived diagnostics. This is not construction time.
construction_hamming_distance = coloring_hamming_distance


@dataclass(frozen=True)
class CounterfactualDirectionChange:
    """INFERENCE: one chosen dual control and one imagined coloring response.

    The graph-native stage is retained as an exact witness/falsifier, but its
    recolored ``after`` snapshot is not construction history and cannot itself
    authorize a focus commitment.
    """

    parameter: DualDomainParameter
    before_history: GraphNativeWitnessExpansionState
    stage: GraphNativeDualStageCertificate

    @property
    def decision(self) -> DecisionKind:
        return "counterfactual_change_direction"

    @property
    def before(self) -> ConstructionState:
        return self.parameter.chart.base

    @property
    def after(self) -> ConstructionState:
        """INFERENCE: the imagined response snapshot."""

        return self.stage.dual_certificate.after

    @property
    def imagined_state_count(self) -> int:
        return 1

    @property
    def displacement(self) -> int:
        return coloring_hamming_distance(self.before, self.after)

    @property
    def finite_displacement_budget(self) -> int:
        return len(self.before.coloring)

    @property
    def valid(self) -> bool:
        focus = self.parameter.continuation.embedding.focus
        if not self.parameter.valid or not self.stage.valid:
            return False
        if self.stage.before_history != self.before_history:
            return False
        if self.stage.dual_certificate.parameter is not self.parameter:
            return False
        if self.before.admissible_colors(focus):
            return False
        if focus in self.before.coloring or focus in self.after.coloring:
            return False
        if dict(self.before.graph) != dict(self.after.graph):
            return False
        if set(self.before.coloring) != set(self.after.coloring):
            return False
        return (
            self.imagined_state_count == 1
            and 0 < self.displacement <= self.finite_displacement_budget
            and self.after.committed_edges_valid
        )


def imagine_change_direction(
    parameter: DualDomainParameter,
    history: GraphNativeWitnessExpansionState,
) -> CounterfactualDirectionChange:
    """INFERENCE: evaluate one chosen current dual parameter without realizing it."""

    stage = apply_graph_native_dual_stage(parameter, history)
    change = CounterfactualDirectionChange(
        parameter=parameter,
        before_history=history,
        stage=stage,
    )
    if not change.valid:
        raise AssertionError("chosen counterfactual direction change failed certification")
    return change


# Compatibility aliases preserve archived experiments while making new names carry
# the authoritative semantics. They remain inference-only.
ChangeDirectionAction = CounterfactualDirectionChange
realize_change_direction = imagine_change_direction


@dataclass(frozen=True)
class CommitFocusAction:
    """REALIZED: execute one previously certified ``void -> V4`` event."""

    certificate: CertifiedInstantiation
    after: ConstructionState

    @property
    def decision(self) -> DecisionKind:
        return "commit_focus"

    @property
    def before(self) -> ConstructionState:
        return self.certificate.realized

    @property
    def focus(self) -> str:
        return self.certificate.focus

    @property
    def color(self) -> int:
        return self.certificate.color

    @property
    def affected_state(self) -> ConstructionState:
        return self.after

    @property
    def affected_state_count(self) -> int:
        return 1

    @property
    def displacement(self) -> int:
        return coloring_hamming_distance(self.before, self.after)

    @property
    def finite_displacement_budget(self) -> int:
        return 1

    @property
    def valid(self) -> bool:
        if not self.certificate.valid:
            return False
        if dict(self.before.graph) != dict(self.after.graph):
            return False
        expected = dict(self.before.coloring)
        expected[self.focus] = self.color
        return (
            dict(self.after.coloring) == expected
            and self.affected_state_count == 1
            and self.displacement == self.finite_displacement_budget == 1
            and self.after.committed_edges_valid
        )


def realize_focus_commit(certificate: CertifiedInstantiation) -> CommitFocusAction:
    """REALIZED: execute only an explicit construction-authority certificate."""

    after = instantiate(certificate)
    action = CommitFocusAction(certificate=certificate, after=after)
    if not action.valid:
        raise AssertionError("certified focus commit failed realization")
    return action

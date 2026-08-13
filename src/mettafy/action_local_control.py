from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    GraphNativeDualStageCertificate,
    apply_graph_native_dual_stage,
)
from mettafy.plane_dual_control import DualDomainParameter
from mettafy.witness_expansion import GraphNativeWitnessExpansionState

DecisionKind: TypeAlias = Literal["change_direction", "commit_focus"]


def construction_hamming_distance(
    before: ConstructionState,
    after: ConstructionState,
) -> int:
    """Count changed committed assignments on one fixed graph carrier."""

    if dict(before.graph) != dict(after.graph):
        raise ValueError("construction distance requires one fixed graph carrier")
    missing = object()
    return sum(
        before.coloring.get(vertex, missing) != after.coloring.get(vertex, missing)
        for vertex in before.graph
    )


@dataclass(frozen=True)
class ChangeDirectionAction:
    """One chosen nonzero dual control and exactly one realized successor state."""

    parameter: DualDomainParameter
    before_history: GraphNativeWitnessExpansionState
    stage: GraphNativeDualStageCertificate

    @property
    def decision(self) -> DecisionKind:
        return "change_direction"

    @property
    def before(self) -> ConstructionState:
        return self.parameter.chart.base

    @property
    def after(self) -> ConstructionState:
        return self.stage.dual_certificate.after

    @property
    def affected_state(self) -> ConstructionState:
        return self.after

    @property
    def affected_state_count(self) -> int:
        return 1

    @property
    def displacement(self) -> int:
        return construction_hamming_distance(self.before, self.after)

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
            self.affected_state_count == 1
            and 0 < self.displacement <= self.finite_displacement_budget
            and self.after.committed_edges_valid
        )


def realize_change_direction(
    parameter: DualDomainParameter,
    history: GraphNativeWitnessExpansionState,
) -> ChangeDirectionAction:
    """Realize one already-chosen current dual parameter, without sibling lookahead."""

    stage = apply_graph_native_dual_stage(parameter, history)
    action = ChangeDirectionAction(
        parameter=parameter,
        before_history=history,
        stage=stage,
    )
    if not action.valid:
        raise AssertionError("chosen change-direction action failed certification")
    return action


@dataclass(frozen=True)
class CommitFocusAction:
    """Commit one currently admissible focus color.

    Focus commitment is not a stop action.  It is the ordinary Four Color
    construction step available when the exact admissible-color complement is
    nonempty.
    """

    before: ConstructionState
    focus: str
    color: int
    after: ConstructionState

    @property
    def decision(self) -> DecisionKind:
        return "commit_focus"

    @property
    def affected_state(self) -> ConstructionState:
        return self.after

    @property
    def affected_state_count(self) -> int:
        return 1

    @property
    def displacement(self) -> int:
        return construction_hamming_distance(self.before, self.after)

    @property
    def finite_displacement_budget(self) -> int:
        return 1

    @property
    def valid(self) -> bool:
        if self.focus in self.before.coloring:
            return False
        if self.color not in self.before.admissible_colors(self.focus):
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


def realize_focus_commit(
    before: ConstructionState,
    focus: str,
    color: int,
) -> CommitFocusAction:
    """Commit one chosen color only when it is admissible at the focus now."""

    if color not in before.admissible_colors(focus):
        raise ValueError("focus color is not currently admissible")
    after = before.commit(focus, color)
    action = CommitFocusAction(before=before, focus=focus, color=color, after=after)
    if not action.valid:
        raise AssertionError("chosen focus commit failed certification")
    return action

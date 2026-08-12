from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from mettafy.cacophony_router import fresh_current_dual_parameters
from mettafy.color_construction import ConstructionState
from mettafy.graph_native_staging import (
    GraphNativeDualStageCertificate,
    RebasedZeroPoint,
    apply_graph_native_dual_stage,
    rebase_zero_after_dual_stage,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.witness_expansion import GraphNativeStageId, GraphNativeWitnessExpansionState
from mettafy.zero_point_correspondence import same_construction_state


@dataclass(frozen=True)
class CertifiedStagedFocusSlackRoute:
    """Finite receding-horizon route made only from fresh graph-native controls."""

    embedding: DegreeFiveTriangulatedEmbedding
    before_history: GraphNativeWitnessExpansionState
    stages: tuple[GraphNativeDualStageCertificate, ...]
    rebased_points: tuple[RebasedZeroPoint, ...]

    @property
    def stage_count(self) -> int:
        return len(self.stages)

    @property
    def extra_stage_cost(self) -> int:
        return self.stage_count - 1

    @property
    def final_state(self) -> ConstructionState:
        if not self.stages:
            return self.embedding.state
        return self.stages[-1].dual_certificate.after

    @property
    def stage_ids(self) -> tuple[GraphNativeStageId, ...]:
        return tuple(stage.stage_id for stage in self.stages)

    @property
    def valid(self) -> bool:
        if not self.embedding.valid or not self.stages:
            return False
        if len(self.rebased_points) != len(self.stages) - 1:
            return False
        current_embedding = self.embedding
        current_history = self.before_history

        for index, stage in enumerate(self.stages):
            if not stage.valid or stage.before_history != current_history:
                return False
            if not same_construction_state(
                current_embedding.state,
                stage.dual_certificate.parameter.chart.base,
            ):
                return False

            is_last = index == len(self.stages) - 1
            if is_last:
                if not stage.target_has_focus_slack:
                    return False
                current_history = stage.after_history
                continue

            if stage.target_has_focus_slack:
                return False
            expected = rebase_zero_after_dual_stage(stage)
            if expected is None or not expected.valid:
                return False
            point = self.rebased_points[index]
            if not point.valid:
                return False
            if not same_construction_state(expected.embedding.state, point.embedding.state):
                return False
            current_embedding = point.embedding
            current_history = stage.after_history

        return (
            len(set(self.stage_ids)) == len(self.stage_ids)
            and bool(self.final_state.admissible_colors(self.embedding.focus))
        )


QueueEntry = tuple[
    DegreeFiveTriangulatedEmbedding,
    GraphNativeWitnessExpansionState,
    tuple[GraphNativeDualStageCertificate, ...],
    tuple[RebasedZeroPoint, ...],
]


def route_focus_slack_bounded(
    embedding: DegreeFiveTriangulatedEmbedding,
    history: GraphNativeWitnessExpansionState,
    *,
    max_stages: int,
) -> CertifiedStagedFocusSlackRoute | None:
    """Breadth-first receding-horizon search over fresh current dual controls.

    This is a finite certificate search, not a theorem oracle.  At every node it
    derives controls from the *current* exact embedding and filters them through
    the retained nonreplay history.  A ``None`` result means only that no route
    was certified within the caller-supplied stage budget.
    """

    if max_stages < 1:
        raise ValueError("max_stages must be positive")
    if not embedding.valid:
        raise ValueError("a valid retained degree-five embedding is required")
    if embedding.state.admissible_colors(embedding.focus):
        raise ValueError("bounded routing is only needed at zero focus slack")

    queue: deque[QueueEntry] = deque([(embedding, history, (), ())])
    seen: set[tuple[tuple[tuple[str, int], ...], frozenset[GraphNativeStageId]]] = {
        (_coloring_key(embedding.state), frozenset(history.stage_history))
    }

    while queue:
        current_embedding, current_history, stages, points = queue.popleft()
        if len(stages) >= max_stages:
            continue

        for parameter in fresh_current_dual_parameters(current_embedding, current_history):
            stage = apply_graph_native_dual_stage(parameter, current_history)
            next_stages = stages + (stage,)
            if stage.target_has_focus_slack:
                route = CertifiedStagedFocusSlackRoute(
                    embedding=embedding,
                    before_history=history,
                    stages=next_stages,
                    rebased_points=points,
                )
                if not route.valid:
                    raise AssertionError("bounded staged route failed exact certification")
                return route

            if len(next_stages) >= max_stages:
                continue
            point = rebase_zero_after_dual_stage(stage)
            if point is None:
                raise AssertionError("zero-slack stage did not retain a successor zero-point")
            next_history = stage.after_history
            key = (
                _coloring_key(point.embedding.state),
                frozenset(next_history.stage_history),
            )
            if key in seen:
                continue
            seen.add(key)
            queue.append(
                (
                    point.embedding,
                    next_history,
                    next_stages,
                    points + (point,),
                )
            )
    return None


def _coloring_key(state: ConstructionState) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(state.coloring.items()))

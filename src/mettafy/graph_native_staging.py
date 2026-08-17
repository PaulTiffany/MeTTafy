from __future__ import annotations

from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.color_construction import ConstructionState
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainNonzeroCertificate,
    DualDomainParameter,
    apply_dual_nonzero_parameter,
    canonical_edge,
    derive_dual_domain_parameters,
)
from mettafy.witness_expansion import (
    GraphNativeStageId,
    GraphNativeWitnessExpansionState,
    apply_graph_native_stage,
)
from mettafy.zero_point_correspondence import (
    ControlParameterization,
    ZeroPointCorrespondence,
    dual_defect_parameterization,
    kempe_parameterization,
    zero_point_correspondence,
)


def committed_carrier_edges(state: ConstructionState) -> frozenset[tuple[str, str]]:
    """Exact physical edge carrier available to recoloring controls."""

    committed = set(state.coloring)
    return frozenset(
        canonical_edge(vertex, neighbor)
        for vertex, neighbors in state.graph.items()
        for neighbor in neighbors
        if vertex in committed and neighbor in committed and vertex != neighbor
    )


def graph_native_witness_state(
    state: ConstructionState,
) -> GraphNativeWitnessExpansionState:
    """Initialize proof history from the fixed committed physical carrier."""

    return GraphNativeWitnessExpansionState(
        carrier_edges=committed_carrier_edges(state),
    )


def stage_id_for_dual_parameter(parameter: DualDomainParameter) -> GraphNativeStageId:
    """Content-address a dual control by mode and crossed physical cut edges."""

    return GraphNativeStageId(
        translation_mode=parameter.translation_mode,
        crossed_edges=parameter.path.crossed_edges,
    )


@dataclass(frozen=True)
class GraphNativeDualStageCertificate:
    """One dual construction move plus its nonreplay proof-history update."""

    before_history: GraphNativeWitnessExpansionState
    stage_id: GraphNativeStageId
    dual_certificate: DualDomainNonzeroCertificate
    after_history: GraphNativeWitnessExpansionState

    @property
    def target_has_focus_slack(self) -> bool:
        return self.dual_certificate.target_has_focus_slack

    @property
    def valid(self) -> bool:
        if not self.dual_certificate.valid:
            return False
        parameter = self.dual_certificate.parameter
        if self.stage_id != stage_id_for_dual_parameter(parameter):
            return False
        before = parameter.chart.base
        after = self.dual_certificate.after
        carrier = committed_carrier_edges(before)
        if carrier != self.before_history.carrier_edges:
            return False
        if committed_carrier_edges(after) != carrier:
            return False
        if self.stage_id in self.before_history.stage_history:
            return False
        try:
            expected_history = apply_graph_native_stage(
                self.before_history,
                self.stage_id,
            )
        except ValueError:
            return False
        return expected_history == self.after_history


def apply_graph_native_dual_stage(
    parameter: DualDomainParameter,
    history: GraphNativeWitnessExpansionState,
) -> GraphNativeDualStageCertificate:
    """Use a legal dual symmetry once as proof progress on its physical carrier.

    The underlying domain translation remains a reversible graph symmetry.  The
    history layer only prevents the same content-addressed physical cut and V4
    mode from being counted twice as construction progress.
    """

    if committed_carrier_edges(parameter.chart.base) != history.carrier_edges:
        raise ValueError("dual parameter does not act on the retained physical carrier")

    stage_id = stage_id_for_dual_parameter(parameter)
    after_history = apply_graph_native_stage(history, stage_id)
    dual_certificate = apply_dual_nonzero_parameter(parameter)
    certificate = GraphNativeDualStageCertificate(
        before_history=history,
        stage_id=stage_id,
        dual_certificate=dual_certificate,
        after_history=after_history,
    )
    if not certificate.valid:
        raise AssertionError("graph-native dual stage failed exact certification")
    return certificate


@dataclass(frozen=True)
class RebasedZeroPoint:
    """Corresponding control parameterizations reconstructed at the actual z1."""

    embedding: DegreeFiveTriangulatedEmbedding
    kempe_chart: ControlParameterization
    dual_chart: ControlParameterization
    correspondence: ZeroPointCorrespondence

    @property
    def valid(self) -> bool:
        return (
            self.embedding.valid
            and self.correspondence.valid
            and self.kempe_chart is self.correspondence.left
            and self.dual_chart is self.correspondence.right
            and self.correspondence.shared_zero is self.embedding.state
        )


def rebase_zero_after_dual_stage(
    stage: GraphNativeDualStageCertificate,
) -> RebasedZeroPoint | None:
    """Move the common origin to the exact successor when focus slack is still zero."""

    if not stage.valid:
        raise ValueError("cannot rebase an invalid graph-native stage")
    if stage.target_has_focus_slack:
        return None

    parameter = stage.dual_certificate.parameter
    previous_embedding = parameter.continuation.embedding
    after = stage.dual_certificate.after
    embedding = DegreeFiveTriangulatedEmbedding(
        state=after,
        focus=previous_embedding.focus,
        boundary=previous_embedding.boundary,
        faces=previous_embedding.faces,
    )
    if not embedding.valid:
        raise AssertionError("ledger-preserving dual stage did not retain embedding witness")

    kempe_chart = kempe_parameterization(after)
    dual_chart = dual_defect_parameterization(after, embedding.focus)
    correspondence = zero_point_correspondence(kempe_chart, dual_chart)
    rebased = RebasedZeroPoint(
        embedding=embedding,
        kempe_chart=kempe_chart,
        dual_chart=dual_chart,
        correspondence=correspondence,
    )
    if not rebased.valid:
        raise AssertionError("successor control parameterizations failed shared-z0 certification")
    return rebased


def dual_parameters_at_zero(point: RebasedZeroPoint) -> tuple[DualDomainParameter, ...]:
    """Derive all current singleton-mode dual controls from the retained embedding."""

    if not point.valid:
        raise ValueError("a valid rebased zero-point is required")
    defects = C5DefectState(point.embedding.boundary_colors)
    if not defects.is_saturated_four_color_boundary:
        raise ValueError("dual continuation requires zero focus slack on a saturated C5")

    singleton_modes = tuple(
        mode for mode, count in defects.mode_counts.items() if count == 1
    )
    if len(singleton_modes) != 2:
        raise AssertionError("saturated degree-five boundary must have two singleton modes")

    parameters: list[DualDomainParameter] = []
    for mode in singleton_modes:
        parameters.extend(
            derive_dual_domain_parameters(
                point.dual_chart,
                point.embedding,
                mode,
            )
        )
    return tuple(parameters)


def fresh_dual_parameters_at_zero(
    point: RebasedZeroPoint,
    history: GraphNativeWitnessExpansionState,
) -> tuple[DualDomainParameter, ...]:
    """Current graph-derived dual controls not previously consumed as proof progress."""

    if committed_carrier_edges(point.embedding.state) != history.carrier_edges:
        raise ValueError("rebased zero-point does not share the retained physical carrier")
    return tuple(
        parameter
        for parameter in dual_parameters_at_zero(point)
        if stage_id_for_dual_parameter(parameter) not in history.stage_history
    )

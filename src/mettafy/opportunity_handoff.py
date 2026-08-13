from __future__ import annotations

from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.dual_path_switching import selected_dual_primal_edges
from mettafy.plane_dual_control import (
    DualDomainParameter,
    Edge,
    derive_dual_domain_parameters,
    derive_embedded_dual_continuation,
)
from mettafy.plane_parameterization import NONZERO_MODES, V4
from mettafy.shared_opportunity_transport import (
    SharedOpportunityTransportCertificate,
    certify_shared_opportunity_transport,
)
from mettafy.zero_point_correspondence import dual_defect_parameterization


@dataclass(frozen=True)
class OpportunityHandoffCertificate:
    """Exact local handoff after one realized sigma consequence.

    A source action in singleton direction sigma preserves its own two-mode
    opportunity carrier.  Each of the other two directional carriers is
    retyped by symmetric difference with the one realized physical path P.

    If focus slack is now positive, the local construction may stop and no
    successor direction is asserted.  If zero focus slack persists, sigma is
    still singleton and exactly one of the two modes in O_sigma is the other
    singleton direction currently applicable at the successor.
    """

    transport: SharedOpportunityTransportCertificate

    @property
    def parameter(self) -> DualDomainParameter:
        return self.transport.parameter

    @property
    def source_mode(self) -> V4:
        return self.transport.sigma

    @property
    def opportunity_modes(self) -> tuple[V4, V4]:
        return self.transport.opportunity_modes

    @property
    def path_edges(self) -> frozenset[Edge]:
        return self.transport.path_edges

    @property
    def stop_available(self) -> bool:
        embedding = self.transport.after_embedding
        return bool(embedding.state.admissible_colors(embedding.focus))

    @property
    def source_other_singleton_mode(self) -> V4:
        defects = C5DefectState(self.transport.before_embedding.boundary_colors)
        modes = tuple(
            mode
            for mode, count in defects.mode_counts.items()
            if count == 1 and mode != self.source_mode
        )
        if len(modes) != 1:
            raise AssertionError("source must have exactly one other singleton mode")
        return modes[0]

    @property
    def resulting_other_singleton_mode(self) -> V4 | None:
        if self.stop_available:
            return None
        defects = C5DefectState(self.transport.after_embedding.boundary_colors)
        modes = tuple(
            mode
            for mode, count in defects.mode_counts.items()
            if count == 1 and mode != self.source_mode
        )
        if len(modes) != 1:
            raise AssertionError("zero-slack successor must have one other singleton mode")
        return modes[0]

    @property
    def direction_changed(self) -> bool | None:
        resulting = self.resulting_other_singleton_mode
        if resulting is None:
            return None
        return resulting != self.source_other_singleton_mode

    def carrier_before(self, mode: V4) -> frozenset[Edge]:
        return selected_dual_primal_edges(self.transport.before_embedding, mode)

    def carrier_after(self, mode: V4) -> frozenset[Edge]:
        return selected_dual_primal_edges(self.transport.after_embedding, mode)

    @property
    def valid(self) -> bool:
        if not self.transport.valid:
            return False

        sigma = self.source_mode
        if sigma not in NONZERO_MODES:
            return False
        if frozenset(self.opportunity_modes) != frozenset(
            mode for mode in NONZERO_MODES if mode != sigma
        ):
            return False

        if self.carrier_after(sigma) != self.carrier_before(sigma):
            return False

        for mode in self.opportunity_modes:
            if self.carrier_after(mode) != self.carrier_before(mode).symmetric_difference(
                self.path_edges
            ):
                return False

        if self.stop_available:
            return self.resulting_other_singleton_mode is None

        after = self.transport.after_embedding
        defects = C5DefectState(after.boundary_colors)
        if not defects.is_saturated_four_color_boundary:
            return False
        if defects.mode_counts[sigma] != 1:
            return False

        resulting = self.resulting_other_singleton_mode
        if resulting is None or resulting not in self.opportunity_modes:
            return False

        continuation = derive_embedded_dual_continuation(after, resulting)
        return continuation.valid and continuation.translation_mode == resulting


def certify_opportunity_handoff(
    parameter: DualDomainParameter,
) -> OpportunityHandoffCertificate:
    """Certify stop-or-current-handoff after one chosen present action."""

    certificate = OpportunityHandoffCertificate(
        transport=certify_shared_opportunity_transport(parameter)
    )
    if not certificate.valid:
        raise AssertionError("cross-direction opportunity handoff failed certification")
    return certificate


@dataclass(frozen=True)
class CurrentOpportunityTotalityCertificate:
    """Either stop is available now, or four current dual controls exist now.

    No route or future destination is stored.  When zero focus slack persists,
    the actual successor is reparameterized at its own zero-point and the two
    singleton directions each yield their two embedding-derived path controls.
    """

    handoff: OpportunityHandoffCertificate
    current_parameters: tuple[DualDomainParameter, ...]

    @property
    def valid(self) -> bool:
        if not self.handoff.valid:
            return False
        after = self.handoff.transport.after_embedding

        if self.handoff.stop_available:
            return (
                bool(after.state.admissible_colors(after.focus))
                and not self.current_parameters
            )

        if after.state.admissible_colors(after.focus):
            return False
        defects = C5DefectState(after.boundary_colors)
        if not defects.is_saturated_four_color_boundary:
            return False

        singleton_modes = frozenset(
            mode for mode, count in defects.mode_counts.items() if count == 1
        )
        resulting = self.handoff.resulting_other_singleton_mode
        if resulting is None:
            return False
        if singleton_modes != frozenset({self.handoff.source_mode, resulting}):
            return False
        if len(self.current_parameters) != 4:
            return False
        if any(not parameter.valid for parameter in self.current_parameters):
            return False
        if any(
            parameter.continuation.embedding != after
            for parameter in self.current_parameters
        ):
            return False

        mode_counts = {
            mode: sum(
                parameter.translation_mode == mode
                for parameter in self.current_parameters
            )
            for mode in singleton_modes
        }
        return set(mode_counts.values()) == {2}


def certify_current_opportunity_totality(
    parameter: DualDomainParameter,
) -> CurrentOpportunityTotalityCertificate:
    """Certify present stop-or-four-control totality after one current action."""

    handoff = certify_opportunity_handoff(parameter)
    after = handoff.transport.after_embedding
    if handoff.stop_available:
        current: tuple[DualDomainParameter, ...] = ()
    else:
        defects = C5DefectState(after.boundary_colors)
        singleton_modes = tuple(
            sorted(mode for mode, count in defects.mode_counts.items() if count == 1)
        )
        chart = dual_defect_parameterization(after.state, after.focus)
        parameters: list[DualDomainParameter] = []
        for mode in singleton_modes:
            parameters.extend(derive_dual_domain_parameters(chart, after, mode))
        current = tuple(parameters)

    certificate = CurrentOpportunityTotalityCertificate(
        handoff=handoff,
        current_parameters=current,
    )
    if not certificate.valid:
        raise AssertionError("current opportunity totality failed certification")
    return certificate

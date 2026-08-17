from __future__ import annotations

from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.handed_opportunity_pair import (
    HandedOffOpportunityPairCertificate,
    certify_handed_off_opportunity_pair,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    derive_dual_domain_parameters,
)
from mettafy.plane_parameterization import V4
from mettafy.shared_opportunity_transport import (
    SharedOpportunityTransportCertificate,
    certify_shared_opportunity_transport,
)
from mettafy.zero_point_correspondence import (
    dual_defect_parameterization,
    same_construction_state,
)


@dataclass(frozen=True)
class HandedPairCompletionBranch:
    """One member of a handed pair realized first, then the surviving sibling.

    Defined only when the first action retains zero focus slack.  The second
    control is re-derived at the actual successor and matched by its retained
    physical path, rather than copied forward as a future coordinate.
    """

    first: SharedOpportunityTransportCertificate
    second_parameter: DualDomainParameter
    second: SharedOpportunityTransportCertificate

    @property
    def final_embedding(self) -> DegreeFiveTriangulatedEmbedding:
        return self.second.after_embedding

    @property
    def valid(self) -> bool:
        if not self.first.valid or not self.second.valid:
            return False
        if self.second.parameter is not self.second_parameter:
            return False
        if self.first.after_embedding.state.admissible_colors(
            self.first.after_embedding.focus
        ):
            return False
        if self.second_parameter.chart.base is not self.first.after_embedding.state:
            return False
        return self.second_parameter.translation_mode == self.first.sigma


@dataclass(frozen=True)
class HandedOpportunityPairDynamicsCertificate:
    """Joint law of the two controls sharing one handed-off opportunity.

    The pair has a homogeneous immediate focus response: either both members
    expose a focus color commitment, or neither does.  In the persistent case,
    realizing both members in either order gives the same final construction
    state and swaps the repeated/other-singleton V4 roles while keeping the
    handed mode singleton.
    """

    pair: HandedOffOpportunityPairCertificate
    first_transports: tuple[
        SharedOpportunityTransportCertificate,
        SharedOpportunityTransportCertificate,
    ]
    completions: tuple[HandedPairCompletionBranch, ...]

    @property
    def handed_mode(self) -> V4 | None:
        return self.pair.handed_mode

    @property
    def focus_commit_flags(self) -> tuple[bool, bool]:
        return tuple(
            bool(
                transport.after_embedding.state.admissible_colors(
                    transport.after_embedding.focus
                )
            )
            for transport in self.first_transports
        )  # type: ignore[return-value]

    @property
    def homogeneous_focus_response(self) -> bool:
        return self.focus_commit_flags[0] == self.focus_commit_flags[1]

    @property
    def persistent(self) -> bool:
        return not self.focus_commit_flags[0]

    @property
    def valid(self) -> bool:
        if not self.pair.valid or self.pair.focus_commit_available:
            return False
        if len(self.pair.handed_parameters) != 2:
            return False
        if any(not transport.valid for transport in self.first_transports):
            return False
        if tuple(
            transport.parameter for transport in self.first_transports
        ) != self.pair.handed_parameters:
            return False
        if not self.homogeneous_focus_response:
            return False

        if not self.persistent:
            return not self.completions
        if len(self.completions) != 2 or any(
            not completion.valid for completion in self.completions
        ):
            return False

        final_first = self.completions[0].final_embedding
        final_second = self.completions[1].final_embedding
        if not same_construction_state(final_first.state, final_second.state):
            return False

        mode = self.handed_mode
        if mode is None:
            return False
        start = self.pair.totality.handoff.transport.after_embedding
        start_defects = C5DefectState(start.boundary_colors)
        final_defects = C5DefectState(final_first.boundary_colors)
        if not start_defects.is_saturated_four_color_boundary:
            return False
        if not final_defects.is_saturated_four_color_boundary:
            return False

        repeated = next(
            candidate
            for candidate, count in start_defects.mode_counts.items()
            if count == 3
        )
        other_singleton = next(
            candidate
            for candidate, count in start_defects.mode_counts.items()
            if count == 1 and candidate != mode
        )
        return (
            start_defects.mode_counts[mode] == 1
            and final_defects.mode_counts[mode] == 1
            and final_defects.mode_counts[repeated] == 1
            and final_defects.mode_counts[other_singleton] == 3
            and not final_first.state.admissible_colors(final_first.focus)
        )


def _remaining_parameter_after(
    first: SharedOpportunityTransportCertificate,
    remaining_source: DualDomainParameter,
) -> DualDomainParameter:
    after = first.after_embedding
    chart = dual_defect_parameterization(after.state, after.focus)
    current = derive_dual_domain_parameters(chart, after, first.sigma)
    matches = tuple(
        parameter
        for parameter in current
        if parameter.path.crossed_edges == remaining_source.path.crossed_edges
        and parameter.path.terminal_edges == remaining_source.path.terminal_edges
    )
    if len(matches) != 1:
        raise AssertionError("retained sibling path did not rederive uniquely")
    return matches[0]


def certify_handed_opportunity_pair_dynamics(
    parameter: DualDomainParameter,
) -> HandedOpportunityPairDynamicsCertificate | None:
    """Certify the joint two-control law handed off by one actual predecessor."""

    pair = certify_handed_off_opportunity_pair(parameter)
    if pair.focus_commit_available:
        return None

    first = tuple(
        certify_shared_opportunity_transport(current)
        for current in pair.handed_parameters
    )
    if len(first) != 2:
        raise AssertionError("handed opportunity did not contain exactly two controls")
    first_transports = (first[0], first[1])
    flags = tuple(
        bool(
            transport.after_embedding.state.admissible_colors(
                transport.after_embedding.focus
            )
        )
        for transport in first_transports
    )
    if flags[0] != flags[1]:
        raise AssertionError("handed pair lost its homogeneous focus response")

    completions: tuple[HandedPairCompletionBranch, ...]
    if flags[0]:
        completions = ()
    else:
        branches: list[HandedPairCompletionBranch] = []
        for index in range(2):
            other = pair.handed_parameters[1 - index]
            second_parameter = _remaining_parameter_after(first_transports[index], other)
            branches.append(
                HandedPairCompletionBranch(
                    first=first_transports[index],
                    second_parameter=second_parameter,
                    second=certify_shared_opportunity_transport(second_parameter),
                )
            )
        completions = tuple(branches)

    certificate = HandedOpportunityPairDynamicsCertificate(
        pair=pair,
        first_transports=first_transports,
        completions=completions,
    )
    if not certificate.valid:
        raise AssertionError("handed opportunity pair dynamics failed certification")
    return certificate

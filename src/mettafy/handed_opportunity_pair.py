from __future__ import annotations

from dataclasses import dataclass

from mettafy.opportunity_handoff import (
    CurrentOpportunityTotalityCertificate,
    certify_current_opportunity_totality,
)
from mettafy.plane_dual_control import DualDomainParameter
from mettafy.plane_parameterization import V4


@dataclass(frozen=True)
class HandedOffOpportunityPairCertificate:
    """The two current controls carried by the successor's handed-off direction.

    This object is deliberately smaller than the successor's full four-control
    permission surface.  It retains only the *resulting other singleton mode*
    supplied by the actual zero-slack successor and the two embedding-derived
    controls in that direction.

    Focus admissibility is a color-commit permission, not a stop action.  If a
    focus color can be committed now, no handed-off dual pair is required.
    """

    totality: CurrentOpportunityTotalityCertificate
    handed_parameters: tuple[DualDomainParameter, ...]

    @property
    def focus_commit_available(self) -> bool:
        return self.totality.handoff.focus_commit_available

    @property
    def handed_mode(self) -> V4 | None:
        return self.totality.handoff.resulting_other_singleton_mode

    @property
    def valid(self) -> bool:
        if not self.totality.valid:
            return False
        if self.focus_commit_available:
            return self.handed_mode is None and not self.handed_parameters

        mode = self.handed_mode
        if mode is None:
            return False
        if mode not in self.totality.handoff.opportunity_modes:
            return False
        if len(self.handed_parameters) != 2:
            return False
        if any(not parameter.valid for parameter in self.handed_parameters):
            return False
        if any(parameter.translation_mode != mode for parameter in self.handed_parameters):
            return False

        expected = tuple(
            parameter
            for parameter in self.totality.current_parameters
            if parameter.translation_mode == mode
        )
        return self.handed_parameters == expected


def certify_handed_off_opportunity_pair(
    parameter: DualDomainParameter,
) -> HandedOffOpportunityPairCertificate:
    """Derive exactly the two controls in the direction handed off now."""

    totality = certify_current_opportunity_totality(parameter)
    mode = totality.handoff.resulting_other_singleton_mode
    if totality.handoff.focus_commit_available:
        handed: tuple[DualDomainParameter, ...] = ()
    else:
        if mode is None:
            raise AssertionError("zero-slack successor lost its handed-off singleton mode")
        handed = tuple(
            current
            for current in totality.current_parameters
            if current.translation_mode == mode
        )

    certificate = HandedOffOpportunityPairCertificate(
        totality=totality,
        handed_parameters=handed,
    )
    if not certificate.valid:
        raise AssertionError("handed-off opportunity pair failed exact certification")
    return certificate

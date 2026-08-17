from __future__ import annotations

from dataclasses import dataclass

from mettafy.dual_path_switching import (
    AlternatingPathSwitchCertificate,
    certify_alternating_path_switch,
)
from mettafy.dual_phase_topology import (
    PhaseTopologyCertificate,
    certify_phase_topology,
)
from mettafy.plane_dual_control import DualDomainParameter


@dataclass(frozen=True)
class DualControlTopologyDeltaCertificate:
    """Exact local topological change induced by one current dual control.

    The degree-five phase identity is

        Phi = 10 + 2 C - S.

    Because a certified path switch preserves the same pentagonal carrier, its
    local change therefore obeys

        Delta Phi = 2 Delta C - Delta S.

    This certificate concerns one currently applicable control only.  It
    contains no future route or destination coordinate.
    """

    parameter: DualDomainParameter
    switch: AlternatingPathSwitchCertificate
    before: PhaseTopologyCertificate
    after: PhaseTopologyCertificate

    @property
    def delta_cycles(self) -> int:
        return self.after.alternating_cycle_count - self.before.alternating_cycle_count

    @property
    def delta_two_edge_terminal_paths(self) -> int:
        return (
            self.after.two_edge_terminal_path_count
            - self.before.two_edge_terminal_path_count
        )

    @property
    def delta_phase_rank(self) -> int:
        return (
            self.after.phase.phase_fragment_rank
            - self.before.phase.phase_fragment_rank
        )

    @property
    def predicted_delta_phase_rank(self) -> int:
        return 2 * self.delta_cycles - self.delta_two_edge_terminal_paths

    @property
    def valid(self) -> bool:
        if (
            not self.parameter.valid
            or not self.switch.valid
            or not self.before.valid
            or not self.after.valid
        ):
            return False
        if self.switch.parameter != self.parameter:
            return False
        if self.before.embedding != self.parameter.continuation.embedding:
            return False
        if self.after.embedding != self.switch.after_embedding:
            return False
        if self.before.embedding.boundary != self.after.embedding.boundary:
            return False
        if self.before.boundary_terminal_incidence_count != 10:
            return False
        if self.after.boundary_terminal_incidence_count != 10:
            return False
        return self.delta_phase_rank == self.predicted_delta_phase_rank


def certify_dual_control_topology_delta(
    parameter: DualDomainParameter,
) -> DualControlTopologyDeltaCertificate:
    """Certify Delta Phi = 2 Delta C - Delta S for one exact path switch."""

    if not parameter.valid:
        raise ValueError("a valid current dual parameter is required")
    switch = certify_alternating_path_switch(parameter)
    certificate = DualControlTopologyDeltaCertificate(
        parameter=parameter,
        switch=switch,
        before=certify_phase_topology(parameter.continuation.embedding),
        after=certify_phase_topology(switch.after_embedding),
    )
    if not certificate.valid:
        raise AssertionError("dual control topology delta failed exact certification")
    return certificate

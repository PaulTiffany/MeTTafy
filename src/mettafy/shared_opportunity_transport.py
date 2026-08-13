from __future__ import annotations

from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.dual_path_switching import (
    AlternatingPathSwitchCertificate,
    certify_alternating_path_switch,
    disk_primal_edges,
    selected_dual_primal_edges,
)
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    Edge,
    canonical_edge,
    derive_embedded_dual_continuation,
)
from mettafy.plane_parameterization import V4, color_difference, v4_add
from mettafy.v4_action_lipschitz import edge_opportunity_modes


@dataclass(frozen=True)
class SharedOpportunityTransportCertificate:
    """One realized path consequence preserves the selected shared opportunity.

    Fix a current singleton translation mode sigma.  The other two nonzero V4
    modes form one shared opportunity class O_sigma.  The selected dual carrier
    is exactly the physical union of edges carrying those two modes.

    A sigma-domain action realizes one path P inside that carrier.  Along P the
    two opportunity labels exchange; outside P they do not change.  The physical
    opportunity carrier itself, its local degree-two passage through every disk
    triangle, and its two exact continuation paths are therefore retained.
    """

    parameter: DualDomainParameter
    switch: AlternatingPathSwitchCertificate

    @property
    def sigma(self) -> V4:
        return self.parameter.translation_mode

    @property
    def opportunity_modes(self) -> tuple[V4, V4]:
        return edge_opportunity_modes(self.sigma)

    @property
    def before_embedding(self) -> DegreeFiveTriangulatedEmbedding:
        return self.parameter.continuation.embedding

    @property
    def after_embedding(self) -> DegreeFiveTriangulatedEmbedding:
        return self.switch.after_embedding

    @property
    def path_edges(self) -> frozenset[Edge]:
        return frozenset(self.parameter.path.crossed_edges)

    @property
    def opportunity_carrier_before(self) -> frozenset[Edge]:
        return selected_dual_primal_edges(self.before_embedding, self.sigma)

    @property
    def opportunity_carrier_after(self) -> frozenset[Edge]:
        return selected_dual_primal_edges(self.after_embedding, self.sigma)

    @property
    def valid(self) -> bool:
        if not self.parameter.valid or not self.switch.valid:
            return False
        if self.switch.parameter is not self.parameter:
            return False

        before_defects = C5DefectState(self.before_embedding.boundary_colors)
        after_defects = C5DefectState(self.after_embedding.boundary_colors)
        if not before_defects.is_saturated_four_color_boundary:
            return False
        if before_defects.mode_counts[self.sigma] != 1:
            return False
        if after_defects.mode_counts[self.sigma] != 1:
            return False

        opportunity = frozenset(self.opportunity_modes)
        if self.opportunity_carrier_before != self.opportunity_carrier_after:
            return False
        if not self.path_edges <= self.opportunity_carrier_before:
            return False

        before_continuation = self.parameter.continuation
        after_continuation = derive_embedded_dual_continuation(
            self.after_embedding,
            self.sigma,
        )
        if after_continuation.terminal_pairing != before_continuation.terminal_pairing:
            return False
        if after_continuation.paths != before_continuation.paths:
            return False

        disk_edges = disk_primal_edges(self.before_embedding)
        if disk_edges != disk_primal_edges(self.after_embedding):
            return False

        for face in self.before_embedding.disk_faces:
            face_edges = frozenset(
                canonical_edge(face[index], face[(index + 1) % 3])
                for index in range(3)
            )
            if len(face_edges.intersection(self.opportunity_carrier_before)) != 2:
                return False
            if len(face_edges.intersection(self.opportunity_carrier_after)) != 2:
                return False

        for edge in disk_edges:
            before_mode = color_difference(
                self.before_embedding.state.coloring[edge[0]],
                self.before_embedding.state.coloring[edge[1]],
            )
            after_mode = color_difference(
                self.after_embedding.state.coloring[edge[0]],
                self.after_embedding.state.coloring[edge[1]],
            )
            if edge in self.path_edges:
                if before_mode not in opportunity or after_mode not in opportunity:
                    return False
                if after_mode != v4_add(before_mode, self.sigma):
                    return False
                if frozenset({before_mode, after_mode}) != opportunity:
                    return False
            elif before_mode != after_mode:
                return False

        return True


def certify_shared_opportunity_transport(
    parameter: DualDomainParameter,
) -> SharedOpportunityTransportCertificate:
    """Certify consequence/retyping without promoting opportunity to realization."""

    if not parameter.valid:
        raise ValueError("a valid current dual parameter is required")
    certificate = SharedOpportunityTransportCertificate(
        parameter=parameter,
        switch=certify_alternating_path_switch(parameter),
    )
    if not certificate.valid:
        raise AssertionError("shared opportunity transport failed exact certification")
    return certificate

from __future__ import annotations

from dataclasses import dataclass

from mettafy.dual_involution_phase import (
    DualInvolutionPhaseSignature,
    dual_involution_phase_signature,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding
from mettafy.plane_parameterization import NONZERO_MODES, V4
from mettafy.trivalent_dual_splice import (
    AlternatingComponent,
    TrivalentDualSpliceSignature,
    trivalent_dual_splice_signature,
)


def _complementary_modes(excluded_mode: V4) -> tuple[V4, V4]:
    if excluded_mode not in NONZERO_MODES:
        raise ValueError("excluded mode must be nonzero in V4")
    modes = tuple(mode for mode in NONZERO_MODES if mode != excluded_mode)
    return (modes[0], modes[1])


def _is_two_edge_terminal_path(component: AlternatingComponent) -> bool:
    return not component.is_cycle and len(component.primal_edges) == 2


@dataclass(frozen=True)
class PhaseTopologyCertificate:
    """Exact topological accounting of the dual involution phase rank.

    Each complementary two-mode network is a disjoint union of terminal paths
    and internal alternating cycles.  The ordered product of its two matching
    involutions advances by two matching arcs.  Every ordinary path and every
    cycle therefore contributes two parity fragments; the unique degenerate
    case is a terminal path of exactly two arcs, whose two parities meet in one
    product fragment.

    Summing the three complementary networks gives

        Phi = 2 P + 2 C - S,

    where P is the total number of terminal paths, C the total number of
    internal alternating cycles, and S the number of two-edge terminal paths.
    For a pentagonal boundary every physical boundary edge is selected in two
    of the three complementary networks, so there are ten terminal incidences,
    hence P = 5 and

        Phi = 10 + 2 C - S.
    """

    embedding: DegreeFiveTriangulatedEmbedding
    phase: DualInvolutionPhaseSignature
    splice: TrivalentDualSpliceSignature

    @property
    def terminal_path_count(self) -> int:
        return sum(
            1
            for mode in NONZERO_MODES
            for component in self.splice.components(mode)
            if not component.is_cycle
        )

    @property
    def alternating_cycle_count(self) -> int:
        return self.splice.total_alternating_cycles

    @property
    def two_edge_terminal_path_count(self) -> int:
        return sum(
            1
            for mode in NONZERO_MODES
            for component in self.splice.components(mode)
            if _is_two_edge_terminal_path(component)
        )

    @property
    def boundary_terminal_incidence_count(self) -> int:
        return sum(
            len(component.terminals)
            for mode in NONZERO_MODES
            for component in self.splice.components(mode)
        )

    @property
    def topological_phase_rank(self) -> int:
        return (
            2 * self.terminal_path_count
            + 2 * self.alternating_cycle_count
            - self.two_edge_terminal_path_count
        )

    @property
    def degree_five_phase_rank(self) -> int:
        return (
            10
            + 2 * self.alternating_cycle_count
            - self.two_edge_terminal_path_count
        )

    def network_fragment_prediction(self, excluded_mode: V4) -> int:
        components = self.splice.components(excluded_mode)
        short_paths = sum(
            1 for component in components if _is_two_edge_terminal_path(component)
        )
        return 2 * len(components) - short_paths

    @property
    def valid(self) -> bool:
        if not self.embedding.valid or not self.phase.valid or not self.splice.valid:
            return False
        if self.phase.embedding != self.embedding or self.splice.embedding != self.embedding:
            return False

        for excluded_mode in NONZERO_MODES:
            left_mode, right_mode = _complementary_modes(excluded_mode)
            product = self.phase.product(left_mode, right_mode)
            if product.fragment_count != self.network_fragment_prediction(excluded_mode):
                return False

        # Every one of the five boundary edges belongs to exactly two of the
        # three complementary networks.  The retained path/cycle decomposition
        # must therefore expose ten terminal incidences and five terminal paths.
        if self.boundary_terminal_incidence_count != 10:
            return False
        if self.terminal_path_count != 5:
            return False

        return (
            self.phase.phase_fragment_rank == self.topological_phase_rank
            and self.topological_phase_rank == self.degree_five_phase_rank
        )


def certify_phase_topology(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> PhaseTopologyCertificate:
    """Bank the exact identity Phi = 10 + 2 C - S on a retained disk."""

    certificate = PhaseTopologyCertificate(
        embedding=embedding,
        phase=dual_involution_phase_signature(embedding),
        splice=trivalent_dual_splice_signature(embedding),
    )
    if not certificate.valid:
        raise AssertionError("dual phase topological accounting failed certification")
    return certificate

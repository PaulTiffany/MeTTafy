from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.dual_path_switching import (
    AlternatingPathSwitchCertificate,
    certify_alternating_path_switch,
    dual_pairing_signature,
    disk_primal_edges,
    selected_dual_primal_edges,
)
from mettafy.plane_dual_control import DegreeFiveTriangulatedEmbedding, DualDomainParameter, Edge, Pair
from mettafy.plane_dual_pairing import DegreeFiveDualPairing
from mettafy.plane_parameterization import NONZERO_MODES, V4, color_difference, frontier_modes

SurgeryCase: TypeAlias = Literal["endpoint_slide", "interlaced_pair"]


def mode_edges(
    embedding: DegreeFiveTriangulatedEmbedding,
    mode: V4,
) -> frozenset[Edge]:
    """Physical disk edges carrying exactly one nonzero V4 mode."""

    if mode not in NONZERO_MODES:
        raise ValueError("mode must be nonzero in V4")
    return frozenset(
        edge
        for edge in disk_primal_edges(embedding)
        if color_difference(
            embedding.state.coloring[edge[0]],
            embedding.state.coloring[edge[1]],
        )
        == mode
    )


@dataclass(frozen=True)
class ModeNetworkTriangleCertificate:
    """Exact F2 algebra of the three two-mode dual carriers.

    For the three nonzero modes alpha, beta, gamma, let

        F_mu = {e : mode(e) != mu}.

    Then F_alpha xor F_beta = F_gamma, and the physical overlap of F_alpha
    and F_beta is exactly the common gamma-mode carrier.  The overlap identity
    is the important guard against treating the two dual networks as disjoint
    Jordan arcs when they actually share graph edges.
    """

    embedding: DegreeFiveTriangulatedEmbedding

    @property
    def valid(self) -> bool:
        if not self.embedding.valid:
            return False
        alpha, beta, gamma = NONZERO_MODES
        f_alpha = selected_dual_primal_edges(self.embedding, alpha)
        f_beta = selected_dual_primal_edges(self.embedding, beta)
        f_gamma = selected_dual_primal_edges(self.embedding, gamma)
        return (
            f_alpha.symmetric_difference(f_beta) == f_gamma
            and f_beta.symmetric_difference(f_gamma) == f_alpha
            and f_gamma.symmetric_difference(f_alpha) == f_beta
            and f_alpha.intersection(f_beta) == mode_edges(self.embedding, gamma)
            and f_beta.intersection(f_gamma) == mode_edges(self.embedding, alpha)
            and f_gamma.intersection(f_alpha) == mode_edges(self.embedding, beta)
        )


def cyclically_adjacent(pair: Pair, size: int = 5) -> bool:
    left, right = pair
    return left != right and (left - right) % size in (1, size - 1)


def cyclically_interlaced(first: Pair, second: Pair, size: int = 5) -> bool:
    """Whether two disjoint boundary pairs alternate around a cyclic boundary."""

    if len({*first, *second}) != 4:
        return False
    start, end = first
    span = (end - start) % size
    if span == 0:
        return False

    def strictly_between(value: int) -> bool:
        offset = (value - start) % size
        return 0 < offset < span

    return strictly_between(second[0]) != strictly_between(second[1])


@dataclass(frozen=True)
class JordanMod2SurgeryCertificate:
    """Jordan/mod-2 anatomy of one pivot dual-domain translation.

    This certificate deliberately does *not* assert that a pivot must become
    direct.  It certifies the pieces that survive that conjecture's kill test:

    * the three two-mode networks form an exact F2 triangle;
    * their pairwise intersections are shared physical single-mode carriers;
    * surgery preserves F_sigma and xors the physical path into both others;
    * the boundary endpoints are forced into one of two Jordan patterns.

    The successor pairing is retained as an observation, so a pivot-to-pivot
    transition remains representable rather than being rejected by definition.
    """

    parameter: DualDomainParameter
    switch: AlternatingPathSwitchCertificate
    repeated_mode: V4
    other_singleton_mode: V4
    case: SurgeryCase
    target_other_singleton_mode: V4

    @property
    def before(self) -> DegreeFiveTriangulatedEmbedding:
        return self.parameter.continuation.embedding

    @property
    def after(self) -> DegreeFiveTriangulatedEmbedding:
        return self.switch.after_embedding

    @property
    def path_terminals(self) -> Pair:
        return self.parameter.path.terminal_edges

    @property
    def source_regime(self) -> str:
        return dual_pairing_signature(self.before).regime

    @property
    def successor_regime(self) -> str:
        return dual_pairing_signature(self.after).regime

    @property
    def expected_direct_pairing(self) -> tuple[Pair, Pair]:
        return DegreeFiveDualPairing(
            self.after.boundary_colors,
            self.target_other_singleton_mode,
        ).opening_pairing

    @property
    def actual_target_pairing(self) -> tuple[Pair, Pair]:
        signature = dual_pairing_signature(self.after)
        for record in signature.pairings:
            if record.mode == self.target_other_singleton_mode:
                return record.terminal_pairing
        raise AssertionError("target singleton mode missing from successor signature")

    @property
    def target_pairing_is_direct(self) -> bool:
        return self.actual_target_pairing == self.expected_direct_pairing

    @property
    def jordan_boundary_parity_holds(self) -> bool:
        source_modes = frontier_modes(self.before.boundary_colors)
        sigma = self.parameter.translation_mode
        sigma_index = source_modes.index(sigma)
        beta_index = source_modes.index(self.other_singleton_mode)
        if self.case == "endpoint_slide":
            return cyclically_adjacent(self.path_terminals)
        return cyclically_interlaced(
            self.path_terminals,
            (sigma_index, beta_index),
        )

    @property
    def valid(self) -> bool:
        if not self.parameter.valid or not self.switch.valid:
            return False
        if self.switch.parameter != self.parameter:
            return False
        if self.source_regime != "pivot":
            return False
        if not ModeNetworkTriangleCertificate(self.before).valid:
            return False
        if not ModeNetworkTriangleCertificate(self.after).valid:
            return False
        if not self.jordan_boundary_parity_holds:
            return False

        defects = C5DefectState(self.before.boundary_colors)
        counts = defects.mode_counts
        sigma = self.parameter.translation_mode
        if counts[sigma] != 1:
            return False
        if counts[self.repeated_mode] != 3 or counts[self.other_singleton_mode] != 1:
            return False
        if {sigma, self.repeated_mode, self.other_singleton_mode} != set(NONZERO_MODES):
            return False

        source_modes = frontier_modes(self.before.boundary_colors)
        endpoint_modes = tuple(source_modes[index] for index in self.path_terminals)
        if self.case == "endpoint_slide":
            if set(endpoint_modes) != {self.repeated_mode, self.other_singleton_mode}:
                return False
            if self.target_other_singleton_mode != self.other_singleton_mode:
                return False
        else:
            if endpoint_modes != (self.repeated_mode, self.repeated_mode):
                return False
            if self.target_other_singleton_mode != self.repeated_mode:
                return False

        after_counts = Counter(frontier_modes(self.after.boundary_colors))
        if after_counts[sigma] != 1 or after_counts[self.target_other_singleton_mode] != 1:
            return False

        path = self.switch.path_edges
        if selected_dual_primal_edges(self.after, sigma) != selected_dual_primal_edges(
            self.before,
            sigma,
        ):
            return False
        for mode in NONZERO_MODES:
            if mode == sigma:
                continue
            if selected_dual_primal_edges(
                self.after,
                mode,
            ) != selected_dual_primal_edges(self.before, mode).symmetric_difference(path):
                return False
        return True


def certify_jordan_mod2_surgery(
    parameter: DualDomainParameter,
) -> JordanMod2SurgeryCertificate:
    """Certify exact shared-edge-aware mod-2 surgery for one pivot parameter."""

    before = parameter.continuation.embedding
    signature = dual_pairing_signature(before)
    if signature.regime != "pivot":
        raise ValueError("Jordan pivot surgery requires a pivot source geometry")

    defects = C5DefectState(before.boundary_colors)
    sigma = parameter.translation_mode
    repeated = next(mode for mode, count in defects.mode_counts.items() if count == 3)
    other_singleton = next(
        mode
        for mode, count in defects.mode_counts.items()
        if count == 1 and mode != sigma
    )
    source_modes = frontier_modes(before.boundary_colors)
    endpoint_modes = tuple(source_modes[index] for index in parameter.path.terminal_edges)
    if set(endpoint_modes) == {repeated, other_singleton}:
        case: SurgeryCase = "endpoint_slide"
        target = other_singleton
    elif endpoint_modes == (repeated, repeated):
        case = "interlaced_pair"
        target = repeated
    else:
        raise AssertionError("pivot path endpoints violate the saturated C5 Jordan cases")

    switch = certify_alternating_path_switch(parameter)
    certificate = JordanMod2SurgeryCertificate(
        parameter=parameter,
        switch=switch,
        repeated_mode=repeated,
        other_singleton_mode=other_singleton,
        case=case,
        target_other_singleton_mode=target,
    )
    if not certificate.valid:
        raise AssertionError("Jordan/mod-2 surgery failed exact certification")
    return certificate

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    DualDomainParameter,
    Edge,
    Pair,
    apply_dual_nonzero_parameter,
    canonical_edge,
    derive_dual_domain_parameters,
)
from mettafy.plane_parameterization import (
    NONZERO_MODES,
    V4,
    color_difference,
    v4_add,
)
from mettafy.zero_point_correspondence import dual_defect_parameterization

PairingKind: TypeAlias = Literal["direct", "pivot"]
PairingRegime: TypeAlias = Literal["direct", "pivot"]


@dataclass(frozen=True)
class SingletonModePairing:
    """Actual embedded pairing and focus consequence for one singleton V4 mode."""

    mode: V4
    terminal_pairing: tuple[Pair, Pair]
    kind: PairingKind


@dataclass(frozen=True)
class DualPairingSignature:
    """The two singleton-mode continuation types at one saturated degree-five z0."""

    embedding: DegreeFiveTriangulatedEmbedding
    pairings: tuple[SingletonModePairing, SingletonModePairing]

    @property
    def regime(self) -> PairingRegime:
        if any(pairing.kind == "direct" for pairing in self.pairings):
            return "direct"
        return "pivot"

    @property
    def valid(self) -> bool:
        if not self.embedding.valid:
            return False
        defects = C5DefectState(self.embedding.boundary_colors)
        if not defects.is_saturated_four_color_boundary:
            return False
        singleton_modes = frozenset(
            mode for mode, count in defects.mode_counts.items() if count == 1
        )
        if singleton_modes != frozenset(pairing.mode for pairing in self.pairings):
            return False
        return len(self.pairings) == 2


def disk_primal_edges(embedding: DegreeFiveTriangulatedEmbedding) -> frozenset[Edge]:
    """Physical primal edges met by the retained triangulated disk dual."""

    if not embedding.valid:
        raise ValueError("a valid retained triangulated embedding is required")
    return frozenset(
        canonical_edge(face[index], face[(index + 1) % 3])
        for face in embedding.disk_faces
        for index in range(3)
    )


def selected_dual_primal_edges(
    embedding: DegreeFiveTriangulatedEmbedding,
    excluded_mode: V4,
) -> frozenset[Edge]:
    """Primal edge carrier of the two-mode dual network excluding one V4 mode."""

    if excluded_mode not in NONZERO_MODES:
        raise ValueError("excluded mode must be nonzero in V4")
    return frozenset(
        edge
        for edge in disk_primal_edges(embedding)
        if color_difference(
            embedding.state.coloring[edge[0]],
            embedding.state.coloring[edge[1]],
        )
        != excluded_mode
    )


def dual_pairing_signature(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> DualPairingSignature:
    """Derive both current singleton-mode pairings from the actual embedding."""

    if not embedding.valid:
        raise ValueError("a valid retained degree-five embedding is required")
    defects = C5DefectState(embedding.boundary_colors)
    if not defects.is_saturated_four_color_boundary:
        raise ValueError("pairing signature requires a saturated four-color C5")

    chart = dual_defect_parameterization(embedding.state, embedding.focus)
    singleton_modes = tuple(
        sorted(mode for mode, count in defects.mode_counts.items() if count == 1)
    )
    if len(singleton_modes) != 2:
        raise AssertionError("saturated degree-five boundary must have two singleton modes")

    records: list[SingletonModePairing] = []
    for mode in singleton_modes:
        parameters = derive_dual_domain_parameters(chart, embedding, mode)
        outcomes = tuple(
            apply_dual_nonzero_parameter(parameter).target_has_focus_slack
            for parameter in parameters
        )
        if outcomes[0] != outcomes[1]:
            raise AssertionError(
                "one embedded pairing must give the same focus consequence on both paths"
            )
        continuation = parameters[0].continuation
        records.append(
            SingletonModePairing(
                mode=mode,
                terminal_pairing=continuation.terminal_pairing,
                kind="direct" if outcomes[0] else "pivot",
            )
        )

    signature = DualPairingSignature(
        embedding=embedding,
        pairings=(records[0], records[1]),
    )
    if not signature.valid:
        raise AssertionError("dual pairing signature failed exact certification")
    return signature


@dataclass(frozen=True)
class AlternatingPathSwitchCertificate:
    """Exact V4 edge-mode switch induced by one embedded dual path translation.

    Let sigma be the translation mode and P the crossed primal edge carrier of
    the selected dual path.  Every edge of P has one of the other two nonzero
    V4 modes, and adding sigma swaps those two modes.  No disk edge outside P
    changes mode.  Consequently, for each other nonzero mode tau,

        F_tau(after) = F_tau(before) symmetric_difference P,

    while F_sigma is unchanged.  Here F_mu denotes the primal edge carrier of
    the two-mode dual network obtained by excluding mu.
    """

    parameter: DualDomainParameter
    after_embedding: DegreeFiveTriangulatedEmbedding

    @property
    def translation_mode(self) -> V4:
        return self.parameter.translation_mode

    @property
    def path_edges(self) -> frozenset[Edge]:
        return frozenset(self.parameter.path.crossed_edges)

    @property
    def valid(self) -> bool:
        if not self.parameter.valid or not self.after_embedding.valid:
            return False
        before = self.parameter.continuation.embedding
        if self.after_embedding.focus != before.focus:
            return False
        if self.after_embedding.boundary != before.boundary:
            return False
        if self.after_embedding.faces != before.faces:
            return False
        if dict(self.after_embedding.state.graph) != dict(before.state.graph):
            return False

        realized = apply_dual_nonzero_parameter(self.parameter)
        if dict(realized.after.coloring) != dict(self.after_embedding.state.coloring):
            return False

        disk_edges = disk_primal_edges(before)
        if disk_edges != disk_primal_edges(self.after_embedding):
            return False
        if not self.path_edges <= disk_edges:
            return False

        sigma = self.translation_mode
        for edge in disk_edges:
            before_mode = color_difference(
                before.state.coloring[edge[0]],
                before.state.coloring[edge[1]],
            )
            after_mode = color_difference(
                self.after_embedding.state.coloring[edge[0]],
                self.after_embedding.state.coloring[edge[1]],
            )
            if edge in self.path_edges:
                if before_mode == sigma:
                    return False
                if after_mode != v4_add(before_mode, sigma):
                    return False
            elif after_mode != before_mode:
                return False

        if selected_dual_primal_edges(before, sigma) != selected_dual_primal_edges(
            self.after_embedding,
            sigma,
        ):
            return False

        for mode in NONZERO_MODES:
            if mode == sigma:
                continue
            before_selected = selected_dual_primal_edges(before, mode)
            after_selected = selected_dual_primal_edges(self.after_embedding, mode)
            if after_selected != before_selected.symmetric_difference(self.path_edges):
                return False
        return True


def certify_alternating_path_switch(
    parameter: DualDomainParameter,
) -> AlternatingPathSwitchCertificate:
    """Reconstruct the exact successor embedding and certify dual-network surgery."""

    if not parameter.valid:
        raise ValueError("a valid embedding-derived dual parameter is required")
    realized = apply_dual_nonzero_parameter(parameter)
    before = parameter.continuation.embedding
    after_embedding = DegreeFiveTriangulatedEmbedding(
        state=realized.after,
        focus=before.focus,
        boundary=before.boundary,
        faces=before.faces,
    )
    certificate = AlternatingPathSwitchCertificate(parameter, after_embedding)
    if not certificate.valid:
        raise AssertionError("alternating dual-path switch failed exact certification")
    return certificate

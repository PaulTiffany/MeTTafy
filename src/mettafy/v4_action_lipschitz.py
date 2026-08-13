from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.color_construction import ConstructionState
from mettafy.plane_dual_control import (
    DualDomainNonzeroCertificate,
    DualDomainParameter,
    apply_dual_nonzero_parameter,
    canonical_edge,
)
from mettafy.plane_parameterization import (
    COLOR_TO_V4,
    NONZERO_MODES,
    ZERO,
    Color,
    V4,
    color_difference,
    v4_add,
)

ChoiceBit: TypeAlias = Literal[0, 1]
V4_TO_COLOR = {mode: color for color, mode in COLOR_TO_V4.items()}


def palette_distance(left: Color, right: Color) -> int:
    """Discrete metric on the four terminal palette states."""

    if left not in COLOR_TO_V4 or right not in COLOR_TO_V4:
        raise ValueError("palette distance is defined only on Q4")
    return 0 if left == right else 1


def apply_palette_choice(color: Color, mode: V4, choice: ChoiceBit) -> Color:
    """Apply one local binary choice: 0 stays put, 1 takes the unique V4 partner."""

    if color not in COLOR_TO_V4:
        raise ValueError("color lies outside Q4")
    if mode not in NONZERO_MODES:
        raise ValueError("choice direction must be a nonzero V4 mode")
    if choice not in (0, 1):
        raise ValueError("choice must be binary")
    if choice == 0:
        return color
    return V4_TO_COLOR[v4_add(COLOR_TO_V4[color], mode)]


def palette_choice_is_lipschitz_one(mode: V4, choice: ChoiceBit) -> bool:
    """Exhaustively certify that one fixed local choice is an L=1 palette isometry."""

    if mode not in NONZERO_MODES or choice not in (0, 1):
        return False
    colors = tuple(sorted(COLOR_TO_V4))
    return all(
        palette_distance(
            apply_palette_choice(left, mode, choice),
            apply_palette_choice(right, mode, choice),
        )
        == palette_distance(left, right)
        for left in colors
        for right in colors
    )


def changed_partner(color: Color, mode: V4) -> Color:
    """The unique other palette state reached by changing direction along ``mode``."""

    partner = apply_palette_choice(color, mode, 1)
    if partner == color:
        raise AssertionError("nonzero V4 translation unexpectedly fixed a palette state")
    return partner


@dataclass(frozen=True)
class DualDomainBinaryChoiceCertificate:
    """Pointwise stay/change-direction law underlying one exact dual domain action.

    For the chosen nonzero mode sigma, each committed vertex carries one bit
    chi(v): zero outside the translated domain and one inside it.  The realized
    coloring is

        c'(v) = c(v) + chi(v) sigma.

    Hence every committed edge uv obeys

        delta'(uv) = delta(uv) + (chi(u) xor chi(v)) sigma.

    A crossed cut edge is exactly an edge whose endpoint choices differ.  The
    retained dual parameter already certifies that no such edge has mode sigma,
    so the updated edge difference remains nonzero.
    """

    parameter: DualDomainParameter
    realization: DualDomainNonzeroCertificate

    @property
    def before(self) -> ConstructionState:
        return self.parameter.chart.base

    @property
    def after(self) -> ConstructionState:
        return self.realization.after

    @property
    def mode(self) -> V4:
        return self.parameter.translation_mode

    def choice(self, vertex: str) -> ChoiceBit:
        if vertex not in self.before.coloring:
            raise ValueError("choice is defined only for committed vertices")
        return 1 if vertex in self.parameter.translated_vertices else 0

    @property
    def choice_crossed_edges(self) -> frozenset[tuple[str, str]]:
        return frozenset(
            canonical_edge(vertex, neighbor)
            for vertex, neighbors in self.before.graph.items()
            for neighbor in neighbors
            if vertex in self.before.coloring
            and neighbor in self.before.coloring
            and vertex < neighbor
            and self.choice(vertex) != self.choice(neighbor)
        )

    @property
    def valid(self) -> bool:
        if not self.parameter.valid or not self.realization.valid:
            return False
        if self.realization.parameter is not self.parameter:
            return False
        if dict(self.before.graph) != dict(self.after.graph):
            return False
        if set(self.before.coloring) != set(self.after.coloring):
            return False
        if not palette_choice_is_lipschitz_one(self.mode, 0):
            return False
        if not palette_choice_is_lipschitz_one(self.mode, 1):
            return False

        expected_cut = frozenset(self.parameter.path.crossed_edges)
        if self.choice_crossed_edges != expected_cut:
            return False

        for vertex, before_color in self.before.coloring.items():
            if self.after.coloring[vertex] != apply_palette_choice(
                before_color,
                self.mode,
                self.choice(vertex),
            ):
                return False

        for vertex, neighbors in self.before.graph.items():
            if vertex not in self.before.coloring:
                continue
            for neighbor in neighbors:
                if neighbor not in self.before.coloring or vertex >= neighbor:
                    continue
                before_mode = color_difference(
                    self.before.coloring[vertex],
                    self.before.coloring[neighbor],
                )
                after_mode = color_difference(
                    self.after.coloring[vertex],
                    self.after.coloring[neighbor],
                )
                choices_differ = self.choice(vertex) ^ self.choice(neighbor)
                expected_mode = (
                    v4_add(before_mode, self.mode)
                    if choices_differ
                    else before_mode
                )
                if after_mode != expected_mode:
                    return False
                if choices_differ:
                    if canonical_edge(vertex, neighbor) not in expected_cut:
                        return False
                    if before_mode == self.mode or after_mode == ZERO:
                        return False
                elif after_mode != before_mode:
                    return False

        return self.after.committed_edges_valid


def certify_dual_domain_binary_choice(
    parameter: DualDomainParameter,
) -> DualDomainBinaryChoiceCertificate:
    """Certify the exact pointwise binary-choice law for one chosen dual action."""

    if not parameter.valid:
        raise ValueError("a valid chosen dual parameter is required")
    certificate = DualDomainBinaryChoiceCertificate(
        parameter=parameter,
        realization=apply_dual_nonzero_parameter(parameter),
    )
    if not certificate.valid:
        raise AssertionError("dual-domain binary-choice law failed certification")
    return certificate

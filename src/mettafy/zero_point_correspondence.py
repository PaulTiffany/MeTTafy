from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import StateKey, state_key
from mettafy.kempe_traversal import KempeMove, all_component_moves, apply_kempe_move
from mettafy.plane_parameterization import frontier_modes

ParameterLabel: TypeAlias = str
KempeParameter: TypeAlias = KempeMove | None

KEMPE_COMPONENT_FAMILY = "kempe-components"
DUAL_DEFECT_FAMILY = "v4-dual-defects"
ZERO_PARAMETER: None = None


def same_construction_state(left: ConstructionState, right: ConstructionState) -> bool:
    """Exact equality at the fixed Four Color construction species."""

    return (
        dict(left.graph) == dict(right.graph)
        and dict(left.coloring) == dict(right.coloring)
        and left.surface_genus == right.surface_genus == 0
        and left.committed_edges_valid
        and right.committed_edges_valid
    )


@dataclass(frozen=True)
class ControlParameterization:
    """One control description based at an exact construction state.

    ``coordinate_labels`` describe directions exposed by this parameterization.
    They are not construction-state coordinates.  The distinguished zero
    parameter always realizes the unchanged ``base`` state.
    """

    family: str
    base: ConstructionState
    coordinate_labels: tuple[ParameterLabel, ...]

    @property
    def zero_state(self) -> ConstructionState:
        return self.base

    @property
    def zero_key(self) -> StateKey:
        return state_key(self.base)

    @property
    def valid(self) -> bool:
        return (
            bool(self.family)
            and self.base.surface_genus == 0
            and self.base.committed_edges_valid
            and len(set(self.coordinate_labels)) == len(self.coordinate_labels)
        )


@dataclass(frozen=True)
class ZeroPointCorrespondence:
    """Certificate that two parameterizations share the same construction z0.

    Correspondence is deliberately only a zero-point statement.  It grants no
    transport between nonzero parameters of the two families.
    """

    left: ControlParameterization
    right: ControlParameterization

    @property
    def valid(self) -> bool:
        return (
            self.left.valid
            and self.right.valid
            and same_construction_state(self.left.zero_state, self.right.zero_state)
        )

    @property
    def shared_zero(self) -> ConstructionState:
        if not self.valid:
            raise ValueError("parameterizations do not share an exact construction zero-point")
        return self.left.zero_state


def reparameterize_at_zero(correspondence: ZeroPointCorrespondence) -> ConstructionState:
    """Change control description without changing the Four Color state."""

    return correspondence.shared_zero


def kempe_parameterization(state: ConstructionState) -> ControlParameterization:
    """Current two-color component controls, all based at ``state``."""

    labels = tuple(_kempe_label(state, move) for move in all_component_moves(state))
    chart = ControlParameterization(KEMPE_COMPONENT_FAMILY, state, labels)
    if not chart.valid:
        raise AssertionError("invalid Kempe control parameterization")
    return chart


def dual_defect_parameterization(
    state: ConstructionState, focus: str
) -> ControlParameterization:
    """V4 degree-five boundary coordinates based at the same construction state.

    This exposes only the derivative parameterization.  A nonzero domain
    translation still requires its own embedded cut/witness certificate.
    """

    if focus not in state.graph:
        raise ValueError(f"unknown focus vertex {focus!r}")
    if focus in state.coloring:
        raise ValueError("focus must remain uncommitted during dual parameterization")

    neighbors = tuple(state.graph[focus])
    if len(neighbors) != 5 or any(vertex not in state.coloring for vertex in neighbors):
        raise ValueError("dual degree-five parameterization requires five committed neighbors")
    for index, left in enumerate(neighbors):
        right = neighbors[(index + 1) % 5]
        if right not in state.graph[left]:
            raise ValueError("focus-neighbor order is not a witnessed C5 boundary")

    boundary = tuple(state.coloring[vertex] for vertex in neighbors)
    modes = frontier_modes(boundary)
    labels = tuple(
        f"delta_{index}={mode[0]}{mode[1]}" for index, mode in enumerate(modes)
    )
    chart = ControlParameterization(DUAL_DEFECT_FAMILY, state, labels)
    if not chart.valid:
        raise AssertionError("invalid V4 dual-defect parameterization")
    return chart


def zero_point_correspondence(
    left: ControlParameterization, right: ControlParameterization
) -> ZeroPointCorrespondence:
    certificate = ZeroPointCorrespondence(left, right)
    if not certificate.valid:
        raise ValueError("parameterizations are not based at the same construction state")
    return certificate


def realize_kempe_parameter(
    chart: ControlParameterization, parameter: KempeParameter
) -> ConstructionState:
    """Realize zero as identity; realize nonzero only when currently available."""

    if chart.family != KEMPE_COMPONENT_FAMILY or not chart.valid:
        raise ValueError("parameterization is not a valid Kempe component chart")
    if parameter is ZERO_PARAMETER:
        return chart.zero_state
    if parameter not in all_component_moves(chart.base):
        raise ValueError("nonzero Kempe parameter is not available at this zero-point")
    return apply_kempe_move(chart.base, parameter)


@dataclass(frozen=True)
class KempeNonzeroParameterCertificate:
    """Family-specific certificate for a nonzero move away from shared z0."""

    chart: ControlParameterization
    move: KempeMove
    after: ConstructionState

    @property
    def valid(self) -> bool:
        if self.chart.family != KEMPE_COMPONENT_FAMILY or not self.chart.valid:
            return False
        if self.move not in all_component_moves(self.chart.base):
            return False
        replayed = apply_kempe_move(self.chart.base, self.move)
        return (
            not same_construction_state(self.chart.base, self.after)
            and dict(replayed.graph) == dict(self.after.graph)
            and dict(replayed.coloring) == dict(self.after.coloring)
            and self.after.surface_genus == 0
            and self.after.committed_edges_valid
        )


def apply_kempe_nonzero_parameter(
    chart: ControlParameterization, move: KempeMove
) -> KempeNonzeroParameterCertificate:
    after = realize_kempe_parameter(chart, move)
    certificate = KempeNonzeroParameterCertificate(chart, move, after)
    if not certificate.valid:
        raise AssertionError("nonzero Kempe parameter failed exact certification")
    return certificate


def _kempe_label(state: ConstructionState, move: KempeMove) -> str:
    seed_color = state.coloring[move.seed]
    return f"{move.seed}:{seed_color}<->{move.other_color}"

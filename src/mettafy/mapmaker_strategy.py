from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mettafy.active_inference_boundary import CertifiedInstantiation, instantiate, void_count
from mettafy.color_construction import ConstructionState
from mettafy.meta_construct_closure import DecisionReachability


class MapMakerDomain(str, Enum):
    """Whether a primitive operates on realized or imaginary state."""

    DO = "do"
    IMAGINE = "imagine"


class MapMakerOperation(str, Enum):
    """The primitive epistemic/control operation."""

    OBSERVE = "observe"
    ACT = "act"


@dataclass(frozen=True)
class OperationalCell:
    """One cell of the complete Do/Imagine x Observe/Act product."""

    domain: MapMakerDomain
    operation: MapMakerOperation


class MapMakerMode(str, Enum):
    """The four primitive MapMaker strategies."""

    OVERVIEW = "overview"
    LOCAL_EXPANSION = "local_expansion"
    COUNTER_PLAY = "counter_play"
    DRAW = "draw"


class MapMakerCapability(str, Enum):
    """Irreducible local capability axes for the Pareto comparison."""

    GLOBAL_OVERVIEW = "global_overview"
    LOCAL_NEIGHBOR_EXPANSION = "local_neighbor_expansion"
    INTERACTIVE_COUNTER_PLAY = "interactive_counter_play"
    BLIND_REALIZED_WRITE = "blind_realized_write"


MODE_CELL: dict[MapMakerMode, OperationalCell] = {
    MapMakerMode.OVERVIEW: OperationalCell(MapMakerDomain.DO, MapMakerOperation.OBSERVE),
    MapMakerMode.LOCAL_EXPANSION: OperationalCell(
        MapMakerDomain.IMAGINE, MapMakerOperation.OBSERVE
    ),
    MapMakerMode.COUNTER_PLAY: OperationalCell(MapMakerDomain.IMAGINE, MapMakerOperation.ACT),
    MapMakerMode.DRAW: OperationalCell(MapMakerDomain.DO, MapMakerOperation.ACT),
}

CELL_MODE: dict[OperationalCell, MapMakerMode] = {cell: mode for mode, cell in MODE_CELL.items()}

MODE_CAPABILITIES: dict[MapMakerMode, frozenset[MapMakerCapability]] = {
    MapMakerMode.OVERVIEW: frozenset({MapMakerCapability.GLOBAL_OVERVIEW}),
    MapMakerMode.LOCAL_EXPANSION: frozenset({MapMakerCapability.LOCAL_NEIGHBOR_EXPANSION}),
    MapMakerMode.COUNTER_PLAY: frozenset({MapMakerCapability.INTERACTIVE_COUNTER_PLAY}),
    MapMakerMode.DRAW: frozenset({MapMakerCapability.BLIND_REALIZED_WRITE}),
}

CANONICAL_PARETO_PROGRAM: tuple[MapMakerMode, ...] = (
    MapMakerMode.OVERVIEW,
    MapMakerMode.LOCAL_EXPANSION,
    MapMakerMode.COUNTER_PLAY,
    MapMakerMode.DRAW,
)

PRECOMMIT_MODES = frozenset(
    {
        MapMakerMode.OVERVIEW,
        MapMakerMode.LOCAL_EXPANSION,
        MapMakerMode.COUNTER_PLAY,
    }
)


def mode_for_cell(cell: OperationalCell) -> MapMakerMode:
    """Return the unique primitive implementing one operational product cell."""

    return CELL_MODE[cell]


def operational_product_complete() -> bool:
    """The four modes are exactly the 2x2 Do/Imagine x Observe/Act product."""

    expected = {
        OperationalCell(domain, operation)
        for domain in MapMakerDomain
        for operation in MapMakerOperation
    }
    return set(MODE_CELL.values()) == expected and len(CELL_MODE) == len(expected)


def mode_dominates(lhs: MapMakerMode, rhs: MapMakerMode) -> bool:
    """Weak capability dominance on the declared primitive axes."""

    return MODE_CAPABILITIES[rhs] <= MODE_CAPABILITIES[lhs]


def program_capabilities(program: tuple[MapMakerMode, ...]) -> frozenset[MapMakerCapability]:
    capabilities: set[MapMakerCapability] = set()
    for mode in program:
        capabilities.update(MODE_CAPABILITIES[mode])
    return frozenset(capabilities)


def capability_complete(program: tuple[MapMakerMode, ...]) -> bool:
    """Whether a program covers all declared MapMaker capability axes."""

    return program_capabilities(program) == frozenset(MapMakerCapability)


def is_precommit_program(program: tuple[MapMakerMode, ...]) -> bool:
    """The preserved precommit order is Do:Observe; Imagine:Observe; Imagine:Act*."""

    if len(program) < 2:
        return False
    if program[0] is not MapMakerMode.OVERVIEW:
        return False
    if program[1] is not MapMakerMode.LOCAL_EXPANSION:
        return False
    return all(mode is MapMakerMode.COUNTER_PLAY for mode in program[2:])


def is_operational_normal_form(program: tuple[MapMakerMode, ...]) -> bool:
    """Full MapMaker normal form: O ; L ; C* ; D."""

    if len(program) < 3 or program[-1] is not MapMakerMode.DRAW:
        return False
    return is_precommit_program(program[:-1])


def is_blind_draw_suffix(program: tuple[MapMakerMode, ...]) -> bool:
    """Compatibility name for the ordered authority-crossing normal form."""

    return is_operational_normal_form(program)


@dataclass(frozen=True)
class MapMakerDecision:
    """One transferable SRMF-style deciding residue plus a blind draw.

    The `DecisionReachability` chain contains the auditable "if this, then this"
    spine. Its labels preserve the operational product order:

        Do:Observe ; Imagine:Observe ; Imagine:Act*

    Draw is intentionally absent until the chain has already compressed through
    the actual-map authority check, where it becomes the final Do:Act.
    """

    reachability: DecisionReachability
    precommit_modes: tuple[MapMakerMode, ...]

    def __post_init__(self) -> None:
        if not is_precommit_program(self.precommit_modes):
            raise ValueError(
                "precommit modes must preserve Do:Observe -> Imagine:Observe -> Imagine:Act*"
            )
        expected_steps = max(len(self.reachability.states) - 1, 0)
        if len(self.precommit_modes) != expected_steps:
            raise ValueError("one precommit mode label is required per refinement step")

    def certificate(self) -> CertifiedInstantiation:
        return self.reachability.compress()

    def strategy_word(self) -> tuple[MapMakerMode, ...]:
        """The transferable control word has normal form O ; L ; C* ; D."""

        return (*self.precommit_modes, MapMakerMode.DRAW)

    def draw(self) -> ConstructionState:
        """Do:Act: realize the certified choice without another perception step."""

        return instantiate(self.certificate())

    def realized_void_delta(self) -> int:
        certificate = self.certificate()
        return void_count(certificate.realized) - void_count(instantiate(certificate))

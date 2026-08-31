from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mettafy.active_inference_boundary import CertifiedInstantiation, instantiate, void_count
from mettafy.color_construction import ConstructionState
from mettafy.meta_construct_closure import DecisionReachability


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
    """Precommit thought may use only non-writing modes."""

    return all(mode in PRECOMMIT_MODES for mode in program)


def is_blind_draw_suffix(program: tuple[MapMakerMode, ...]) -> bool:
    """A realized program may cross authority exactly once, at its final draw."""

    if not program or program[-1] is not MapMakerMode.DRAW:
        return False
    return is_precommit_program(program[:-1])


@dataclass(frozen=True)
class MapMakerDecision:
    """One transferable SRMF-style deciding residue plus a blind draw.

    The `DecisionReachability` chain contains the auditable "if this, then this"
    spine. `precommit_modes` records only Overview / Local Expansion /
    Counter-Play labels. Draw is intentionally absent until the chain has already
    compressed through the actual-map authority check.
    """

    reachability: DecisionReachability
    precommit_modes: tuple[MapMakerMode, ...]

    def __post_init__(self) -> None:
        if not is_precommit_program(self.precommit_modes):
            raise ValueError("precommit reasoning cannot contain draw")
        expected_steps = max(len(self.reachability.states) - 1, 0)
        if len(self.precommit_modes) != expected_steps:
            raise ValueError("one precommit mode label is required per refinement step")

    def certificate(self) -> CertifiedInstantiation:
        return self.reachability.compress()

    def strategy_word(self) -> tuple[MapMakerMode, ...]:
        """The transferable control word has the normal form (O|L|C)* D."""

        return (*self.precommit_modes, MapMakerMode.DRAW)

    def draw(self) -> ConstructionState:
        """Realize without performing another perception step."""

        return instantiate(self.certificate())

    def realized_void_delta(self) -> int:
        certificate = self.certificate()
        return void_count(certificate.realized) - void_count(instantiate(certificate))

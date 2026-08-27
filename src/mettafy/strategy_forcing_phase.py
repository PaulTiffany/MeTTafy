from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from mettafy.strategy_color_projection import (
    StutteringMove,
    TrivialCrossingMove,
    color_phase,
)
from mettafy.strategy_staging import StrategyTangle

ColorSimulationWitness: TypeAlias = StutteringMove | TrivialCrossingMove


@dataclass(frozen=True)
class StrategyResponseQuotient:
    """INFERENCE: proof-relevant live response classes after strategic quotienting."""

    classes: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(set(self.classes)) != len(self.classes):
            raise ValueError("response quotient classes must be unique")

    @property
    def rank(self) -> int:
        """Number of strategically live response classes."""

        return len(self.classes)

    @property
    def forced(self) -> bool:
        """Exactly one live response class remains."""

        return self.rank == 1

    @property
    def checkmate(self) -> bool:
        """No strategically live response class remains."""

        return self.rank == 0


@dataclass(frozen=True)
class StrategyGameState:
    """INFERENCE: one tangle paired with the bounded observer's live response quotient."""

    tangle: StrategyTangle
    responses: StrategyResponseQuotient


@dataclass(frozen=True)
class StrategyForcingWitness:
    """INFERENCE: supported Strategy/color simulation plus strict response-rank descent."""

    before: StrategyGameState
    after: StrategyGameState
    simulation: ColorSimulationWitness

    @property
    def rank_drop(self) -> int:
        return self.before.responses.rank - self.after.responses.rank

    @property
    def color_phase_preserved(self) -> bool:
        return color_phase(self.simulation.before_projection.word) == color_phase(
            self.simulation.after_projection.word
        )

    @property
    def valid(self) -> bool:
        return (
            self.simulation.valid
            and self.simulation.before == self.before.tangle
            and self.simulation.after == self.after.tangle
            and self.after.responses.rank < self.before.responses.rank
            and self.rank_drop > 0
            and self.color_phase_preserved
        )

    @property
    def reaches_checkmate_from_forced(self) -> bool:
        """A strict step from rank one can only land at rank zero."""

        if not self.valid or not self.before.responses.forced:
            return False
        return self.after.responses.checkmate


def witness_strategy_forcing(
    simulation: ColorSimulationWitness,
    before_classes: tuple[str, ...],
    after_classes: tuple[str, ...],
) -> StrategyForcingWitness:
    """Build a forcing receipt from an independently checked color simulation.

    The caller supplies only the response-class labels.  Geometry, projection,
    stuttering/uncrossing validity, and retained color phase are replayed from the
    existing simulation witness rather than trusted as new claims.
    """

    if not simulation.valid:
        raise ValueError("forcing requires a valid Strategy/color simulation witness")

    before_responses = StrategyResponseQuotient(before_classes)
    after_responses = StrategyResponseQuotient(after_classes)
    if after_responses.rank >= before_responses.rank:
        raise ValueError("forcing must strictly reduce live response-class rank")

    before = StrategyGameState(simulation.before, before_responses)
    after = StrategyGameState(simulation.after, after_responses)
    witness = StrategyForcingWitness(before, after, simulation)
    if not witness.valid:
        raise AssertionError("forcing witness failed replay or color-phase preservation")
    return witness

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

StageId = str
WitnessAtom = str
StageStatus = Literal["continuable", "exhausted"]


@dataclass(frozen=True)
class WitnessExpansionState:
    """Finite retained-witness state for compelled staging.

    ``witness_atoms`` records facts that later stages are not allowed to forget.
    ``stage_universe`` is a caller-supplied finite universe of concrete stage
    certificates available on the fixed construction object.  This class does
    not prove that the universe is complete or that any particular stage exists.

    The only well-founded quantity certified here is the number of declared
    stages that have not yet been consumed.
    """

    witness_atoms: frozenset[WitnessAtom]
    stage_universe: frozenset[StageId]
    stage_history: tuple[StageId, ...] = ()

    def __post_init__(self) -> None:
        if any(not stage for stage in self.stage_universe):
            raise ValueError("stage identifiers must be nonempty")
        if len(set(self.stage_history)) != len(self.stage_history):
            raise ValueError("a compelled stage cannot be consumed twice")
        if not set(self.stage_history) <= self.stage_universe:
            raise ValueError("stage history contains an undeclared stage")

    @property
    def remaining_stages(self) -> frozenset[StageId]:
        return self.stage_universe - frozenset(self.stage_history)

    @property
    def stage_rank(self) -> int:
        """Well-founded finite rank for the declared stage universe."""

        return len(self.remaining_stages)

    @property
    def status(self) -> StageStatus:
        if self.remaining_stages:
            return "continuable"
        return "exhausted"


def apply_compelled_stage(
    state: WitnessExpansionState,
    stage_id: StageId,
    introduced_witnesses: frozenset[WitnessAtom],
) -> WitnessExpansionState:
    """Consume one fresh stage while strictly enlarging the retained witness.

    Replaying a consumed stage is rejected.  This makes the known reversible
    locked-boundary two-cycle unavailable as a *progress* step once the concrete
    cut/certificate that justified it has already been consumed.

    This function does not assert that a fresh admissible stage always exists,
    nor that exhausting the finite stage universe opens the original center.
    Those are theorem obligations outside this mechanical witness.
    """

    if stage_id not in state.stage_universe:
        raise ValueError("stage is outside the declared finite universe")
    if stage_id in state.stage_history:
        raise ValueError("stage has already been consumed")

    novel = introduced_witnesses - state.witness_atoms
    if not novel:
        raise ValueError("a compelled stage must strictly enlarge the retained witness")

    after = WitnessExpansionState(
        witness_atoms=state.witness_atoms | introduced_witnesses,
        stage_universe=state.stage_universe,
        stage_history=state.stage_history + (stage_id,),
    )
    if not state.witness_atoms < after.witness_atoms:
        raise AssertionError("compelled staging must strictly enlarge the witness")
    if after.stage_rank != state.stage_rank - 1:
        raise AssertionError("every compelled stage must consume exactly one finite stage")
    return after

from __future__ import annotations

from dataclasses import dataclass

from mettafy.color_construction import ConstructionState
from mettafy.ordered_shape import OrderedShapeLedger, certify_shape_progress
from mettafy.sequential_frontier import CleanFrontierTurn, clean_frontier_turns


@dataclass(frozen=True)
class TurnActionSignature:
    """Public signature of one currently lawful whole-component action.

    The signature deliberately contains no private route, search heuristic, or
    decision policy.  It records only the current realized action boundary and
    the restoration possibilities exposed by its successor.
    """

    seed: str
    source_color: int
    target_color: int
    component: frozenset[str]
    boundary_hits: frozenset[str]
    restoration_colors_after: frozenset[int]


@dataclass(frozen=True)
class ExtensionalEvitability:
    """Actions that are lawful from the realized state alone.

    This is intentionally history-free.  If an exact inverse returns to the
    same realized construction state, this object must return to the same value.
    That makes it a falsifiable candidate for the extensional part of what the
    project has been calling an evitability or future-action state.
    """

    restoration_colors: frozenset[int]
    turns: frozenset[TurnActionSignature]

    @property
    def restoration_forced(self) -> bool:
        return len(self.restoration_colors) == 1


@dataclass(frozen=True)
class RetainedEvitability:
    """Current lawful actions classified against retained resolved structure.

    ``consequential_turns`` are lawful actions that the existing C6/Theseus
    certificate would admit as fresh ordered progress. ``replay_turns`` remain
    lawful state transformations but repeat an already resolved physical shape.
    ``blocked_turns`` are lawful transformations rejected for some other C6
    reason, such as failure to retain an earlier lineage.

    This is an exploratory witness layer, not a promoted Four Color proof claim.
    It asks whether future-action structure is better represented by state alone
    or by state together with retained constructional knowledge.
    """

    extensional: ExtensionalEvitability
    consequential_turns: frozenset[TurnActionSignature]
    replay_turns: frozenset[TurnActionSignature]
    blocked_turns: frozenset[TurnActionSignature]


def turn_action_signature(turn: CleanFrontierTurn) -> TurnActionSignature:
    if not turn.valid:
        raise ValueError("evitability signature requires a valid clean frontier turn")
    return TurnActionSignature(
        seed=turn.move.seed,
        source_color=turn.before.coloring[turn.move.seed],
        target_color=turn.move.other_color,
        component=turn.component,
        boundary_hits=turn.boundary_hits,
        restoration_colors_after=turn.after.admissible_colors(turn.focus),
    )


def extensional_evitability(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, ...],
) -> ExtensionalEvitability:
    """Derive the public future-action surface from the actual current state."""

    turns = clean_frontier_turns(state, focus, boundary)
    return ExtensionalEvitability(
        restoration_colors=state.admissible_colors(focus),
        turns=frozenset(turn_action_signature(turn) for turn in turns),
    )


def retained_evitability(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, ...],
    ledger: OrderedShapeLedger,
) -> RetainedEvitability:
    """Classify current actions using only public state plus retained C6 facts."""

    extensional = extensional_evitability(state, focus, boundary)
    consequential: set[TurnActionSignature] = set()
    replays: set[TurnActionSignature] = set()
    blocked: set[TurnActionSignature] = set()

    for turn in clean_frontier_turns(state, focus, boundary):
        signature = turn_action_signature(turn)
        certificate = certify_shape_progress(ledger, turn)
        if certificate.valid:
            consequential.add(signature)
        elif certificate.equivalent_replay:
            replays.add(signature)
        else:
            blocked.add(signature)

    return RetainedEvitability(
        extensional=extensional,
        consequential_turns=frozenset(consequential),
        replay_turns=frozenset(replays),
        blocked_turns=frozenset(blocked),
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping

from mettafy.color_construction import PALETTE4
from mettafy.evitability import TurnActionSignature
from mettafy.placement_order import (
    PlacementLedger,
    PlacementOrderedEvitability,
    placement_ordered_evitability,
)

EventKind = Literal["place", "transform"]


@dataclass(frozen=True, order=True)
class RealizationEvent:
    """One concrete identity-bearing realization in construction time.

    ``time`` is a total ledger index. ``epoch`` is the public action epoch that
    created the identity. Several transformations caused by one atomic public
    action may therefore have distinct ledger indices while sharing one epoch.
    """

    time: int
    kind: EventKind
    lineage: str
    realized_color: int
    epoch: int | None = None

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("realization time must be nonnegative")
        if not self.lineage:
            raise ValueError("realization requires a nonempty lineage")
        if self.realized_color not in PALETTE4:
            raise ValueError("realization requires a concrete Q4 identity")
        if self.epoch is not None and self.epoch < 0:
            raise ValueError("realization epoch must be nonnegative")

    @property
    def realization_epoch(self) -> int:
        return self.time if self.epoch is None else self.epoch


@dataclass(frozen=True, order=True)
class CurrentRealizedState:
    """Current successor identity of one persistent lineage."""

    lineage: str
    realized_color: int
    generation: int
    born_at: int


@dataclass(frozen=True)
class HeldDifference:
    """Difference retained between locus, lineage, and current-state ontologies.

    ``unrealized_loci`` records carrier sites that have not become realized
    states. ``lineage_birth_order`` records first realization of persistent
    lineages. ``current_state_birth_tiers`` records public realization epochs
    of currently realized successor identities without inventing an ordering
    inside one atomic action. ``current_state_birth_order`` is the deterministic
    flattened display projection of those tiers.
    """

    unrealized_loci: frozenset[str]
    lineage_birth_order: tuple[str, ...]
    current_state_birth_order: tuple[str, ...]
    current_state_birth_tiers: tuple[frozenset[str], ...]
    generations: tuple[tuple[str, int], ...]

    @property
    def order_disagreement(self) -> bool:
        return self.lineage_birth_order != self.current_state_birth_order


@dataclass(frozen=True)
class TriadicSnapshot:
    """SRMF^3-style exploratory carrier: locus, realized state, held difference."""

    loci: frozenset[str]
    realized: tuple[CurrentRealizedState, ...]
    difference: HeldDifference

    @property
    def extensional_projection(self) -> tuple[frozenset[str], tuple[tuple[str, int], ...]]:
        """Forget history while retaining the static loci and current identities."""

        identities = tuple(sorted((state.lineage, state.realized_color) for state in self.realized))
        return self.loci, identities


@dataclass(frozen=True)
class TriadicHistory:
    """Construction history that keeps both ontology clocks instead of choosing one.

    Loci exist in the carrier before realization. A first placement creates a
    persistent lineage. A later transformation creates a new current realized
    state of that lineage without rewriting when the lineage first appeared.

    Atomic public actions can transform several lineages in one realization
    epoch. This prevents the ledger's serialization from inventing causal order
    inside a simultaneous whole-component transformation.
    """

    loci: frozenset[str]
    events: tuple[RealizationEvent, ...] = ()

    def __post_init__(self) -> None:
        if any(not locus for locus in self.loci):
            raise ValueError("carrier loci must be nonempty names")
        if tuple(event.time for event in self.events) != tuple(range(len(self.events))):
            raise ValueError("realization events must use contiguous construction time")
        if any(event.lineage not in self.loci for event in self.events):
            raise ValueError("realization event references a locus outside the carrier")
        epochs = tuple(event.realization_epoch for event in self.events)
        if epochs != tuple(sorted(epochs)):
            raise ValueError("realization epochs must be nondecreasing")
        self._validate_event_history()

    def _validate_event_history(self) -> None:
        current: dict[str, int] = {}
        for event in self.events:
            if event.kind == "place":
                if event.lineage in current:
                    raise ValueError("a realized lineage cannot be placed twice")
                current[event.lineage] = event.realized_color
            else:
                if event.lineage not in current:
                    raise ValueError("cannot transform an unrealized locus")
                if current[event.lineage] == event.realized_color:
                    raise ValueError("transformation must create a distinct successor identity")
                current[event.lineage] = event.realized_color

    @property
    def next_epoch(self) -> int:
        if not self.events:
            return 0
        return max(event.realization_epoch for event in self.events) + 1

    def place(self, lineage: str, realized_color: int) -> TriadicHistory:
        event = RealizationEvent(
            len(self.events),
            "place",
            lineage,
            realized_color,
            self.next_epoch,
        )
        return TriadicHistory(self.loci, self.events + (event,))

    def transform(self, lineage: str, realized_color: int) -> TriadicHistory:
        return self.transform_many({lineage: realized_color})

    def transform_many(self, successors: Mapping[str, int]) -> TriadicHistory:
        """Realize several successor identities in one atomic public-action epoch."""

        if not successors:
            raise ValueError("atomic transformation requires at least one successor")
        epoch = self.next_epoch
        start = len(self.events)
        events = tuple(
            RealizationEvent(
                start + index,
                "transform",
                lineage,
                realized_color,
                epoch,
            )
            for index, (lineage, realized_color) in enumerate(sorted(successors.items()))
        )
        return TriadicHistory(self.loci, self.events + events)

    @property
    def lineage_birth_order(self) -> tuple[str, ...]:
        return tuple(event.lineage for event in self.events if event.kind == "place")

    @property
    def current_states(self) -> tuple[CurrentRealizedState, ...]:
        latest: dict[str, RealizationEvent] = {}
        generations: dict[str, int] = {}
        for event in self.events:
            latest[event.lineage] = event
            if event.kind == "place":
                generations[event.lineage] = 0
            else:
                generations[event.lineage] += 1

        states = (
            CurrentRealizedState(
                lineage=lineage,
                realized_color=event.realized_color,
                generation=generations[lineage],
                born_at=event.realization_epoch,
            )
            for lineage, event in latest.items()
        )
        return tuple(sorted(states, key=lambda state: state.lineage))

    @property
    def current_state_birth_tiers(self) -> tuple[frozenset[str], ...]:
        by_epoch: dict[int, set[str]] = {}
        for state in self.current_states:
            by_epoch.setdefault(state.born_at, set()).add(state.lineage)
        return tuple(
            frozenset(by_epoch[epoch])
            for epoch in sorted(by_epoch)
        )

    @property
    def current_state_birth_order(self) -> tuple[str, ...]:
        return tuple(
            lineage
            for tier in self.current_state_birth_tiers
            for lineage in sorted(tier)
        )

    def snapshot(self) -> TriadicSnapshot:
        realized_lineages = frozenset(state.lineage for state in self.current_states)
        generations = tuple(sorted((state.lineage, state.generation) for state in self.current_states))
        difference = HeldDifference(
            unrealized_loci=self.loci - realized_lineages,
            lineage_birth_order=self.lineage_birth_order,
            current_state_birth_order=self.current_state_birth_order,
            current_state_birth_tiers=self.current_state_birth_tiers,
            generations=generations,
        )
        return TriadicSnapshot(self.loci, self.current_states, difference)

    def lineage_ledger(self) -> PlacementLedger:
        ledger = PlacementLedger()
        for event in self.events:
            if event.kind == "place":
                ledger = ledger.place(event.lineage, event.realized_color)
        return ledger


@dataclass(frozen=True)
class EpochOrderedEvitability:
    """Current-state action order that preserves ties inside one realization epoch."""

    first_actors: frozenset[str]
    first_epoch: int | None
    first_actions: frozenset[TurnActionSignature]
    deferred_actions: frozenset[TurnActionSignature]

    @property
    def empty(self) -> bool:
        return not self.first_actors

    @property
    def first_actor(self) -> str | None:
        """Return the unique first actor, or None when the public epoch leaves a tie."""

        if len(self.first_actors) != 1:
            return None
        return next(iter(self.first_actors))


@dataclass(frozen=True)
class TriadicOrderedEvitability:
    """Two lawful action orders plus the held difference between their clocks."""

    lineage_order: PlacementOrderedEvitability
    current_state_order: EpochOrderedEvitability
    difference: HeldDifference

    @property
    def order_disagreement(self) -> bool:
        lineage_actor = self.lineage_order.first_actor
        lineage_tier = frozenset() if lineage_actor is None else frozenset({lineage_actor})
        return lineage_tier != self.current_state_order.first_actors


def _epoch_ordered_evitability(
    actions: frozenset[TurnActionSignature],
    history: TriadicHistory,
) -> EpochOrderedEvitability:
    current = {state.lineage: state for state in history.current_states}
    unrealized = frozenset(action.seed for action in actions if action.seed not in current)
    if unrealized:
        names = ", ".join(sorted(unrealized))
        raise ValueError(f"unrealized site cannot act as a state: {names}")

    if not actions:
        return EpochOrderedEvitability(
            first_actors=frozenset(),
            first_epoch=None,
            first_actions=frozenset(),
            deferred_actions=frozenset(),
        )

    first_epoch = min(current[action.seed].born_at for action in actions)
    first_actors = frozenset(
        action.seed for action in actions if current[action.seed].born_at == first_epoch
    )
    first_actions = frozenset(action for action in actions if action.seed in first_actors)
    return EpochOrderedEvitability(
        first_actors=first_actors,
        first_epoch=first_epoch,
        first_actions=first_actions,
        deferred_actions=actions - first_actions,
    )


def triadic_ordered_evitability(
    actions: Iterable[TurnActionSignature],
    history: TriadicHistory,
) -> TriadicOrderedEvitability:
    """Order one public action surface under both retained ontology clocks."""

    action_set = frozenset(actions)
    snapshot = history.snapshot()
    return TriadicOrderedEvitability(
        lineage_order=placement_ordered_evitability(action_set, history.lineage_ledger()),
        current_state_order=_epoch_ordered_evitability(action_set, history),
        difference=snapshot.difference,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

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
    """One concrete identity-bearing realization in construction time."""

    time: int
    kind: EventKind
    lineage: str
    realized_color: int

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("realization time must be nonnegative")
        if not self.lineage:
            raise ValueError("realization requires a nonempty lineage")
        if self.realized_color not in PALETTE4:
            raise ValueError("realization requires a concrete Q4 identity")


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
    lineages. ``current_state_birth_order`` records when the currently realized
    successor identities came into existence. Their disagreement is preserved
    rather than normalized away.
    """

    unrealized_loci: frozenset[str]
    lineage_birth_order: tuple[str, ...]
    current_state_birth_order: tuple[str, ...]
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
        """Forget history while retaining the static carrier and current identities."""

        identities = tuple(sorted((state.lineage, state.realized_color) for state in self.realized))
        return self.loci, identities


@dataclass(frozen=True)
class TriadicHistory:
    """Construction history that keeps both ontology clocks instead of choosing one.

    Loci exist in the carrier before realization. A first placement creates a
    persistent lineage. A later transformation creates a new current realized
    state of that lineage without rewriting when the lineage first appeared.
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

    def place(self, lineage: str, realized_color: int) -> TriadicHistory:
        event = RealizationEvent(len(self.events), "place", lineage, realized_color)
        return TriadicHistory(self.loci, self.events + (event,))

    def transform(self, lineage: str, realized_color: int) -> TriadicHistory:
        event = RealizationEvent(len(self.events), "transform", lineage, realized_color)
        return TriadicHistory(self.loci, self.events + (event,))

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
                born_at=event.time,
            )
            for lineage, event in latest.items()
        )
        return tuple(sorted(states, key=lambda state: state.lineage))

    @property
    def current_state_birth_order(self) -> tuple[str, ...]:
        return tuple(
            state.lineage
            for state in sorted(self.current_states, key=lambda state: state.born_at)
        )

    def snapshot(self) -> TriadicSnapshot:
        realized_lineages = frozenset(state.lineage for state in self.current_states)
        generations = tuple(sorted((state.lineage, state.generation) for state in self.current_states))
        difference = HeldDifference(
            unrealized_loci=self.loci - realized_lineages,
            lineage_birth_order=self.lineage_birth_order,
            current_state_birth_order=self.current_state_birth_order,
            generations=generations,
        )
        return TriadicSnapshot(self.loci, self.current_states, difference)

    def lineage_ledger(self) -> PlacementLedger:
        ledger = PlacementLedger()
        for event in self.events:
            if event.kind == "place":
                ledger = ledger.place(event.lineage, event.realized_color)
        return ledger

    def current_state_ledger(self) -> PlacementLedger:
        ledger = PlacementLedger()
        current_by_lineage = {state.lineage: state for state in self.current_states}
        for lineage in self.current_state_birth_order:
            state = current_by_lineage[lineage]
            ledger = ledger.place(lineage, state.realized_color)
        return ledger


@dataclass(frozen=True)
class TriadicOrderedEvitability:
    """Two lawful action orders plus the held difference between their clocks."""

    lineage_order: PlacementOrderedEvitability
    current_state_order: PlacementOrderedEvitability
    difference: HeldDifference

    @property
    def order_disagreement(self) -> bool:
        return self.lineage_order.first_actor != self.current_state_order.first_actor


def triadic_ordered_evitability(
    actions: Iterable[TurnActionSignature],
    history: TriadicHistory,
) -> TriadicOrderedEvitability:
    """Order one public action surface under both retained ontology clocks."""

    action_set = frozenset(actions)
    snapshot = history.snapshot()
    return TriadicOrderedEvitability(
        lineage_order=placement_ordered_evitability(action_set, history.lineage_ledger()),
        current_state_order=placement_ordered_evitability(
            action_set,
            history.current_state_ledger(),
        ),
        difference=snapshot.difference,
    )

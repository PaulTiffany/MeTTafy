from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from mettafy.color_construction import PALETTE4
from mettafy.evitability import TurnActionSignature


@dataclass(frozen=True, order=True)
class PlacementEvent:
    """First realization of one persistent state lineage.

    A placement event is concrete: a lineage is not a realized state until an
    identity-bearing color is supplied. Later whole-component transformations
    may change the realized color of that lineage, but they do not rewrite when
    the lineage first entered the construction.
    """

    lineage: str
    realized_color: int

    def __post_init__(self) -> None:
        if not self.lineage:
            raise ValueError("placement requires a nonempty state lineage")
        if self.realized_color not in PALETTE4:
            raise ValueError("placement requires a concrete Q4 identity")


@dataclass(frozen=True)
class PlacementLedger:
    """Constructional birth order for realized state lineages.

    Tuple position is the order. Unplaced graph locations may be sites or loci,
    but they are not represented here as hollow states. The order is retained
    across successor identities because it records first realization, not the
    current color of a lineage.
    """

    events: tuple[PlacementEvent, ...] = ()

    def __post_init__(self) -> None:
        lineages = tuple(event.lineage for event in self.events)
        if len(lineages) != len(set(lineages)):
            raise ValueError("a state lineage can be placed only once")

    @property
    def lineages(self) -> tuple[str, ...]:
        return tuple(event.lineage for event in self.events)

    def place(self, lineage: str, realized_color: int) -> PlacementLedger:
        if lineage in self.lineages:
            raise ValueError("state lineage is already realized")
        return PlacementLedger(self.events + (PlacementEvent(lineage, realized_color),))

    def is_realized(self, lineage: str) -> bool:
        return lineage in self.lineages

    def birth_rank(self, lineage: str) -> int:
        try:
            return self.lineages.index(lineage)
        except ValueError as exc:
            raise ValueError("unrealized site has no constructional birth rank") from exc

    def unrealized_sites(self, sites: Iterable[str]) -> frozenset[str]:
        """Return locations that exist in a carrier description but are not states yet."""

        return frozenset(site for site in sites if not self.is_realized(site))


@dataclass(frozen=True)
class PlacementOrderedEvitability:
    """Evitability tier induced only by first-realization order.

    If multiple public actions are currently lawful, the earliest-placed
    eligible state lineage owns the first action tier. We deliberately do not
    rank that actor's alternative actions against one another: private choice
    remains opaque. Later eligible actors are deferred rather than deleted.
    """

    first_actor: str | None
    first_birth_rank: int | None
    first_actions: frozenset[TurnActionSignature]
    deferred_actions: frozenset[TurnActionSignature]

    @property
    def empty(self) -> bool:
        return self.first_actor is None


def placement_ordered_evitability(
    actions: Iterable[TurnActionSignature],
    ledger: PlacementLedger,
) -> PlacementOrderedEvitability:
    """Order a public action surface by first placement, never by hidden policy."""

    action_set = frozenset(actions)
    unrealized = frozenset(action.seed for action in action_set if not ledger.is_realized(action.seed))
    if unrealized:
        names = ", ".join(sorted(unrealized))
        raise ValueError(f"unrealized site cannot act as a state: {names}")

    if not action_set:
        return PlacementOrderedEvitability(
            first_actor=None,
            first_birth_rank=None,
            first_actions=frozenset(),
            deferred_actions=frozenset(),
        )

    first_rank = min(ledger.birth_rank(action.seed) for action in action_set)
    first_actor = ledger.events[first_rank].lineage
    first_actions = frozenset(action for action in action_set if action.seed == first_actor)
    deferred = action_set - first_actions

    return PlacementOrderedEvitability(
        first_actor=first_actor,
        first_birth_rank=first_rank,
        first_actions=first_actions,
        deferred_actions=deferred,
    )

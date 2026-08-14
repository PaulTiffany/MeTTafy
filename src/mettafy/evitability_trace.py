from __future__ import annotations

from dataclasses import dataclass

from mettafy.evitability_interaction import (
    ActionExchange,
    EvitabilitySurface,
    PublicResponseRelation,
)


@dataclass(frozen=True)
class AlternatingInteractionTrace:
    """Deterministic replay of public action/evitability interactions.

    The trace contains no private chooser. At each step the observed action must
    be available on the actor's current public surface, the other agent's next
    surface must be exactly derived by the public response relation, and actors
    alternate. If the preceding impact leaves a singleton reply, the next actor
    is mechanically required to emit that unique action. A dead end cannot have
    a successor exchange.

    This is an exploratory interaction witness, not Four Color proof coverage.
    """

    relation: PublicResponseRelation
    initial_surfaces: tuple[EvitabilitySurface, EvitabilitySurface]
    exchanges: tuple[ActionExchange, ...]

    def __post_init__(self) -> None:
        actors = tuple(surface.actor for surface in self.initial_surfaces)
        if len(set(actors)) != 2:
            raise ValueError("alternating trace requires exactly two distinct agents")

    def _replay(self) -> tuple[bool, dict[str, EvitabilitySurface]]:
        current = {surface.actor: surface for surface in self.initial_surfaces}
        previous: ActionExchange | None = None

        for exchange in self.exchanges:
            trigger = exchange.impact.trigger
            actor = trigger.actor
            if actor not in current:
                return False, current

            responders = tuple(name for name in current if name != actor)
            if len(responders) != 1:
                return False, current
            responder = responders[0]

            if previous is not None:
                previous_actor = previous.impact.trigger.actor
                if actor == previous_actor:
                    return False, current
                previous_after = previous.impact.after
                if previous_after.dead_end:
                    return False, current
                if previous_after.forced and trigger != previous_after.unique_action:
                    return False, current

            try:
                expected = self.relation.exchange(
                    trigger,
                    current[actor],
                    current[responder],
                )
            except ValueError:
                return False, current

            if exchange != expected:
                return False, current

            current[responder] = exchange.impact.after
            previous = exchange

        return True, current

    @property
    def valid(self) -> bool:
        valid, _ = self._replay()
        return valid

    @property
    def final_surfaces(self) -> tuple[EvitabilitySurface, EvitabilitySurface]:
        valid, current = self._replay()
        if not valid:
            raise ValueError("cannot derive final surfaces from an invalid trace")
        first, second = sorted(current)
        return (current[first], current[second])

    @property
    def forced_impacts(self) -> int:
        if not self.valid:
            raise ValueError("cannot inspect an invalid trace")
        return sum(exchange.impact.forced for exchange in self.exchanges)

    @property
    def contracting_impacts(self) -> int:
        if not self.valid:
            raise ValueError("cannot inspect an invalid trace")
        return sum(exchange.impact.contracted for exchange in self.exchanges)

    @property
    def configuration_replay(self) -> bool:
        """Whether the trace revisits an already observed pair of action surfaces."""

        if not self.valid:
            raise ValueError("cannot inspect an invalid trace")

        current = {surface.actor: surface for surface in self.initial_surfaces}
        seen = {tuple((actor, current[actor]) for actor in sorted(current))}

        for exchange in self.exchanges:
            actor = exchange.impact.trigger.actor
            responder = next(name for name in current if name != actor)
            current[responder] = exchange.impact.after
            signature = tuple((name, current[name]) for name in sorted(current))
            if signature in seen:
                return True
            seen.add(signature)
        return False

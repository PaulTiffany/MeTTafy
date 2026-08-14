from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class PublicAction:
    """One action visible at an agent boundary.

    Nothing here represents the actor's private policy, utility, search tree, or
    reason for selecting the action.  The interaction layer receives only the
    action that actually crossed the public boundary.
    """

    actor: str
    label: str

    def __post_init__(self) -> None:
        if not self.actor:
            raise ValueError("public action requires an actor")
        if not self.label:
            raise ValueError("public action requires a label")


@dataclass(frozen=True)
class EvitabilitySurface:
    """The currently available public future actions for one opaque agent."""

    actor: str
    actions: frozenset[PublicAction]

    def __post_init__(self) -> None:
        if not self.actor:
            raise ValueError("evitability surface requires an actor")
        foreign = frozenset(action for action in self.actions if action.actor != self.actor)
        if foreign:
            raise ValueError("evitability surface contains actions owned by another actor")

    @property
    def forced(self) -> bool:
        """Whether the public relation leaves exactly one future action."""

        return len(self.actions) == 1

    @property
    def dead_end(self) -> bool:
        """Whether no compatible future action remains."""

        return not self.actions

    @property
    def unique_action(self) -> PublicAction:
        if not self.forced:
            raise ValueError("future action is not uniquely forced")
        return next(iter(self.actions))


@dataclass(frozen=True)
class EvitabilityImpact:
    """Certificate that one public action constrained another agent's future.

    ``compatible_replies`` is derived from the public response relation.  The
    successor surface must be exactly the intersection of those replies with
    the responder's previously available actions.  No private chooser is a
    certificate input.
    """

    trigger: PublicAction
    before: EvitabilitySurface
    compatible_replies: frozenset[PublicAction]
    after: EvitabilitySurface

    @property
    def valid(self) -> bool:
        return (
            self.trigger.actor != self.before.actor
            and self.after.actor == self.before.actor
            and all(action.actor == self.before.actor for action in self.compatible_replies)
            and self.after.actions == self.before.actions & self.compatible_replies
        )

    @property
    def contracted(self) -> bool:
        return self.valid and self.after.actions < self.before.actions

    @property
    def forced(self) -> bool:
        return self.valid and self.after.forced

    @property
    def dead_end(self) -> bool:
        return self.valid and self.after.dead_end


@dataclass(frozen=True)
class PublicResponseRelation:
    """Directional compatibility between observed actions and lawful replies.

    This is the public interaction law.  A pair ``(a, b)`` means that after
    action ``a`` is observed, reply ``b`` remains compatible.  Directionality
    matters: the relation does not assume that action/reaction is symmetric.
    """

    pairs: frozenset[tuple[PublicAction, PublicAction]]

    def __post_init__(self) -> None:
        if any(trigger.actor == reply.actor for trigger, reply in self.pairs):
            raise ValueError("response relation must cross an agent boundary")

    def replies_to(self, trigger: PublicAction) -> frozenset[PublicAction]:
        return frozenset(reply for observed, reply in self.pairs if observed == trigger)

    def apply(
        self,
        trigger: PublicAction,
        responder: EvitabilitySurface,
    ) -> EvitabilityImpact:
        """Transform the responder's future-action surface from public facts only."""

        compatible = self.replies_to(trigger)
        after = EvitabilitySurface(
            actor=responder.actor,
            actions=responder.actions & compatible,
        )
        impact = EvitabilityImpact(
            trigger=trigger,
            before=responder,
            compatible_replies=compatible,
            after=after,
        )
        if not impact.valid:
            raise ValueError("trigger/reply relation does not define a valid cross-agent impact")
        return impact

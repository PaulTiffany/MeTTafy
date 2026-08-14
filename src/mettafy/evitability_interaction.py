from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class PublicAction:
    """One action visible at an agent boundary.

    Nothing here represents the actor's private policy, utility, search tree, or
    reason for selecting the action. The interaction layer receives only the
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

    ``compatible_replies`` is derived from the public response relation. The
    successor surface must be exactly the intersection of those replies with
    the responder's previously available actions. No private chooser is a
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
class ActionExchange:
    """One lawful public action together with its effect on the other side.

    The trigger must itself belong to the acting agent's current evitability
    surface. This prevents the interaction layer from injecting an action that
    was never publicly available to the actor.
    """

    actor_surface: EvitabilitySurface
    impact: EvitabilityImpact

    @property
    def valid(self) -> bool:
        trigger = self.impact.trigger
        return (
            self.actor_surface.actor == trigger.actor
            and trigger in self.actor_surface.actions
            and self.actor_surface.actor != self.impact.before.actor
            and self.impact.valid
        )


@dataclass(frozen=True)
class PublicResponseRelation:
    """Directional compatibility between observed actions and lawful replies.

    This is the public interaction law. A pair ``(a, b)`` means that after
    action ``a`` is observed, reply ``b`` remains compatible. Directionality
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

    def exchange(
        self,
        trigger: PublicAction,
        actor_surface: EvitabilitySurface,
        responder: EvitabilitySurface,
    ) -> ActionExchange:
        """Certify both trigger availability and its public effect on the responder."""

        exchange = ActionExchange(
            actor_surface=actor_surface,
            impact=self.apply(trigger, responder),
        )
        if not exchange.valid:
            raise ValueError("public action was not available on the actor's current surface")
        return exchange


@dataclass(frozen=True, order=True)
class PolicyHypothesis:
    """Observer-side hypothesis about an opaque agent's public choices.

    These hypotheses are not supplied to the interaction law and are not claims
    about the agent's actual internals. They are deterministic audit objects for
    asking what, if anything, an observed action reveals about hidden policy.
    """

    actor: str
    name: str
    predictions: frozenset[tuple[str, PublicAction]]

    def __post_init__(self) -> None:
        if not self.actor or not self.name:
            raise ValueError("policy hypothesis requires actor and name")
        contexts = tuple(context for context, _ in self.predictions)
        if len(contexts) != len(set(contexts)):
            raise ValueError("policy hypothesis predicts more than one action per context")
        if any(action.actor != self.actor for _, action in self.predictions):
            raise ValueError("policy hypothesis predicts an action owned by another actor")

    def prediction(self, context: str) -> PublicAction | None:
        matches = tuple(action for key, action in self.predictions if key == context)
        if len(matches) > 1:
            raise AssertionError("duplicate context escaped policy-hypothesis validation")
        return matches[0] if matches else None


@dataclass(frozen=True)
class ObserverPolicyClass:
    """Current equivalence class of observer-side hypotheses about one agent."""

    actor: str
    hypotheses: frozenset[PolicyHypothesis]

    def __post_init__(self) -> None:
        if not self.actor:
            raise ValueError("observer policy class requires an actor")
        if any(hypothesis.actor != self.actor for hypothesis in self.hypotheses):
            raise ValueError("observer class mixes hypotheses about different actors")

    @property
    def resolved(self) -> bool:
        return len(self.hypotheses) == 1

    @property
    def contradicted(self) -> bool:
        return not self.hypotheses

    def compatible_with_surface(
        self,
        context: str,
        surface: EvitabilitySurface,
    ) -> ObserverPolicyClass:
        """Discard hypotheses already incompatible with the public action surface."""

        if surface.actor != self.actor:
            raise ValueError("surface belongs to another actor")
        return ObserverPolicyClass(
            actor=self.actor,
            hypotheses=frozenset(
                hypothesis
                for hypothesis in self.hypotheses
                if hypothesis.prediction(context) in surface.actions
            ),
        )

    def observe(self, context: str, action: PublicAction) -> PolicyRefinement:
        """Refine only by the action that actually crossed the public boundary."""

        if action.actor != self.actor:
            raise ValueError("observed action belongs to another actor")
        after = ObserverPolicyClass(
            actor=self.actor,
            hypotheses=frozenset(
                hypothesis
                for hypothesis in self.hypotheses
                if hypothesis.prediction(context) == action
            ),
        )
        refinement = PolicyRefinement(
            before=self,
            context=context,
            observed=action,
            after=after,
        )
        if not refinement.valid:
            raise AssertionError("observer policy refinement was not exact")
        return refinement


@dataclass(frozen=True)
class PolicyRefinement:
    """Exact deterministic filtering of policy hypotheses by one observation."""

    before: ObserverPolicyClass
    context: str
    observed: PublicAction
    after: ObserverPolicyClass

    @property
    def valid(self) -> bool:
        expected = frozenset(
            hypothesis
            for hypothesis in self.before.hypotheses
            if hypothesis.prediction(self.context) == self.observed
        )
        return (
            self.observed.actor == self.before.actor
            and self.after.actor == self.before.actor
            and self.after.hypotheses == expected
        )

    @property
    def strict(self) -> bool:
        return self.valid and self.after.hypotheses < self.before.hypotheses

    @property
    def informative(self) -> bool:
        return self.strict

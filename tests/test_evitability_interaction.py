from __future__ import annotations

from dataclasses import fields

import pytest

from mettafy.evitability_interaction import (
    EvitabilitySurface,
    ObserverPolicyClass,
    PolicyHypothesis,
    PublicAction,
    PublicResponseRelation,
)

A0 = PublicAction("A", "a0")
A1 = PublicAction("A", "a1")
B0 = PublicAction("B", "b0")
B1 = PublicAction("B", "b1")

A_OPEN = EvitabilitySurface("A", frozenset({A0, A1}))
B_OPEN = EvitabilitySurface("B", frozenset({B0, B1}))


def _relation() -> PublicResponseRelation:
    return PublicResponseRelation(
        frozenset(
            {
                # A0 constrains B to exactly one compatible reply.
                (A0, B1),
                # A1 leaves B unresolved.
                (A1, B0),
                (A1, B1),
                # B1 then constrains A to exactly one compatible reply.
                (B1, A1),
                # B0 leaves A unresolved.
                (B0, A0),
                (B0, A1),
            }
        )
    )


def _b_policy_class() -> ObserverPolicyClass:
    return ObserverPolicyClass(
        actor="B",
        hypotheses=frozenset(
            {
                PolicyHypothesis(
                    actor="B",
                    name="prefers-b0-when-open",
                    predictions=frozenset(
                        {
                            ("forced-after-a0", B1),
                            ("open-after-a1", B0),
                        }
                    ),
                ),
                PolicyHypothesis(
                    actor="B",
                    name="prefers-b1-when-open",
                    predictions=frozenset(
                        {
                            ("forced-after-a0", B1),
                            ("open-after-a1", B1),
                        }
                    ),
                ),
            }
        ),
    )


def test_action_by_a_mechanically_forces_b_future_action() -> None:
    exchange = _relation().exchange(A0, A_OPEN, B_OPEN)
    impact = exchange.impact

    assert exchange.valid
    assert impact.valid
    assert impact.contracted
    assert impact.forced
    assert not impact.dead_end
    assert impact.before.actions == frozenset({B0, B1})
    assert impact.after.actions == frozenset({B1})
    assert impact.after.unique_action == B1


def test_forced_b_action_reciprocally_forces_a_future_action() -> None:
    relation = _relation()
    a_to_b = relation.exchange(A0, A_OPEN, B_OPEN)
    forced_b_surface = a_to_b.impact.after
    forced_b = forced_b_surface.unique_action

    b_to_a = relation.exchange(forced_b, forced_b_surface, A_OPEN)

    assert b_to_a.valid
    assert b_to_a.impact.contracted
    assert b_to_a.impact.forced
    assert b_to_a.impact.after.actions == frozenset({A1})
    assert b_to_a.impact.after.unique_action == A1


def test_exchange_rejects_action_not_available_to_actor() -> None:
    relation = _relation()
    a_only_a1 = EvitabilitySurface("A", frozenset({A1}))

    with pytest.raises(ValueError, match="not available"):
        relation.exchange(A0, a_only_a1, B_OPEN)


def test_forcedness_is_derived_from_relation_not_hardcoded() -> None:
    baseline = _relation()
    assert baseline.exchange(A0, A_OPEN, B_OPEN).impact.forced

    # Mutation 1: one extra compatible response destroys forcedness.
    expanded = PublicResponseRelation(baseline.pairs | frozenset({(A0, B0)}))
    expanded_impact = expanded.exchange(A0, A_OPEN, B_OPEN).impact
    assert expanded_impact.valid
    assert not expanded_impact.contracted
    assert not expanded_impact.forced
    assert expanded_impact.after == B_OPEN

    # Mutation 2: removing the unique response produces a dead end, not a
    # fabricated forced action.
    erased = PublicResponseRelation(baseline.pairs - frozenset({(A0, B1)}))
    erased_impact = erased.exchange(A0, A_OPEN, B_OPEN).impact
    assert erased_impact.valid
    assert erased_impact.contracted
    assert not erased_impact.forced
    assert erased_impact.dead_end


def test_forced_action_need_not_reveal_private_preference() -> None:
    relation = _relation()
    a_to_b = relation.exchange(A0, A_OPEN, B_OPEN)
    forced_b_surface = a_to_b.impact.after
    assert forced_b_surface == EvitabilitySurface("B", frozenset({B1}))

    observer = _b_policy_class()
    lawful_hypotheses = observer.compatible_with_surface(
        "forced-after-a0",
        forced_b_surface,
    )
    refinement = lawful_hypotheses.observe("forced-after-a0", B1)

    # Both incompatible private preferences induce the same public action when
    # the relation leaves B only one lawful future action. Compliance therefore
    # provides no extra evidence about which private preference is present.
    assert lawful_hypotheses == observer
    assert refinement.valid
    assert not refinement.informative
    assert refinement.after == refinement.before
    assert not refinement.after.resolved


def test_unforced_action_can_refine_observer_policy_class() -> None:
    relation = _relation()
    a_to_b = relation.exchange(A1, A_OPEN, B_OPEN)
    open_b_surface = a_to_b.impact.after
    assert open_b_surface == B_OPEN
    assert not open_b_surface.forced

    observer = _b_policy_class().compatible_with_surface(
        "open-after-a1",
        open_b_surface,
    )
    refinement = observer.observe("open-after-a1", B1)

    assert refinement.valid
    assert refinement.informative
    assert refinement.after.resolved
    surviving = refinement.after.hypotheses
    assert {hypothesis.name for hypothesis in surviving} == {"prefers-b1-when-open"}


def test_public_interaction_surface_contains_no_private_policy_slot() -> None:
    # Structural witness: policy hypotheses live only in a separate observer
    # layer. Neither the action surface nor the response relation can receive an
    # agent's private chooser, utility, or search tree.
    surface_fields = {field.name for field in fields(EvitabilitySurface)}
    relation_fields = {field.name for field in fields(PublicResponseRelation)}

    assert surface_fields == {"actor", "actions"}
    assert relation_fields == {"pairs"}


def test_directionality_is_not_silently_treated_as_symmetry() -> None:
    relation = _relation()

    assert relation.replies_to(A0) == frozenset({B1})
    assert relation.replies_to(B1) == frozenset({A1})
    assert A0 not in relation.replies_to(B1)

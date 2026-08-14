from __future__ import annotations

from dataclasses import fields

from mettafy.evitability_interaction import (
    EvitabilitySurface,
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


def test_action_by_a_mechanically_forces_b_future_action() -> None:
    impact = _relation().apply(A0, B_OPEN)

    assert impact.valid
    assert impact.contracted
    assert impact.forced
    assert not impact.dead_end
    assert impact.before.actions == frozenset({B0, B1})
    assert impact.after.actions == frozenset({B1})
    assert impact.after.unique_action == B1


def test_forced_b_action_reciprocally_forces_a_future_action() -> None:
    relation = _relation()
    a_to_b = relation.apply(A0, B_OPEN)
    forced_b = a_to_b.after.unique_action

    b_to_a = relation.apply(forced_b, A_OPEN)

    assert b_to_a.valid
    assert b_to_a.contracted
    assert b_to_a.forced
    assert b_to_a.after.actions == frozenset({A1})
    assert b_to_a.after.unique_action == A1


def test_forcedness_is_derived_from_relation_not_hardcoded() -> None:
    baseline = _relation()
    assert baseline.apply(A0, B_OPEN).forced

    # Mutation 1: one extra compatible response destroys forcedness.
    expanded = PublicResponseRelation(baseline.pairs | frozenset({(A0, B0)}))
    expanded_impact = expanded.apply(A0, B_OPEN)
    assert expanded_impact.valid
    assert not expanded_impact.contracted
    assert not expanded_impact.forced
    assert expanded_impact.after == B_OPEN

    # Mutation 2: removing the unique response produces a dead end, not a
    # fabricated forced action.
    erased = PublicResponseRelation(baseline.pairs - frozenset({(A0, B1)}))
    erased_impact = erased.apply(A0, B_OPEN)
    assert erased_impact.valid
    assert erased_impact.contracted
    assert not erased_impact.forced
    assert erased_impact.dead_end


def test_public_interaction_surface_contains_no_private_policy_slot() -> None:
    # Structural witness: the public calculus has no field in which either
    # agent's private chooser, utility, or search tree could be supplied.
    surface_fields = {field.name for field in fields(EvitabilitySurface)}
    relation_fields = {field.name for field in fields(PublicResponseRelation)}

    assert surface_fields == {"actor", "actions"}
    assert relation_fields == {"pairs"}


def test_directionality_is_not_silently_treated_as_symmetry() -> None:
    relation = _relation()

    assert relation.replies_to(A0) == frozenset({B1})
    assert relation.replies_to(B1) == frozenset({A1})
    assert A0 not in relation.replies_to(B1)

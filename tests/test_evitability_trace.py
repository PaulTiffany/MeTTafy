from __future__ import annotations

from mettafy.evitability_interaction import (
    EvitabilitySurface,
    PublicAction,
    PublicResponseRelation,
)
from mettafy.evitability_trace import AlternatingInteractionTrace

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
                (A0, B1),
                (A1, B0),
                (A1, B1),
                (B1, A1),
                (B0, A0),
                (B0, A1),
            }
        )
    )


def test_alternating_forcing_composes_without_private_policy() -> None:
    relation = _relation()

    first = relation.exchange(A0, A_OPEN, B_OPEN)
    b_forced = first.impact.after
    second = relation.exchange(B1, b_forced, A_OPEN)

    trace = AlternatingInteractionTrace(
        relation=relation,
        initial_surfaces=(A_OPEN, B_OPEN),
        exchanges=(first, second),
    )

    assert trace.valid
    assert trace.forced_impacts == 2
    assert trace.contracting_impacts == 2
    assert trace.final_surfaces == (
        EvitabilitySurface("A", frozenset({A1})),
        EvitabilitySurface("B", frozenset({B1})),
    )
    assert not trace.configuration_replay


def test_trace_rejects_skipping_a_mechanically_forced_reply() -> None:
    relation = _relation()
    first = relation.exchange(A0, A_OPEN, B_OPEN)

    # Build a superficially valid B0 exchange against the original open B
    # surface. The trace must reject it because A0 has already contracted B's
    # actual current surface to the singleton {B1}.
    wrong_second = relation.exchange(B0, B_OPEN, A_OPEN)
    trace = AlternatingInteractionTrace(
        relation=relation,
        initial_surfaces=(A_OPEN, B_OPEN),
        exchanges=(first, wrong_second),
    )

    assert not trace.valid


def test_forcedness_does_not_by_itself_imply_progress() -> None:
    relation = _relation()

    first = relation.exchange(A0, A_OPEN, B_OPEN)
    b_forced = first.impact.after
    second = relation.exchange(B1, b_forced, A_OPEN)
    a_forced = second.impact.after

    # Once both surfaces are singleton, the same forced reactions remain lawful
    # but no longer contract either future-action surface.
    third = relation.exchange(A1, a_forced, b_forced)
    fourth = relation.exchange(B1, third.impact.after, a_forced)

    trace = AlternatingInteractionTrace(
        relation=relation,
        initial_surfaces=(A_OPEN, B_OPEN),
        exchanges=(first, second, third, fourth),
    )

    assert trace.valid
    assert trace.forced_impacts == 4
    assert trace.contracting_impacts == 2
    assert not third.impact.contracted
    assert not fourth.impact.contracted
    assert trace.configuration_replay


def test_dead_end_has_no_lawful_successor_exchange() -> None:
    baseline = _relation()
    erased = PublicResponseRelation(baseline.pairs - frozenset({(A0, B1)}))
    first = erased.exchange(A0, A_OPEN, B_OPEN)
    assert first.impact.dead_end

    # A standalone B action can be formed only against some other surface, but
    # it cannot follow this trace because the actual B surface is empty.
    unrelated_second = erased.exchange(B0, B_OPEN, A_OPEN)
    trace = AlternatingInteractionTrace(
        relation=erased,
        initial_surfaces=(A_OPEN, B_OPEN),
        exchanges=(first, unrelated_second),
    )

    assert not trace.valid

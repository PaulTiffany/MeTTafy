from __future__ import annotations

import pytest

from mettafy.evitability import TurnActionSignature
from mettafy.triadic_evitability import TriadicHistory, triadic_ordered_evitability


def _action(seed: str, source: int, target: int) -> TurnActionSignature:
    return TurnActionSignature(
        seed=seed,
        source_color=source,
        target_color=target,
        component=frozenset({seed}),
        boundary_hits=frozenset({seed}),
        restoration_colors_after=frozenset(),
    )


def _late_transform_history() -> TriadicHistory:
    return (
        TriadicHistory(frozenset({"a", "b", "v"}))
        .place("a", 0)
        .place("b", 1)
        .transform("a", 2)
    )


def _early_transform_history() -> TriadicHistory:
    return (
        TriadicHistory(frozenset({"a", "b", "v"}))
        .place("a", 0)
        .transform("a", 2)
        .place("b", 1)
    )


def test_same_static_world_can_retain_different_realization_history() -> None:
    late = _late_transform_history().snapshot()
    early = _early_transform_history().snapshot()

    # Carrier plus current extensional identities are exactly the same.
    assert late.extensional_projection == early.extensional_projection
    assert late.extensional_projection == (
        frozenset({"a", "b", "v"}),
        (("a", 2), ("b", 1)),
    )

    # Persistent lineage chronology is also the same: a existed before b.
    assert late.difference.lineage_birth_order == ("a", "b")
    assert early.difference.lineage_birth_order == ("a", "b")

    # But the currently realized successor identities were born in different order.
    assert late.difference.current_state_birth_order == ("b", "a")
    assert early.difference.current_state_birth_order == ("a", "b")
    assert late.difference != early.difference

    # The carrier locus v remains a site, not a fabricated hollow state.
    assert late.difference.unrealized_loci == frozenset({"v"})
    assert early.difference.unrealized_loci == frozenset({"v"})


def test_held_difference_changes_ordered_evitability_without_changing_snapshot() -> None:
    late_history = _late_transform_history()
    early_history = _early_transform_history()
    actions = frozenset({_action("a", 2, 0), _action("b", 1, 3)})

    late = triadic_ordered_evitability(actions, late_history)
    early = triadic_ordered_evitability(actions, early_history)

    # Both projections agree on persistent lineage age.
    assert late.lineage_order.first_actor == "a"
    assert early.lineage_order.first_actor == "a"

    # The current-state clock differs solely because a_2 was realized at a
    # different constructional time relative to b_1.
    assert late.current_state_order.first_actor == "b"
    assert early.current_state_order.first_actor == "a"
    assert late.order_disagreement
    assert not early.order_disagreement

    # Forgetting the held difference makes the two histories observationally identical.
    assert (
        late_history.snapshot().extensional_projection
        == early_history.snapshot().extensional_projection
    )


def test_transform_creates_a_new_current_state_without_rewriting_lineage_birth() -> None:
    history = TriadicHistory(frozenset({"a", "b"})).place("a", 0).transform("a", 2)
    state = history.current_states[0]

    assert history.lineage_birth_order == ("a",)
    assert state.lineage == "a"
    assert state.realized_color == 2
    assert state.generation == 1
    assert state.born_at == 1


def test_unrealized_locus_cannot_transform_or_enter_action_order() -> None:
    history = TriadicHistory(frozenset({"a", "v"})).place("a", 0)

    with pytest.raises(ValueError, match="cannot transform an unrealized locus"):
        history.transform("v", 2)

    with pytest.raises(ValueError, match="unrealized site cannot act"):
        triadic_ordered_evitability({_action("v", 2, 3)}, history)


def test_invalid_history_cannot_smuggle_a_hollow_state_into_the_ledger() -> None:
    with pytest.raises(ValueError, match="outside the carrier"):
        TriadicHistory(frozenset({"a"})).place("b", 1)

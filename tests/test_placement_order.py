from __future__ import annotations

import pytest

from mettafy.evitability import TurnActionSignature
from mettafy.placement_order import PlacementEvent, PlacementLedger, placement_ordered_evitability


def _action(seed: str, source: int, target: int) -> TurnActionSignature:
    return TurnActionSignature(
        seed=seed,
        source_color=source,
        target_color=target,
        component=frozenset({seed}),
        boundary_hits=frozenset({seed}),
        restoration_colors_after=frozenset(),
    )


def test_unplaced_locations_are_sites_not_hollow_states() -> None:
    ledger = PlacementLedger().place("a", 0).place("b", 1)

    assert ledger.lineages == ("a", "b")
    assert ledger.unrealized_sites(("a", "b", "v")) == frozenset({"v"})
    assert not ledger.is_realized("v")

    with pytest.raises(ValueError, match="birth rank"):
        ledger.birth_rank("v")

    with pytest.raises(ValueError, match="unrealized site cannot act"):
        placement_ordered_evitability({_action("v", 2, 3)}, ledger)


def test_placement_requires_a_concrete_identity() -> None:
    with pytest.raises(ValueError, match="nonempty"):
        PlacementEvent("", 0)
    with pytest.raises(ValueError, match="concrete Q4 identity"):
        PlacementEvent("a", 4)


def test_first_placed_eligible_state_owns_first_evitability_tier() -> None:
    ledger = PlacementLedger().place("a", 0).place("b", 1).place("c", 2)
    b_action = _action("b", 1, 3)
    c_action = _action("c", 2, 0)

    ordered = placement_ordered_evitability({c_action, b_action}, ledger)

    assert ordered.first_actor == "b"
    assert ordered.first_birth_rank == 1
    assert ordered.first_actions == frozenset({b_action})
    assert ordered.deferred_actions == frozenset({c_action})


def test_same_extensional_actions_can_have_different_order_from_different_birth_history() -> None:
    b_action = _action("b", 1, 3)
    c_action = _action("c", 2, 0)
    actions = frozenset({b_action, c_action})

    b_first = PlacementLedger().place("b", 1).place("c", 2)
    c_first = PlacementLedger().place("c", 2).place("b", 1)

    assert placement_ordered_evitability(actions, b_first).first_actor == "b"
    assert placement_ordered_evitability(actions, c_first).first_actor == "c"


def test_birth_order_does_not_invent_a_private_tiebreak_within_first_actor() -> None:
    ledger = PlacementLedger().place("a", 0).place("b", 1)
    a_to_2 = _action("a", 0, 2)
    a_to_3 = _action("a", 0, 3)
    b_to_0 = _action("b", 1, 0)

    ordered = placement_ordered_evitability({a_to_2, a_to_3, b_to_0}, ledger)

    assert ordered.first_actor == "a"
    assert ordered.first_actions == frozenset({a_to_2, a_to_3})
    assert ordered.deferred_actions == frozenset({b_to_0})


def test_successor_identity_does_not_reset_first_placement_order() -> None:
    ledger = PlacementLedger().place("a", 0).place("b", 1)

    # The current source color of lineage a may have changed after a lawful
    # component transformation. Its constructional birth rank remains earlier.
    transformed_a_action = _action("a", 2, 0)
    b_action = _action("b", 1, 3)

    ordered = placement_ordered_evitability({transformed_a_action, b_action}, ledger)

    assert ledger.birth_rank("a") == 0
    assert ordered.first_actor == "a"


def test_empty_action_surface_has_no_fabricated_first_actor() -> None:
    ledger = PlacementLedger().place("a", 0)
    ordered = placement_ordered_evitability((), ledger)

    assert ordered.empty
    assert ordered.first_actor is None
    assert ordered.first_birth_rank is None
    assert not ordered.first_actions
    assert not ordered.deferred_actions

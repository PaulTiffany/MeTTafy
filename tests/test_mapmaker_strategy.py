from __future__ import annotations

import pytest

import mettafy.color_construction as color_construction
import mettafy.mapmaker_strategy as mapmaker
import mettafy.meta_construct_closure as closure

BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary_colors: tuple[int, int, int, int, int]) -> color_construction.ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return color_construction.ConstructionState(
        graph, dict(zip(BOUNDARY, boundary_colors, strict=True))
    )


def deciding_chain() -> closure.DecisionReachability:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = closure.ImaginaryProjection(
        box=closure.ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == "decide" else None,
    )
    allowed = {
        ("overview", "expand"),
        ("expand", "counter"),
        ("counter", "decide"),
    }
    return closure.DecisionReachability(
        projection=projection,
        states=("overview", "expand", "counter", "decide"),
        admissible_step=lambda before, after: (before, after) in allowed,
    )


def test_modes_are_exactly_do_imagine_x_observe_act() -> None:
    assert mapmaker.operational_product_complete()
    assert mapmaker.MODE_CELL == {
        mapmaker.MapMakerMode.OVERVIEW: mapmaker.OperationalCell(
            mapmaker.MapMakerDomain.DO, mapmaker.MapMakerOperation.OBSERVE
        ),
        mapmaker.MapMakerMode.LOCAL_EXPANSION: mapmaker.OperationalCell(
            mapmaker.MapMakerDomain.IMAGINE, mapmaker.MapMakerOperation.OBSERVE
        ),
        mapmaker.MapMakerMode.COUNTER_PLAY: mapmaker.OperationalCell(
            mapmaker.MapMakerDomain.IMAGINE, mapmaker.MapMakerOperation.ACT
        ),
        mapmaker.MapMakerMode.DRAW: mapmaker.OperationalCell(
            mapmaker.MapMakerDomain.DO, mapmaker.MapMakerOperation.ACT
        ),
    }
    for mode, cell in mapmaker.MODE_CELL.items():
        assert mapmaker.mode_for_cell(cell) is mode


def test_four_modes_are_pairwise_pareto_incomparable() -> None:
    for lhs in mapmaker.MapMakerMode:
        for rhs in mapmaker.MapMakerMode:
            assert mapmaker.mode_dominates(lhs, rhs) is (lhs is rhs)


def test_canonical_program_is_capability_complete() -> None:
    assert mapmaker.capability_complete(mapmaker.CANONICAL_PARETO_PROGRAM)
    assert set().union(
        *(mapmaker.MODE_CAPABILITIES[mode] for mode in mapmaker.CANONICAL_PARETO_PROGRAM)
    ) == set(mapmaker.MapMakerCapability)


def test_draw_is_the_only_write_and_has_no_perception_capability() -> None:
    assert mapmaker.MODE_CAPABILITIES[mapmaker.MapMakerMode.DRAW] == frozenset(
        {mapmaker.MapMakerCapability.BLIND_REALIZED_WRITE}
    )
    for mode in mapmaker.PRECOMMIT_MODES:
        assert (
            mapmaker.MapMakerCapability.BLIND_REALIZED_WRITE
            not in mapmaker.MODE_CAPABILITIES[mode]
        )


def test_precommit_order_is_do_observe_imagine_observe_imagine_act_star() -> None:
    assert mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
        )
    )
    assert mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.COUNTER_PLAY,
        )
    )
    assert not mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.OVERVIEW,
        )
    )
    assert not mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
        )
    )
    assert not mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.DRAW,
        )
    )


def test_authority_crossing_normal_form_preserves_previous_ordering() -> None:
    assert mapmaker.is_operational_normal_form(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.DRAW,
        )
    )
    assert mapmaker.is_operational_normal_form(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.DRAW,
        )
    )
    assert not mapmaker.is_operational_normal_form(
        (mapmaker.MapMakerMode.DRAW, mapmaker.MapMakerMode.OVERVIEW)
    )
    assert not mapmaker.is_operational_normal_form(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.DRAW,
        )
    )


def test_mapmaker_decision_labels_the_ordered_if_then_spine_and_draws_once() -> None:
    reachability = deciding_chain()
    decision = mapmaker.MapMakerDecision(
        reachability=reachability,
        precommit_modes=(
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.COUNTER_PLAY,
        ),
    )

    assert decision.strategy_word() == (
        mapmaker.MapMakerMode.OVERVIEW,
        mapmaker.MapMakerMode.LOCAL_EXPANSION,
        mapmaker.MapMakerMode.COUNTER_PLAY,
        mapmaker.MapMakerMode.DRAW,
    )
    assert mapmaker.is_operational_normal_form(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1
    assert decision.draw().coloring["v"] == 3


def test_order_violation_cannot_enter_decision_residue() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="preserve Do:Observe"):
        mapmaker.MapMakerDecision(
            reachability=reachability,
            precommit_modes=(
                mapmaker.MapMakerMode.OVERVIEW,
                mapmaker.MapMakerMode.COUNTER_PLAY,
                mapmaker.MapMakerMode.LOCAL_EXPANSION,
            ),
        )


def test_one_mode_label_is_required_per_if_then_step() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="one precommit mode label"):
        mapmaker.MapMakerDecision(
            reachability=reachability,
            precommit_modes=(
                mapmaker.MapMakerMode.OVERVIEW,
                mapmaker.MapMakerMode.LOCAL_EXPANSION,
            ),
        )


def test_unbounded_imagination_still_allows_long_ordered_consequence_chain() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = closure.ImaginaryProjection(
        box=closure.ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == 10_000 else None,
    )
    reachability = closure.DecisionReachability(
        projection=projection,
        states=tuple(range(10_001)),
        admissible_step=lambda before, after: after == before + 1,
    )
    modes = (
        mapmaker.MapMakerMode.OVERVIEW,
        mapmaker.MapMakerMode.LOCAL_EXPANSION,
        *(mapmaker.MapMakerMode.COUNTER_PLAY for _ in range(9_998)),
    )

    decision = mapmaker.MapMakerDecision(reachability=reachability, precommit_modes=modes)

    assert mapmaker.is_operational_normal_form(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1

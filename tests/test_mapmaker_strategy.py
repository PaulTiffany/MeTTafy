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


def test_precommit_normal_form_excludes_draw() -> None:
    assert mapmaker.is_precommit_program(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
        )
    )
    assert not mapmaker.is_precommit_program(
        (mapmaker.MapMakerMode.OVERVIEW, mapmaker.MapMakerMode.DRAW)
    )


def test_authority_crossing_normal_form_is_thought_star_then_draw() -> None:
    assert mapmaker.is_blind_draw_suffix(
        (
            mapmaker.MapMakerMode.OVERVIEW,
            mapmaker.MapMakerMode.LOCAL_EXPANSION,
            mapmaker.MapMakerMode.COUNTER_PLAY,
            mapmaker.MapMakerMode.DRAW,
        )
    )
    assert mapmaker.is_blind_draw_suffix((mapmaker.MapMakerMode.DRAW,))
    assert not mapmaker.is_blind_draw_suffix(
        (mapmaker.MapMakerMode.DRAW, mapmaker.MapMakerMode.OVERVIEW)
    )
    assert not mapmaker.is_blind_draw_suffix((mapmaker.MapMakerMode.OVERVIEW,))


def test_mapmaker_decision_labels_the_if_then_spine_and_draws_once() -> None:
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
    assert mapmaker.is_blind_draw_suffix(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1
    assert decision.draw().coloring["v"] == 3


def test_draw_cannot_appear_inside_decision_reachability_labels() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="cannot contain draw"):
        mapmaker.MapMakerDecision(
            reachability=reachability,
            precommit_modes=(
                mapmaker.MapMakerMode.OVERVIEW,
                mapmaker.MapMakerMode.DRAW,
                mapmaker.MapMakerMode.COUNTER_PLAY,
            ),
        )


def test_one_mode_label_is_required_per_if_then_step() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="one precommit mode label"):
        mapmaker.MapMakerDecision(
            reachability=reachability,
            precommit_modes=(mapmaker.MapMakerMode.OVERVIEW,),
        )


def test_unbounded_imagination_still_allows_long_transferable_mode_residue() -> None:
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
    modes = tuple(
        mapmaker.MapMakerMode.LOCAL_EXPANSION
        if index % 2 == 0
        else mapmaker.MapMakerMode.COUNTER_PLAY
        for index in range(10_000)
    )

    decision = mapmaker.MapMakerDecision(reachability=reachability, precommit_modes=modes)

    assert mapmaker.is_blind_draw_suffix(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1

from __future__ import annotations

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.mapmaker_strategy import (
    CANONICAL_PARETO_PROGRAM,
    capability_complete,
    is_blind_draw_suffix,
    is_precommit_program,
    MapMakerCapability,
    MapMakerDecision,
    MapMakerMode,
    MODE_CAPABILITIES,
    mode_dominates,
    PRECOMMIT_MODES,
)
from mettafy.meta_construct_closure import (
    DecisionReachability,
    ImaginaryProjection,
    ImaginationBox,
)


BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary_colors: tuple[int, int, int, int, int]) -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(graph, dict(zip(BOUNDARY, boundary_colors, strict=True)))


def deciding_chain() -> DecisionReachability:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == "decide" else None,
    )
    allowed = {
        ("overview", "expand"),
        ("expand", "counter"),
        ("counter", "decide"),
    }
    return DecisionReachability(
        projection=projection,
        states=("overview", "expand", "counter", "decide"),
        admissible_step=lambda before, after: (before, after) in allowed,
    )


def test_four_modes_are_pairwise_pareto_incomparable() -> None:
    for lhs in MapMakerMode:
        for rhs in MapMakerMode:
            assert mode_dominates(lhs, rhs) is (lhs is rhs)


def test_canonical_program_is_capability_complete() -> None:
    assert capability_complete(CANONICAL_PARETO_PROGRAM)
    assert set().union(*(MODE_CAPABILITIES[mode] for mode in CANONICAL_PARETO_PROGRAM)) == set(
        MapMakerCapability
    )


def test_draw_is_the_only_write_and_has_no_perception_capability() -> None:
    assert MODE_CAPABILITIES[MapMakerMode.DRAW] == frozenset(
        {MapMakerCapability.BLIND_REALIZED_WRITE}
    )
    for mode in PRECOMMIT_MODES:
        assert MapMakerCapability.BLIND_REALIZED_WRITE not in MODE_CAPABILITIES[mode]


def test_precommit_normal_form_excludes_draw() -> None:
    assert is_precommit_program(
        (
            MapMakerMode.OVERVIEW,
            MapMakerMode.LOCAL_EXPANSION,
            MapMakerMode.COUNTER_PLAY,
            MapMakerMode.LOCAL_EXPANSION,
        )
    )
    assert not is_precommit_program((MapMakerMode.OVERVIEW, MapMakerMode.DRAW))


def test_authority_crossing_normal_form_is_thought_star_then_draw() -> None:
    assert is_blind_draw_suffix(
        (
            MapMakerMode.OVERVIEW,
            MapMakerMode.LOCAL_EXPANSION,
            MapMakerMode.COUNTER_PLAY,
            MapMakerMode.DRAW,
        )
    )
    assert is_blind_draw_suffix((MapMakerMode.DRAW,))
    assert not is_blind_draw_suffix((MapMakerMode.DRAW, MapMakerMode.OVERVIEW))
    assert not is_blind_draw_suffix((MapMakerMode.OVERVIEW,))


def test_mapmaker_decision_labels_the_if_then_spine_and_draws_once() -> None:
    reachability = deciding_chain()
    decision = MapMakerDecision(
        reachability=reachability,
        precommit_modes=(
            MapMakerMode.OVERVIEW,
            MapMakerMode.LOCAL_EXPANSION,
            MapMakerMode.COUNTER_PLAY,
        ),
    )

    assert decision.strategy_word() == (
        MapMakerMode.OVERVIEW,
        MapMakerMode.LOCAL_EXPANSION,
        MapMakerMode.COUNTER_PLAY,
        MapMakerMode.DRAW,
    )
    assert is_blind_draw_suffix(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1
    assert decision.draw().coloring["v"] == 3


def test_draw_cannot_appear_inside_decision_reachability_labels() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="cannot contain draw"):
        MapMakerDecision(
            reachability=reachability,
            precommit_modes=(
                MapMakerMode.OVERVIEW,
                MapMakerMode.DRAW,
                MapMakerMode.COUNTER_PLAY,
            ),
        )


def test_one_mode_label_is_required_per_if_then_step() -> None:
    reachability = deciding_chain()

    with pytest.raises(ValueError, match="one precommit mode label"):
        MapMakerDecision(
            reachability=reachability,
            precommit_modes=(MapMakerMode.OVERVIEW,),
        )


def test_unbounded_imagination_still_allows_long_transferable_mode_residue() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == 10_000 else None,
    )
    reachability = DecisionReachability(
        projection=projection,
        states=tuple(range(10_001)),
        admissible_step=lambda before, after: after == before + 1,
    )
    modes = tuple(
        MapMakerMode.LOCAL_EXPANSION if index % 2 == 0 else MapMakerMode.COUNTER_PLAY
        for index in range(10_000)
    )

    decision = MapMakerDecision(reachability=reachability, precommit_modes=modes)

    assert is_blind_draw_suffix(decision.strategy_word())
    assert decision.certificate().color == 3
    assert decision.realized_void_delta() == 1

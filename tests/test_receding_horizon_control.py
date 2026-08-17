from __future__ import annotations

from itertools import product

from mettafy.color_construction import ConstructionState
from mettafy.plane_parameterization import proper_cycle
from mettafy.receding_horizon_control import FocusSlackPathCertificate, audit_control_component

BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary: tuple[int, int, int, int, int]) -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(graph, dict(zip(BOUNDARY, boundary)))


def persistent_double_lock_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )


def saturated_boundaries() -> tuple[tuple[int, int, int, int, int], ...]:
    return tuple(
        (word[0], word[1], word[2], word[3], word[4])
        for word in product(range(4), repeat=5)
        if proper_cycle(word) and len(set(word)) == 4
    )


def test_all_saturated_bare_c5_states_have_one_stage_slack_witness() -> None:
    boundaries = saturated_boundaries()
    assert len(boundaries) == 120

    for boundary in boundaries:
        result = audit_control_component(wheel_state(boundary), "v")
        assert isinstance(result, FocusSlackPathCertificate)
        assert result.valid
        assert len(result.moves) == 1


def test_persistent_exterior_requires_two_receding_horizon_stages() -> None:
    result = audit_control_component(persistent_double_lock_state(), "v")
    assert isinstance(result, FocusSlackPathCertificate)
    assert result.valid
    assert len(result.moves) == 2
    assert result.final.admissible_colors("v")


def test_initial_positive_slack_is_a_zero_stage_certificate() -> None:
    result = audit_control_component(wheel_state((0, 1, 0, 1, 2)), "v")
    assert isinstance(result, FocusSlackPathCertificate)
    assert result.valid
    assert result.moves == ()
    assert result.final.admissible_colors("v") == frozenset({3})


def test_certificate_replay_uses_only_controls_available_at_each_state() -> None:
    result = audit_control_component(persistent_double_lock_state(), "v")
    assert isinstance(result, FocusSlackPathCertificate)

    replay = result.replay()
    assert len(replay) == len(result.moves) + 1
    assert all(state.committed_edges_valid for state in replay)
    assert all(state.surface_genus == 0 for state in replay)
    assert all(dict(state.graph) == dict(result.initial.graph) for state in replay)

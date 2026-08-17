from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import ColorationControlSurface, state_key
from mettafy.kempe_traversal import KempeMove


def persistent_double_lock_state() -> ConstructionState:
    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    return ConstructionState(
        graph,
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
        },
    )


def test_controls_are_derived_from_current_graph_state() -> None:
    surface = ColorationControlSurface(persistent_double_lock_state(), "v")
    controls = surface.controls(surface.initial)
    assert controls
    assert all(move.seed in surface.initial.coloring for move in controls)


def test_bounded_exploration_preserves_the_same_carrier_and_species() -> None:
    surface = ColorationControlSurface(persistent_double_lock_state(), "v")
    states, transitions = surface.explore(max_depth=2)

    assert transitions
    assert len(states) > 1
    for state in states.values():
        assert dict(state.graph) == dict(surface.initial.graph)
        assert state.surface_genus == 0
        assert set(state.coloring) == set(surface.initial.coloring)
        assert state.committed_edges_valid


def test_shortest_focus_slack_path_is_two_on_persistent_carrier() -> None:
    surface = ColorationControlSurface(persistent_double_lock_state(), "v")
    path = surface.shortest_focus_slack_path(max_depth=2)
    assert path is not None
    assert len(path) == 2

    current = surface.initial
    for move in path:
        current = surface.step(current, move)
    assert current.admissible_colors("v")


def test_noncommuting_controls_define_distinct_surface_points() -> None:
    surface = ColorationControlSurface(persistent_double_lock_state(), "v")
    t_ab = KempeMove(seed="a", other_color=1)
    t_bc = KempeMove(seed="b", other_color=2)

    left, right = surface.ordered_pair_endpoints(t_ab, t_bc)
    assert state_key(left) != state_key(right)
    assert not surface.pair_commutes(t_ab, t_bc)


def test_commuting_controls_land_on_same_surface_point() -> None:
    surface = ColorationControlSurface(persistent_double_lock_state(), "v")
    t_ac = KempeMove(seed="a", other_color=2)
    t_ad = KempeMove(seed="c", other_color=3)

    left, right = surface.ordered_pair_endpoints(t_ac, t_ad)
    assert state_key(left) == state_key(right)
    assert surface.pair_commutes(t_ac, t_ad)
    assert left.admissible_colors("v") == frozenset({0})

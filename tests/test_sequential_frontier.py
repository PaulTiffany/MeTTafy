from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.sequential_frontier import (
    clean_frontier_turns,
    shortest_clean_frontier_audit_route,
)

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"


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
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
        },
    )


def three_interior_lock_state() -> ConstructionState:
    disk_faces = (
        ("b", "x0", "x1"),
        ("x1", "x2", "x0"),
        ("e", "x2", "d"),
        ("a", "x0", "b"),
        ("x1", "d", "x2"),
        ("e", "x0", "a"),
        ("e", "x0", "x2"),
        ("c", "x1", "b"),
        ("c", "x1", "d"),
    )
    coloring = {
        "a": 0,
        "b": 1,
        "c": 0,
        "d": 2,
        "e": 3,
        "x0": 2,
        "x1": 3,
        "x2": 1,
    }
    vertices = {FOCUS, *BOUNDARY, *coloring}
    adjacency = {vertex: set() for vertex in vertices}

    def add_edge(left: str, right: str) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    for index, vertex in enumerate(BOUNDARY):
        add_edge(FOCUS, vertex)
        add_edge(vertex, BOUNDARY[(index + 1) % 5])
    for face in disk_faces:
        for index, vertex in enumerate(face):
            add_edge(vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    return ConstructionState(graph, coloring)


def _turn_signature(state: ConstructionState) -> tuple[tuple[str, int, frozenset[str]], ...]:
    return tuple(
        (turn.move.seed, turn.move.other_color, turn.component)
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
    )


def test_clean_turn_means_one_complete_component_and_one_frontier_change() -> None:
    state = persistent_double_lock_state()
    turns = clean_frontier_turns(state, FOCUS, BOUNDARY)

    assert _turn_signature(state) == (
        ("a", 2, frozenset({"a"})),
        ("c", 3, frozenset({"c"})),
    )
    assert all(turn.valid for turn in turns)
    assert all(turn.boundary_hits == frozenset({turn.move.seed}) for turn in turns)
    assert all(
        turn.changed_boundary_vertices == frozenset({turn.move.seed})
        for turn in turns
    )


def test_persistent_double_lock_resolves_in_two_clean_turns() -> None:
    state = persistent_double_lock_state()
    route = shortest_clean_frontier_audit_route(
        state,
        FOCUS,
        BOUNDARY,
        max_turns=2,
    )

    assert route is not None
    assert route.valid
    assert len(route.turns) == 2
    assert tuple(
        (turn.move.seed, turn.move.other_color)
        for turn in route.turns
    ) == (("a", 2), ("c", 3))
    assert route.final.admissible_colors(FOCUS) == frozenset({0})


def test_three_interior_kill_witness_needs_three_clean_turns() -> None:
    state = three_interior_lock_state()

    assert _turn_signature(state) == (
        ("a", 2, frozenset({"a", "x0"})),
        ("c", 3, frozenset({"c", "x1"})),
    )
    assert shortest_clean_frontier_audit_route(
        state,
        FOCUS,
        BOUNDARY,
        max_turns=2,
    ) is None

    route = shortest_clean_frontier_audit_route(
        state,
        FOCUS,
        BOUNDARY,
        max_turns=3,
    )
    assert route is not None
    assert route.valid
    assert len(route.turns) == 3
    assert tuple(
        (turn.move.seed, turn.move.other_color)
        for turn in route.turns
    ) == (("a", 2), ("d", 1), ("a", 0))
    assert route.final.admissible_colors(FOCUS) == frozenset({2})

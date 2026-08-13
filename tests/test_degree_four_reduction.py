from __future__ import annotations

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.degree_four_reduction import (
    certify_degree_four_reduction,
    degree_four_opening_move,
)

BOUNDARY = ("a", "b", "c", "d")
FOCUS = "v"


def _state(
    extra_edges: tuple[tuple[str, str], ...] = (),
    extra_colors: dict[str, int] | None = None,
) -> ConstructionState:
    colors = {"a": 0, "b": 1, "c": 2, "d": 3}
    colors.update(extra_colors or {})
    vertices = {FOCUS, *BOUNDARY, *colors}
    adjacency = {vertex: set() for vertex in vertices}

    def add(left: str, right: str) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    for index, vertex in enumerate(BOUNDARY):
        add(FOCUS, vertex)
        add(vertex, BOUNDARY[(index + 1) % 4])
    for left, right in extra_edges:
        add(left, right)

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    return ConstructionState(graph, colors)


def test_degree_four_first_opposite_pair_opening_is_certified() -> None:
    state = _state()

    certificate = certify_degree_four_reduction(state, FOCUS, BOUNDARY)

    assert certificate is not None
    assert certificate.move.seed == "a"
    assert certificate.move.other_color == 2
    assert certificate.valid


def test_degree_four_connected_first_pair_forces_complementary_opening() -> None:
    state = _state(
        extra_edges=(("a", "x"), ("x", "y"), ("y", "c")),
        extra_colors={"x": 2, "y": 0},
    )

    certificate = certify_degree_four_reduction(state, FOCUS, BOUNDARY)

    assert certificate is not None
    assert certificate.move.seed == "b"
    assert certificate.move.other_color == 3
    assert certificate.valid


def test_degree_four_both_opposite_pairs_connected_rejects_planarity_premise() -> None:
    state = _state(
        extra_edges=(
            ("a", "x"),
            ("x", "y"),
            ("y", "c"),
            ("b", "z"),
            ("z", "w"),
            ("w", "d"),
        ),
        extra_colors={"x": 2, "y": 0, "z": 3, "w": 1},
    )

    with pytest.raises(ValueError, match="planar crosscut premise"):
        degree_four_opening_move(state, FOCUS, BOUNDARY)


def test_degree_four_with_existing_slack_needs_no_kempe_move() -> None:
    state = ConstructionState(
        {
            FOCUS: BOUNDARY,
            "a": (FOCUS, "b", "d"),
            "b": (FOCUS, "a", "c"),
            "c": (FOCUS, "b", "d"),
            "d": (FOCUS, "a", "c"),
        },
        {"a": 0, "b": 1, "c": 0, "d": 2},
    )

    assert degree_four_opening_move(state, FOCUS, BOUNDARY) is None

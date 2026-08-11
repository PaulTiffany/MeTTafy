from __future__ import annotations

import pytest

from mettafy.color_construction import (
    ConstructionState,
    TraversalRewriteCertificate,
    brown_projection,
    terminal_decode,
)


def pentagon_with_center() -> dict[str, tuple[str, ...]]:
    return {
        "v0": ("v1", "v4", "c"),
        "v1": ("v0", "v2", "c"),
        "v2": ("v1", "v3", "c"),
        "v3": ("v2", "v4", "c"),
        "v4": ("v3", "v0", "c"),
        "c": ("v0", "v1", "v2", "v3", "v4"),
    }


def test_admissible_color_space_is_exact_neighbor_complement() -> None:
    graph = pentagon_with_center()
    state = ConstructionState(
        graph,
        {"v0": 0, "v1": 1, "v2": 0, "v3": 2, "v4": 3},
    )
    assert state.neighbor_color_image("c") == frozenset({0, 1, 2, 3})
    assert state.admissible_colors("c") == frozenset()

    open_state = ConstructionState(
        graph,
        {"v0": 0, "v1": 1, "v2": 0, "v3": 1, "v4": 2},
    )
    assert open_state.neighbor_color_image("c") == frozenset({0, 1, 2})
    assert open_state.admissible_colors("c") == frozenset({3})


def test_brown_projection_is_many_to_one_and_cannot_recover_construction() -> None:
    graph = {
        "a": ("b",),
        "b": ("a", "c"),
        "c": ("b",),
        "d": (),
    }
    left = ConstructionState(graph, {"a": 0, "b": 1})
    right = ConstructionState(graph, {"b": 0, "c": 1})
    assert left != right
    assert brown_projection(left) == brown_projection(right)


def test_terminal_decode_is_available_only_after_completion() -> None:
    graph = {"a": ("b",), "b": ("a",)}
    partial = ConstructionState(graph, {"a": 0})
    with pytest.raises(ValueError, match="completed construction"):
        terminal_decode(partial)

    complete = partial.commit("b", 1)
    assert terminal_decode(complete) == {"a": 0, "b": 1}


def test_construction_commit_uses_current_adjacency_not_brown_projection() -> None:
    graph = {"a": ("b",), "b": ("a",)}
    state = ConstructionState(graph, {"a": 0})
    observation = brown_projection(state)
    assert observation.brown
    assert state.admissible_colors("b") == frozenset({1, 2, 3})
    with pytest.raises(ValueError, match="not admissible"):
        state.commit("b", 0)


def test_rewrite_certificate_requires_actual_ledger_preserving_desaturation() -> None:
    graph = pentagon_with_center()
    before = ConstructionState(
        graph,
        {"v0": 0, "v1": 1, "v2": 0, "v3": 2, "v4": 3},
    )
    # A legal desaturation of this isolated wheel boundary.
    after = ConstructionState(
        graph,
        {"v0": 0, "v1": 1, "v2": 0, "v3": 1, "v4": 2},
    )
    certificate = TraversalRewriteCertificate(before, after, "c")
    assert certificate.valid
    assert before.admissible_colors("c") == frozenset()
    assert after.admissible_colors("c") == frozenset({3})


def test_rewrite_certificate_rejects_edge_breaking_state() -> None:
    graph = {
        **pentagon_with_center(),
        "x": ("v3",),
    }
    graph["v3"] = graph["v3"] + ("x",)
    before = ConstructionState(
        graph,
        {"v0": 0, "v1": 1, "v2": 0, "v3": 2, "v4": 3, "x": 1},
    )
    # The isolated-wheel recoloring would make v3=1 collide with exterior x=1.
    with pytest.raises(ValueError, match="committed edge"):
        ConstructionState(
            graph,
            {"v0": 0, "v1": 1, "v2": 0, "v3": 1, "v4": 2, "x": 1},
        )

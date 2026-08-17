from __future__ import annotations

from collections import Counter

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import opening_single_moves, single_move_locked


def locked_planar_c5_state() -> ConstructionState:
    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "x", "p"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "y"),
        "e": ("v", "d", "a", "q"),
        "x": ("b", "y"),
        "y": ("x", "d"),
        "p": ("b", "q"),
        "q": ("p", "e"),
    }
    return ConstructionState(
        graph,
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
            "x": 2,
            "y": 1,
            "p": 3,
            "q": 1,
        },
    )


def undirected_edge(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left < right else (right, left)


def test_locked_witness_has_explicit_planar_embedding_certificate() -> None:
    state = locked_planar_c5_state()
    faces = (
        ("v", "b", "a"),
        ("v", "c", "b"),
        ("v", "d", "c"),
        ("v", "e", "d"),
        ("v", "a", "e"),
        ("a", "b", "p", "q", "e"),
        ("b", "c", "d", "y", "x"),
        ("b", "x", "y", "d", "e", "q", "p"),
    )

    graph_edges = {
        undirected_edge(vertex, neighbor)
        for vertex, neighbors in state.graph.items()
        for neighbor in neighbors
        if vertex != neighbor
    }
    face_edge_counts: Counter[tuple[str, str]] = Counter()
    for face in faces:
        for left, right in zip(face, face[1:] + face[:1]):
            face_edge_counts[undirected_edge(left, right)] += 1

    assert set(face_edge_counts) == graph_edges
    assert set(face_edge_counts.values()) == {2}
    assert len(state.graph) - len(graph_edges) + len(faces) == 2


def test_planar_saturated_c5_can_be_genuinely_single_move_locked() -> None:
    state = locked_planar_c5_state()
    assert state.admissible_colors("v") == frozenset()
    assert opening_single_moves(state, "v") == ()
    assert single_move_locked(state, "v")

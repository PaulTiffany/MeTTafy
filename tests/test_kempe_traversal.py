from __future__ import annotations

from collections import Counter

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    KempeTraversalCertificate,
    apply_kempe_move,
    opening_single_moves,
    single_move_locked,
)


def planar_traversal_state() -> ConstructionState:
    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e", "x"),
        "b": ("v", "a", "c", "x", "y"),
        "c": ("v", "b", "d", "y", "z"),
        "d": ("v", "c", "e", "z"),
        "e": ("v", "d", "a"),
        "x": ("a", "b", "y"),
        "y": ("b", "c", "x", "z"),
        "z": ("c", "d", "y"),
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
            "y": 3,
            "z": 1,
        },
    )


def undirected_edge(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left < right else (right, left)


def test_planar_witness_has_explicit_spherical_embedding_certificate() -> None:
    state = planar_traversal_state()
    faces = (
        ("v", "b", "a"),
        ("v", "c", "b"),
        ("v", "d", "c"),
        ("v", "e", "d"),
        ("v", "a", "e"),
        ("a", "b", "x"),
        ("a", "x", "y", "z", "d", "e"),
        ("b", "c", "y"),
        ("b", "y", "x"),
        ("c", "d", "z"),
        ("c", "z", "y"),
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


def test_saturated_focus_has_legal_single_move_openings() -> None:
    state = planar_traversal_state()
    assert state.admissible_colors("v") == frozenset()
    openings = opening_single_moves(state, "v")
    assert openings
    assert not single_move_locked(state, "v")

    opened = apply_kempe_move(state, openings[0])
    assert opened.committed_edges_valid
    assert opened.admissible_colors("v")


def test_exact_component_moves_compose_without_breaking_the_ledger() -> None:
    state = planar_traversal_state()
    first = KempeMove(seed="a", other_color=2)
    second = KempeMove(seed="b", other_color=3)
    certificate = KempeTraversalCertificate(
        initial=state,
        focus="v",
        moves=(first, second),
    )
    replay = certificate.replay()
    assert all(step.committed_edges_valid for step in replay)
    assert certificate.valid
    assert certificate.final.admissible_colors("v")


def test_component_swap_preserves_every_committed_edge() -> None:
    state = planar_traversal_state()
    for move in (
        KempeMove(seed="a", other_color=2),
        KempeMove(seed="b", other_color=3),
    ):
        state = apply_kempe_move(state, move)
        assert state.committed_edges_valid

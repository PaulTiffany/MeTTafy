from __future__ import annotations

from collections import Counter

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    KempeTraversalCertificate,
    apply_kempe_move,
    single_move_locked,
    two_color_component,
)

BOUNDARY = ("a", "b", "c", "d", "e")


def persistent_double_lock_state() -> ConstructionState:
    """Small planar carrier where the canonical A/B stage remains locked.

    The two extra carrier edges b-d and b-e witness the initial B/C and B/D
    locks.  After swapping the A/B component a-b-c, those *same physical edges*
    witness the new A/C and A/D locks.  No new geometric carrier has appeared;
    only its color-language typing has changed.
    """

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


def boundary_word(state: ConstructionState) -> tuple[int, int, int, int, int]:
    colors = tuple(state.coloring[vertex] for vertex in BOUNDARY)
    return (colors[0], colors[1], colors[2], colors[3], colors[4])


def undirected_edge(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left < right else (right, left)


def test_persistent_double_lock_has_explicit_planar_embedding_certificate() -> None:
    state = persistent_double_lock_state()
    faces = (
        ("v", "b", "a"),
        ("v", "c", "b"),
        ("v", "d", "c"),
        ("v", "e", "d"),
        ("v", "a", "e"),
        ("a", "b", "e"),
        ("b", "c", "d"),
        ("b", "d", "e"),
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


def test_canonical_ab_stage_can_remain_single_move_locked() -> None:
    state = persistent_double_lock_state()
    assert boundary_word(state) == (0, 1, 0, 2, 3)
    assert single_move_locked(state, "v")

    ab_component = two_color_component(state, "a", 1)
    assert ab_component == frozenset({"a", "b", "c"})

    after = apply_kempe_move(state, KempeMove(seed="a", other_color=1))
    assert after.committed_edges_valid
    assert boundary_word(after) == (1, 0, 1, 2, 3)
    assert single_move_locked(after, "v")


def test_persistent_lock_retypes_the_same_geometric_carrier() -> None:
    state = persistent_double_lock_state()
    after = apply_kempe_move(state, KempeMove(seed="a", other_color=1))

    carrier_edges = (("b", "d"), ("b", "e"))
    before_types = tuple(
        frozenset({state.coloring[left], state.coloring[right]})
        for left, right in carrier_edges
    )
    after_types = tuple(
        frozenset({after.coloring[left], after.coloring[right]})
        for left, right in carrier_edges
    )

    assert before_types == (frozenset({1, 2}), frozenset({1, 3}))
    assert after_types == (frozenset({0, 2}), frozenset({0, 3}))
    assert all(right in state.graph[left] for left, right in carrier_edges)
    assert all(right in after.graph[left] for left, right in carrier_edges)


def test_persistent_double_lock_is_not_closure_alternative_staging_opens() -> None:
    state = persistent_double_lock_state()

    # The canonical A/B stage is persistently locked, but fidelity requires us
    # to retain other legal stages instead of declaring closure.  Recolor the
    # singleton 0/2 component at a, then the singleton 0/3 component at c.
    first = KempeMove(seed="a", other_color=2)
    after_first = apply_kempe_move(state, first)
    assert boundary_word(after_first) == (2, 1, 0, 2, 3)
    assert after_first.admissible_colors("v") == frozenset()

    second = KempeMove(seed="c", other_color=3)
    after_second = apply_kempe_move(after_first, second)
    assert after_second.committed_edges_valid
    assert boundary_word(after_second) == (2, 1, 3, 2, 3)
    assert after_second.admissible_colors("v") == frozenset({0})

    certificate = KempeTraversalCertificate(
        initial=state,
        focus="v",
        moves=(first, second),
    )
    assert certificate.valid

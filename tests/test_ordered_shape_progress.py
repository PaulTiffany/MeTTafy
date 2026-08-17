from __future__ import annotations

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.ordered_shape import (
    OrderedShapeLedger,
    PhysicalComponentShape,
    certify_shape_progress,
    resolved_component_shape,
)
from mettafy.sequential_frontier import (
    clean_frontier_turns,
    shortest_clean_frontier_audit_route,
)

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"


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


def _clean_turn(state: ConstructionState, seed: str, other_color: int):
    matches = tuple(
        turn
        for turn in clean_frontier_turns(state, FOCUS, BOUNDARY)
        if turn.move.seed == seed and turn.move.other_color == other_color
    )
    assert len(matches) == 1
    return matches[0]


def test_m6_exact_inverse_replay_is_an_inconsequential_label_change() -> None:
    state = three_interior_lock_state()
    first = _clean_turn(state, "a", 2)

    first_certificate = certify_shape_progress(OrderedShapeLedger(), first)
    assert first_certificate.valid
    assert first_certificate.new_lineage
    assert first_certificate.consequential
    ledger = first_certificate.commit()

    inverse = _clean_turn(first.after, "a", 0)
    inverse_certificate = certify_shape_progress(ledger, inverse)

    assert resolved_component_shape(inverse) == resolved_component_shape(first)
    assert inverse_certificate.derived_shape_matches
    assert inverse_certificate.equivalent_replay
    assert not inverse_certificate.fresh
    assert not inverse_certificate.strict_refinement
    assert not inverse_certificate.consequential
    assert not inverse_certificate.valid
    with pytest.raises(ValueError, match="label-only replay"):
        inverse_certificate.commit()


def test_same_lineage_is_a_move_only_when_physical_shape_strictly_refines() -> None:
    state = three_interior_lock_state()
    route = shortest_clean_frontier_audit_route(
        state,
        FOCUS,
        BOUNDARY,
        max_turns=3,
    )

    assert route is not None
    assert route.valid
    assert len(route.turns) == 3

    ledger = OrderedShapeLedger()
    certificates = []
    for turn in route.turns:
        certificate = certify_shape_progress(ledger, turn)
        assert certificate.valid
        assert certificate.consequential
        certificates.append(certificate)
        ledger = certificate.commit()

    first_shape = resolved_component_shape(route.turns[0])
    third_shape = resolved_component_shape(route.turns[2])
    third_certificate = certificates[2]

    assert first_shape.lineage == third_shape.lineage
    assert first_shape.vertices < third_shape.vertices
    assert first_shape.edges <= third_shape.edges
    assert third_shape.strictly_refines(first_shape)
    assert third_certificate.prior_lineage_shapes == frozenset({first_shape})
    assert third_certificate.strict_refinement
    assert not third_certificate.new_lineage
    assert len(ledger.resolved) == 3


def test_incompatible_same_lineage_rewrite_is_not_growth() -> None:
    earlier = PhysicalComponentShape(
        color_pair=frozenset({0, 2}),
        vertices=frozenset({"a", "x0"}),
        edges=frozenset({("a", "x0")}),
        frontier_hits=frozenset({"a"}),
    )
    rewrite = PhysicalComponentShape(
        color_pair=frozenset({0, 2}),
        vertices=frozenset({"a", "x1"}),
        edges=frozenset({("a", "x1")}),
        frontier_hits=frozenset({"a"}),
    )

    assert rewrite.same_lineage(earlier)
    assert not rewrite.retains(earlier)
    assert not rewrite.strictly_refines(earlier)

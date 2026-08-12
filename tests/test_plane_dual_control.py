from __future__ import annotations

import pytest

from mettafy.color_construction import ConstructionState
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    apply_dual_nonzero_parameter,
    canonical_edge,
    derive_dual_domain_parameters,
    derive_embedded_dual_continuation,
)
from mettafy.zero_point_correspondence import (
    dual_defect_parameterization,
    kempe_parameterization,
    zero_point_correspondence,
)

BOUNDARY = ("a", "b", "c", "d", "e")
SIGMA = (0, 1)


def focus_slack_pairing_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e", "d"),
        "b": ("v", "a", "c", "d"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "a", "b"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )


def focus_slack_embedding() -> DegreeFiveTriangulatedEmbedding:
    return DegreeFiveTriangulatedEmbedding(
        state=focus_slack_pairing_state(),
        focus="v",
        boundary=BOUNDARY,
        faces=(
            ("v", "b", "a"),
            ("v", "c", "b"),
            ("v", "d", "c"),
            ("v", "e", "d"),
            ("v", "a", "e"),
            ("a", "b", "d"),
            ("b", "c", "d"),
            ("a", "d", "e"),
        ),
    )


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


def persistent_embedding() -> DegreeFiveTriangulatedEmbedding:
    return DegreeFiveTriangulatedEmbedding(
        state=persistent_double_lock_state(),
        focus="v",
        boundary=BOUNDARY,
        faces=(
            ("v", "b", "a"),
            ("v", "c", "b"),
            ("v", "d", "c"),
            ("v", "e", "d"),
            ("v", "a", "e"),
            ("a", "b", "e"),
            ("b", "c", "d"),
            ("b", "d", "e"),
        ),
    )


def test_embedding_derived_dual_parameter_shares_the_existing_zero_point() -> None:
    embedding = focus_slack_embedding()
    assert embedding.valid

    dual = dual_defect_parameterization(embedding.state, "v")
    kempe = kempe_parameterization(embedding.state)
    correspondence = zero_point_correspondence(kempe, dual)
    assert correspondence.valid
    assert correspondence.shared_zero is embedding.state

    parameters = derive_dual_domain_parameters(dual, embedding, SIGMA)
    assert len(parameters) == 2
    assert all(parameter.chart.zero_state is embedding.state for parameter in parameters)


def test_actual_positive_pairing_is_derived_from_faces_and_creates_focus_slack() -> None:
    embedding = focus_slack_embedding()
    continuation = derive_embedded_dual_continuation(embedding, SIGMA)

    assert continuation.valid
    assert continuation.terminal_pairing == ((0, 1), (3, 4))
    crossed = {
        path.terminal_edges: frozenset(path.crossed_edges)
        for path in continuation.paths
    }
    assert crossed[(0, 1)] == frozenset(
        {
            canonical_edge("a", "b"),
            canonical_edge("b", "d"),
            canonical_edge("b", "c"),
        }
    )
    assert crossed[(3, 4)] == frozenset(
        {
            canonical_edge("d", "e"),
            canonical_edge("a", "e"),
        }
    )

    chart = dual_defect_parameterization(embedding.state, "v")
    for parameter in derive_dual_domain_parameters(chart, embedding, SIGMA):
        certificate = apply_dual_nonzero_parameter(parameter)
        assert certificate.valid
        assert certificate.target_has_focus_slack
        assert certificate.after.admissible_colors("v")
        assert certificate.after.committed_edges_valid
        assert dict(certificate.after.graph) == dict(embedding.state.graph)


def test_actual_persistent_pairing_is_derived_without_inventing_focus_slack() -> None:
    embedding = persistent_embedding()
    assert embedding.valid
    continuation = derive_embedded_dual_continuation(embedding, SIGMA)

    assert continuation.valid
    assert continuation.terminal_pairing == ((0, 4), (1, 3))
    crossed = {
        path.terminal_edges: frozenset(path.crossed_edges)
        for path in continuation.paths
    }
    assert crossed[(0, 4)] == frozenset(
        {
            canonical_edge("a", "b"),
            canonical_edge("a", "e"),
        }
    )
    assert crossed[(1, 3)] == frozenset(
        {
            canonical_edge("b", "c"),
            canonical_edge("b", "d"),
            canonical_edge("d", "e"),
        }
    )

    chart = dual_defect_parameterization(embedding.state, "v")
    for parameter in derive_dual_domain_parameters(chart, embedding, SIGMA):
        certificate = apply_dual_nonzero_parameter(parameter)
        assert certificate.valid
        assert not certificate.target_has_focus_slack
        assert certificate.after.admissible_colors("v") == frozenset()
        assert certificate.after.committed_edges_valid
        assert dict(certificate.after.coloring) != dict(embedding.state.coloring)


def test_nonzero_dual_parameter_cannot_borrow_another_construction_zero() -> None:
    positive = focus_slack_embedding()
    persistent = persistent_embedding()
    positive_chart = dual_defect_parameterization(positive.state, "v")

    with pytest.raises(ValueError, match="share the same zero-point"):
        derive_dual_domain_parameters(positive_chart, persistent, SIGMA)

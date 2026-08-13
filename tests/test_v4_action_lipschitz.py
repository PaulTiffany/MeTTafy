from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    derive_dual_domain_parameters,
)
from mettafy.plane_parameterization import (
    COLOR_TO_V4,
    NONZERO_MODES,
    ZERO,
    color_difference,
    v4_add,
)
from mettafy.v4_action_lipschitz import (
    apply_palette_choice,
    certify_dual_domain_binary_choice,
    changed_partner,
    palette_choice_is_lipschitz_one,
)
from mettafy.zero_point_correspondence import dual_defect_parameterization

BOUNDARY = ("a", "b", "c", "d", "e")
SINGLETON_MODES = ((0, 1), (1, 1))


def persistent_embedding() -> DegreeFiveTriangulatedEmbedding:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    state = ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )
    embedding = DegreeFiveTriangulatedEmbedding(
        state=state,
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
    assert embedding.valid
    return embedding


def test_each_palette_choice_is_exactly_lipschitz_one() -> None:
    for mode in NONZERO_MODES:
        assert palette_choice_is_lipschitz_one(mode, 0)
        assert palette_choice_is_lipschitz_one(mode, 1)
        for color in COLOR_TO_V4:
            assert apply_palette_choice(color, mode, 0) == color
            partner = changed_partner(color, mode)
            assert partner != color
            assert apply_palette_choice(partner, mode, 1) == color


def test_domain_action_is_pointwise_binary_and_edge_local() -> None:
    embedding = persistent_embedding()
    chart = dual_defect_parameterization(embedding.state, embedding.focus)

    certified = 0
    for mode in SINGLETON_MODES:
        for parameter in derive_dual_domain_parameters(chart, embedding, mode):
            certificate = certify_dual_domain_binary_choice(parameter)
            assert certificate.valid
            certified += 1

            assert certificate.choice_crossed_edges == frozenset(
                parameter.path.crossed_edges
            )
            assert {
                vertex
                for vertex in certificate.before.coloring
                if certificate.choice(vertex) == 1
            } == set(parameter.translated_vertices)

            for vertex in certificate.before.coloring:
                choice = certificate.choice(vertex)
                expected = apply_palette_choice(
                    certificate.before.coloring[vertex],
                    mode,
                    choice,
                )
                assert certificate.after.coloring[vertex] == expected
                # Repeating the same pointwise choice bit and mode returns the
                # original palette state because every nonzero V4 mode has order two.
                assert apply_palette_choice(expected, mode, choice) == (
                    certificate.before.coloring[vertex]
                )

            crossed = frozenset(parameter.path.crossed_edges)
            for vertex, neighbors in certificate.before.graph.items():
                if vertex not in certificate.before.coloring:
                    continue
                for neighbor in neighbors:
                    if neighbor not in certificate.before.coloring or vertex >= neighbor:
                        continue
                    before_mode = color_difference(
                        certificate.before.coloring[vertex],
                        certificate.before.coloring[neighbor],
                    )
                    after_mode = color_difference(
                        certificate.after.coloring[vertex],
                        certificate.after.coloring[neighbor],
                    )
                    choices_differ = (
                        certificate.choice(vertex) ^ certificate.choice(neighbor)
                    )
                    if choices_differ:
                        assert (vertex, neighbor) in crossed or (neighbor, vertex) in crossed
                        assert before_mode != mode
                        assert after_mode == v4_add(before_mode, mode)
                        assert after_mode != ZERO
                    else:
                        assert after_mode == before_mode

    assert certified == 4

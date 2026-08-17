from __future__ import annotations

from mettafy.nilpotent_traversal import (
    BASIS4,
    ZERO4,
    DesaturationCertificate,
    ExternalEdgeConstraint,
    admissible_colors,
    cyclic_terminal_states,
    direct_extension_count,
    nilpotent_power,
    saturated_boundary_dependency,
)


def test_nilpotency_index_is_exactly_four() -> None:
    seed = BASIS4[0]
    assert nilpotent_power(seed, 0) != ZERO4
    assert nilpotent_power(seed, 1) != ZERO4
    assert nilpotent_power(seed, 2) != ZERO4
    assert nilpotent_power(seed, 3) != ZERO4
    assert nilpotent_power(seed, 4) == ZERO4
    assert nilpotent_power(seed, 5) == ZERO4


def test_four_nonzero_cyclic_states_precede_annihilation() -> None:
    states = cyclic_terminal_states()
    assert len(states) == 4
    assert len(set(states)) == 4
    assert all(state != ZERO4 for state in states)
    assert nilpotent_power(BASIS4[0], 4) == ZERO4


def test_admissible_color_space_is_exact_complement() -> None:
    assert admissible_colors(frozenset()) == frozenset({0, 1, 2, 3})
    assert admissible_colors(frozenset({0})) == frozenset({1, 2, 3})
    assert admissible_colors(frozenset({0, 1})) == frozenset({2, 3})
    assert admissible_colors(frozenset({0, 1, 2})) == frozenset({3})
    assert admissible_colors(frozenset({0, 1, 2, 3})) == frozenset()


def test_saturated_c5_has_unique_nonadjacent_repeated_color_dependency() -> None:
    word = (0, 1, 0, 2, 3)
    dependency = saturated_boundary_dependency(word)
    assert dependency.repeated_color == 0
    assert {dependency.left_index, dependency.right_index} == {0, 2}
    assert dependency.repeated_positions_are_nonadjacent
    assert dependency.kernel_vector == (1, 0, -1, 0, 0)
    assert direct_extension_count(word) == 0


def test_three_color_c5_reopens_exactly_one_terminal_choice() -> None:
    word = (0, 1, 0, 1, 2)
    assert direct_extension_count(word) == 1
    assert admissible_colors(frozenset(word)) == frozenset({3})


def test_nilpotent_dependency_does_not_authorize_invalid_graph_recoloring() -> None:
    before = (0, 1, 0, 2, 3)
    # This target desaturates the ring but collides with a fixed exterior
    # color-3 neighbor attached at boundary position 0.
    after = (3, 0, 2, 3, 2)
    certificate = DesaturationCertificate(
        before=before,
        after=after,
        external_edges=(ExternalEdgeConstraint(0, 3),),
    )
    assert certificate.source_is_saturated
    assert certificate.target_is_desaturated
    assert certificate.source_external_edges_valid
    assert not certificate.target_external_edges_valid
    assert not certificate.valid


def test_desaturation_requires_positive_ledger_certificate() -> None:
    before = (0, 1, 0, 2, 3)
    after = (0, 1, 0, 1, 2)
    certificate = DesaturationCertificate(before=before, after=after)
    assert certificate.valid
    assert direct_extension_count(after) == 1

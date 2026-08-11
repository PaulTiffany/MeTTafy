from __future__ import annotations

from fractions import Fraction

import pytest

from mettafy.four_color_contract import (
    BROWN,
    ContractExpansionWitness,
    FiniteDiffusionStep,
    classify_cycle5_boundary,
    cycle5_proper_assignments,
    decode_or_brown,
    edge_ledger,
    inherited_obligations_preserved,
    terminal_coloring_valid,
)


def test_exact_edge_ledger_and_terminal_palette() -> None:
    graph = {"a": ("b",), "b": ("a", "c"), "c": ("b",)}
    assert edge_ledger(graph) == frozenset({("a", "b"), ("b", "c")})
    assert terminal_coloring_valid(graph, {"a": 0, "b": 1, "c": 0})
    assert not terminal_coloring_valid(graph, {"a": 0, "b": 0, "c": 1})
    assert not terminal_coloring_valid(graph, {"a": 0, "b": 1, "c": BROWN})


def test_contract_expansion_preserves_inherited_and_new_obligations() -> None:
    before = {"a": ("b",), "b": ("a",)}
    after = {"a": ("b",), "b": ("a", "c"), "c": ("b",)}
    witness = ContractExpansionWitness(
        before_graph=before,
        after_graph=after,
        before_coloring={"a": 0, "b": 1},
        after_coloring={"a": 0, "b": 1, "c": 0},
        distortion=Fraction(1, 3),
        reserve=Fraction(1, 2),
    )
    assert inherited_obligations_preserved(before, after)
    assert witness.preserves_species


def test_contract_expansion_fails_closed_on_lost_edge_or_exhausted_budget() -> None:
    before = {"a": ("b",), "b": ("a",)}
    after = {"a": (), "b": ()}
    witness = ContractExpansionWitness(
        before_graph=before,
        after_graph=after,
        before_coloring={"a": 0, "b": 1},
        after_coloring={"a": 0, "b": 1},
        distortion=Fraction(2),
        reserve=Fraction(1),
    )
    assert not witness.preserves_species


def test_degree_five_boundary_exhaustion_is_complete() -> None:
    proper = cycle5_proper_assignments()
    classes = classify_cycle5_boundary()
    assert len(proper) == 240
    assert len(classes["immediate"]) == 120
    assert len(classes["saturated"]) == 120
    assert len(classes["immediate"]) + len(classes["saturated"]) == len(proper)
    assert all(len(set(boundary)) < 4 for boundary in classes["immediate"])
    assert all(len(set(boundary)) == 4 for boundary in classes["saturated"])


def test_finite_diffusion_preserves_mass_and_decoder_fails_closed_on_tie() -> None:
    half = Fraction(1, 2)
    zero = Fraction(0)
    identity_mix = FiniteDiffusionStep(
        (
            (half, half, zero, zero),
            (half, half, zero, zero),
            (zero, zero, half, half),
            (zero, zero, half, half),
        )
    )
    initial = (Fraction(1), zero, zero, zero)
    evolved = identity_mix.evolve(initial)
    assert sum(evolved, Fraction(0)) == 1
    assert evolved == (half, half, zero, zero)
    assert decode_or_brown(evolved) == BROWN


def test_finite_diffusion_rejects_non_stochastic_operator() -> None:
    with pytest.raises(ValueError, match="preserve total mass"):
        FiniteDiffusionStep(((Fraction(1), Fraction(1)), (Fraction(0), Fraction(1))))

from __future__ import annotations

import pytest

from mettafy.witness_expansion import WitnessExpansionState, apply_compelled_stage


def test_compelled_stage_preserves_and_strictly_enlarges_witness() -> None:
    before = WitnessExpansionState(
        witness_atoms=frozenset({"C5-boundary", "edge-ledger", "locked-pairing"}),
        stage_universe=frozenset({"cut-left", "cut-right"}),
    )

    after = apply_compelled_stage(
        before,
        "cut-left",
        frozenset({"dual-path:left", "cut-ledger:left"}),
    )

    assert before.witness_atoms < after.witness_atoms
    assert after.stage_history == ("cut-left",)
    assert after.stage_rank == before.stage_rank - 1
    assert after.status == "continuable"


def test_compelled_stage_rejects_reversible_replay() -> None:
    before = WitnessExpansionState(
        witness_atoms=frozenset({"locked-boundary"}),
        stage_universe=frozenset({"same-cut"}),
    )
    after = apply_compelled_stage(
        before,
        "same-cut",
        frozenset({"same-cut-certificate"}),
    )

    with pytest.raises(ValueError, match="already been consumed"):
        apply_compelled_stage(
            after,
            "same-cut",
            frozenset({"attempted-inverse"}),
        )


def test_compelled_stage_requires_new_witness_information() -> None:
    before = WitnessExpansionState(
        witness_atoms=frozenset({"path:p"}),
        stage_universe=frozenset({"p"}),
    )

    with pytest.raises(ValueError, match="strictly enlarge"):
        apply_compelled_stage(before, "p", frozenset({"path:p"}))


def test_finite_stage_exhaustion_is_not_theorem_closure() -> None:
    before = WitnessExpansionState(
        witness_atoms=frozenset({"locked-boundary"}),
        stage_universe=frozenset({"p"}),
    )
    after = apply_compelled_stage(
        before,
        "p",
        frozenset({"path:p"}),
    )

    assert after.stage_rank == 0
    assert after.status == "exhausted"
    # Exhaustion deliberately says nothing about whether the center opened.
    assert "center-open" not in after.witness_atoms


def test_stage_history_must_be_unique_and_declared() -> None:
    with pytest.raises(ValueError, match="cannot be consumed twice"):
        WitnessExpansionState(
            witness_atoms=frozenset(),
            stage_universe=frozenset({"p"}),
            stage_history=("p", "p"),
        )

    with pytest.raises(ValueError, match="undeclared stage"):
        WitnessExpansionState(
            witness_atoms=frozenset(),
            stage_universe=frozenset({"p"}),
            stage_history=("q",),
        )

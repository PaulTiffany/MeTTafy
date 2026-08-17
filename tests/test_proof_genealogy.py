from __future__ import annotations

from pathlib import Path

from mettafy.proof_genealogy import four_color_proof_genealogy


def test_genealogy_preserves_frozen_ground_results() -> None:
    genealogy = four_color_proof_genealogy()

    genealogy.assert_structurally_sound()
    assert genealogy.falsified_claims("H0") == ("C0",)
    assert genealogy.supported_claims("H0") == ("C1",)


def test_green_successor_candidate_does_not_erase_c0() -> None:
    genealogy = four_color_proof_genealogy()
    candidates = genealogy.successor_candidates("C0")

    assert len(candidates) == 1
    assert candidates[0].id == "H1-C0-Degree4Kempe"
    assert candidates[0].status == "mechanically-passed"
    assert genealogy.unresolved_claims() == ("C0",)


def test_genealogy_projection_does_not_promote_candidate_as_coverage() -> None:
    projection = four_color_proof_genealogy().to_metta()

    assert "(Finding F-C0-Degree4MissingColor H0 C0 Falsified)" in projection
    assert "(Finding F-C1-ExhaustiveNormalForm H0 C1 Supported)" in projection
    assert "(SuccessorCandidate H1-C0-Degree4Kempe H0 C0 MechanicallyPassed)" in projection
    assert "(Covers H1-C0-Degree4Kempe C0)" not in projection
    assert "(Supersedes H1-C0-Degree4Kempe H0)" not in projection


def test_genealogy_metta_projection_is_exact() -> None:
    genealogy = four_color_proof_genealogy()
    path = Path("exemplars/four_color/proof_genealogy.metta")

    assert path.read_text(encoding="utf-8") == genealogy.to_metta()

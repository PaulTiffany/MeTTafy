from __future__ import annotations

from pathlib import Path

from mettafy.engineering_targets import four_color_engineering_index, semantic_signature


def test_flat_python_exemplars_are_pinned_and_provenanced() -> None:
    index = four_color_engineering_index()

    assert index.provenance_errors() == ()
    assert {exemplar.repository for exemplar in index.exemplars} == {
        "PaulTiffany/Come",
        "PaulTiffany/notebook_compiler",
    }


def test_c5_fuzzy_search_finds_present_state_separation() -> None:
    index = four_color_engineering_index()

    matches = index.rank("N-C5-PresentStateOnly")

    assert matches[0].exemplar == "X-NB-ControlBoardTemporalLocality"
    assert matches[0].score == 1.0
    assert matches[0].concepts == frozenset({"temporal-locality"})


def test_c6_fuzzy_search_recovers_three_old_python_patterns() -> None:
    index = four_color_engineering_index()

    matches = index.rank("N-C6-FreshShapeProgress")

    assert {match.exemplar for match in matches} == {
        "X-COME-DerivedOnly",
        "X-NB-DeterminismIdentity",
        "X-NB-FrozenArtifactGraph",
    }
    assert all(match.score == 0.4 for match in matches)
    assert {match.exemplar: match.concepts for match in matches} == {
        "X-COME-DerivedOnly": frozenset({"novelty", "replay"}),
        "X-NB-DeterminismIdentity": frozenset({"identity", "replay"}),
        "X-NB-FrozenArtifactGraph": frozenset({"identity", "persistence"}),
    }


def test_c6_search_keeps_unimplemented_emergent_refinement_visible() -> None:
    index = four_color_engineering_index()

    assert index.concept_voids() == {
        "N-C6-FreshShapeProgress": ("strict-refinement",),
    }


def test_c7_fuzzy_search_finds_finite_ordered_verifier() -> None:
    index = four_color_engineering_index()

    matches = index.rank("N-C7-FiniteClosure")

    assert matches[0].exemplar == "X-NB-OrderedVerifier"
    assert matches[0].score == 1.0
    assert matches[0].concepts == frozenset({"closure", "finite-order"})


def test_semantic_aliases_bridge_math_and_engineering_vocabulary() -> None:
    math = semantic_signature("reversible replay must not be fresh; retain identity")
    engineering = semantic_signature(
        "Input echo is not Derived; immutable SHA-256 artifacts are retained"
    )

    assert math & engineering == frozenset({"identity", "novelty", "persistence", "replay"})


def test_growth_of_complexity_maps_to_strict_emergent_refinement() -> None:
    signature = semantic_signature(
        "growth of complexity through emergence must strictly refine the retained state"
    )

    assert "strict-refinement" in signature


def test_metta_projection_is_exact_and_never_claims_witness_coverage() -> None:
    index = four_color_engineering_index()
    root = Path(__file__).resolve().parents[1]
    committed = (
        root / "exemplars" / "four_color" / "engineering_targets.metta"
    ).read_text(encoding="utf-8")
    relations = "\n".join(
        line
        for line in committed.splitlines()
        if line and not line.lstrip().startswith(";")
    )

    assert committed == index.to_metta()
    assert "(EngineeringMatch " in relations
    assert "(Covers " not in relations
    assert "(Witness " not in relations

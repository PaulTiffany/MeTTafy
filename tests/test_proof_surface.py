from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from mettafy.proof_surface import four_color_ordered_surface


def test_ordered_surface_is_structurally_sound_and_frozen() -> None:
    surface = four_color_ordered_surface()

    surface.assert_structurally_sound()
    assert surface.frozen_commit == "7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b"
    assert surface.frozen_proof == "docs/four-color-ordered-construction-proof.md"
    assert surface.bare_claims() == ()
    assert surface.dependency_cycles() == ()
    assert surface.reference_errors() == ()


def test_surface_exposes_current_mechanical_coverage_voids() -> None:
    surface = four_color_ordered_surface()

    assert surface.unwitnessed_claims() == ("C0", "C1", "C6")
    assert surface.unmutated_claims() == ()
    assert surface.unexecuted_mutations() == (
        "M0-DropMinimality",
        "M1-BreakBoundaryNormalForm",
        "M2-AllowPlanarCrossing",
        "M3-DirtyFrontierTurn",
        "M4-BreakRepeatedPair",
        "M5-StoreFutureRoute",
        "M6-ReplayResolvedShape",
        "M7-AllowSaturatedExhaustion",
        "M8-CorruptRestoredEdge",
    )


def test_degree_five_extension_sees_the_entire_upstream_surface() -> None:
    surface = four_color_ordered_surface()

    assert surface.ancestors("C8") == frozenset(
        {"C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"}
    )


def test_surface_does_not_mask_missing_evidence_or_mutation_plans() -> None:
    surface = four_color_ordered_surface()

    without_shape_evidence = replace(
        surface,
        evidence=tuple(fiber for fiber in surface.evidence if fiber.claim != "C6"),
    )
    assert without_shape_evidence.bare_claims() == ("C6",)

    without_shape_mutation = replace(
        surface,
        mutations=tuple(mutation for mutation in surface.mutations if mutation.target != "C6"),
    )
    assert without_shape_mutation.unmutated_claims() == ("C6",)


def test_metta_projection_is_exactly_the_typed_surface() -> None:
    surface = four_color_ordered_surface()
    path = Path("exemplars/four_color/proof_surface.metta")

    assert path.read_text(encoding="utf-8") == surface.to_metta()

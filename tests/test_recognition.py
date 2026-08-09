"""Tests for the Issue #32 recognition seam."""

from __future__ import annotations

from mettafy.exemplars import exemplar_strategy_targets
from mettafy.recognition import evaluate_against_held_out, recognize_from_structural
from mettafy.structural import extract_structural_evidence

# Minimal high-level sources (same pinned text used by structural tests).
FOURCOLOR_V = r'''
Theorem four_color_finite m : finite_simple_map m -> colorable_with 4 m.
Proof.
intros fin_m.
pose proof (discretize.discretize_to_hypermap fin_m) as [G planarG colG].
exact (colG (combinatorial4ct.four_color_hypermap planarG)).
Qed.

Theorem four_color m : simple_map m -> colorable_with 4 m.
Proof. revert m; exact (finitize.compactness_extension four_color_finite). Qed.
'''

COMBINATORIAL4CT_V = r'''
Theorem four_color_hypermap G : planar_bridgeless G -> four_colorable G.
Proof.
move=> geoG; apply: cube_colorable.
pose n := #|cube G|.+1; move: geoGQ (leqnn n); rewrite {1}/n.
elim: {G}n (cube G) => // n IHn G geoG; rewrite ltnS leq_eqVlt.
case/predU1P=> [Dn | /IHn]; [rewrite -{n}Dn in IHn | exact].
have [// | noncolG] := decide_colorable G.
by have [] := @unavoidability the_reducibility G.
Qed.
'''

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"


def _evidence():
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    return extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)


def test_recognize_produces_strategies_or_abstentions():
    evidence = _evidence()
    result = recognize_from_structural(evidence)
    # At least one high-precision prediction or an explicit abstention list.
    assert result.strategies or result.abstentions
    for s in result.strategies:
        assert 0.0 <= s.confidence <= 1.0
        assert s.evidence, "every prediction must carry evidence"


def test_recognizer_does_not_see_held_out_labels():
    """Sanity: the recognizer API never receives the answer key."""
    evidence = _evidence()
    # Call with only structural evidence; no held-out dict is passed.
    result = recognize_from_structural(evidence)
    dumped = str(result.to_dict())
    for label in (
        "FiniteReduction",
        "Discretization",
        "Unavoidability",
        "Reducibility",
        "Discharging",
    ):
        assert label not in dumped


def test_post_hoc_evaluation_is_separate():
    evidence = _evidence()
    result = recognize_from_structural(evidence)

    # Minimal held-out target mimicking the manifest shape.
    held_out = {
        "high-level-finite": ["Discretization", "RepresentationChange", "ProofByTransport"],
        "finite-combinatorial-core": [
            "StructuralReduction",
            "Induction",
            "MinimalCounterexample",
            "DecisionProcedure",
            "Unavoidability",
            "Reducibility",
        ],
    }
    report = evaluate_against_held_out(result, held_out)
    assert report["evaluation_only"] is True
    assert "predicted_kinds" in report

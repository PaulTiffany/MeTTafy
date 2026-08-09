"""Mechanical tests for the Issue #32 Rocq structural membrane."""

from __future__ import annotations

import json

import pytest

from mettafy.structural import (
    EXTRACTOR_VERSION,
    ObservableFeature,
    UnitKind,
    blind_audit_map,
    blind_structural_view,
    extract_structural_evidence,
)

FOURCOLOR_V = r'''(* (c) Copyright 2006-2018 Microsoft Corporation and Inria.                  *)
(* Distributed under the terms of CeCILL-B.                                  *)
From fourcolor Require Import real realplane.
From fourcolor Require combinatorial4ct discretize finitize.

Theorem four_color_finite m : finite_simple_map m -> colorable_with 4 m.
Proof.
intros fin_m.
pose proof (discretize.discretize_to_hypermap fin_m) as [G planarG colG].
exact (colG (combinatorial4ct.four_color_hypermap planarG)).
Qed.

Theorem four_color m : simple_map m -> colorable_with 4 m.
Proof. revert m; exact (finitize.compactness_extension four_color_finite). Qed.
'''

COMBINATORIAL4CT_V = r'''From fourcolor Require Import unavoidability reducibility.
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


def _sources() -> dict[str, str]:
    return {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }


def test_extractor_produces_typed_units_and_provenance():
    evidence = extract_structural_evidence(
        _sources(), upstream_sha=UPSTREAM_SHA, mettafy_sha="test-sha"
    )
    assert len(evidence.units) == 3
    assert {unit.kind for unit in evidence.units} == {UnitKind.THEOREM}
    assert evidence.provenance.upstream_sha == UPSTREAM_SHA
    assert evidence.provenance.mettafy_sha == "test-sha"
    assert evidence.provenance.extractor_version == EXTRACTOR_VERSION
    assert set(evidence.provenance.input_hashes) == set(_sources())


def test_extraction_and_blind_projection_are_deterministic():
    first = extract_structural_evidence(_sources(), upstream_sha=UPSTREAM_SHA)
    second = extract_structural_evidence(_sources(), upstream_sha=UPSTREAM_SHA)
    assert first.to_dict() == second.to_dict()
    assert blind_structural_view(first).to_dict() == blind_structural_view(second).to_dict()


def test_blind_payload_contains_no_source_names_paths_references_or_answer_labels():
    evidence = extract_structural_evidence(_sources(), upstream_sha=UPSTREAM_SHA)
    dumped = json.dumps(blind_structural_view(evidence).to_dict(), sort_keys=True).lower()

    forbidden = (
        "fourcolor",
        "four_color",
        "combinatorial4ct",
        "discretize",
        "finitize",
        "compactness_extension",
        "unavoidability",
        "reducibility",
        "finite reduction",
        "finitereduction",
        "proofbytransport",
        "representationchange",
        "discharging",
        "theories/",
        ".v",
        UPSTREAM_SHA.lower(),
    )
    for token in forbidden:
        assert token not in dumped, f"blind payload leaked {token!r}"

    assert "input_hashes" not in dumped
    assert all(unit.source_token.startswith("source:") for unit in blind_structural_view(evidence).units)


def test_audit_join_recovers_original_names_only_outside_blind_payload():
    evidence = extract_structural_evidence(_sources(), upstream_sha=UPSTREAM_SHA)
    audit = blind_audit_map(evidence)
    names = {entry["original_name"] for entry in audit.values()}
    assert names == {"four_color_finite", "four_color", "four_color_hypermap"}
    assert set(audit) == {unit.local_id for unit in blind_structural_view(evidence).units}


def test_comments_cannot_manufacture_features_including_nested_comments():
    clean = r'''Theorem harmless x : x = x.
Proof. exact x. Qed.
'''
    poisoned = r'''Theorem harmless x : x = x.
Proof.
(* induction decide_colorable rewrite (* nested unavoidability *) apply: fake *)
exact x.
Qed.
'''
    clean_evidence = extract_structural_evidence(
        {"a.v": clean}, upstream_sha=UPSTREAM_SHA
    )
    poisoned_evidence = extract_structural_evidence(
        {"renamed-proof-role.v": poisoned}, upstream_sha=UPSTREAM_SHA
    )
    assert clean_evidence.units[0].features == poisoned_evidence.units[0].features
    assert ObservableFeature.INDUCTION not in poisoned_evidence.units[0].features
    assert ObservableFeature.DECISION_CALL not in poisoned_evidence.units[0].features
    assert ObservableFeature.REWRITE_TRANSPORT not in poisoned_evidence.units[0].features


def test_malformed_comment_fails_closed():
    with pytest.raises(ValueError, match="unterminated Rocq comment"):
        extract_structural_evidence(
            {"broken.v": "Theorem t : True. Proof. (* induction"},
            upstream_sha=UPSTREAM_SHA,
        )


def test_composition_requires_observed_dataflow_not_multiple_application_words():
    unrelated = r'''Theorem unrelated x : x = x.
Proof. apply identity. exact x. Qed.
'''
    composed = r'''Theorem composed x : x = x.
Proof.
pose proof (first x) as [w transport].
exact (transport (second w)).
Qed.
'''
    evidence = extract_structural_evidence(
        {"unrelated.v": unrelated, "composed.v": composed}, upstream_sha=UPSTREAM_SHA
    )
    by_name = {unit.original_name: set(unit.features) for unit in evidence.units}
    assert ObservableFeature.COMPOSITION not in by_name["unrelated"]
    assert ObservableFeature.COMPOSITION in by_name["composed"]


def test_high_level_fixture_exposes_only_mechanical_feature_vocabulary():
    evidence = extract_structural_evidence(_sources(), upstream_sha=UPSTREAM_SHA)
    features = {feature for unit in evidence.units for feature in unit.features}
    assert ObservableFeature.APPLICATION in features
    assert ObservableFeature.COMPOSITION in features
    assert ObservableFeature.INDUCTION in features
    assert ObservableFeature.DECISION_CALL in features

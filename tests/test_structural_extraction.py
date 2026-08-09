"""Tests for the Issue #32 structural evidence layer.

These tests use the exact high-level source of the pinned Four Color artifact
that is already public and short. They verify determinism, provenance retention,
absence of semantic labels inside the IR, and the blind projection contract.
"""

from __future__ import annotations

import json

from mettafy.structural import (
    EXTRACTOR_VERSION,
    ObservableFeature,
    UnitKind,
    blind_structural_view,
    extract_structural_evidence,
)

# Exact text of the two high-level files at the pinned commit
# (f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2). Kept inline so the test
# remains self-contained and does not require network or a local checkout.

FOURCOLOR_V = r'''(* (c) Copyright 2006-2018 Microsoft Corporation and Inria.                  *)
(* Distributed under the terms of CeCILL-B.                                  *)
From fourcolor Require Import real realplane.
From fourcolor Require combinatorial4ct discretize finitize.

(******************************************************************************)
(*   This files contains the proof of the high-level statement of the Four    *)
(* Color Theorem, whose statement uses only the elementary real topology      *)
(* defined in libraries real and realplane. The theorem is stated for an      *)
(* arbitrary model of the real line, which we show in separate libraries      *)
(* (dedekind and realcategorical) is equivalent to assuming the classical     *)
(* excluded middle axiom.                                                     *)
(*   We only import the real and realplane libraries, which do not introduce  *)
(* any extra-logical context, in particular no new notation, so that the      *)
(* interpretation of the text below is as transparent as possible.            *)
(*   Accordingly we use qualified names refer to the supporting result in the *)
(* finitize, discretize and combinatorial4ct libraries, and do not rely on    *)
(* the ssreflect extensions in the formulation of the final arguments.        *)
(******************************************************************************)

Section FourColorTheorem.

Variable Rmodel : Real.model.
Let R := Real.model_structure Rmodel.
Implicit Type m : map R.

Theorem four_color_finite m : finite_simple_map m -> colorable_with 4 m.
Proof.
intros fin_m.
pose proof (discretize.discretize_to_hypermap fin_m) as [G planarG colG].
exact (colG (combinatorial4ct.four_color_hypermap planarG)).
Qed.

Theorem four_color m : simple_map m -> colorable_with 4 m.
Proof. revert m; exact (finitize.compactness_extension four_color_finite). Qed.

End FourColorTheorem.
'''

COMBINATORIAL4CT_V = r'''(* (c) Copyright 2006-2018 Microsoft Corporation and Inria.                  *)
(* Distributed under the terms of CeCILL-B.                                  *)
From mathcomp Require Import ssreflect ssrfun ssrbool eqtype ssrnat seq choice.
From mathcomp Require Import fintype path fingraph.
From fourcolor Require Import hypermap geometry color coloring cube present.
From fourcolor Require Import unavoidability reducibility.
Set SsrOldRewriteGoalsOrder.

(******************************************************************************)
(*   The (constructive) proof of the Four Color Theorem for finite            *)
(* combinatorial hypermaps.                                                   *)
(******************************************************************************)

Set Implicit Arguments.
Unset Strict Implicit.
Unset Printing Implicit Defensive.

Theorem four_color_hypermap G : planar_bridgeless G -> four_colorable G.
Proof.
move=> geoG; apply: cube_colorable.
have{geoG} geoGQ: planar_bridgeless_plain_precubic (cube G).
  split; last exact/cubic_precubic/cubic_cube.
  split; last exact: plain_cube.
  by split; [rewrite planar_cube | rewrite bridgeless_cube]; apply: geoG.
pose n := #|cube G|.+1; move: geoGQ (leqnn n); rewrite {1}/n.
elim: {G}n (cube G) => // n IHn G geoG; rewrite ltnS leq_eqVlt.
case/predU1P=> [Dn | /IHn]; [rewrite -{n}Dn in IHn | exact].
have [// | noncolG] := decide_colorable G.
by have [] := @unavoidability the_reducibility G.
Qed.
'''

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"


def test_extractor_produces_units():
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    evidence = extract_structural_evidence(
        sources, upstream_sha=UPSTREAM_SHA, mettafy_sha="test"
    )
    assert len(evidence.units) >= 2
    kinds = {u.kind for u in evidence.units}
    assert UnitKind.THEOREM in kinds


def test_determinism():
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    e1 = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    e2 = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    assert e1.to_dict() == e2.to_dict()
    assert e1.provenance.extractor_version == EXTRACTOR_VERSION


def test_provenance_and_hashes():
    sources = {"theories/proof/fourcolor.v": FOURCOLOR_V}
    evidence = extract_structural_evidence(
        sources, upstream_sha=UPSTREAM_SHA, mettafy_sha="deadbeef"
    )
    assert evidence.provenance.upstream_sha == UPSTREAM_SHA
    assert evidence.provenance.mettafy_sha == "deadbeef"
    assert "theories/proof/fourcolor.v" in evidence.provenance.input_hashes


def test_no_semantic_strategy_labels_in_ir():
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    evidence = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    dumped = json.dumps(evidence.to_dict())
    # Held-out strategy vocabulary must not appear inside the structural IR.
    forbidden = [
        "FiniteReduction",
        "Discretization",
        "RepresentationChange",
        "ProofByTransport",
        "CompactnessExtension",
        "Unavoidability",
        "Reducibility",
        "Discharging",
        "MinimalCounterexample",
    ]
    for label in forbidden:
        assert label not in dumped, f"semantic label {label} leaked into IR"


def test_blind_view_strips_path_role():
    sources = {"theories/proof/fourcolor.v": FOURCOLOR_V}
    evidence = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    blind = blind_structural_view(evidence)
    for unit in blind["units"]:
        path = unit["span"]["path"]
        assert path.startswith("path:"), "path role leakage remains"
        assert "fourcolor" not in path and "proof" not in path


def test_audit_map_retains_original_names():
    sources = {"theories/proof/fourcolor.v": FOURCOLOR_V}
    evidence = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    audit = evidence.audit_map()
    names = {info["original_name"] for info in audit.values()}
    assert "four_color_finite" in names or "four_color" in names


def test_observable_features_present():
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    evidence = extract_structural_evidence(sources, upstream_sha=UPSTREAM_SHA)
    all_features = {f for u in evidence.units for f in u.features}
    # We expect at least composition / application on the high-level theorems
    # and induction / decision on the combinatorial core.
    assert ObservableFeature.APPLICATION in all_features or ObservableFeature.COMPOSITION in all_features

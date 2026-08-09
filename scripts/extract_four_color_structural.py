#!/usr/bin/env python3
"""Produce StructuralEvidence, recognition, and post-hoc evaluation artifacts
for the pinned high-level Four Color layers (Issue #32).

Usage (from repository root, after install or with PYTHONPATH=src):

    python scripts/extract_four_color_structural.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mettafy.recognition import (  # noqa: E402
    evaluate_against_held_out,
    recognize_from_structural,
)
from mettafy.structural import (  # noqa: E402
    EXTRACTOR_VERSION,
    ObservableFeature,
    blind_structural_view,
    extract_structural_evidence,
)

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

FOURCOLOR_V = r'''(* (c) Copyright 2006-2018 Microsoft Corporation and Inria.                  *)
(* Distributed under the terms of CeCILL-B.                                  *)
From fourcolor Require Import real realplane.
From fourcolor Require combinatorial4ct discretize finitize.

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

# Held-out targets (evaluation only; never fed to the recognizer).
HELD_OUT = {
    "high-level-finite": ["Discretization", "RepresentationChange", "ProofByTransport"],
    "high-level-general": ["CompactnessExtension", "FiniteReduction"],
    "finite-combinatorial-core": [
        "StructuralReduction",
        "Induction",
        "MinimalCounterexample",
        "DecisionProcedure",
        "Unavoidability",
        "Reducibility",
    ],
}


def main() -> int:
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    evidence = extract_structural_evidence(
        sources,
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="issue-32-working",
    )

    out_dir = ROOT / "artifacts" / "witnesses"
    out_dir.mkdir(parents=True, exist_ok=True)

    full_path = out_dir / "rocq-structural-fourcolor-highlevel.json"
    blind_path = out_dir / "rocq-structural-fourcolor-highlevel-blind.json"
    audit_path = out_dir / "rocq-structural-fourcolor-highlevel-audit.json"
    recog_path = out_dir / "rocq-recognition-fourcolor-highlevel.json"
    eval_path = out_dir / "rocq-evaluation-fourcolor-highlevel.json"

    generated_at = datetime.now(timezone.utc).isoformat()

    full = evidence.to_dict()
    full["generated_at"] = generated_at
    full["claim_boundary"] = (
        "Structural observations only. No semantic strategy labels are asserted. "
        "Rocq remains the sole authority for theorem validity."
    )

    observations = []
    for unit in evidence.units:
        feats = set(unit.features)
        if ObservableFeature.COMPOSITION in feats or ObservableFeature.APPLICATION in feats:
            observations.append(
                {
                    "local_id": unit.local_id,
                    "plain_language": (
                        "The body is a short composition of applications: "
                        "one step obtains a hypermap and a coloring transport, "
                        "another step applies a previously established combinatorial result."
                    ),
                    "mathematical": (
                        "Finite case reduces by discretization to a hypermap, "
                        "invokes the combinatorial four-color theorem, then transports "
                        "the coloring; the general case is a compactness extension of "
                        "the finite result."
                    ),
                    "features": [f.value for f in unit.features],
                    "confidence": "structural-high",
                    "status": "observed",
                }
            )
        if ObservableFeature.INDUCTION in feats:
            observations.append(
                {
                    "local_id": unit.local_id,
                    "plain_language": (
                        "An inductive argument on a size measure appears, "
                        "together with a decision procedure for colorability "
                        "and a reference to an unavoidability result."
                    ),
                    "mathematical": (
                        "Proof proceeds by induction on the cardinality of the "
                        "cubified hypermap; the base relies on a colorability "
                        "decision procedure and the unavoidability of a set of "
                        "reducible configurations."
                    ),
                    "features": [f.value for f in unit.features],
                    "confidence": "structural-high",
                    "status": "observed",
                }
            )

    full["structural_observations"] = observations

    # Recognition (blind with respect to held-out labels).
    recognition = recognize_from_structural(evidence)
    full["abstentions"] = recognition.abstentions

    with full_path.open("w", encoding="utf-8") as fh:
        json.dump(full, fh, indent=2, sort_keys=True)
        fh.write("\n")

    blind = blind_structural_view(evidence)
    blind["generated_at"] = generated_at
    with blind_path.open("w", encoding="utf-8") as fh:
        json.dump(blind, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with audit_path.open("w", encoding="utf-8") as fh:
        json.dump(evidence.audit_map(), fh, indent=2, sort_keys=True)
        fh.write("\n")

    recog_payload = recognition.to_dict()
    recog_payload["generated_at"] = generated_at
    recog_payload["extractor_version"] = EXTRACTOR_VERSION
    with recog_path.open("w", encoding="utf-8") as fh:
        json.dump(recog_payload, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # Post-hoc evaluation only.
    evaluation = evaluate_against_held_out(recognition, HELD_OUT)
    evaluation["generated_at"] = generated_at
    with eval_path.open("w", encoding="utf-8") as fh:
        json.dump(evaluation, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"Extractor version : {EXTRACTOR_VERSION}")
    print(f"Units extracted   : {len(evidence.units)}")
    print(f"Observations      : {len(observations)}")
    print(f"Strategies        : {len(recognition.strategies)}")
    print(f"Abstentions       : {len(recognition.abstentions)}")
    print(f"Full artifact     : {full_path}")
    print(f"Blind artifact    : {blind_path}")
    print(f"Audit map         : {audit_path}")
    print(f"Recognition       : {recog_path}")
    print(f"Evaluation        : {eval_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

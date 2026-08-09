#!/usr/bin/env python3
"""Produce the first Issue #32 StructuralEvidence artifact for the pinned
high-level Four Color layers.

Usage (from repository root, after install or with PYTHONPATH=src):

    python scripts/extract_four_color_structural.py

The script is deliberately self-contained: it embeds the exact source of
the two high-level files at the pinned commit so that the artifact can be
regenerated without a network fetch or a full Rocq checkout.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running from a source checkout without installation.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

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

    full = evidence.to_dict()
    full["generated_at"] = datetime.now(timezone.utc).isoformat()
    full["claim_boundary"] = (
        "Structural observations only. No semantic strategy labels are asserted. "
        "Rocq remains the sole authority for theorem validity."
    )

    # First evidence-backed structural observation (plain + mathematical form).
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
    full["abstentions"] = []  # none at this stage; later recognizers may abstain

    with full_path.open("w", encoding="utf-8") as fh:
        json.dump(full, fh, indent=2, sort_keys=True)
        fh.write("\n")

    blind = blind_structural_view(evidence)
    blind["generated_at"] = full["generated_at"]
    with blind_path.open("w", encoding="utf-8") as fh:
        json.dump(blind, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with audit_path.open("w", encoding="utf-8") as fh:
        json.dump(evidence.audit_map(), fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"Extractor version : {EXTRACTOR_VERSION}")
    print(f"Units extracted   : {len(evidence.units)}")
    print(f"Observations      : {len(observations)}")
    print(f"Full artifact     : {full_path}")
    print(f"Blind artifact    : {blind_path}")
    print(f"Audit map         : {audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

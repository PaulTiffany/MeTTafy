#!/usr/bin/env python3
"""Generate deterministic Issue #32 structural/recognition witness artifacts.

This bootstrap witness uses two exact, hash-verified source fixtures copied from
rocq-community/fourcolor at the declared upstream commit. It does not replay or
validate the Rocq proof; WIT-ROCQ-REPLAY owns that independent authority claim.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mettafy.recognition import (  # noqa: E402
    evaluate_against_held_out,
    recognize_from_structural,
)
from mettafy.structural import (  # noqa: E402
    EXTRACTOR_VERSION,
    blind_audit_map,
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

FIXTURE_HASHES = {
    "theories/proof/fourcolor.v": "61a0b38fa69b4030a10eec5e6a78ca6e1b36dbbf224c9a5c5b24b9f676aebb46",
    "theories/proof/combinatorial4ct.v": "bef1b755ab55bdd656750c292ed63cae3f2af56ea146328f9e9df9f448fd0177",
}

HELD_OUT_BY_ORIGINAL_NAME = {
    "four_color_finite": ["Discretization", "RepresentationChange", "ProofByTransport"],
    "four_color": ["CompactnessExtension", "FiniteReduction"],
    "four_color_hypermap": [
        "StructuralReduction",
        "Induction",
        "MinimalCounterexample",
        "DecisionProcedure",
        "Unavoidability",
        "Reducibility",
    ],
}


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _repository_sha() -> str:
    environment_sha = os.environ.get("GITHUB_SHA")
    if environment_sha:
        return environment_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("cannot establish MeTTafy repository SHA") from exc


def _verified_sources() -> dict[str, str]:
    sources = {
        "theories/proof/fourcolor.v": FOURCOLOR_V,
        "theories/proof/combinatorial4ct.v": COMBINATORIAL4CT_V,
    }
    observed = {path: _sha256_text(text) for path, text in sources.items()}
    if observed != FIXTURE_HASHES:
        raise RuntimeError(
            "pinned Four Color bootstrap fixture drifted; update only after "
            "independent comparison with the declared upstream commit"
        )
    return sources


def _held_out_by_blind_unit(audit: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for blind_id, entry in audit.items():
        original_name = entry.get("original_name")
        targets = HELD_OUT_BY_ORIGINAL_NAME.get(original_name)
        if targets is not None:
            result[blind_id] = targets
    return result


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    repository_sha = _repository_sha()
    sources = _verified_sources()
    evidence = extract_structural_evidence(
        sources,
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha=repository_sha,
    )
    blind = blind_structural_view(evidence)

    # The recognizer's type boundary accepts only this blind projection.
    recognition = recognize_from_structural(blind)

    # Audit metadata and answer-key labels are joined only after recognition.
    audit = blind_audit_map(evidence)
    held_out = _held_out_by_blind_unit(audit)
    evaluation = evaluate_against_held_out(recognition, held_out)

    blind_payload = blind.to_dict()
    blind_hash = _sha256_json(blind_payload)

    full_payload = {
        "schema_version": 1,
        "witness": "WIT-ROCQ-STRUCTURAL-BOOTSTRAP",
        "claim": (
            "The declared hash-verified Rocq source fixtures deterministically yield "
            "bounded structural features and a one-way classifier-safe projection."
        ),
        "non_claims": [
            "Four Color theorem validity",
            "completeness of Rocq structural extraction",
            "correctness of every semantic strategy interpretation",
            "equivalence between Rocq proof terms and emitted MeTTa",
            "identity with a live upstream checkout beyond the committed fixture hashes",
        ],
        "authority": "Rocq proof validity remains outside this witness",
        "repository_sha": repository_sha,
        "upstream_declared_sha": UPSTREAM_SHA,
        "extractor_version": EXTRACTOR_VERSION,
        "verified_fixture_hashes": FIXTURE_HASHES,
        "blind_projection_sha256": blind_hash,
        "structural_evidence": evidence.to_dict(),
    }

    recognition_payload = {
        "schema_version": 1,
        "repository_sha": repository_sha,
        "extractor_version": EXTRACTOR_VERSION,
        "blind_projection_sha256": blind_hash,
        **recognition.to_dict(),
    }
    evaluation_payload = {
        "schema_version": 1,
        "repository_sha": repository_sha,
        "blind_projection_sha256": blind_hash,
        **evaluation,
    }

    out_dir = ROOT / "artifacts" / "witnesses"
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "full": out_dir / "rocq-structural-fourcolor-highlevel.json",
        "blind": out_dir / "rocq-structural-fourcolor-highlevel-blind.json",
        "audit": out_dir / "rocq-structural-fourcolor-highlevel-audit.json",
        "recognition": out_dir / "rocq-recognition-fourcolor-highlevel.json",
        "evaluation": out_dir / "rocq-evaluation-fourcolor-highlevel.json",
    }

    _write_json(outputs["full"], full_payload)
    _write_json(outputs["blind"], blind_payload)
    _write_json(outputs["audit"], audit)
    _write_json(outputs["recognition"], recognition_payload)
    _write_json(outputs["evaluation"], evaluation_payload)

    print(f"Repository SHA      : {repository_sha}")
    print(f"Extractor version   : {EXTRACTOR_VERSION}")
    print(f"Raw units           : {len(evidence.units)}")
    print(f"Blind projection    : {blind_hash}")
    print(f"Strategies promoted : {len(recognition.strategies)}")
    print(f"Abstentions         : {len(recognition.abstentions)}")
    for label, path in outputs.items():
        print(f"{label:20}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

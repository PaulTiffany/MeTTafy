from __future__ import annotations

import json
from pathlib import Path

from mettafy.recognition import evaluate_against_held_out, recognize_from_structural
from mettafy.structural import (
    blind_audit_map,
    blind_structural_view,
    extract_structural_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "reduction-convergence.json"
UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

SOURCE = r'''
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
    raw = extract_structural_evidence(
        {"fixture.v": SOURCE},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="reduction-convergence-witness",
    )
    blind = blind_structural_view(raw)

    # Freeze the blind prediction before the audit map or held-out annotation is joined.
    recognition = recognize_from_structural(blind)
    frozen = recognition.to_dict()

    failures: list[str] = []
    promote_traces = [
        trace
        for trace in recognition.rule_traces
        if trace.rule_id == "recognition.reduction.counterexample-discharge.v1"
        and trace.decision == "promote"
    ]
    if len(promote_traces) != 1:
        failures.append("counterexample-discharge rule did not promote exactly once")

    predictions = list(recognition.predictions_by_unit.values())
    if predictions != [["Reduction"]]:
        failures.append(f"blind prediction drifted: {predictions!r}")

    dumped = json.dumps(frozen, sort_keys=True).lower()
    for forbidden in ("four_color_hypermap", "unavoidability", "the_reducibility", "reducibility"):
        if forbidden in dumped:
            failures.append(f"blind recognition leaked held-out/source token: {forbidden}")

    # Only now cross the audit boundary and join the held-out annotation.
    audit = blind_audit_map(raw)
    unit_id = next(
        blind_id
        for blind_id, info in audit.items()
        if info["original_name"] == "four_color_hypermap"
    )
    evaluation = evaluate_against_held_out(
        recognition,
        {unit_id: ["Reducibility"]},
    )
    matches = evaluation["matches"]
    if not any(
        item["unit"] == unit_id
        and item["predicted"] == "Reduction"
        and "Reducibility" in item["held_out_hit"]
        for item in matches
    ):
        failures.append("post-hoc held-out comparison did not record Reduction/Reducibility convergence")

    payload = {
        "witness": "WIT-REDUCTION-CONVERGENCE",
        "result": "pass" if not failures else "fail",
        "claim": (
            "A source-neutral rule using only induction, case split, decision call, and proof "
            "application independently promotes generic Reduction on the pinned high-level "
            "Four Color unit, and post-hoc held-out evaluation aligns that prediction with "
            "the annotated Reducibility strategy."
        ),
        "non_claims": [
            "the observed unit is itself a formal proof of reducibility",
            "the recognizer inspected theorem names or imported module names",
            "the current structural signature is sufficient for arbitrary reducibility proofs",
            "unavoidability or reducibility implementation details were interpreted",
        ],
        "blind_prediction": frozen,
        "post_hoc_evaluation": evaluation,
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("; ".join(failures))
    print(
        "Reduction convergence witness passed: blind generic Reduction prediction aligns "
        "post-hoc with held-out Reducibility on the pinned high-level Four Color unit."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

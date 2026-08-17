from __future__ import annotations

import json
from pathlib import Path

from mettafy.reducibility_gate import (
    TraversalCertificate,
    assess_admissible_traversal,
    extract_blind_discharge_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "reducibility-admissible-traversal.json"

PINNED_HIGH_LEVEL = r'''
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
    failures: list[str] = []
    evidence = extract_blind_discharge_evidence(PINNED_HIGH_LEVEL)

    pinned_trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=evidence,
    )
    if not evidence.complete:
        failures.append("pinned high-level proof does not expose the complete bounded discharge skeleton")
    if pinned_trace.decision != "certificate_required":
        failures.append("pinned Four Color candidate must fail closed without an independent certificate")

    good_certificate = TraversalCertificate.from_boundaries(
        boundary_before="boundary:fixture:v1",
        boundary_after="boundary:fixture:v1",
        measure_before=5,
        measure_after=4,
    )
    positive_trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=evidence,
        certificate=good_certificate,
    )
    if positive_trace.decision != "admissible_traversal":
        failures.append("independently certified boundary-preserving descent did not pass")

    bad_boundary = TraversalCertificate.from_boundaries(
        boundary_before="boundary:fixture:v1",
        boundary_after="boundary:fixture:v2",
        measure_before=5,
        measure_after=4,
    )
    bad_boundary_trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=evidence,
        certificate=bad_boundary,
    )
    if bad_boundary_trace.decision != "certificate_rejected":
        failures.append("boundary-changing traversal was not rejected")

    bad_descent = TraversalCertificate.from_boundaries(
        boundary_before="boundary:fixture:v1",
        boundary_after="boundary:fixture:v1",
        measure_before=5,
        measure_after=5,
    )
    bad_descent_trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=evidence,
        certificate=bad_descent,
    )
    if bad_descent_trace.decision != "certificate_rejected":
        failures.append("non-decreasing traversal was not rejected")

    payload = {
        "witness": "WIT-REDUCIBILITY-ADMISSIBLE-TRAVERSAL",
        "result": "pass" if not failures else "fail",
        "claim": (
            "A generic Reduction candidate can be upgraded to an admissible traversal only when "
            "a bounded contradiction/discharge skeleton is present and an independent certificate "
            "proves observable-boundary preservation plus strict decrease of a non-negative measure."
        ),
        "pinned_four_color_state": {
            "discharge_evidence": evidence.to_dict(),
            "gate_trace": pinned_trace.to_dict(),
            "interpretation": (
                "The pinned high-level Four Color unit is a traced reduction-family candidate, "
                "but remains certificate_required at this authority boundary."
            ),
        },
        "positive_control": {
            "certificate": good_certificate.to_dict(),
            "gate_trace": positive_trace.to_dict(),
        },
        "negative_controls": {
            "boundary_changed": {
                "certificate": bad_boundary.to_dict(),
                "gate_trace": bad_boundary_trace.to_dict(),
            },
            "no_strict_descent": {
                "certificate": bad_descent.to_dict(),
                "gate_trace": bad_descent_trace.to_dict(),
            },
        },
        "non_claims": [
            "the pinned high-level Four Color proof supplies a traversal certificate",
            "the referenced Four Color configuration is formally reducible at this layer",
            "the synthetic positive-control boundary or measure models the actual Four Color proof",
            "the gate replaces Rocq theorem validity or deeper reducibility checking",
        ],
        "next_obligation": (
            "Extract an independently checkable boundary object and well-founded obstruction measure "
            "from the deeper pinned reducibility layer, then feed that certificate into this gate."
        ),
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print("Reducibility admissible-traversal witness passed: fail-closed gate and controls verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

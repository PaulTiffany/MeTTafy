from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mettafy.reducibility import (
    ReductionState,
    evaluate_reducibility,
    strategy_from_certificate,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "traced-reducibility.json"


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def main() -> int:
    boundary = digest("external-boundary")
    before = ReductionState("state:before", boundary, 11)
    after = ReductionState("state:after", boundary, 7)

    trace, certificate, provenance = evaluate_reducibility(before, after)
    failures: list[str] = []

    if trace.decision != "certify":
        failures.append("valid boundary-preserving strict descent did not certify")
    if certificate is None:
        failures.append("valid reduction emitted no certificate")
        strategy = None
        authorization = None
    else:
        strategy, authorization = strategy_from_certificate(certificate)
        if strategy.kind.value != "Reduction":
            failures.append("certificate did not authorize Reduction Strategy IR")
        if authorization.source_id != certificate.certificate_id:
            failures.append("Strategy authorization did not point to certificate")

    changed_boundary, changed_certificate, _ = evaluate_reducibility(
        before,
        ReductionState("state:changed-boundary", digest("different-boundary"), 7),
    )
    if changed_boundary.decision != "reject" or changed_certificate is not None:
        failures.append("changed observable boundary did not fail closed")

    no_descent, no_descent_certificate, _ = evaluate_reducibility(
        before,
        ReductionState("state:no-descent", boundary, 11),
    )
    if no_descent.decision != "reject" or no_descent_certificate is not None:
        failures.append("nondecreasing obstruction did not fail closed")

    payload = {
        "witness": "WIT-TRACED-REDUCIBILITY",
        "result": "pass" if not failures else "fail",
        "claim": (
            "A Reduction Strategy may be authorized only by a certificate proving identical "
            "observable boundary hash and strict descent of an explicit obstruction measure."
        ),
        "non_claims": [
            "the current Rocq Four Color configurations have already been mapped to this contract",
            "the chosen obstruction measure is globally sufficient for Four Color",
            "unavoidability or the Four Color Theorem follows from this contract alone",
        ],
        "certified_case": {
            "trace": trace.__dict__,
            "certificate": certificate.__dict__ if certificate is not None else None,
            "strategy": strategy.to_dict() if strategy is not None else None,
            "authorization": authorization.__dict__ if authorization is not None else None,
            "provenance": [edge.__dict__ for edge in provenance],
        },
        "negative_cases": {
            "changed_boundary": changed_boundary.__dict__,
            "no_strict_descent": no_descent.__dict__,
        },
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print("Traced reducibility witness passed: boundary preservation + strict descent authorize Reduction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from pathlib import Path

from mettafy.reducibility import ReducibilityCertificate, certify_reducibility

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "reducibility-trace.json"


def make(
    certificate_id: str,
    before_boundary: tuple[str, ...],
    after_boundary: tuple[str, ...],
    before: int,
    after: int,
) -> ReducibilityCertificate:
    return ReducibilityCertificate(
        certificate_id=certificate_id,
        local_id="unit:00001",
        boundary_before=before_boundary,
        boundary_after=after_boundary,
        obstruction_before=before,
        obstruction_after=after,
    )


def main() -> int:
    valid = make("cert:valid", ("a", "b", "c"), ("a", "b", "c"), 11, 8)
    drift = make("cert:drift", ("a", "b", "c"), ("a", "b", "d"), 11, 8)
    flat = make("cert:flat", ("a", "b", "c"), ("a", "b", "c"), 11, 11)

    strategy, provenance = certify_reducibility(valid)
    drift_strategy, _ = certify_reducibility(drift)
    flat_strategy, _ = certify_reducibility(flat)

    failures: list[str] = []
    if strategy is None:
        failures.append("valid certificate did not promote")
    if drift_strategy is not None:
        failures.append("boundary drift promoted")
    if flat_strategy is not None:
        failures.append("non-descent promoted")
    if [edge.relation for edge in provenance] != [
        "authorized_by",
        "preserves_boundary",
        "strictly_decreases",
    ]:
        failures.append("provenance relations drifted")

    payload = {
        "witness": "WIT-REDUCIBILITY-TRACE",
        "result": "pass" if not failures else "fail",
        "claim": (
            "Reducibility promotion in this bounded certificate layer requires both exact "
            "boundary preservation and strict decrease of a non-negative obstruction measure."
        ),
        "non_claims": [
            "the current Rocq extractor already derives these certificates from arbitrary source",
            "unavoidability of reducible configurations",
            "the Four Color Theorem",
        ],
        "valid_case": {
            "boundary_preserved": valid.boundary_preserved,
            "strict_descent": valid.strict_descent,
            "promoted": strategy is not None,
        },
        "negative_cases": {
            "boundary_drift_promoted": drift_strategy is not None,
            "non_descent_promoted": flat_strategy is not None,
        },
        "provenance_relations": [edge.relation for edge in provenance],
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print("Reducibility witness passed: boundary preservation + strict descent required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

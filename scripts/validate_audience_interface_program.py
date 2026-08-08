#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "certification" / "audience-interface-v1.json"
ALLOWED_STRENGTHS = {"bounded", "behavioral", "artifact", "diagnostic", "formal"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"audience interface certification invalid: {message}")


def main() -> int:
    data: dict[str, Any] = json.loads(PROGRAM.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("unsupported schema_version")
    if data.get("grade") != "audience_green":
        fail("grade must be audience_green")
    if data.get("status") != "implemented":
        fail("audience program must remain implemented once promoted")

    witnesses = data.get("witnesses")
    required = data.get("requires")
    if not isinstance(witnesses, list) or len(witnesses) != 5:
        fail("exactly five audience witnesses are required in v1")
    if not isinstance(required, list) or len(required) != 5:
        fail("exactly five required witness ids are required")

    by_id: dict[str, dict[str, Any]] = {}
    for witness in witnesses:
        if not isinstance(witness, dict):
            fail("every witness must be an object")
        witness_id = witness.get("id")
        if not isinstance(witness_id, str) or not witness_id.startswith("WIT-"):
            fail(f"invalid witness id: {witness_id!r}")
        if witness_id in by_id:
            fail(f"duplicate witness id: {witness_id}")
        by_id[witness_id] = witness
        for field in ("audience", "command", "evidence", "metric", "claim"):
            if not isinstance(witness.get(field), str) or not witness[field].strip():
                fail(f"{witness_id}: missing {field}")
        if witness.get("strength") not in ALLOWED_STRENGTHS:
            fail(f"{witness_id}: invalid strength")
        non_claims = witness.get("non_claims")
        if not isinstance(non_claims, list) or not non_claims:
            fail(f"{witness_id}: non_claims are required")
        threshold = witness.get("threshold")
        if threshold != {"op": "eq", "value": 0}:
            fail(f"{witness_id}: v1 threshold must be zero failures")

        executable = witness["command"].split()[1]
        if not (ROOT / executable).is_file():
            fail(f"{witness_id}: executable witness is missing: {executable}")

    if set(required) != set(by_id):
        fail("requires must match the five declared witnesses exactly")

    composition = data.get("composition", {})
    if composition.get("all_required") is not True:
        fail("all five witnesses must be required")
    if composition.get("no_implicit_authority_promotion") is not True:
        fail("implicit authority promotion must be forbidden")
    if composition.get("base_product_green_is_not_implied") is not True:
        fail("audience green must not imply overall product green")

    print("Audience Interface Certification v1 valid: audience_green requires 5/5 witnesses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

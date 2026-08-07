#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "certification" / "witness-registry-v1.json"
ALLOWED_STATUS = {"implemented", "planned", "retired"}
ALLOWED_STRENGTH = {"diagnostic", "bounded", "behavioral", "artifact", "formal"}
REQUIRED = {"id", "name", "status", "kind", "strength", "claim", "non_claims", "authority", "replayable"}
VERSION = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


def fail(message: str) -> None:
    raise SystemExit(f"witness registry invalid: {message}")


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    version = data.get("version")
    if not isinstance(version, str):
        fail("registry version is required")
    match = VERSION.fullmatch(version)
    if match is None or match.group("major") != "1":
        fail(f"unsupported registry version {version!r}; expected semantic version 1.x.y")

    witnesses = data.get("witnesses")
    if not isinstance(witnesses, list) or not witnesses:
        fail("witnesses must be a non-empty list")

    seen: set[str] = set()
    for index, witness in enumerate(witnesses):
        if not isinstance(witness, dict):
            fail(f"witness {index} is not an object")
        missing = sorted(REQUIRED - witness.keys())
        if missing:
            fail(f"witness {index} missing fields: {', '.join(missing)}")
        wid = witness["id"]
        if not isinstance(wid, str) or not wid.startswith("WIT-"):
            fail(f"invalid witness id: {wid!r}")
        if wid in seen:
            fail(f"duplicate witness id: {wid}")
        seen.add(wid)
        if witness["status"] not in ALLOWED_STATUS:
            fail(f"{wid} has unsupported status {witness['status']!r}")
        if witness["strength"] not in ALLOWED_STRENGTH:
            fail(f"{wid} has unsupported strength {witness['strength']!r}")
        if not isinstance(witness["claim"], str) or not witness["claim"].strip():
            fail(f"{wid} has empty claim boundary")
        non_claims = witness["non_claims"]
        if not isinstance(non_claims, list) or not non_claims or not all(
            isinstance(item, str) and item.strip() for item in non_claims
        ):
            fail(f"{wid} must declare at least one non-claim")
        if not isinstance(witness["authority"], str) or not witness["authority"].strip():
            fail(f"{wid} has no authority source")
        if not isinstance(witness["replayable"], bool):
            fail(f"{wid} replayable must be boolean")

    composition = data.get("composition", {})
    if composition.get("no_implicit_promotion") is not True:
        fail("composition must forbid implicit authority promotion")
    if not composition.get("conflict_policy"):
        fail("composition conflict policy is required")

    print(f"Mechanical witness registry v{version} valid: {len(witnesses)} witnesses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

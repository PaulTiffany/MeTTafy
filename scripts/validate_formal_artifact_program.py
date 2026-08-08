#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "certification" / "formal-artifact-v1.json"
REPLAY = ROOT / "scripts" / "replay_four_color_proof.sh"
REGISTRY = ROOT / "certification" / "witness-registry-v1.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"formal artifact certification invalid: {message}")


def main() -> int:
    data: dict[str, Any] = json.loads(PROGRAM.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("unsupported schema_version")
    if data.get("grade") != "formal_artifact_green":
        fail("grade must be formal_artifact_green")
    if data.get("status") != "implemented":
        fail("formal artifact program must be implemented")
    if data.get("requires") != ["WIT-ROCQ-REPLAY"]:
        fail("formal_artifact_green must require exactly WIT-ROCQ-REPLAY")

    witness = data.get("witness")
    if not isinstance(witness, dict) or witness.get("id") != "WIT-ROCQ-REPLAY":
        fail("formal witness definition is missing")
    if witness.get("strength") != "formal":
        fail("WIT-ROCQ-REPLAY must retain formal strength")
    if witness.get("threshold") != {"op": "eq", "value": 0}:
        fail("formal replay threshold must be zero failures")
    non_claims = witness.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        fail("formal witness must preserve explicit non-claims")

    source = witness.get("source")
    toolchain = witness.get("toolchain")
    if not isinstance(source, dict):
        fail("formal witness source contract is missing")
    if not isinstance(toolchain, dict):
        fail("formal witness toolchain contract is missing")

    expected_source = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
    expected_image = (
        "coqorg/coq@sha256:e50d77c4c5a9aa0d76ae1b343d79c5f922da3a75054b79c5dc635895438e4674"
    )
    if source.get("commit") != expected_source:
        fail("pinned Four Color source commit drifted")
    if toolchain.get("container") != expected_image:
        fail("pinned checker container drifted")

    replay = REPLAY.read_text(encoding="utf-8")
    for required in (
        expected_source,
        expected_image,
        'EXPECTED_COQ="8.20.1"',
        'EXPECTED_OCAML="4.13.1"',
        'EXPECTED_OPAM="2.3.0"',
        '"certifying": True',
    ):
        if required not in replay:
            fail(f"replay script no longer carries required invariant: {required}")

    registry: dict[str, Any] = json.loads(REGISTRY.read_text(encoding="utf-8"))
    witness_entries = registry.get("witnesses")
    if not isinstance(witness_entries, list):
        fail("central witness registry has no witness list")
    entries = {
        item.get("id"): item
        for item in witness_entries
        if isinstance(item, dict)
    }
    registered = entries.get("WIT-ROCQ-REPLAY")
    if not isinstance(registered, dict):
        fail("WIT-ROCQ-REPLAY missing from witness registry")
    if registered.get("status") != "implemented":
        fail("WIT-ROCQ-REPLAY must be implemented in the central witness registry")
    if registered.get("strength") != "formal":
        fail("central registry weakened WIT-ROCQ-REPLAY strength")

    composition = data.get("composition")
    if not isinstance(composition, dict):
        fail("formal artifact composition policy is missing")
    if composition.get("no_implicit_authority_promotion") is not True:
        fail("implicit authority promotion must remain forbidden")
    if composition.get("semantic_claims_require_independent_witnesses") is not True:
        fail("formal replay must not close semantic claims")

    print("Formal Artifact Certification v1 valid: formal_artifact_green requires WIT-ROCQ-REPLAY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

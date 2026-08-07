from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses"
MANIFEST = ROOT / "exemplars" / "four_color" / "manifest.json"
METTA = ROOT / "exemplars" / "four_color" / "high_level_strategy.metta"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    metta = METTA.read_text(encoding="utf-8")
    failures: list[str] = []

    upstream = manifest.get("upstream", {})
    commit = upstream.get("commit")
    repository = upstream.get("repository")
    checker = upstream.get("checker")
    license_name = upstream.get("license")

    required_values = {
        "upstream commit": commit,
        "upstream repository": repository,
        "checker": checker,
        "license": license_name,
    }
    for name, value in required_values.items():
        if not isinstance(value, str) or not value:
            failures.append(f"missing {name}")

    if isinstance(commit, str) and f"(SourceCommit FourColorSprint01 {commit})" not in metta:
        failures.append("MeTTa target source commit does not match manifest")
    if "(CheckerAuthority FourColorSprint01 Rocq)" not in metta:
        failures.append("MeTTa target does not declare Rocq checker authority")
    if "(NotAuthority LearnedModel ProofValidity)" not in metta:
        failures.append("MeTTa target is missing learned-model non-authority boundary")

    proof_layers = manifest.get("proof_layers", [])
    if not isinstance(proof_layers, list) or not proof_layers:
        failures.append("manifest has no proof layers")
    else:
        ids: set[str] = set()
        for layer in proof_layers:
            layer_id = layer.get("id") if isinstance(layer, dict) else None
            if not isinstance(layer_id, str) or not layer_id:
                failures.append("proof layer missing id")
                continue
            if layer_id in ids:
                failures.append(f"duplicate proof layer id: {layer_id}")
            ids.add(layer_id)
            strategies = layer.get("strategies")
            if not isinstance(strategies, list) or not strategies:
                failures.append(f"proof layer {layer_id} has no held-out strategy annotations")

    paths = upstream.get("paths", [])
    if not isinstance(paths, list) or not paths:
        failures.append("manifest has no pinned proof paths")
    elif any(not isinstance(path, str) or not path.endswith(".v") for path in paths):
        failures.append("manifest proof paths are not all Rocq/Coq .v sources")

    evidence = {
        "witness": "WIT-REVIEWER-TRACEABILITY",
        "audience": "research reviewer and reproducibility auditor",
        "claim": "The Four Color teaching target is internally traceable to one pinned upstream repository commit and declares its checker/non-authority boundary consistently.",
        "non_claims": ["the semantic annotations are correct", "the upstream proof currently replays", "historical claims are complete"],
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "metta_target_sha256": hashlib.sha256(METTA.read_bytes()).hexdigest(),
        "proof_layer_count": len(proof_layers) if isinstance(proof_layers, list) else 0,
        "failures": failures,
        "result": "pass" if not failures else "fail",
    }
    (OUT / "reviewer-traceability.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise SystemExit("; ".join(failures))
    print("Research reviewer traceability witness passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

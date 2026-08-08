from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses"
FIXTURE = ROOT / "examples" / "four_color" / "solver.py"
EXPECTED_KEYS = {"id", "kind", "confidence", "evidence", "children"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "mettafy.cli", str(FIXTURE), "--format", "json"]
    first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=10)
    second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=10)
    bad = subprocess.run(
        [sys.executable, "-m", "mettafy.cli", str(FIXTURE), "--format", "invalid"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=10,
    )

    failures: list[str] = []
    if first.returncode != 0:
        failures.append(f"valid CLI invocation exited {first.returncode}")
    if first.stdout != second.stdout:
        failures.append("identical CLI invocations produced different JSON bytes")

    payload: object = None
    try:
        payload = json.loads(first.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"stdout is not valid JSON: {exc}")

    records = payload if isinstance(payload, list) else []
    if not records:
        failures.append("valid fixture returned no strategy records")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            failures.append(f"record {index} is not an object")
            continue
        if set(record) != EXPECTED_KEYS:
            failures.append(f"record {index} keys drifted: {sorted(record)}")
        confidence = record.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            failures.append(f"record {index} has invalid confidence")
        if not isinstance(record.get("evidence"), list):
            failures.append(f"record {index} evidence is not a list")

    if bad.returncode == 0:
        failures.append("invalid format unexpectedly succeeded")
    if "Traceback" in bad.stderr:
        failures.append("argparse contract failure leaked a Python traceback")

    evidence = {
        "witness": "WIT-DOWNSTREAM-CONTRACT",
        "audience": "downstream software integrator",
        "claim": "The installed Python CLI exposes deterministic JSON and bounded argument-error semantics for the certified fixture.",
        "non_claims": ["API stability outside the declared JSON surface", "semantic correctness of recovered strategies"],
        "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        "record_count": len(records),
        "deterministic_stdout": first.stdout == second.stdout,
        "invalid_argument_exit": bad.returncode,
        "failures": failures,
        "result": "pass" if not failures else "fail",
    }
    (OUT / "downstream-integrator-contract.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise SystemExit("; ".join(failures))
    print(f"Downstream integrator witness passed with {len(records)} strategy records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

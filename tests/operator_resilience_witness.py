from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses"

CASES = [
    "def f(:\n    pass\n",
    "def f():\n    return (\n",
    "class X\n    pass\n",
    "if True print('x')\n",
    "def f():\n\t  return 1\n",
    "async def f(:\n    pass\n",
    "for x in:\n    pass\n",
    "try:\n    pass\n",
    "match x:\n    case:\n        pass\n",
    "def f():\n    return '\udcff'\n",
]


def run_case(index: int, source: str) -> tuple[bool, str]:
    script = (
        "from mettafy.analysis import analyze_source\n"
        f"source = {source!r}\n"
        "try:\n"
        "    analyze_source(source, filename='<adversarial>')\n"
        "except SyntaxError:\n"
        "    raise SystemExit(0)\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=2,
        )
    except subprocess.TimeoutExpired:
        return False, f"case {index}: timeout"
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "nonzero exit"
        return False, f"case {index}: {detail}"
    if len(result.stdout) + len(result.stderr) > 65536:
        return False, f"case {index}: diagnostic output exceeded 64 KiB"
    return True, ""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for i, case in enumerate(CASES):
        ok, failure = run_case(i, case)
        if not ok:
            failures.append(failure)

    evidence = {
        "witness": "WIT-OPERATOR-RESILIENCE",
        "audience": "security and production operator",
        "claim": "The certified malformed-source corpus terminates within two seconds per case and fails only through declared syntax rejection, without runaway diagnostic output.",
        "non_claims": ["memory safety of CPython", "resilience against arbitrary hostile inputs", "sandboxing of executable user code"],
        "case_count": len(CASES),
        "timeout_seconds_per_case": 2,
        "max_diagnostic_bytes": 65536,
        "failures": failures,
        "result": "pass" if not failures else "fail",
    }
    (OUT / "operator-resilience.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise SystemExit("; ".join(failures))
    print(f"Operator resilience witness passed across {len(CASES)} malformed inputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Isolated Hyperon execution driver for MeTTafy witness collection.

Adapted from the mutation-gated ``notebook_compiler.metta_driver`` witness rail.
The driver executes one MeTTa source form-by-form so query results, final
Atomspace contents, and public state deltas all come from the same witnessed
sequence.

This process boundary is fault containment, not a security sandbox.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

_EVAL_MARKER = "!"


def _engine_version() -> str:
    try:
        return version("hyperon")
    except PackageNotFoundError:
        return "unknown"


def introspect(source: str) -> dict[str, Any]:
    """Execute *source* form-by-form and return three mutually consistent channels."""
    record: dict[str, Any] = {
        "ok": False,
        "engine": "hyperon",
        "engine_version": _engine_version(),
        "results": [],
        "atoms": [],
        "steps": [],
        "error": "",
    }
    try:
        from hyperon import MeTTa

        metta = MeTTa()
        space = metta.space()
        before = [str(existing) for existing in space.get_atoms()]
        results: list[list[str]] = []
        steps: list[dict[str, Any]] = []
        pending_eval = False

        for atom in metta.parse_all(source):
            rendered = str(atom)
            if rendered == _EVAL_MARKER:
                pending_eval = True
                continue

            if pending_eval:
                pending_eval = False
                reduced = [str(result) for result in metta.evaluate_atom(atom)]
                results.append(reduced)
            else:
                space.add_atom(atom)
                reduced = []

            after = [str(existing) for existing in space.get_atoms()]
            steps.append(
                {
                    "form": rendered,
                    "results": reduced,
                    "added": _extra(after, before),
                    "removed": _extra(before, after),
                }
            )
            before = after

        record["results"] = results
        record["atoms"] = [
            {"atom": str(atom), "metatype": type(atom).__name__}
            for atom in space.get_atoms()
        ]
        record["steps"] = steps
        record["ok"] = True
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"

    return record


def _extra(minuend: list[str], subtrahend: list[str]) -> list[str]:
    """Return an order-preserving, multiplicity-aware multiset difference."""
    remaining: Counter[str] = Counter(subtrahend)
    extra: list[str] = []
    for item in minuend:
        if remaining[item] > 0:
            remaining[item] -= 1
        else:
            extra.append(item)
    return extra


def main(argv: list[str]) -> None:
    if len(argv) != 3:
        raise SystemExit("usage: hyperon_driver.py <source.metta> <out.json>")

    source = Path(argv[1]).read_bytes().decode()
    Path(argv[2]).write_bytes(json.dumps(introspect(source), indent=2).encode())


if __name__ == "__main__":
    main(sys.argv)

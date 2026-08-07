from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROGRAM = ROOT / "certification" / "program-v1.json"
ALLOWED_STATUSES = {"implemented", "planned"}
ALLOWED_OPS = {"eq", "gte", "lte", "set_eq"}


class ProgramError(ValueError):
    pass


def _thresholds(gate: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    threshold = gate.get("threshold")
    if isinstance(threshold, dict):
        result.append(threshold)
    metrics = gate.get("metrics")
    if isinstance(metrics, dict):
        for name, value in metrics.items():
            if not isinstance(value, dict):
                raise ProgramError(f"{gate['id']}: metric {name!r} has no threshold object")
            result.append(value)
    return result


def validate_program(program: dict[str, Any], *, root: Path = ROOT) -> dict[str, bool]:
    if program.get("schema_version") != 1:
        raise ProgramError("unsupported certification schema_version")
    if not isinstance(program.get("version"), str) or not program["version"]:
        raise ProgramError("program version is required")

    gates = program.get("gates")
    if not isinstance(gates, list) or not gates:
        raise ProgramError("program must define at least one gate")

    by_id: dict[str, dict[str, Any]] = {}
    for raw_gate in gates:
        if not isinstance(raw_gate, dict):
            raise ProgramError("every gate must be an object")
        gate_id = raw_gate.get("id")
        if not isinstance(gate_id, str) or not gate_id:
            raise ProgramError("every gate must have a non-empty id")
        if gate_id in by_id:
            raise ProgramError(f"duplicate gate id: {gate_id}")
        by_id[gate_id] = raw_gate

        status = raw_gate.get("status")
        if status not in ALLOWED_STATUSES:
            raise ProgramError(f"{gate_id}: invalid status {status!r}")
        if not isinstance(raw_gate.get("surface"), str):
            raise ProgramError(f"{gate_id}: surface is required")

        thresholds = _thresholds(raw_gate)
        if not thresholds:
            raise ProgramError(f"{gate_id}: at least one threshold is required")
        for threshold in thresholds:
            op = threshold.get("op")
            if op not in ALLOWED_OPS:
                raise ProgramError(f"{gate_id}: unsupported threshold operator {op!r}")
            if "value" not in threshold:
                raise ProgramError(f"{gate_id}: threshold value is required")

        benchmark = raw_gate.get("benchmark")
        if status == "implemented" and benchmark is not None:
            benchmark_path = root / str(benchmark)
            if not benchmark_path.is_file():
                raise ProgramError(
                    f"{gate_id}: implemented benchmark does not exist: {benchmark}"
                )

    grades = program.get("grades")
    if not isinstance(grades, dict) or not grades:
        raise ProgramError("program must define grades")

    readiness: dict[str, bool] = {}
    unresolved = set(grades)
    while unresolved:
        progressed = False
        for grade_name in sorted(unresolved):
            spec = grades[grade_name]
            if not isinstance(spec, dict):
                raise ProgramError(f"grade {grade_name}: specification must be an object")

            gate_ids = spec.get("requires", [])
            grade_ids = spec.get("requires_grades", [])
            if not isinstance(gate_ids, list) or not isinstance(grade_ids, list):
                raise ProgramError(f"grade {grade_name}: requirements must be lists")

            missing = [gate_id for gate_id in gate_ids if gate_id not in by_id]
            if missing:
                raise ProgramError(f"grade {grade_name}: unknown gates {missing}")
            unknown_grades = [name for name in grade_ids if name not in grades]
            if unknown_grades:
                raise ProgramError(f"grade {grade_name}: unknown grades {unknown_grades}")
            if any(name not in readiness for name in grade_ids):
                continue

            gates_ready = all(by_id[gate_id]["status"] == "implemented" for gate_id in gate_ids)
            grades_ready = all(readiness[name] for name in grade_ids)
            readiness[grade_name] = gates_ready and grades_ready
            unresolved.remove(grade_name)
            progressed = True
            break

        if not progressed:
            raise ProgramError("grade dependency cycle detected")

    required_fields = program.get("certificate_required_fields")
    if not isinstance(required_fields, list) or not required_fields:
        raise ProgramError("certificate_required_fields must be a non-empty list")
    if len(required_fields) != len(set(required_fields)):
        raise ProgramError("certificate_required_fields contains duplicates")

    return readiness


def load_program(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ProgramError("program root must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MeTTafy certification policy")
    parser.add_argument("program", nargs="?", type=Path, default=DEFAULT_PROGRAM)
    parser.add_argument("--status", action="store_true", help="print grade implementation readiness")
    args = parser.parse_args()

    program = load_program(args.program)
    readiness = validate_program(program)
    if args.status:
        print(json.dumps({"program_version": program["version"], "grade_ready": readiness}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

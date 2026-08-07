from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "certification" / "program-v1.json"
VALIDATOR = ROOT / "scripts" / "validate_certification_program.py"


def run_validator(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_program() -> dict:
    return json.loads(PROGRAM.read_text(encoding="utf-8"))


def write_program(tmp_path: Path, program: dict) -> Path:
    path = tmp_path / "program.json"
    path.write_text(json.dumps(program), encoding="utf-8")
    return path


def test_program_v1_validates_and_reports_only_engineering_ready() -> None:
    result = run_validator(PROGRAM, "--status")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["program_version"] == "1.0.0"
    assert payload["grade_ready"] == {
        "engineering_green": True,
        "exemplar_green": False,
        "product_green": False,
    }


def test_duplicate_gate_ids_are_rejected(tmp_path: Path) -> None:
    program = load_program()
    program["gates"].append(deepcopy(program["gates"][0]))
    result = run_validator(write_program(tmp_path, program))
    assert result.returncode != 0
    assert "duplicate gate id" in result.stderr


def test_planned_gate_cannot_make_grade_ready(tmp_path: Path) -> None:
    program = load_program()
    first_required = program["grades"]["engineering_green"]["requires"][0]
    gate = next(item for item in program["gates"] if item["id"] == first_required)
    gate["status"] = "planned"
    result = run_validator(write_program(tmp_path, program), "--status")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["grade_ready"]["engineering_green"] is False
    assert payload["grade_ready"]["product_green"] is False


def test_implemented_benchmark_must_exist(tmp_path: Path) -> None:
    program = load_program()
    gate = next(item for item in program["gates"] if item["id"] == "EPI-BLINDING")
    gate["status"] = "implemented"
    result = run_validator(write_program(tmp_path, program))
    assert result.returncode != 0
    assert "implemented benchmark does not exist" in result.stderr


def test_every_grade_reference_resolves(tmp_path: Path) -> None:
    program = load_program()
    program["grades"]["engineering_green"]["requires"].append("DOES-NOT-EXIST")
    result = run_validator(write_program(tmp_path, program))
    assert result.returncode != 0
    assert "unknown gates" in result.stderr


def test_every_gate_has_a_threshold(tmp_path: Path) -> None:
    program = load_program()
    gate = deepcopy(program["gates"][0])
    gate.pop("threshold", None)
    gate.pop("metrics", None)
    program["gates"][0] = gate
    result = run_validator(write_program(tmp_path, program))
    assert result.returncode != 0
    assert "at least one threshold is required" in result.stderr

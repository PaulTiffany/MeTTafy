from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"


def snapshot() -> dict[str, str]:
    return {
        str(path.relative_to(OUT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(OUT.rglob("*"))
        if path.is_file()
    }


def run_build() -> None:
    subprocess.run(
        [sys.executable, "scripts/build_pages.py"],
        cwd=ROOT,
        check=True,
    )


def test_pages_build_is_deterministic() -> None:
    run_build()
    first = snapshot()
    run_build()
    second = snapshot()

    assert first == second
    assert "index.html" in first
    assert "four-color.html" in first
    assert "provenance.html" in first
    assert "build-manifest.json" in first


def test_pages_build_contains_auditable_fallback() -> None:
    run_build()
    page = (OUT / "four-color.html").read_text(encoding="utf-8")

    assert "@mettascript/grapher@3.4.0" in page
    assert "Show raw MeTTa" in page
    assert "CheckerAuthority" in page

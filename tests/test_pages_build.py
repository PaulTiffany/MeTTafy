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


def test_pages_build_contains_reducible_pedagogical_demo() -> None:
    run_build()
    page = (OUT / "four-color.html").read_text(encoding="utf-8")
    demo = (OUT / "four-color-demo.metta").read_text(encoding="utf-8")

    assert "Press <strong>Play</strong>" in page
    assert "pedagogical toy" in page
    assert "(= (pipeline finite-map) (pipeline discretized-hypermap))" in demo
    assert "(pipeline finite-map)" in demo


def test_legacy_docs_urls_redirect_to_generated_pages() -> None:
    run_build()

    expected = {
        "docs/index.html": "../index.html",
        "docs/four-color.html": "../four-color.html",
        "docs/auditability.html": "../audit.html",
        "docs/provenance.html": "../provenance.html",
    }
    for relative, target in expected.items():
        redirect = (OUT / relative).read_text(encoding="utf-8")
        assert f"url={target}" in redirect
        assert f'href="{target}"' in redirect

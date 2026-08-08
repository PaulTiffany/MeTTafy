from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses"
BASE = "http://127.0.0.1:8000"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    focus_sequence: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"{BASE}/four-color.html", wait_until="networkidle")

        for _ in range(10):
            page.keyboard.press("Tab")
            snapshot = page.evaluate(
                """() => {
                  const el = document.activeElement;
                  if (!el) return '';
                  const label = el.getAttribute('aria-label') || el.textContent || '';
                  return `${el.tagName}:${label.trim().slice(0, 80)}`;
                }"""
            )
            focus_sequence.append(snapshot)

        meaningful = [item for item in focus_sequence if item and not item.startswith("BODY:")]
        if len(meaningful) < 5:
            failures.append(f"only {len(meaningful)} meaningful keyboard focus stops observed")
        if not any(item.startswith("A:") for item in meaningful):
            failures.append("keyboard traversal did not reach a link")
        if not any(item.startswith("SUMMARY:") or item.startswith("BUTTON:") for item in meaningful):
            failures.append("keyboard traversal did not reach an interactive lesson control")

        # WCAG 2.2 SC 1.4.10's vertical-content endpoint is 320 CSS pixels wide.
        # Testing a 320 CSS-pixel viewport is a bounded mechanical reflow witness.
        # Real browser zoom and assistive-technology behavior remain in the manual gate.
        page.set_viewport_size({"width": 320, "height": 800})
        page.reload(wait_until="networkidle")
        overflow = page.evaluate(
            """() => ({
              viewport: window.innerWidth,
              documentWidth: document.documentElement.scrollWidth,
              bodyWidth: document.body.scrollWidth,
            })"""
        )
        if overflow["documentWidth"] > overflow["viewport"] + 2:
            failures.append(
                f"320 CSS-pixel reflow overflow: document={overflow['documentWidth']} "
                f"viewport={overflow['viewport']}"
            )
        browser.close()

    evidence = {
        "witness": "WIT-HUMAN-OPERABILITY",
        "audience": "keyboard, low-vision, and human-audit user",
        "claim": (
            "The primary Four Color lesson exposes meaningful keyboard focus stops and remains "
            "horizontally contained at the WCAG 1.4.10 vertical-content endpoint of 320 CSS pixels."
        ),
        "non_claims": [
            "full WCAG 2.2 AA conformance",
            "real-browser zoom equivalence",
            "screen-reader usability",
            "all browser/device combinations",
        ],
        "focus_sequence": focus_sequence,
        "reflow_320_css_px": overflow,
        "failures": failures,
        "result": "pass" if not failures else "fail",
    }
    (OUT / "human-operability.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise SystemExit("; ".join(failures))
    print("Human operability witness passed: keyboard traversal and 320 CSS-pixel reflow verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

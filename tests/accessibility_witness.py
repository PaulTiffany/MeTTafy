from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://127.0.0.1:8000/"
PRIMARY_PAGES = ("index.html", "four-color.html", "audit.html", "provenance.html")
AXE_PATH = Path("_vendor/axe-core/axe.min.js")
OUT = Path("artifacts/witnesses/accessibility.json")
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]


def scan_page(page: Page, relative: str) -> dict:
    response = page.goto(urljoin(BASE_URL, relative), wait_until="networkidle")
    if response is None or not response.ok:
        raise AssertionError(
            f"accessibility witness could not load {relative}: "
            f"{None if response is None else response.status}"
        )

    page.add_script_tag(path=str(AXE_PATH))
    result = page.evaluate(
        """
        async (tags) => {
          if (!window.axe) throw new Error('axe-core did not load');
          const result = await window.axe.run(document, {
            runOnly: { type: 'tag', values: tags },
            resultTypes: ['violations', 'incomplete', 'passes', 'inapplicable']
          });
          return {
            url: location.href,
            testEngine: result.testEngine,
            testEnvironment: result.testEnvironment,
            testRunner: result.testRunner,
            violations: result.violations,
            incomplete: result.incomplete,
            passes: result.passes,
            inapplicable: result.inapplicable
          };
        }
        """,
        TAGS,
    )
    return result


def compact_node(node: dict) -> dict:
    return {
        "target": node["target"],
        "html": node["html"],
        "failureSummary": node.get("failureSummary"),
        "any": node.get("any", []),
        "all": node.get("all", []),
        "none": node.get("none", []),
    }


def main() -> int:
    if not AXE_PATH.is_file():
        raise SystemExit(
            "missing pinned axe-core artifact; run scripts/fetch_axe_core.sh first"
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        pages = [scan_page(page, relative) for relative in PRIMARY_PAGES]
        browser.close()

    violations = [
        {
            "page": item["url"],
            "id": violation["id"],
            "impact": violation.get("impact"),
            "help": violation["help"],
            "helpUrl": violation["helpUrl"],
            "tags": violation["tags"],
            "nodes": [compact_node(node) for node in violation["nodes"]],
        }
        for item in pages
        for violation in item["violations"]
    ]
    incomplete = [
        {
            "page": item["url"],
            "id": finding["id"],
            "impact": finding.get("impact"),
            "help": finding["help"],
            "helpUrl": finding["helpUrl"],
            "tags": finding["tags"],
            "node_count": len(finding["nodes"]),
            "nodes": [compact_node(node) for node in finding["nodes"]],
        }
        for item in pages
        for finding in item["incomplete"]
    ]

    payload = {
        "witness": "WIT-WCAG-AUTO",
        "engine": "axe-core",
        "engine_version": "4.12.1",
        "standard_scope": "mechanically detectable WCAG 2.0/2.1/2.2 Level A/AA rules",
        "tags": TAGS,
        "claim_boundary": (
            "Zero violations means axe-core found no automatically detectable violations "
            "within the configured rule tags. It is not full WCAG conformance."
        ),
        "pages": [
            {
                "url": item["url"],
                "violation_count": len(item["violations"]),
                "incomplete_count": len(item["incomplete"]),
                "pass_count": len(item["passes"]),
                "inapplicable_count": len(item["inapplicable"]),
            }
            for item in pages
        ],
        "violations": violations,
        "incomplete_manual_review": incomplete,
        "metrics": {
            "automated_violations": len(violations),
            "incomplete_manual_review_items": len(incomplete),
            "incomplete_manual_review_nodes": sum(
                finding["node_count"] for finding in incomplete
            ),
            "pages_scanned": len(pages),
        },
        "result": "pass" if not violations else "fail",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "Accessibility witness: "
        f"{len(violations)} automated violations; "
        f"{len(incomplete)} incomplete/manual-review findings "
        f"({payload['metrics']['incomplete_manual_review_nodes']} nodes) "
        f"across {len(pages)} pages."
    )
    if violations:
        for violation in violations:
            print(
                f"- {violation['page']}: {violation['id']} "
                f"({violation['impact']}): {violation['help']}"
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import sys
from urllib.parse import urljoin, urlparse

from playwright.sync_api import ConsoleMessage, Page, Request, sync_playwright

BASE_URL = "http://127.0.0.1:8000/"
PAGES = ("index.html", "four-color.html", "audit.html", "provenance.html")


def fail(message: str) -> None:
    raise AssertionError(message)


def attach_runtime_guards(page: Page) -> tuple[list[str], list[str], list[str]]:
    console_errors: list[str] = []
    page_errors: list[str] = []
    failed_requests: list[str] = []

    def on_console(message: ConsoleMessage) -> None:
        if message.type == "error":
            console_errors.append(message.text)

    def on_request_failed(request: Request) -> None:
        failed_requests.append(f"{request.method} {request.url}: {request.failure}")

    page.on("console", on_console)
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    page.on("requestfailed", on_request_failed)
    return console_errors, page_errors, failed_requests


def assert_internal_links(page: Page) -> None:
    hrefs = page.locator("a[href]").evaluate_all(
        "els => els.map(el => el.getAttribute('href')).filter(Boolean)"
    )
    origin = urlparse(BASE_URL)
    checked: set[str] = set()
    for href in hrefs:
        target = urljoin(page.url, href)
        parsed = urlparse(target)
        if parsed.scheme not in ("http", "https") or parsed.netloc != origin.netloc:
            continue
        clean = parsed._replace(fragment="").geturl()
        if clean in checked:
            continue
        checked.add(clean)
        response = page.request.get(clean)
        if not response.ok:
            fail(f"broken internal link from {page.url}: {clean} -> {response.status}")


def assert_grapher_product(page: Page) -> None:
    page.wait_for_function("customElements.get('metta-grapher') !== undefined")
    grapher = page.locator("metta-grapher")
    if grapher.count() != 2:
        fail(f"expected two MeTTaScript Grapher embeds, found {grapher.count()}")

    page.wait_for_function(
        """
        () => [...document.querySelectorAll('metta-grapher')].every(
          el => el.grapher !== null && el.shadowRoot?.querySelector('svg.mg-svg')
        )
        """
    )

    state = page.evaluate(
        """
        () => [...document.querySelectorAll('metta-grapher')].map(el => ({
          src: el.getAttribute('src'),
          hasGrapher: el.grapher !== null,
          hasSvg: Boolean(el.shadowRoot?.querySelector('svg.mg-svg'))
        }))
        """
    )
    if state[0]["src"] != "four-color.metta":
        fail(f"unexpected authoritative Grapher source: {state[0]['src']}")
    if state[1]["src"] != "four-color-demo.metta":
        fail(f"unexpected reduction Grapher source: {state[1]['src']}")
    if not all(item["hasGrapher"] and item["hasSvg"] for item in state):
        fail("MeTTaScript Grapher custom element mounted without a usable SVG canvas")

    trace = page.evaluate(
        """
        () => {
          const g = document.querySelectorAll('metta-grapher')[1].grapher;
          if (!g || typeof g.playTrace !== 'function' ||
              typeof g.traceForward !== 'function' || typeof g.traceInfo !== 'function') {
            return null;
          }
          g.playTrace();
          const before = g.traceInfo();
          if (!before || before.total < 2) return { before, after: null };
          g.traceForward();
          return { before, after: g.traceInfo() };
        }
        """
    )
    if trace is None:
        fail("reduction Grapher mounted without the supported trace API")
    before = trace["before"]
    after = trace["after"]
    if before is None or before["total"] < 2:
        fail(f"reduction demo did not produce a multi-state MeTTa trace: {before}")
    if after is None or after["index"] <= before["index"]:
        fail(f"Grapher trace did not advance: before={before}, after={after}")


def runtime_diagnostics(
    console_errors: list[str], page_errors: list[str], failed_requests: list[str]
) -> str:
    sections: list[str] = []
    if console_errors:
        sections.append("console errors:\n" + "\n".join(console_errors))
    if page_errors:
        sections.append("uncaught page errors:\n" + "\n".join(page_errors))
    if failed_requests:
        sections.append("failed requests:\n" + "\n".join(failed_requests))
    return "\n\n".join(sections)


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        console_errors, page_errors, failed_requests = attach_runtime_guards(page)

        try:
            for relative in PAGES:
                response = page.goto(urljoin(BASE_URL, relative), wait_until="networkidle")
                if response is None or not response.ok:
                    fail(
                        f"page failed: {relative} -> "
                        f"{None if response is None else response.status}"
                    )
                assert_internal_links(page)
                if relative == "four-color.html":
                    assert_grapher_product(page)

            response = page.goto(
                urljoin(BASE_URL, "docs/auditability.html"), wait_until="networkidle"
            )
            if response is None or not response.ok:
                fail("legacy auditability URL did not resolve")
            page.wait_for_url("**/audit.html")

            diagnostics = runtime_diagnostics(console_errors, page_errors, failed_requests)
            if diagnostics:
                fail("browser runtime was not clean:\n" + diagnostics)
        except Exception as exc:
            diagnostics = runtime_diagnostics(console_errors, page_errors, failed_requests)
            if diagnostics:
                print("Browser runtime diagnostics:\n" + diagnostics, file=sys.stderr)
            raise exc
        finally:
            browser.close()

    print("Browser product smoke passed: pages, links, Grapher mount, and MeTTa trace are usable.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"browser smoke failed: {exc}", file=sys.stderr)
        raise

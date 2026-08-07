#!/usr/bin/env python3
"""Build the MeTTafy teaching site from checked-in exemplar artifacts.

The core site uses only the Python standard library. When the Pages workflow has
checked out and built the pinned MeTTaScript source, its Grapher browser bundle
is copied into the site as the primary interactive MeTTa visualization.
"""

from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
SITE = ROOT / "site"
EXEMPLAR = ROOT / "exemplars" / "four_color"
MANIFEST_PATH = EXEMPLAR / "manifest.json"
METTA_PATH = EXEMPLAR / "high_level_strategy.metta"
AUTHORITATIVE_INPUTS = [MANIFEST_PATH, METTA_PATH]

METTASCRIPT_VERSION = "3.4.0"
METTASCRIPT_COMMIT = "abe13439196bccdb48b6636773a46ec9772a7aaf"
METTASCRIPT_ROOT = ROOT / "_vendor" / "MeTTaScript"
GRAPHHER_BUNDLE = METTASCRIPT_ROOT / "packages" / "grapher" / "dist" / "embed.js"
METTASCRIPT_LICENSE = METTASCRIPT_ROOT / "LICENSE"

FOUR_COLOR_DEMO = """(= (pipeline finite-map) (pipeline discretized-hypermap))
(= (pipeline discretized-hypermap) (pipeline combinatorial-core))
(= (pipeline combinatorial-core) (pipeline transported-coloring))
(= (pipeline transported-coloring) (pipeline compactness-extension))
(pipeline finite-map)
"""

STRATEGY_STEPS = [
    ("Finite map", "Start with a finite planar map"),
    ("Discretize", "Convert geometry into a combinatorial hypermap"),
    ("Combinatorial core", "Apply the finite Four Color machinery"),
    ("Transport back", "Carry the coloring back to the original map"),
    ("Compactness", "Extend the finite result to the general case"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page(title: str, body: str, *, current: str = "", scripts: str = "") -> str:
    def nav(label: str, href: str, key: str) -> str:
        active = ' aria-current="page" class="active"' if current == key else ""
        return f'<a href="{href}"{active}>{html.escape(label)}</a>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="MeTTafy: computational proof history taught through semantic decompilation into MeTTa.">
  <title>{html.escape(title)} · MeTTafy</title>
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="index.html">MeTTafy</a>
    <nav aria-label="Primary">
      {nav('Learn', 'index.html', 'learn')}
      {nav('Four Color', 'four-color.html', 'four-color')}
      {nav('Audit', 'audit.html', 'audit')}
      {nav('Provenance', 'provenance.html', 'provenance')}
    </nav>
  </header>
  <main>{body}</main>
  <footer>
    <p>Open-source teaching and research project. Human-auditable interpretation is the design target.</p>
    <p><a href="https://github.com/PaulTiffany/MeTTafy">Source on GitHub</a></p>
  </footer>
  {scripts}
</body>
</html>
"""


def redirect_page(target: str, label: str) -> str:
    target = html.escape(target, quote=True)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={target}"><meta name="robots" content="noindex"><title>Moved · MeTTafy</title></head><body><p>This page moved to <a href="{target}">{html.escape(label)}</a>.</p></body></html>"""


def build_index() -> str:
    body = """
<section class="hero">
  <p class="eyebrow">Computational proof, made inspectable</p>
  <h1>Learn MeTTa through the history of mathematics becoming executable.</h1>
  <p class="lede">MeTTafy recovers reusable reasoning strategies from programs and formal proofs, then represents those strategies in MeTTa. Each historical exemplar is both a teaching lesson and a machine-interpretability benchmark.</p>
  <div class="actions"><a class="button" href="four-color.html">Start Sprint 01: Four Color</a><a class="button secondary" href="audit.html">How to challenge MeTTafy</a></div>
</section>
<section class="cards" aria-label="Learning path">
  <article><span>1</span><h2>See the problem</h2><p>Begin with the mathematical intuition and historical stakes.</p></article>
  <article><span>2</span><h2>Find computation</h2><p>Identify where a proof changes representation, searches, reduces, checks, or transports.</p></article>
  <article><span>3</span><h2>MeTTafy it</h2><p>Expose those moves as an inspectable strategy graph rather than hiding them in control flow.</p></article>
  <article><span>4</span><h2>Challenge it</h2><p>Trace every semantic claim down to source evidence and an independent checker.</p></article>
</section>
<section class="callout"><h2>The rule</h2><blockquote>If an interpretation cannot be projected into a faithful human explanation and traced back to evidence, the interpretation is not finished.</blockquote></section>
"""
    return page("Learn", body, current="learn")


def strategy_player() -> str:
    parts: list[str] = []
    for i, (label, description) in enumerate(STRATEGY_STEPS):
        if i:
            parts.append('<span class="strategy-arrow" data-arrow aria-hidden="true">→</span>')
        parts.append(
            f'<div class="strategy-step" data-step data-label="{html.escape(label, quote=True)}" title="{html.escape(description, quote=True)}"><strong>{html.escape(label)}</strong><br><small>{html.escape(description)}</small></div>'
        )
    return "".join(parts)


def simple_step_view() -> str:
    return f"""
<details>
  <summary>Use the simple step view</summary>
  <p>This lightweight view is kept as an accessibility and resilience companion to the MeTTaScript visualization.</p>
  <div class="strategy-player" data-strategy-player>
    <div class="strategy-track">{strategy_player()}</div>
    <div class="player-controls" aria-label="Strategy animation controls">
      <button type="button" data-action="prev">Prev</button>
      <button type="button" class="primary" data-action="play" aria-pressed="false">Play</button>
      <button type="button" data-action="next">Next</button>
      <button type="button" data-action="reset">Reset</button>
    </div>
    <p class="player-status" data-status aria-live="polite"></p>
  </div>
</details>
"""


def build_four_color(manifest: dict, metta: str, *, grapher_available: bool) -> str:
    commit = html.escape(manifest["upstream"]["commit"])
    layer_html = "".join(
        '<article class="strategy-card"><h3>'
        + html.escape(layer["id"].replace("-", " ").title())
        + "</h3><p>"
        + " → ".join(f"<code>{html.escape(s)}</code>" for s in layer["strategies"])
        + "</p></article>"
        for layer in manifest["proof_layers"]
    )

    if grapher_available:
        visualization = f"""
<section>
  <h2>Explore it with MeTTaScript Grapher</h2>
  <p><a href="https://github.com/MesTTo/MeTTaScript">MesTTo's MeTTaScript</a> provides the Grapher used here. MeTTafy supplies the historical lesson and strategy artifact; Grapher supplies the interactive MeTTa graph and reduction interface. This site builds Grapher from MeTTaScript {METTASCRIPT_VERSION} at pinned commit <code>{METTASCRIPT_COMMIT[:12]}</code>.</p>
  <metta-grapher height="540px" src="four-color.metta"></metta-grapher>
  <details><summary>Show raw MeTTa</summary><pre><code>{html.escape(metta)}</code></pre></details>
</section>
<section>
  <h2>Watch a MeTTa reduction</h2>
  <p>The small program below is deliberately a <strong>pedagogical projection</strong> of the proof pipeline, not the Four Color proof. In Grapher, use its reduction controls to step through the rewrite.</p>
  <metta-grapher height="440px" src="four-color-demo.metta"></metta-grapher>
  <details><summary>Show the toy MeTTa rewrite program</summary><pre><code>{html.escape(FOUR_COLOR_DEMO)}</code></pre></details>
  {simple_step_view()}
</section>
"""
        scripts = '<script type="module" src="assets/vendor/mettascript-grapher/embed.js"></script>\n<script src="assets/strategy-player.js" defer></script>'
    else:
        visualization = f"""
<section>
  <h2>Explore the strategy</h2>
  <p>This local build does not include the upstream viewer bundle. The published Pages workflow builds MesTTo's Grapher from the pinned MeTTaScript source; the raw MeTTa and simple step view remain usable here.</p>
  <details open><summary>Show raw MeTTa</summary><pre><code>{html.escape(metta)}</code></pre></details>
  {simple_step_view()}
  <details><summary>Show the toy MeTTa rewrite program</summary><pre><code>{html.escape(FOUR_COLOR_DEMO)}</code></pre></details>
</section>
"""
        scripts = '<script src="assets/strategy-player.js" defer></script>'

    body = f"""
<section class="lesson-head">
  <p class="eyebrow">Sprint 01 · Four Color Theorem</p>
  <h1>One theorem, three generations of computational trust.</h1>
  <p class="lede">The Four Color story runs from a nineteenth-century conjecture, through a famous failed proof, into controversial computer-assisted checking, and finally into a machine-checked formal proof.</p>
</section>
<section>
  <h2>First: the move in plain English</h2>
  <div class="flow" role="img" aria-label="Finite map is discretized to a hypermap, solved there, transported back, then extended by compactness"><span>finite map</span><b>→</b><span>discretize</span><b>→</b><span>hypermap</span><b>→</b><span>solve</span><b>→</b><span>transport back</span><b>→</b><span>compactness</span></div>
  <p>This is the high-level architecture exposed by the maintained Rocq formalization. The point of MeTTafy is to make moves like these first-class and comparable across very different proofs.</p>
</section>
<section>
  <h2>What MeTTafy currently sees</h2>
  <div class="strategy-grid">{layer_html}</div>
  <p class="status"><strong>Status:</strong> these are held-out exemplar annotations derived from the pinned formal proof. Sprint 01 is not complete until MeTTafy can recover them from proof structure without theorem-name leakage.</p>
</section>
{visualization}
<section>
  <h2>Show me the source boundary</h2>
  <p>Canonical formal artifact: <a href="https://github.com/rocq-community/fourcolor/tree/{commit}"><code>rocq-community/fourcolor@{commit[:12]}</code></a>. MeTTafy does not vendor that proof wholesale.</p>
  <p><a href="provenance.html">Inspect exact hashes and authority boundaries →</a></p>
</section>
"""
    return page("Four Color", body, current="four-color", scripts=scripts)


def build_audit() -> str:
    body = """
<section class="lesson-head"><p class="eyebrow">Human auditability</p><h1>Four questions must survive every abstraction layer.</h1></section>
<section class="audit-grid">
  <article><h2>1. What do you think is happening?</h2><p>Give the semantic move in ordinary language before jargon.</p></article>
  <article><h2>2. Why do you think that?</h2><p>Name the structural evidence: calls, dependencies, proof phases, invariants, or transformations.</p></article>
  <article><h2>3. Show me.</h2><p>Link the claim to the exact pinned source artifact and machine-readable representation.</p></article>
  <article><h2>4. What could you be wrong about?</h2><p>Expose ambiguity, competing labels, lossy projection, unsupported structure, and model uncertainty.</p></article>
</section>
<section class="callout"><h2>Authority boundary</h2><p>Prediction may guide search; verification governs acceptance. Learned classification is evidence. The formal checker remains authority for theorem validity.</p></section>
"""
    return page("Auditability", body, current="audit")


def build_provenance(manifest: dict, hashes: dict[str, str], *, grapher_available: bool) -> str:
    rows = "".join(f"<tr><td><code>{html.escape(path)}</code></td><td><code>{value}</code></td></tr>" for path, value in hashes.items())
    upstream = manifest["upstream"]
    grapher = f"""
<section>
  <h2>Community visualization dependency</h2>
  <dl>
    <dt>Project</dt><dd><a href="https://github.com/MesTTo/MeTTaScript">MesTTo/MeTTaScript — Grapher</a></dd>
    <dt>Version</dt><dd>{METTASCRIPT_VERSION}</dd>
    <dt>Pinned source commit</dt><dd><code>{METTASCRIPT_COMMIT}</code></dd>
    <dt>License</dt><dd>MIT, Copyright © 2026 MesTTo</dd>
    <dt>Role</dt><dd>Interactive MeTTa visualization and reduction UI; MeTTafy does not claim this implementation as its own.</dd>
    <dt>Included in this build</dt><dd>{'yes' if grapher_available else 'no — local fallback build'}</dd>
  </dl>
</section>
"""
    body = f"""
<section class="lesson-head"><p class="eyebrow">Provenance</p><h1>What this page was built from.</h1><p class="lede">The site records cryptographic hashes of its authoritative local exemplar inputs so presentation can be checked against source.</p></section>
<section><table><thead><tr><th>Input</th><th>SHA-256</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Proof authority</h2><dl><dt>Formal proof repository</dt><dd><a href="{html.escape(upstream['repository'])}">{html.escape(upstream['repository'])}</a></dd><dt>Pinned commit</dt><dd><code>{html.escape(upstream['commit'])}</code></dd><dt>License</dt><dd>{html.escape(upstream['license'])}</dd><dt>Checker</dt><dd>{html.escape(upstream['checker'])}</dd></dl></section>
{grapher}
<section class="callout"><h2>What hashes do not prove</h2><p>A matching hash proves which bytes were used to build the lesson. It does not prove that MeTTafy's semantic interpretation is correct. That claim remains separately challengeable.</p></section>
"""
    return page("Provenance", body, current="provenance")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "assets").mkdir()
    (OUT / "docs").mkdir()

    grapher_available = GRAPHHER_BUNDLE.is_file() and METTASCRIPT_LICENSE.is_file()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    metta = METTA_PATH.read_text(encoding="utf-8")
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in AUTHORITATIVE_INPUTS}

    (OUT / "index.html").write_text(build_index(), encoding="utf-8")
    (OUT / "four-color.html").write_text(build_four_color(manifest, metta, grapher_available=grapher_available), encoding="utf-8")
    (OUT / "audit.html").write_text(build_audit(), encoding="utf-8")
    (OUT / "provenance.html").write_text(build_provenance(manifest, hashes, grapher_available=grapher_available), encoding="utf-8")

    aliases = {
        "docs/index.html": "../index.html",
        "docs/four-color.html": "../four-color.html",
        "docs/auditability.html": "../audit.html",
        "docs/audit.html": "../audit.html",
        "docs/provenance.html": "../provenance.html",
    }
    for alias, target in aliases.items():
        (OUT / alias).write_text(redirect_page(target, target), encoding="utf-8")

    shutil.copyfile(SITE / "site.css", OUT / "assets" / "site.css")
    shutil.copyfile(SITE / "strategy-player.js", OUT / "assets" / "strategy-player.js")
    shutil.copyfile(METTA_PATH, OUT / "four-color.metta")
    shutil.copyfile(MANIFEST_PATH, OUT / "four-color-manifest.json")
    (OUT / "four-color-demo.metta").write_text(FOUR_COLOR_DEMO, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    if grapher_available:
        vendor_out = OUT / "assets" / "vendor" / "mettascript-grapher"
        vendor_out.mkdir(parents=True)
        shutil.copyfile(GRAPHHER_BUNDLE, vendor_out / "embed.js")
        shutil.copyfile(METTASCRIPT_LICENSE, vendor_out / "LICENSE")

    build_manifest = {
        "builder": "scripts/build_pages.py",
        "authoritative_inputs": hashes,
        "derived_pedagogical_assets": {
            "four-color-demo.metta": "toy rewrite chain; not proof authority",
            "assets/strategy-player.js": "accessibility/resilience companion visualization",
        },
        "upstream_integrations": {
            "mettascript_grapher": {
                "version": METTASCRIPT_VERSION,
                "source_commit": METTASCRIPT_COMMIT,
                "license": "MIT",
                "copyright": "2026 MesTTo",
                "built_into_site": grapher_available,
            }
        },
    }
    (OUT / "build-manifest.json").write_text(json.dumps(build_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

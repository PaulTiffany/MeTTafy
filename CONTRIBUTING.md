# Contributing to MeTTafy

MeTTafy welcomes contributions from the MeTTa/Hyperon, program-analysis, compiler, theorem-proving, and neuro-symbolic communities.

## Ground rules

1. **Attribute generously.** If an idea or implementation is materially informed by upstream work, cite it in the code, documentation, or `ACKNOWLEDGMENTS.md` as appropriate.
2. **Do not copy ambiguously licensed code.** A public GitHub repository is not automatically reusable. Establish the applicable license first.
3. **Prefer interoperability to duplication.** Use dependencies, adapters, or submodules when an upstream project already owns the canonical implementation.
4. **Separate observations from inferences.** Structural program facts and semantic classifications should remain distinguishable in the IR.
5. **Carry provenance.** New semantic recognizers should identify the source evidence supporting their classifications.
6. **Test semantic claims.** When a transformation claims behavioral preservation, include differential, property-based, solver-backed, or otherwise appropriate verification.
7. **Unknown is acceptable.** A recognizer should abstain rather than confidently misclassify unfamiliar code.
8. **Keep changes reviewable.** Prefer focused pull requests over large mixed changes, especially while the Strategy IR is stabilizing.
9. **Treat published surfaces as products.** A supported CLI, package, Pages lesson, or integration must have an executable gate at the boundary users actually encounter.

## Contribution license

By submitting a contribution for inclusion in MeTTafy, you agree that your contribution may be distributed under the repository's MIT License. You must have the right to submit the material. If a contribution contains or derives from third-party material, identify it explicitly and preserve all required notices and license terms.

No contributor license agreement (CLA) is currently required.

## Pull-request workflow

For substantive changes:

1. open or reference an issue when the design space or intended behavior is non-obvious;
2. work on a focused branch;
3. include tests or explain why a test is not applicable;
4. document relevant prior art and third-party dependencies;
5. open a pull request and complete the repository checklist;
6. keep architecture or semantic decisions in the PR/issue record rather than only in private discussion;
7. require product-facing changes to pass the relevant release gates in `docs/product-hardening.md`.

Trivial typo and documentation fixes do not need a prior issue.

## Product gates

The canonical CI workflows are the release authority for supported engineering surfaces. Before opening a PR, run the locally available subset:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e '.[dev]'
ruff check .
mypy
pytest
python -m build
twine check --strict dist/*
```

Pages changes additionally pass the repository's real-browser product smoke in CI. That check builds the pinned MesTTo/MeTTaScript Grapher, serves the generated site, mounts the actual custom elements in Chromium, checks internal navigation and runtime errors, and exercises the Grapher reduction API.

Do not weaken a gate merely to make a PR green. If a gate is wrong, fix the gate and record why; if the product is wrong, fix the product.

## Adding a strategy recognizer

A new recognizer should document:

- the intended `StrategyKind`;
- structural evidence it requires;
- known false positives and false negatives;
- confidence semantics;
- at least one positive fixture;
- preferably at least one near-miss or negative fixture.

Recognizers should expose why a classification was made. A higher confidence value is not a substitute for inspectable evidence.

## Third-party integrations

Before adding a dependency, git submodule, derived component, or vendored source, update `ACKNOWLEDGMENTS.md` with the canonical upstream URL and applicable license. Preserve required notices in the form required by the upstream license.

Prefer, in order when technically appropriate:

1. a normal package/dependency on the canonical upstream release;
2. a small adapter around the upstream project;
3. a pinned git submodule when source-level integration is genuinely needed;
4. vendoring only with a documented reason and preserved upstream history/license information.

When source-building an upstream component for a published MeTTafy artifact, pin the exact upstream commit, honor its lockfile/toolchain, preserve its license, and record the integrity of the deployed bytes.

## Development

The project remains pre-alpha scientifically and at the public-API level. Production engineering controls do not imply that semantic classifiers are complete, that untrusted execution is sandboxed, or that a formal proof has been re-proved by MeTTafy.

See `docs/product-hardening.md` for the engineering contract and current hardening backlog.

## Community and security

Participation is governed by `CODE_OF_CONDUCT.md`. Security-sensitive reports should follow `SECURITY.md` rather than being posted publicly.

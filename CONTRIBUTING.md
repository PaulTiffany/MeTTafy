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

## Adding a strategy recognizer

A new recognizer should document:

- the intended `StrategyKind`;
- structural evidence it requires;
- known false positives and false negatives;
- confidence semantics;
- at least one positive fixture;
- preferably at least one near-miss or negative fixture.

## Third-party integrations

Before adding a dependency, git submodule, derived component, or vendored source, update `ACKNOWLEDGMENTS.md` with the canonical upstream URL and applicable license. Preserve required notices in the form required by the upstream license.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e '.[dev]'
pytest
```

The project is pre-alpha. Small, reviewable changes with explicit tests are preferred over large framework additions while the Strategy IR is stabilizing.

# Prior art and adjacent work

MeTTafy is deliberately scoped to complement existing open-source work.

## OpenCog Hyperon / MeTTa

Canonical upstream: https://github.com/trueagi-io/hyperon-experimental

Role relative to MeTTafy: target language and execution substrate. MeTTafy does not define MeTTa semantics and should defer to canonical Hyperon/MeTTa behavior when compatibility questions arise.

## MesTTo / MeTTaScript

Canonical upstream: https://github.com/MesTTo/MeTTaScript

Role relative to MeTTafy: adjacent runtime/tooling ecosystem. MeTTaScript already supplies a TypeScript MeTTa implementation, eDSL, debugging, graphing, and host-language interoperability. MeTTafy should integrate with these capabilities where useful rather than reimplement them.

## LogicMOO / metta-src-conversions

Canonical upstream: https://github.com/logicmoo/metta-src-conversions

Role relative to MeTTafy: direct conceptual prior art for translating conventional symbolic/AI programs into MeTTa. The important distinction for MeTTafy is the explicit intermediate step of *semantic strategy recovery and classification* before emission.

At bootstrap, a repository-wide license was not clearly identified, so this project is cited but not incorporated.

## Joern / Code Property Graphs

Canonical upstream: https://github.com/joernio/joern

Role relative to MeTTafy: possible future multi-language structural front end. A Code Property Graph can provide syntax, control-flow, and data-flow facts without making MeTTafy's Strategy IR depend on any one source language.

## Related research areas

MeTTafy overlaps with several established areas without being identical to any of them:

- decompilation and semantic decompilation;
- program synthesis and translation;
- abstract interpretation;
- program analysis and code property graphs;
- algorithm recognition;
- superoptimization;
- inductive program synthesis;
- neuro-symbolic program reasoning;
- verified compilation and translation validation.

The project's differentiating hypothesis is:

> A conventional program can be normalized into an explicit graph of computational strategies, and that graph can serve both as a human-inspectable semantic artifact and as the basis for executable MeTTa generation.

## Community posture

If an upstream project already solves a layer well, MeTTafy should prefer one of the following, in order:

1. consume it as a normal dependency;
2. write a narrow adapter;
3. pin it as a git submodule when source-level co-development or reproducibility justifies that choice;
4. vendor only when operationally necessary and legally unambiguous.

Forking or duplicating community work should require a documented reason.

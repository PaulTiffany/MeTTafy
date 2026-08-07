# MeTTafy

**Semantic decompilation into executable MeTTa.**

MeTTafy is an open-source research project for recovering the *computational strategies* implemented by conventional programs, classifying those strategies explicitly, and re-expressing them as inspectable and executable [MeTTa](https://github.com/trueagi-io/hyperon-experimental) programs.

The goal is **not** ordinary source-to-source transpilation.

```text
source program
    ↓
structural program model
    ↓
semantic strategy recovery
    ↓
strategy graph / ontology
    ↓
MeTTa emission
    ↓
behavioral verification
```

A conventional implementation may express backtracking, constraint propagation, symmetry reduction, graph traversal, dynamic programming, rewriting, external solver delegation, or other strategies through many lines of incidental control flow. MeTTafy aims to recover those strategies as first-class objects rather than merely translating loops into different loops.

## The motivating example

Suppose a Python graph-coloring solver contains adjacency checks, recursive branching, mutation, rollback, and heuristics. A syntactic transpiler preserves those implementation details. MeTTafy instead aims to recognize a composition such as:

```text
BacktrackingSearch
  + ConstraintPropagation
  + VariableSelectionHeuristic
```

and emit both:

1. an explicit semantic representation of those strategies; and
2. executable MeTTa implementing the recovered computation.

The generated representation should retain provenance back to the source program and should be tested against the original implementation rather than trusted merely because it parses.

## Why MeTTa?

MeTTa is the programming language of OpenCog Hyperon. Its metagraph-oriented model allows facts, rules, queries, and programs themselves to participate in a common symbolic substrate. That makes it an unusually interesting target for a semantic intermediate representation: the recovered description of *what a program is doing* can itself be available to subsequent reasoning and transformation.

## Project principles

- **Semantics before syntax.** Recover strategies, constraints, invariants, and effects before emitting target code.
- **Evidence before confidence.** Semantic classifications should retain source spans and structural evidence.
- **Verification before equivalence claims.** Generated MeTTa should be checked against the source implementation on observable behavior.
- **Unknown is a valid classification.** Do not force unfamiliar computations into a convenient ontology.
- **Celebrate the ecosystem.** MeTTafy is intended to build with and alongside existing MeTTa, Hyperon, OpenCog, and community tooling—not replace or rebrand it.
- **Reuse responsibly.** Prefer dependencies, adapters, and git submodules when upstream projects are the canonical implementation. Preserve upstream licenses and notices. Do not vendor ambiguously licensed code.

## Initial scope

The first milestone is intentionally small:

```text
Python graph-coloring solver
    → recover structural evidence
    → classify Backtracking + ConstraintPropagation
    → emit strategy atoms and executable MeTTa
    → differentially verify behavior
```

Python is the initial source language. The architecture is intended to admit richer front ends later, including code-property-graph approaches such as [Joern](https://github.com/joernio/joern), without coupling the semantic layer to Python syntax.

## Prior art and community

MeTTafy exists because there is already a rich open-source ecosystem worth building on.

- **OpenCog Hyperon / MeTTa** — the language and execution substrate that motivates this project: https://github.com/trueagi-io/hyperon-experimental
- **MeTTaScript by MesTTo** — a TypeScript metagraph database and MeTTa reasoning/runtime ecosystem with extensive host-language interoperability: https://github.com/MesTTo/MeTTaScript
- **metta-src-conversions by LogicMOO** — prior work collecting source/MeTTa conversions of AI and symbolic programs: https://github.com/logicmoo/metta-src-conversions
- **Joern / Code Property Graphs** — mature language-agnostic structural program representation that may become an optional future front end: https://github.com/joernio/joern

See [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md) and [`docs/prior-art.md`](docs/prior-art.md) as the project develops.

**MeTTafy is an independent community project. It is not an official project of SingularityNET, OpenCog, Hyperon, MesTTo, LogicMOO, or their contributors.**

## Licensing

MeTTafy-original code is released under the MIT License. Copyright © 2026 Paul Carver Tiffany III.

Third-party projects retain their own copyrights and licenses. Acknowledgment does not imply that their code has been copied into this repository. Any dependency, derived work, vendored component, or submodule will be documented with its upstream source and license.

## Status

Early research prototype / architecture bootstrap. Expect the ontology and intermediate representations to change while the first verified end-to-end example is built.

## Contributing

Collaboration with the MeTTa/Hyperon and broader program-analysis communities is welcome. In particular, corrections to attribution, prior-art references, terminology, or compatibility assumptions are treated as substantive contributions.

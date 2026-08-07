# Architecture

MeTTafy's core research hypothesis is that useful program translation into MeTTa should happen through an explicit semantic intermediate representation rather than by directly rewriting syntax.

## Pipeline

```text
Source
  ↓
Structural IR
  ↓
Strategy recovery
  ↓
Strategy IR / ontology
  ↓
MeTTa emission
  ↓
Behavioral verification
```

### 1. Source front end

The first front end targets Python and should rely on the standard library `ast` module wherever possible. Its job is descriptive, not interpretive: recover functions, calls, branches, loops, recursion, reads/writes, mutation, returns, and source spans.

Future front ends may consume Code Property Graphs or other language-neutral program representations.

### 2. Structural IR

The structural IR records what the program demonstrably does without assigning high-level algorithm names. Example evidence includes:

- recursive call edges;
- state mutation followed by restoration;
- predicates guarding candidate acceptance;
- repeated traversal over neighboring objects;
- monotone accumulators;
- memo-table reads/writes;
- branch pruning;
- external solver calls.

Structural evidence must retain provenance to source spans.

### 3. Strategy recovery

Strategy recovery maps structural evidence into semantic hypotheses. It may combine deterministic recognizers and model-assisted classification, but generated classifications are never considered ground truth merely because they are plausible.

Initial strategy vocabulary:

- `BacktrackingSearch`
- `ConstraintPropagation`
- `BranchAndBound`
- `GraphTraversal`
- `Memoization`
- `DynamicProgramming`
- `Rewrite`
- `Reduction`
- `SymmetryBreaking`
- `HeuristicSelection`
- `FixpointIteration`
- `CertificateCheck`
- `ExternalSolverCall`
- `UnknownStrategy`

### 4. Strategy IR

A strategy node should eventually support fields equivalent to:

```text
id
kind
inputs
preconditions
invariants
effects
termination
children
evidence
source_spans
confidence
```

The IR should distinguish observed structural facts from inferred semantic claims.

### 5. MeTTa emitter

The emitter has two outputs:

1. descriptive strategy atoms representing the recovered semantics;
2. executable MeTTa implementing the recovered computation when supported.

This separation matters: MeTTafy should be able to describe a strategy it cannot yet faithfully compile.

### 6. Verification

Verification is part of translation, not an optional afterthought.

The initial approach is differential testing:

- generate or load test inputs;
- run the original source implementation;
- run the emitted MeTTa implementation;
- compare agreed observables;
- retain counterexamples when results diverge.

Later work may add property-based testing, solver-backed checking, proof certificates, and stronger equivalence notions.

## Four-color / graph-coloring bootstrap

The first end-to-end example uses a small Python graph-coloring solver. The expected semantic decomposition is intentionally modest:

```text
BacktrackingSearch
  ├── ConstraintPropagation
  └── HeuristicSelection (optional in earliest implementation)
```

The milestone succeeds when MeTTafy can:

1. find concrete structural evidence for the classification;
2. emit a machine-readable Strategy IR;
3. emit corresponding MeTTa strategy atoms;
4. execute a supported MeTTa coloring implementation; and
5. differentially test the source and target on a suite of graphs.

## Non-goals for v0.1

- proving arbitrary source/target equivalence;
- supporting every Python feature;
- treating an LLM explanation as a compiler result;
- replacing Hyperon, MeTTaScript, Joern, or existing MeTTa tooling;
- claiming that semantic recompilation automatically improves runtime performance.

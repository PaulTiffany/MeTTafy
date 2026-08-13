# Four Color engineering-target search

This tranche uses the Four Color proof surface as a semantic query generator
against flat Python implementations that already exist in the author's public
repositories.

The purpose is **reuse discovery**, not theorem verification.

```text
mathematical need
-> canonical behavioral concepts
-> pinned flat-Python candidates
-> explicit fuzzy match
-> human/mechanical adaptation
-> only then: possible proof witness
```

A retrieved implementation is therefore represented by `EngineeringMatch`, not
`Witness` or `Covers`.

## Why search engineering code

The proof's novel center is currently weakest at:

- `C5 PresentStateNoninverseContinuation`
- `C6 OrderedShapeProgress`
- `C7 FiniteConstructionClosure`

These claims are stated mathematically, but the underlying contracts are common
engineering problems: avoid treating replay as novelty, preserve identity across
irrelevant representation changes, keep present state free of future
information, and refuse successful termination while finite obligations remain.

Searching old Python by those behaviors can recover machinery built for a
different application without assuming that the original application knew
anything about graph coloring.

## Pinned candidate corpus

### COME — `c3c09334c70fb1ee812e004c35fe2deb0ef51883`

`come/adapters.py` distinguishes ONA `Input` echoes and `Selected` scheduling
from `Derived` output. Only `Derived` lines count as new knowledge.

This is a strong C6 engineering analogue:

```text
activity / replay != new information
```

It is not itself a graph-theoretic witness.

### Notebook Compiler — `67fe52d3820fff3b2d75c974137c68efdaaffb0c`

Four flat Python patterns are indexed:

1. `scripts/check_determinism.py`
   compiles the same input twice in separate directories, normalizes volatile
   representation fields, hashes the normalized artifacts, and requires the
   hashes to agree. This is a candidate implementation pattern for
   orientation/label-independent resolved-shape identity.

2. `src/notebook_compiler/artifacts.py`
   uses frozen typed artifact objects with SHA-256 identity, provenance,
   certificates, manifests, and audit traces. This is a candidate substrate
   for a retained construction ledger.

3. `src/notebook_compiler/control_board.py`
   intentionally contains compile-time state only; later verification belongs
   in a sibling certificate. This is a candidate pattern for C5's
   present-state-only contract.

4. `src/notebook_compiler/verifier.py`
   walks a finite ordered cell sequence, stops at the first failure, records
   the exact failed index, and reports success only after completion and
   terminal validation. This is a candidate pattern for C7/M7.

## Deterministic fuzzy bridge

`src/mettafy/engineering_targets.py` does not use embeddings or an LLM score.
It maps free prose onto a small canonical behavioral vocabulary such as:

- `replay`
- `novelty`
- `identity`
- `persistence`
- `growth`
- `finite-order`
- `closure`
- `temporal-locality`

Matches are ranked by the fraction of a mathematical need's concepts present
in a candidate implementation.

This first pass deliberately exposes one remaining C6 concept void:

```text
growth
```

The old implementations cover replay-vs-novelty, normalized identity, and
retained immutable state, but the indexed corpus does not yet contain an
explicit flat-Python analogue of:

```text
same seed / same mode can still be fresh when the physical carrier strictly grows
```

That is useful output. The search program found reusable machinery **and**
identified the behavior still missing from the current candidate corpus.

## Promotion rule

`EngineeringMatch` is never emitted as `Covers`.

To promote a candidate into the proof's mechanical witness layer we must:

1. adapt the implementation to the actual Four Color state species;
2. write a destructive and positive test against the relevant claim;
3. run the existing witness suite;
4. bank any failure rather than changing the frozen proof silently.

The MeTTa projection in
`exemplars/four_color/engineering_targets.metta` makes the search graph
inspectable while preserving that boundary.

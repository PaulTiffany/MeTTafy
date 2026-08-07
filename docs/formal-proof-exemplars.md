# Formal Proof Exemplars

MeTTafy will use **machine-checkable proof programs** as a high-quality semantic training and evaluation curriculum.

The purpose is not to turn MeTTafy into a theorem prover. The purpose is to learn and test MeTTafication against programs whose intended semantics and correctness can be checked independently.

A second purpose is educational: the exemplar set should expose the history of computational reasoning in topology, geometry, and adjacent fields. Landmark proofs should be presented as lineages from mathematical problem to human strategy to computational intervention to formal/checkable artifact. See [`historical-curriculum.md`](historical-curriculum.md).

## Why formal proofs first

Arbitrary software often has ambiguous intent. Formal proof programs give us unusually strong supervision:

- a theorem statement;
- an executable/checkable proof artifact;
- explicit dependencies;
- tactic/term structure;
- a trusted checker result;
- opportunities to annotate higher-level reasoning strategies;
- exact replay as a verification boundary.

That lets MeTTafy learn the mapping

```text
proof program
    -> structural proof trace
    -> semantic strategy labels
    -> Strategy IR
    -> MeTTa representation
```

without treating human-written labels or learned model scores as ground truth.

## Initial curriculum: topology-heavy formal proofs

Topology is a useful first domain because formal topology proofs exhibit recurring strategy motifs that generalize beyond any single theorem. Candidate motifs include:

- local-to-global reasoning;
- basis refinement;
- neighborhood selection;
- induced/coinduced structure construction;
- continuity by composition;
- compactness / finite extraction;
- closure and interior transformations;
- separation arguments;
- contradiction and minimal-counterexample reasoning;
- quotient / subspace transport;
- monotonicity and lattice-style refinement;
- explicit witness construction.

These are **semantic strategy labels**, not Lean tactic names. A proof using `simpa`, `rw`, or `aesop` may instantiate several different semantic strategies depending on context.

The curriculum is intentionally broader than a single proof assistant or a narrow modern definition of topology. Famous computational lineages in planar graph theory, knot theory, discrete geometry, and algebraic topology are in scope when they illuminate how computation entered geometrical reasoning. Each exemplar should identify its mathematical field precisely.

## Exemplar record

Each exemplar should be represented by a small manifest rather than copied into the repository without context.

Minimum fields:

```text
id
upstream_repository
upstream_commit
upstream_path
theorem_name
upstream_license
checker
checker_version
source_hash
proof_status
strategy_annotations
annotation_provenance
```

Optional derived fields may include:

```text
dependency_graph
proof_term_shape
tactic_trace
local_context_transitions
candidate_strategy_scores
verification_log
history_metadata
```

Historical metadata is documentary and must not become a hidden label channel during evaluation. Benchmark tooling should support a blind mode that removes theorem names, authors, filenames, dates, and narrative descriptions before strategy classification.

## Verification boundary

An exemplar is accepted only when the source proof checks under the pinned toolchain / upstream commit.

Learned or heuristic components may:

- propose a strategy label;
- rank candidate labels;
- cluster proof traces;
- suggest boundaries between proof phases;
- predict which MeTTa rewrite schema may fit.

They may **not** determine whether the theorem is proved or whether a generated transformation is behaviorally / logically correct.

The proof assistant or other exact checker remains authoritative.

## FabricPC

[FabricPC](https://github.com/trueagi-io/FabricPC) is an MIT-licensed predictive-coding framework maintained in the SingularityNET ecosystem. It is a possible optional component for learning structure over proof traces or Strategy IR graphs.

A FabricPC integration, if used, should be an **adapter/dependency**, not a fork or reimplementation.

Its role should be narrow:

```text
verified proof trace
    -> graph features
    -> FabricPC predictive model
    -> candidate strategy scores
    -> MeTTafy evidence layer
    -> exact downstream verification
```

FabricPC output is evidence, not authority.

## Tranch7 rule

MeTTafy adopts a conservative rule for learned components:

> **Prediction may guide search; verification governs acceptance.**

Operational consequences:

1. keep the original formal artifact and pinned checker available;
2. preserve provenance from prediction back to source proof structure;
3. report uncertainty rather than collapsing it into a single label;
4. never silently promote a learned semantic classification into a proof claim;
5. make generated MeTTa replayable and independently checkable where possible;
6. retain counterexamples and failed classifications as training data rather than discarding them;
7. allow abstention when evidence is weak or contradictory.

## Corpus policy

Prefer upstream references over bulk vendoring.

For each corpus source:

- record the canonical upstream URL;
- pin a commit or release;
- record the applicable license;
- preserve required notices if source is redistributed;
- avoid copying entire third-party corpora into MeTTafy when a fetch/index adapter is sufficient.

The initial candidate corpus is `leanprover-community/mathlib4`, licensed under Apache-2.0. MeTTafy should initially index selected topology proofs by reference and metadata rather than importing mathlib source wholesale.

Historical landmark cases may come from other systems (for example Coq, HOL Light, Isabelle, specialized checkers, or citable computational implementations). Their artifacts should be incorporated only through the same provenance, licensing, and reproducibility discipline.

## Milestone success criterion

The first formal-proof milestone succeeds when MeTTafy can take a small pinned set of verified topology proofs and produce:

1. deterministic structural features;
2. explicit semantic strategy annotations with provenance;
3. a MeTTa Strategy IR representation;
4. optional learned candidate scores kept separate from verified facts;
5. a reproducible verification record for every exemplar; and
6. for landmark cases, a citable historical narrative that explains where computation entered the mathematics without leaking those labels into benchmark classification.

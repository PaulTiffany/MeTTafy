# Production certification

MeTTafy does not use **green** as a synonym for “the workflow exited zero.” Green is a versioned certification result.

> **CI produces evidence. The certification program defines what that evidence means.**

The canonical machine-readable program is [`certification/program-v1.json`](../certification/program-v1.json). A threshold change is therefore a product-policy change and must be reviewed like code.

## Three grades

### Engineering green

The shipped software boundary is healthy. All required engineering, packaging, browser, security, and supply-chain gates pass on the same repository commit.

### Exemplar green

MeTTafy has demonstrated semantic recovery on a pinned benchmark without answer leakage. Required strategy quality, evidence quality, robustness, abstention, and exemplar-specific structural tests all pass.

### Product green

`engineering_green` **and** `exemplar_green` both pass on the same certification run.

There is no partial-credit product certificate. Planned gates are not passing gates. A skipped required gate fails certification.

## Unit-test contract

Unit tests protect local invariants. They are necessary but insufficient for certification.

The v1 suite must cover these families explicitly:

| Family | Required behavior |
| --- | --- |
| Python analysis | recursive search + rollback is recognized as `BacktrackingSearch`; candidate-validation helpers are recognized as `ConstraintPropagation`; unsupported structures do not acquire invented strategies; sync and async functions remain parseable; source spans point inside the supplied source |
| IR | `Strategy`, `Evidence`, and `SourceSpan` serialize deterministically; enum values are stable; child strategies remain recursively serializable |
| MeTTa emission | quoting escapes quotes and backslashes; every prediction carries evidence/support atoms; output ordering is deterministic for identical input |
| Exemplar blinding | strategy labels, theorem names, history, documentary repository paths, and source answer keys are absent from classifier input; held-out targets remain available separately |
| CLI | JSON and MeTTa modes both work from the installed wheel; malformed/missing input fails non-zero rather than producing a plausible artifact |
| Pages | identical inputs produce byte-identical output; raw MeTTa fallback survives without Grapher; legacy URLs resolve; provenance contains hashes for authoritative inputs and shipped vendor bytes |
| Browser | primary pages and internal links resolve; console/page/request error counts are zero; both Grapher instances mount SVG; the reduction demo produces at least two trace states and advances |
| Certification program | gate IDs are unique; every grade references existing gates; every gate has an executable metric/threshold definition; `planned` gates cannot satisfy a grade; certificate schema fields are fixed |

A new supported behavior requires a corresponding unit/integration family before it becomes a product promise.

## Benchmark contract

Benchmarks answer a different question: **does semantic recovery remain correct across a controlled corpus rather than a hand-picked happy path?**

### `strategy-recovery-v1`

A labeled corpus of small programs containing positive, mixed, and ambiguous strategy cases. Each case contains:

- immutable case ID;
- source artifact and SHA-256;
- held-out strategy labels;
- allowed alternate labels, if any;
- expected evidence regions or structural predicates;
- provenance and license;
- train/dev/test role. The certification test partition is never used as prompt/context or rule-generation input.

Certification thresholds:

- micro precision **>= 0.95**;
- micro recall **>= 0.80**;
- micro F1 **>= 0.87**;
- 100% of emitted predictions carry source evidence;
- 100% of evidence spans are valid spans in the analyzed artifact.

Precision is deliberately stricter than recall: MeTTafy should abstain rather than hallucinate a reasoning strategy.

### `strategy-perturbations-v1`

Semantics-preserving variants of benchmark programs. Required perturbations in v1:

- identifier renaming;
- comment changes;
- whitespace/formatting changes;
- helper extraction that preserves the same reasoning move.

Thresholds:

- semantic-label invariance **>= 0.95**;
- evidence successfully relocalizes to the changed source **>= 0.95**.

This prevents a classifier from passing by memorizing lexical surfaces.

### `negative-controls-v1`

Programs intentionally lacking supported strategies or containing misleading lexical cues.

Thresholds:

- unsupported false-positive rate **<= 0.02**;
- explicit abstention on unsupported cases **>= 0.98**.

### `four-color-v1`

The first exemplar benchmark is pinned to the maintained Rocq Four Color artifact already named in the exemplar manifest. It has two layers.

**Structural recovery must recover exactly the required high-level dependency edges:**

```text
four_color -> finitize.compactness_extension
four_color -> four_color_finite
four_color_finite -> discretize.discretize_to_hypermap
four_color_finite -> combinatorial4ct.four_color_hypermap
```

Required edge recall is **1.00** and spurious required-scope edges are **0**.

**Semantic recovery** is graded against the held-out strategy target:

```text
FiniteReduction
Discretization
RepresentationChange
ProofByTransport
CompactnessExtension
StructuralReduction
Induction
MinimalCounterexample
DecisionProcedure
Unavoidability
Reducibility
```

Thresholds:

- required-strategy precision **>= 0.95**;
- required-strategy recall **>= 0.90**;
- every accepted semantic claim has source evidence.

The held-out names are scoring targets, not classifier input. The formal checker remains theorem-validity authority; this benchmark scores MeTTafy's interpretation of the proof architecture.

## Leakage rules

A benchmark result is invalid if the evaluated system can see answer-bearing fields that would not exist in a real unknown program. At minimum, certification input must exclude:

- held-out strategy labels;
- theorem names when theorem identity itself reveals the label;
- historical descriptions;
- author names/dates used as lookup keys;
- documentary paths or annotations that encode the expected answer.

`EPI-BLINDING` requires zero detected leakage cases.

## Certificate contents

A certificate is a machine-generated immutable record bound to one run. It must contain:

- certification-program version;
- repository commit;
- UTC generation time;
- requested grade;
- every required gate and its pass/fail/skip result;
- exact measured values and thresholds;
- SHA-256 hashes for every benchmark partition used;
- SHA-256 hashes for release/site artifacts being certified;
- relevant tool/checker/runtime versions;
- final result.

A missing, skipped, or `planned` required gate makes the requested grade **not certified**.

## Threshold governance

Thresholds may change, but never silently. Any change to `certification/program-v1.json` must explain:

1. why the old threshold was inadequate;
2. whether the change is stricter or looser;
3. benchmark impact on the last known baseline;
4. whether the program version must increase.

Do not lower a threshold merely to make a failing release green.

## Standards we align with

The program borrows established product disciplines rather than inventing substitutes: WCAG 2.2 AA is the target accessibility standard, release provenance should evolve toward SLSA-compatible build provenance, and repository/supply-chain checks should remain compatible with OpenSSF-style reviewability. These standards supplement MeTTafy's own epistemic benchmarks; they do not replace them.

## Current certification state

The engineering gates implemented in the current repository are a strong baseline. The epistemic benchmark gates, accessibility budget, SBOM, and release-provenance gates remain `planned` in v1. Therefore **MeTTafy is not yet product-green under this program**.

That is intentional. The point of certification is to make the remaining distance measurable.

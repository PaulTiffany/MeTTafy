# Mechanistic Interpretability: Rule Trace IR

MeTTafy's interpretability target is **mechanistic traceability**, not post-hoc prose.

For the current bounded structural recognizer, a decision is interpretable only when an independent reviewer can reproduce it from classifier-visible inputs and the checked-in rule table without consulting raw source, held-out labels, or an explanatory model.

## Contract

For every blind structural unit and every configured recognition rule, emit a `RuleTrace` containing:

- stable `rule_id`;
- target semantic class;
- required mechanical features;
- observed required features;
- missing required features;
- forbidden features and observed guard violations;
- rule confidence and configured promotion threshold;
- exact decision class;
- bounded reason string.

Current decision classes are:

- `promote` — all premises hold, no guard blocks, confidence reaches threshold;
- `not_applicable` — at least one required premise is absent;
- `blocked` — a forbidden feature is present;
- `below_threshold` — premises hold but configured confidence threshold is higher.

The trace is emitted whether a rule fires or not. This makes abstention inspectable rather than opaque.

## Counterfactual boundary

For the bootstrap Reduction rule,

```text
rule_id: recognition.reduction.dataflow-composition.v1
requires: composition
confidence: 0.78
```

A blind unit with observed `composition` promotes `Reduction` at the default threshold `0.55`.

A near-miss unit with applications but no observed dataflow composition emits:

```text
decision: not_applicable
missing_required_features: [composition]
```

Raising the threshold above `0.78` leaves the mechanical premises unchanged but changes the trace to:

```text
decision: below_threshold
```

These are causal counterfactuals of the checked-in decision procedure, not natural-language guesses about why a black-box model behaved a certain way.

## Authority boundary

The trace layer does not add semantic authority. It exposes the existing authority boundary.

The recognizer still receives only `BlindStructuralEvidence`; raw source text, theorem names, paths, exact upstream identifiers, audit joins, and held-out strategy labels remain unavailable to it.

A trace can therefore justify only statements supported by the bounded structural features and the explicit recognition rules. It cannot upgrade an induction token into a claim of `MinimalCounterexample`, or a decision-shaped call into `CertificateCheck`, unless a future checked-in rule supplies stronger mechanically observable premises.

## Interpretability invariants

The initial witness requires:

1. **semantic invariance** — adding traces does not change the existing promoted/abstained decisions;
2. **replay determinism** — identical blind evidence and rule configuration produce byte-equivalent canonical trace payloads;
3. **source neutrality** — traces contain no raw source identifiers or held-out answer labels;
4. **premise visibility** — every promotion identifies the premises that fired;
5. **counterfactual visibility** — every abstention records which premise/guard/threshold prevented each considered rule from firing;
6. **fail-closed thresholds** — invalid confidence thresholds are rejected rather than interpreted silently.

`WIT-MECHANISTIC-INTERPRETABILITY-TRACE` certifies these properties on the bounded bootstrap corpus.

## Why this matters for the Four Color program

The next structural claims — reducibility, minimal-counterexample reasoning, observer-critical routing, and any SRMF correspondence — are too important to be accepted because a classifier emits a plausible label.

Each future promotion should instead acquire an inspectable rule path:

```text
blind structural evidence
  -> exact premises
  -> explicit rule
  -> trace
  -> Strategy IR candidate
  -> independent downstream witness
```

For reducibility in particular, an eventual trace should identify the exact local structure, the certified transformation family, the preserved boundary invariant, and the well-founded measure that decreases. If those premises are absent, MeTTafy should abstain.

The goal is therefore not an interpreter that sounds convincing. The goal is a system where **prediction may guide search, but every accepted semantic step has a reconstructible mechanical cause.**

# Four Color Reidemeister Staging

**Status:** inference-only research machinery. This document does not claim an independent proof of the Four Color Theorem.

The working hypothesis is that a long MapMaker imagination trace is often a complicated planar projection of a much smaller **boundary-labelled strategy tangle**.

The implementation therefore does not search deeper by default. It first asks whether deeper search is repeatedly presenting the same proof-relevant structure.

## Authority boundary

Reidemeister staging lives entirely inside the existing imagination lane:

```text
RealizedMap
-> roleplay
-> RawStrategyTrace
-> StrategyTangle
-> Reidemeister-like staging
-> StrategyNormalForm
-> strategy-completeness argument
-> InferenceSound
-> CertifiedInstantiation
-> exactly one realized void -> V4 move
```

Forbidden shortcuts remain:

```text
StrategyTangle -> RealizedMap
StrategyNormalForm -> CertifiedInstantiation
normal-form count -> proof of completeness
```

A normal form is inference data. It acquires construction authority only if a separate completeness argument and the existing inference-soundness bridge justify one depth-zero move on the unchanged realized map.

## Reidemeister staging

"Reidemeister" is used operationally rather than as a claim that a coloring trace is literally a classical knot diagram.

The concrete roleplay trace is Unweaved into typed operations such as:

```text
IntroduceRole(B)
Extend(B)
Return(B)
Cross(B, C, sign)
Probe(...)
Periodic((B, C))
```

Each operation is also labelled with the bounded reasoning frame in which it occurred:

```text
reasoning
analysis
inspection
```

Staging then attempts only explicit local rewrites whose proof-relevant interface is intended to remain unchanged.

### R1-like loop collapse

```text
Extend(B), Return(B)
->
identity
```

This removes a projected excursion that returns without adding a new independent role.

### R2-like opposed-pair cancellation

```text
Cross(B, C, +), Cross(B, C, -)
->
identity
```

Cancellation requires the same explicit support and opposite crossing sign. Visual resemblance alone is not enough.

### R3-like staging

Independent operations with disjoint role support may be reordered into a canonical frame order. Operations that share role support do not commute by default.

This is the old staging idea in Four Color form: batch compatible reasoning with reasoning, analysis with analysis, and inspection with inspection without silently reordering noncommuting work.

### Periodic fold

A repeated continuation such as

```text
B C B C B C B C ...
```

may be represented as one token:

```text
Periodic((B, C))
```

but only when that periodic equivalence is explicitly enabled in the normalization policy being tested.

The raw length of the imagined continuation is therefore distinct from its strategic complexity.

## Degrees of freedom are not CoT depth

After one realized anchor role is fixed, at most three independent color roles remain.

A long same-turn imagination trace may revisit already introduced roles many times without consuming additional role freedom.

Conceptually:

```text
real anchor A:       3 independent roles remain
introduce B:         2 remain
introduce C:         1 remains
introduce D:         0 remain
repeat B/C geometry: still 0 new independent roles
```

The implementation records this separately as a `RoleLedger`.

Therefore:

```text
level-of-thinking depth != independent role commitments
```

This distinction is essential to the compression hypothesis.

## Boundary-labelled Strategy Tangle

A `StrategyTangle` contains:

```text
one raw typed trace
one realized-relative anchor role
boundary role labels
one existing StrategySignature
```

Coordinates and concrete run length are not part of the normal-form key unless later counterexamples prove they are proof-relevant.

Color-role names are canonically relabelled relative to the anchor and first introductions, so color permutation does not create a new class merely by naming.

Mirror equivalence is optional and explicit. When enabled, the normalizer compares the projected trace with its reflected presentation and chooses a deterministic representative.

## Strategy interface

Staging is evaluated against a deliberately small interface:

```text
remaining independent roles
boundary form
recognized periodic cycles
response classes
relevant options
```

Two concrete tangles are candidates for the same strategy class when normalization yields the same interface-bearing normal form.

This is stronger than picture similarity and weaker than concrete trace equality.

## Reidemeister complexity

The staging pass records:

```text
R1-like loop collapses
R2-like cancellations
R3-like independent reorders
periodic folds
raw operation count
normal operation count
```

The empirical target is not that every trace has low raw length. It is that raw length can grow while normal-form complexity remains bounded or grows much more slowly.

A useful signal would look like:

```text
raw trace length:       400
normal strategy length:   6
```

The Lean witness `ReidemeisterComplexityWitness` records the four normalization-operation counts without treating them as a construction-time ranking function.

## Discover classes; do not encode the answer

The repository intentionally does not encode a target such as "there are nine strategy classes."

The reporting path computes:

```text
raw traces
raw operations
distinct normal forms
max remaining role degrees
max normalized operation count
```

The class count is whatever survives the quotient.

The current fixtures begin with the two concrete meta-strategy families already under active red-team study:

1. one lengthwise/bottom anchor with the remaining roles extending/responding;
2. two running roles with transverse cancellation/reentry behavior.

The fixtures also include short/long periodic continuations and a mirror pair.

Run:

```text
python scripts/report_four_color_strategy_staging.py
```

to inspect the current empirical compression count.

## Formal obligations

The new Lean lane introduces two explicit open obligations:

```text
EveryStrategyTangleNormalizes
FiniteResponseCompleteNormalForms
```

The second means that a finite set of irreducible normal forms covers every generated strategy tangle while preserving its proof-relevant interface.

No inhabitant is supplied.

Even if finite response-complete normal forms are established, one more semantic step remains: show how every relevant normal form yields a sound depth-zero MapMaker strategy claim. Only then can the existing `StrategyIRComplete` theorem target be discharged.

The dependency spine is therefore:

```text
RoleplayTranscript
-> RawStrategyTrace
-> StrategyTangle
-> ReidemeisterStaging
-> StrategyNormalForm
-> NormalFormCompleteness
-> StrategyIRCompleteness

StrategyIRCompleteness + InferenceSoundness
-> StrategySafeContinuation
```

Everything before `StrategyIRCompleteness` remains inference-only.

## Counterexample discipline

The staging vocabulary is provisional.

When a hard configuration defeats a quotient, the response is:

```text
counterexample
-> identify the missing proof-relevant distinction
-> add the smallest required observable/relation
-> rerun normalization
```

Do not preserve a class merely because it was aesthetically attractive.

Do not add a distinction merely because historical Four Color language contains it.

The objective is to discover the smallest response-complete MapMaker state machine forced by the game itself.

## Checksum

> **Do not search deeper. Uncross what deeper search already means.**

Then, if one depth-zero move is genuinely certified:

> **Imagine many. Instantiate one. Re-observe.**

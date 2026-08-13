# Four Color Proof Surface

**Branch:** `agent/four-color-proof-surface`  
**Frozen proof:** `docs/four-color-ordered-construction-proof.md` at
`7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b`

This tranche re-enters MeTTa after the human-readable Track-B proof has been
written.  MeTTa does **not** rewrite or certify the proof.  It carries the proof's
epistemic surface: typed claims, dependency edges, evidence fibers, mechanical
witness coverage, and destructive mutations.

The operating rule is:

```text
trust the frozen construction
-> expose every proof arrow
-> attach its evidence fiber
-> map mechanical coverage
-> mutate every load-bearing claim
-> bank any concrete failure
```

Mechanical witnesses are the red team.  An LLM confidence score is not a proof
premise and is not a falsifier.

## 1. Surface partition

The surface is divided into four operational layers.

### Ground

Standard substrate needed before the novel construction starts:

- `C0 MinimalCounterexampleReduction`
- `C1 SaturatedBoundaryNormalForm`

### Frontier

Load-bearing claims at the edge of the independent proof:

- `C2 CleanFrontierTurnExistence`
- `C4 RepeatedTurnPairLemma`
- `C6 OrderedShapeProgress`

### Flow

Claims about legal present-state transformation:

- `C3 SingletonCleanTurnFinishes`
- `C5 PresentStateNoninverseContinuation`

### Closure

Claims that turn the local construction into the degree-five extension:

- `C7 FiniteConstructionClosure`
- `C8 DegreeFiveExtension`

The surface graph is encoded in
`src/mettafy/proof_surface.py` and projected without semantic compression to
`exemplars/four_color/proof_surface.metta`.

## 2. No bare proof arrows

Every `C0` through `C8` has an explicit mathematical evidence fiber pointing
back to the frozen proof or its direct planar lemmas.

`ProofSurface.assert_structurally_sound()` rejects:

- unknown claim references;
- dependency cycles;
- claims with no evidence fiber.

This check is deliberately weaker than theorem verification.  It says the
surface is traceable, not that every claim is true.

## 3. Mechanical coverage is a separate coordinate

A mathematical evidence fiber and a mechanical witness are different objects.
The current witnesses are:

- `W-SequentialFrontier` — the retained lock witnesses and exact clean-turn
  transitions;
- `W-FlipFamily4620` — all 4,620 saturated proper colorings over the established
  154-carrier flip family, including both nonterminal orientations;
- `W-GeneratedDisks5000` — the broader locally generated planar-disk audit
  recorded in the proof status document.

The surface currently reports three mechanically unwitnessed claims:

```text
C0 MinimalCounterexampleReduction
C1 SaturatedBoundaryNormalForm
C6 OrderedShapeProgress
```

`C0` and `C1` are standard mathematics, but they remain visible because the
program is mapping the whole proof rather than only its novel center.

`C6` is the important frontier void.  The proof gives the constructional
argument that a genuine turn resolves previously unresolved component-shape
information, but the current witness suite does not yet mechanically certify
that progress law across a declared exhaustive carrier universe.

The surface therefore does not promote `C6` to mechanically closed.

## 4. Destructive mutation queue

Every claim has a planned mutation whose expected result is failure:

| Mutation | Target | Destructive change |
|---|---|---|
| `M0-DropMinimality` | C0 | remove the smaller-counterexample induction premise |
| `M1-BreakBoundaryNormalForm` | C1 | supply a nonproper or nonsaturated frontier |
| `M2-AllowPlanarCrossing` | C2 | permit complementary paths to cross without incidence |
| `M3-DirtyFrontierTurn` | C3 | let a claimed clean component hit two frontier vertices |
| `M4-BreakRepeatedPair` | C4 | destroy one repeated clean occurrence |
| `M5-StoreFutureRoute` | C5 | inject a future route into present-state semantics |
| `M6-ReplayResolvedShape` | C6 | count an exact resolved inverse as fresh progress |
| `M7-AllowSaturatedExhaustion` | C7 | terminate while a clean unresolved continuation remains |
| `M8-CorruptRestoredEdge` | C8 | restore the focus with a forbidden neighborhood color |

A mutation is not considered executed merely because its failure sounds
obvious.  Its status remains `planned` until an executable witness actually
kills it.

This is the anti-masking rule for the test suite itself.

## 5. MeTTa's role

The MeTTa projection contains relations of the form:

```metta
(Claim C6 OrderedShapeProgress Frontier)
(EvidenceFiber E6 C6 Mathematical)
(Covers W-FlipFamily4620 C7)
(Mutation M6-ReplayResolvedShape C6 ExpectedFailure planned)
(DependsOn C7 C6)
```

This lets the proof program ask relational questions instead of accumulating
ad-hoc tests:

```text
which claims have no evidence fiber?
which claims have no passing mechanical witness?
which downstream conclusions depend on a weakly covered frontier claim?
which destructive mutations remain unexecuted?
```

The pinned MeTTaScript runtime witness now parses the proof-surface artifact as
well as the existing Four Color semantic exemplar.  Parsing demonstrates that
the relational artifact is executable MeTTa syntax; it does not establish the
truth of the encoded mathematics.

## 6. Next falsification order

The surface gives a principled work queue.

### Priority A — C6 / M6

Mechanize the distinction between:

```text
legal reversible graph symmetry
```

and

```text
genuine ordered construction progress
```

so that replay of an already resolved component is mechanically rejected as a
new progress certificate while a newly resolved physical component-shape fact
is accepted.

This is the most load-bearing current void because `C7 FiniteConstructionClosure`
depends on `C6`.

### Priority B — C7 / M7

Construct an explicit saturated-exhaustion mutation and require the closure
checker to find the clean unresolved continuation promised by the planar
lemmas.

### Priority C — widen carrier coverage

Generate witness families by declared surface purpose rather than by raw count:

- interior depth;
- bichromatic component entanglement;
- long clean components;
- repeated-state revisitation;
- near-crosscut configurations;
- symmetry classes;
- maximal ordered-turn depth.

Each family must declare which surface claims it attacks.

### Priority D — standard-ground mutations

Bank executable failures for `C0` and `C1` so that even the conventional part
of the proof is represented by the same verification contract.

## 7. Promotion rule

The proof claim and the verification claim remain distinct.

A green witness means only that the declared family failed to falsify the
covered claim.  A proof-surface claim may be promoted mechanically only when its
required evidence, witness coverage, and destructive mutations satisfy the
explicit certification policy chosen for that claim.

The surface therefore supports the same alignment contract used to construct
the proof:

```text
Trust: represent the hypothesis faithfully.
Verify: let explicit mechanics object.
```

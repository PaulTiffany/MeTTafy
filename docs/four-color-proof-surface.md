# Four Color Proof Surface

**Branch:** `agent/four-color-proof-surface`  
**Frozen proof:** `docs/four-color-ordered-construction-proof.md` at
`7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b`

This tranche re-enters MeTTa after the human-readable Track-B proof has been
written. MeTTa does **not** rewrite or certify the proof. It carries the proof's
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

Mechanical witnesses are the red team. An LLM confidence score is not a proof
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

The surface graph is encoded in `src/mettafy/proof_surface.py` and projected
without semantic compression to `exemplars/four_color/proof_surface.metta`.

## 2. No bare proof arrows

Every `C0` through `C8` has an explicit mathematical evidence fiber pointing
back to the frozen proof or its direct planar lemmas.

`ProofSurface.assert_structurally_sound()` rejects unknown claim references,
dependency cycles, claims with no evidence fiber, and any mutation marked
`implemented` without a concrete evidence artifact.

This check is deliberately weaker than theorem verification. It says the
surface is traceable, not that every claim is true.

## 3. Mechanical coverage is a separate coordinate

A mathematical evidence fiber and a mechanical witness are different objects.
The current family witnesses are:

- `W-SequentialFrontier` — retained lock witnesses and exact clean-turn
  transitions;
- `W-FlipFamily4620` — all 4,620 saturated proper colorings over the established
  154-carrier flip family, including both nonterminal orientations;
- `W-GeneratedDisks5000` — the broader locally generated planar-disk audit
  recorded in the proof status document.

The surface still reports three mechanically unwitnessed claims:

```text
C0 MinimalCounterexampleReduction
C1 SaturatedBoundaryNormalForm
C6 OrderedShapeProgress
```

`C0` and `C1` are standard mathematics, but they remain visible because the
program maps the whole proof rather than only its novel center.

`C6` remains the important frontier void. The proof gives the constructional
argument that a genuine turn resolves previously unresolved component-shape
information, but the current family witness suite does not mechanically certify
that progress law across a declared exhaustive carrier universe.

The surface therefore does not promote `C6` to mechanically closed.

## 4. Destructive mutation queue

Each claim has a destructive mutation whose expected result is failure.
`M6-ReplayResolvedShape` is now implemented; all others remain planned.

| Mutation | Target | Status | Destructive change |
|---|---|---|---|
| `M0-DropMinimality` | C0 | planned | remove the smaller-counterexample induction premise |
| `M1-BreakBoundaryNormalForm` | C1 | planned | supply a nonproper or nonsaturated frontier |
| `M2-AllowPlanarCrossing` | C2 | planned | permit complementary paths to cross without incidence |
| `M3-DirtyFrontierTurn` | C3 | planned | let a claimed clean component hit two frontier vertices |
| `M4-BreakRepeatedPair` | C4 | planned | destroy one repeated clean occurrence |
| `M5-StoreFutureRoute` | C5 | planned | inject a future route into present-state semantics |
| `M6-ReplayResolvedShape` | C6 | **implemented** | count an exact resolved inverse as fresh progress |
| `M7-AllowSaturatedExhaustion` | C7 | planned | terminate while a clean unresolved continuation remains |
| `M8-CorruptRestoredEdge` | C8 | planned | restore the focus with a forbidden neighborhood color |

Implemented mutations must name an executable artifact. M6 points to
`tests/test_ordered_shape_progress.py::test_m6_exact_inverse_replay_is_not_fresh_progress`.

This is the anti-masking rule for the test suite itself.

## 5. M6: resolved shape versus reversible recoloring

`src/mettafy/ordered_shape.py` makes the proof distinction explicit.

A `PhysicalComponentShape` retains:

- the unordered two-color pair;
- the physical vertex carrier;
- induced carrier edges;
- frontier contacts.

The unordered color pair is intentional: swapping the same complete component
backwards is a legal graph symmetry but resolves no new physical component
shape. `ShapeProgressCertificate` therefore rejects an exact inverse replay as
fresh progress.

The retained three-interior hard witness supplies the complementary positive
check. Its first and third turns use the same unordered color pair `{0,2}` at
the same boundary seed, but the physical carrier grows from `{a,x0}` to
`{a,x0,x2}`. The second occurrence is therefore accepted as a genuinely new
resolved shape.

This implements mutation sensitivity for M6. It does **not** establish universal
positive coverage for C6, which remains on the surface void list.

## 6. MeTTa's role

The MeTTa projection now contains both the coverage void and the executed M6
mutation without conflating them:

```metta
(Claim C6 OrderedShapeProgress Frontier)
(EvidenceFiber E6 C6 Mathematical)
(Mutation M6-ReplayResolvedShape C6 ExpectedFailure implemented)
(DependsOn C7 C6)
```

This lets the proof program ask relational questions instead of accumulating
ad-hoc tests:

```text
which claims have no evidence fiber?
which claims have no passing family witness?
which downstream conclusions depend on a weakly covered frontier claim?
which destructive mutations remain unexecuted?
```

The pinned MeTTaScript runtime witness parses the proof-surface artifact as well
as the existing Four Color semantic exemplar. Parsing demonstrates executable
MeTTa syntax; it does not establish the truth of the encoded mathematics.

## 7. Next falsification order

### Priority A — C6 positive coverage

M6 now kills the exact inverse-replay confusion. The remaining C6 task is
positive coverage: exercise the ordered-shape certificate across deliberately
chosen carrier families and show that every claimed genuine construction event
is fresh under the physical-shape representation.

This must not be promoted to exhaustive theorem coverage merely because the
unit mutation is green.

### Priority B — C7 / M7

Construct an explicit saturated-exhaustion mutation and require the closure
checker to find the clean unresolved continuation promised by the planar
lemmas.

### Priority C — widen carrier coverage

Generate witness families by declared surface purpose rather than raw count:
interior depth, component entanglement, long clean components, repeated-state
revisitation, near-crosscuts, symmetry classes, and maximal ordered-turn depth.
Each family must declare which surface claims it attacks.

### Priority D — standard-ground mutations

Bank executable failures for `C0` and `C1` so that even the conventional part
of the proof is represented by the same verification contract.

## 8. Promotion rule

The proof claim and verification claim remain distinct.

A green witness means only that the declared family failed to falsify the
covered claim. A proof-surface claim may be promoted mechanically only when its
required evidence, witness coverage, and destructive mutations satisfy the
explicit certification policy chosen for that claim.

The surface therefore supports the same alignment contract used to construct
the proof:

```text
Trust: represent the hypothesis faithfully.
Verify: let explicit mechanics object.
```

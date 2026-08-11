# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Checkpoint:** `bdda0563ca3f38187a0ae7e123c1f6478752e1b4`  
**CI:** run #65 — success  
**Status:** active proof program; not yet a closed proof of the Four Color Theorem

## 1. What this document is

This is the durable human-review surface for the proposed independent Four Color proof program developed in MeTTafy.

Two tracks are intentionally separated:

- **Track A — held-out Rocq reference:** the pinned `rocq-community/fourcolor` development at `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`. It is used for structural comparison and mechanical witnessing only after Track B claims are frozen.
- **Track B — independent MeTTafy proof program:** the Cost-of-Cacophony / bounded-observer / SRMF route developed here. This track must not borrow the Four Color conclusion or held-out semantic labels as premises.

The working discipline is:

> Prediction may guide search; verification governs acceptance.

## 2. Candidate proof architecture

The current independent route is:

```text
planar conflict structure
  -> observer-critical forcing
  -> four-stable / five-routes regime
  -> NoStableFifthClass
  -> admissible SRMF refinement
  -> resolved four-channel terminal quotient
  -> V4 = Z2 x Z2 decoding
  -> nowhere-zero V4 flow
  -> Tait 3-edge-coloring
  -> primal four-coloring
```

A more explicit obligation chain is:

1. represent the planar problem without already assuming four-colorability;
2. derive an observer-relative conflict/coupling condition from planar structure;
3. show four channels remain solvent while a fifth cannot persist stably;
4. show the forced route is an admissible refinement, not an arbitrary recoloring;
5. show repeated admissible refinement terminates by a well-founded measure;
6. show the terminal four-channel state carries the required `V4 = Z2^2` algebra;
7. decode sufficiently controlled fuzzy states into an exact nowhere-zero `V4` flow;
8. invoke the classical downstream transfer from that exact object to a four-coloring.

The proof is **not closed** because obligations 2–5 are not yet all established for the actual planar Four Color problem.

## 3. Certified pieces

### 3.1 Observer-critical collapse

Implemented in `src/mettafy/observer_critical.py`.

For the symmetric `k`-constraint geometry,

```text
M = 1 - rho (k - 1)
```

and

```text
delta_min^2 = k tau^2 / (m^2 M).
```

For observer budget `B_O`, define

```text
M_O = k tau^2 / (m^2 B_O^2).
```

The implementation mechanically checks the exact equivalence

```text
delta_min >= B_O    iff    M <= M_O.
```

Interpretation: a finite observer can be forced to change representation before the mathematical positive-definite singularity is reached.

This proves a resource-geometric forcing mechanism only. It does **not** prove that planar graphs induce the required geometry.

### 3.2 Four stable, five routes

Implemented in `src/mettafy/fifth_class.py`.

For a fixed observer floor `0 < M_O < 1`, define

```text
M_k = 1 - rho (k - 1).
```

Then four channels are stable while five must route exactly in the interval

```text
(1 - M_O)/4 <= rho < (1 - M_O)/3.
```

Equivalently,

```text
M_4 > M_O >= M_5.
```

For the reference `M_O = 1/4`:

```text
3/16 <= rho < 1/4.
```

At `rho = 1/5`:

```text
M_4 = 2/5 > 1/4,
M_5 = 1/5 <= 1/4.
```

This is the first exact conditional fragment of the intended `NoStableFifthClass` theorem.

It does **not** prove that planarity forces `rho` into this interval, nor that an arbitrary planar conflict structure is captured by one symmetric `rho`.

### 3.3 Blind recognition convergence on reduction structure

The source-neutral recognizer now independently identifies a generic `Reduction` pattern in the pinned high-level Four Color proof surface before held-out labels are joined.

The recognition rule uses only mechanically observable structure such as:

- induction/descent;
- case split;
- decision call;
- proof application.

After the blind prediction is frozen, post-hoc evaluation aligns that generic `Reduction` with the held-out `Reducibility` family on the same unit.

This is evidence of structural convergence. It is **not** evidence that the MeTTafy transformation itself is already a formal reducibility proof.

### 3.4 Fail-closed admissible traversal gate

Implemented in `src/mettafy/reducibility_gate.py`.

A stronger admissible-traversal claim requires all of:

```text
independently recognized Reduction candidate
+ complete contradiction/discharge skeleton
+ preserved observable boundary
+ strict decrease of a non-negative well-founded measure.
```

The gate states are:

```text
not_candidate
skeleton_incomplete
certificate_required
certificate_rejected
admissible_traversal
```

The pinned high-level Four Color unit currently reaches:

```text
certificate_required
```

This is intentional. The high-level proof exposes the discharge skeleton, but MeTTafy has not yet extracted an independent boundary object and obstruction measure from the deeper reducibility machinery.

Synthetic positive controls demonstrate that the gate can reach `admissible_traversal` when those obligations are genuinely supplied. Boundary drift or non-decrease fails closed.

## 4. Current central theorem gap

The central unproved bridge remains:

```text
NoStableFifthClass
```

The conditional geometry is already established. The unresolved question is whether the actual planar Four Color problem necessarily supplies the structural conditions that force a putative fifth terminal class to route and then disappear under admissible refinement.

The two main bridge obligations are:

### 4.1 PlanarConflictLowerBound

Need a theorem deriving the relevant effective conflict/coupling bound from planar structure without assuming four-colorability.

The required statement must be strong enough to put the putative fifth class into the four-stable/five-routes regime, or replace the scalar symmetric model with a more general spectral statement that has the same consequence.

Euler's degree argument alone is insufficient: degree-at-most-five supports the Five Color theorem but does not eliminate the fifth color.

### 4.2 AdmissibleRefinementClosure

Need a theorem that the forced SRMF/refinement move:

- preserves the observable boundary obligation;
- changes only admissible latent/internal structure;
- strictly decreases a well-founded obstruction measure;
- can therefore be iterated without cycling;
- cannot stabilize in a fifth terminal semantic class.

The current working correspondence target is:

```text
ReducibilityAsAdmissibleTraversal
```

A satisfactory version should not merely recognize the word or proof pattern "reducible." It should carry a mechanically inspectable certificate of boundary preservation and strict descent.

## 5. Why the Rocq proof matters, and why it is held out

The pinned Rocq proof follows the established high-level structure:

```text
minimal counterexample
  -> unavoidable configuration
  -> reducibility
  -> contradiction.
```

MeTTafy is allowed to inspect this structure as a held-out reference only under the leakage discipline.

The purpose is to ask whether the independently developed Track B machinery converges on the same necessities:

- forcing;
- local reducibility;
- preserved external obligation;
- strict descent;
- contradiction of minimality.

If it does, that is meaningful correspondence. If Track B simply encodes the Rocq labels as recognizer features, the experiment is invalid.

## 6. Intended terminal algebra

The candidate four-channel terminal algebra is

```text
V4 = Z2 x Z2 = {0, a, b, a+b}.
```

A possible SRMF correspondence is currently only a candidate:

```text
TTDC -> 0
TTIE -> a
TTCS -> a+b
TTPR -> b
```

Cardinality alone does not force this group structure.

The decoding lemma under consideration uses representatives of `Z2^2` in `Z^2 / 2Z^2`. If each fuzzy edge value is uniquely within `epsilon < 1/2` of a coset representative, and each vertex residual is bounded by `delta`, then a sufficient exact-decoding condition is

```text
Delta * epsilon + delta < 1,
```

where `Delta` is the maximum incident degree in the decoded flow constraint. In the cubic dual case:

```text
3 epsilon + delta < 1.
```

This is a **decoding** result, not an existence result. Track B must independently produce the fuzzy state satisfying the hypotheses; the existence of a `V4` flow cannot be imported as an oracle.

## 7. Classical downstream transfer boundary

Once an exact nowhere-zero `V4` flow on the appropriate cubic bridgeless planar dual is genuinely available, the remaining transfer is classical:

```text
nowhere-zero V4 flow
  -> Tait 3-edge-coloring of the cubic dual
  -> primal four-coloring.
```

This downstream mathematics may be cited as a trust boundary. It must not be smuggled upstream to establish the existence of the object that Track B is supposed to construct.

## 8. Proof-obligation ledger

| ID | Obligation | Current state |
|---|---|---|
| P1 | Planar representation fidelity | open / partially conventional |
| P2 | Observer quotient laws | conceptual; needs exact theorem surface |
| P3 | `NoStableFifthClass` | **open; central gap** |
| P4 | Terminal quotient algebra is `V4` | open |
| P5 | Nonzero separation | open |
| P6 | Fuzzy-to-exact conservation/decoding | candidate inequality; not full existence proof |
| P7 | Bounded execution/resource theorem | partially certified by observer-critical machinery |
| P8 | Classical transfer trust boundary | available downstream; must remain explicit |
| P9 | Exact final verification | design available; not yet end-to-end |
| P10 | Dependency audit / no hidden 4CT equivalent | ongoing |
| P11 | Amortization/refinement termination | open; tied to descent measure |
| P12 | Observer-critical collapse | **certified** |
| P13 | Imagination detector | **certified as bounded predicate** |
| P14 | Quantum/Born interpretation | optional; explicitly not required for 4CT |

## 9. What would constitute the next genuine mathematical advance

The next high-value result is **not another generic certificate framework**.

It is one of the following concrete bridges:

1. derive a planar spectral/conflict inequality sufficient to force the fifth class into observer-critical routing; or
2. extract from the actual pinned reducibility machinery a source-neutral transformation object with:
   - a mechanically defined boundary;
   - a mechanically defined well-founded measure;
   - proof that the boundary is preserved;
   - proof that the measure strictly decreases;
   - a lift showing a solution of the reduced obligation reconstructs a solution of the source obligation.

Either result would materially narrow `NoStableFifthClass`.

## 10. Human-review questions

A reviewer should currently focus on these questions:

1. Is the symmetric `rho` model merely a useful witness, or can the needed four-vs-five separation be generalized to a spectral condition on arbitrary planar conflict matrices?
2. Is there a non-circular planar invariant that supplies the required lower bound without encoding four-colorability?
3. What is the correct observable boundary for a reducibility traversal?
4. What obstruction measure is both well-founded and genuinely decreased by the reducibility move?
5. Can the lift obligation be stated independently of the known Four Color theorem?
6. Is `V4` structurally forced by the terminal refinement algebra, or only one convenient representation?
7. Does any current step silently import Tait/flow existence rather than only using the downstream equivalence?

A negative answer anywhere is useful: this document is intended to expose the proof's exact failure surface, not to defend it rhetorically.

## 11. Current bottom line

We have **not yet proved the Four Color Theorem by this new route**.

We do have:

- a mechanically certified observer-critical forcing lemma;
- a mechanically certified conditional four-stable/five-routes theorem;
- a leakage-safe structural-recognition program that independently converges on reduction-like structure in the held-out Rocq proof;
- a fail-closed interface specifying what an admissible reducibility traversal must prove;
- a concrete central gap rather than a vague analogy.

The present proof frontier can be summarized as:

```text
conditional fifth-class instability          [proved]
            +
planarity -> required conflict regime         [open]
            +
admissible, terminating refinement            [open]
            +
terminal V4 construction                      [open]
            +
exact decode + classical transfer              [partially specified]
---------------------------------------------------------
new independent Four Color proof               [not yet closed]
```

This file should be updated whenever one of those statuses changes.

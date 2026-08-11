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
planar indexed constraint structure
  -> local five-obligation witness
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

1. represent the planar problem using separately indexed region/vertex parameters without already assuming four-colorability;
2. obtain a degree-five local obstruction in a minimal-counterexample setting and preserve the identity of its five incident constraints even when assigned values coincide;
3. construct the local conflict/coupling operator induced by those five distinct obligations and prove a spectral condition sufficient for observer-critical routing;
4. show four active channels remain solvent while the fifth-obligation representation cannot persist stably;
5. show the forced route is an admissible refinement, not an arbitrary recoloring;
6. show repeated admissible refinement terminates by a well-founded measure;
7. show the terminal four-channel state carries the required `V4 = Z2^2` algebra;
8. decode sufficiently controlled fuzzy states into an exact nowhere-zero `V4` flow;
9. invoke the classical downstream transfer from that exact object to a four-coloring.

The proof is **not closed** because obligations 2–6 are not yet all established for the actual planar Four Color problem.

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

**Semantic correction:** the mechanically certified variable `k` should presently be read as a count of separately indexed active constraint channels. It is not yet licensed to mean "number of colors" or "number of terminal semantic classes." The proof still owes the bridge from the local planar coloring obligations to this channel geometry.

The theorem therefore does **not** prove that planarity forces `rho` into this interval, nor that an arbitrary planar conflict structure is captured by one symmetric `rho`.

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

The conditional geometry is already established. The unresolved question is whether the actual planar Four Color problem supplies the structural conditions that instantiate the five-channel observer geometry and force that representation to route into a terminating four-channel quotient.

The earlier label `PlanarConflictLowerBound` was too coarse. It conflated two different facts:

1. **multiplicity / identity:** how many independently indexed obligations exist;
2. **coupling / conflict:** how strongly those obligations interact in the geometric operator.

These are now separated.

### 4.1 Parameter identity versus value equality

Let `P` be a set of indexed parameters and let

```text
value : P -> X
```

be their current value assignment. Distinct parameter identity does not require distinct values:

```text
p_i != p_j
```

may hold while

```text
value(p_i) = value(p_j).
```

Equivalently, if parameters are represented as indexed pairs

```text
p_i = (i, value_i),
p_j = (j, value_j),
```

then `i != j` keeps the parameter objects distinct even when `value_i = value_j`.

For a graph `G = (V,E)`, the incident coloring obligations at a vertex `v` are indexed by distinct edges or distinct neighboring vertices:

```text
c_(v,u1), ..., c_(v,uk).
```

If `u_i != u_j`, then

```text
c_(v,ui) != c_(v,uj)
```

as obligations, even if the current assignments of `u_i` and `u_j` happen to coincide.

This is the precise form of the "same value, different parameter" observation. It supplies **dimension/multiplicity**, not yet a numerical coupling coefficient.

### 4.2 DistinctIncidentConstraintMultiplicity

The proposed planar bridge now begins with the classical minimal-counterexample route:

```text
planarity
  -> some vertex has degree <= 5
minimal counterexample + reducibility of degree <= 4
  -> every vertex has degree >= 5
therefore
  -> some vertex v has degree exactly 5.
```

At such a vertex, the five incident edge constraints are five separately indexed obligations:

```text
c_(v,u1), ..., c_(v,u5).
```

Their identity survives collisions of assigned values. Thus, if `k` is interpreted as the number of active indexed obligations, the local obstruction genuinely supplies `k = 5` without requiring five numerically distinct values and without calling those obligations five colors.

**Status:** mathematically plausible/classical in outline, but not yet formalized as a Track B theorem. In particular, the degree-`<=4` reducibility step must be stated explicitly rather than hidden inside "minimal counterexample."

### 4.3 SharedConstraintCoupling / spectral bridge

Parameter identity alone does **not** justify the symmetric conflict matrix

```text
G_k = (1 + rho) I - rho J.
```

Five named obligations do not automatically become five pairwise antagonistic directions. This is the remaining genuine geometric bridge.

A safer general formulation introduces a nonnegative symmetric local conflict operator `C_v` on the incident constraint channels and writes

```text
G_v = I - C_v.
```

The observer soft mode is then controlled by

```text
M_v = 1 - lambda_max(C_v).
```

The existing symmetric model is the special case

```text
C_v = rho (J - I),
lambda_max(C_v) = rho (k - 1).
```

So the actual planar obligation is no longer "planarity magically gives rho." It is:

> construct `C_v` from the five separately indexed local coloring obligations and prove a source-independent spectral bound strong enough to cross the observer floor, while an admissible four-channel quotient remains below that threshold.

Schematically, the desired local separation is

```text
lambda_max(C_5) >= 1 - M_O
```

while for the admissible four-channel representation

```text
lambda_max(C_4) < 1 - M_O.
```

The exact relation between `C_5` and `C_4` is still open. It may be a principal restriction, a quotient, or a certificate-bearing refinement rather than literal deletion of one row and column.

**Status:** open; this replaces the vague `PlanarConflictLowerBound` obligation.

### 4.4 AdmissibleRefinementClosure

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
| P3a | `DistinctIncidentConstraintMultiplicity` | newly isolated; classical outline, formalization pending |
| P3b | `SharedConstraintCoupling` / local spectral bound | **open; central geometric gap** |
| P3c | `NoStableFifthClass` | **open; depends on P3a + P3b + refinement closure** |
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

The proof now has a sharper local target:

1. formalize the indexed-parameter lemma and the degree-five local obstruction without importing the Four Color conclusion;
2. define the conflict operator `C_v` induced by the five incident constraints;
3. prove a spectral/Rayleigh bound on `C_v` that crosses the observer threshold;
4. define the admissible four-channel quotient/refinement and prove that its corresponding operator falls on the stable side;
5. connect that transition to a boundary-preserving strict-descent certificate.

An alternative advance would be to extract from the actual pinned reducibility machinery a source-neutral transformation object with:

- a mechanically defined boundary;
- a mechanically defined well-founded measure;
- proof that the boundary is preserved;
- proof that the measure strictly decreases;
- a lift showing a solution of the reduced obligation reconstructs a solution of the source obligation.

Either result would materially narrow `NoStableFifthClass`.

## 10. Human-review questions

A reviewer should currently focus on these questions:

1. Is `k` correctly interpreted as active indexed constraints rather than colors at the observer-critical stage?
2. Does the minimal-counterexample route to a degree-five vertex introduce any hidden Four Color assumption beyond local degree-`<=4` reducibility?
3. What is the principled construction of the local conflict operator `C_v` from incident coloring obligations?
4. Is the symmetric `rho(J-I)` model a justified local special case, or should the proof immediately move to a general spectral/Rayleigh formulation?
5. What is the correct observable boundary for a reducibility traversal?
6. What obstruction measure is both well-founded and genuinely decreased by the reducibility move?
7. Can the lift obligation be stated independently of the known Four Color theorem?
8. Is `V4` structurally forced by the terminal refinement algebra, or only one convenient representation?
9. Does any current step silently import Tait/flow existence rather than only using the downstream equivalence?

A negative answer anywhere is useful: this document is intended to expose the proof's exact failure surface, not to defend it rhetorically.

## 11. Current bottom line

We have **not yet proved the Four Color Theorem by this new route**.

We do have:

- a mechanically certified observer-critical forcing lemma;
- a mechanically certified conditional four-stable/five-routes theorem;
- a now-explicit distinction between parameter identity and value equality;
- a precise local interpretation of `k` as indexed obligation multiplicity rather than color count;
- a leakage-safe structural-recognition program that independently converges on reduction-like structure in the held-out Rocq proof;
- a fail-closed interface specifying what an admissible reducibility traversal must prove;
- a narrower central gap: construct and bound the actual local conflict operator induced by the degree-five planar obstruction.

The present proof frontier can be summarized as:

```text
indexed five-obligation local obstruction        [isolated; formalization pending]
            +
local constraint coupling -> spectral threshold  [open]
            +
conditional four-stable/five-routes geometry     [proved]
            +
admissible, terminating refinement               [open]
            +
terminal V4 construction                         [open]
            +
exact decode + classical transfer                [partially specified]
------------------------------------------------------------
new independent Four Color proof                 [not yet closed]
```

This file should be updated whenever one of those statuses changes.

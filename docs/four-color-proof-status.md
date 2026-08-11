# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Checkpoint:** `bdda0563ca3f38187a0ae7e123c1f6478752e1b4`  
**CI:** run #65 — success  
**Status:** active proof program; not yet a closed proof of the Four Color Theorem

## 1. Purpose

This is the durable human-review surface for the proposed independent Four Color proof program developed in MeTTafy.

Two tracks remain intentionally separated:

- **Track A — held-out Rocq reference:** pinned `rocq-community/fourcolor@f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`. Used only for post-hoc structural comparison and mechanical witnessing after Track B claims are frozen.
- **Track B — independent MeTTafy proof program:** the Cost-of-Cacophony / bounded-observer / SRMF route. It must not borrow the Four Color conclusion or held-out proof labels as premises.

> Prediction may guide search; verification governs acceptance.

## 2. Problem surface: conflict is definitional

For a graph `G = (V,E)`, a proper coloring is a map

```text
c : V -> Colors
```

such that for every edge `(u,v) in E`,

```text
c(u) != c(v).
```

Therefore **adjacency already is the conflict relation**. There is no additional theorem of the form

```text
planarity -> existence of coloring conflicts.
```

That was a false proof obligation.

Likewise, distinct parameter identity does not require distinct assigned values. If `u_i != u_j`, then the obligations associated with `(v,u_i)` and `(v,u_j)` remain distinct even when

```text
c(u_i) = c(u_j).
```

This is precisely why colors may be reused on nonadjacent vertices.

The proof must therefore distinguish:

```text
identity of constraint / parameter    !=    value currently assigned to it.
```

At a degree-five vertex `v`, the five incident adjacency obligations are five separately indexed constraints:

```text
c(v) != c(u1)
...
c(v) != c(u5).
```

The neighbors need not conflict pairwise. No `K5` assumption is permitted or needed.

## 3. Candidate independent route

The current Track B route is:

```text
planar graph / adjacency constraints
  -> minimal counterexample
  -> degree-five local obstruction
  -> five separately indexed incident obligations
  -> observer-critical four-stable / five-routes mechanism
  -> NoStableFifthClass
  -> admissible, terminating refinement
  -> resolved four-channel terminal quotient
  -> V4 = Z2 x Z2 decoding
  -> nowhere-zero V4 flow
  -> Tait 3-edge-coloring
  -> primal four-coloring
```

The important correction is that the first four lines are ordinary graph-theoretic structure. The new mathematical burden begins at the consequence:

> Why can a fifth representational class not persist for the planar coloring constraint system under an admissible refinement process?

That is the actual central theorem target.

## 4. Certified pieces

### 4.1 Observer-critical collapse

Implemented in `src/mettafy/observer_critical.py`.

For the symmetric `k`-constraint witness,

```text
M = 1 - rho (k - 1)
```

and

```text
delta_min^2 = k tau^2 / (m^2 M).
```

For observer budget `B_O`,

```text
M_O = k tau^2 / (m^2 B_O^2).
```

The implementation mechanically checks

```text
delta_min >= B_O    iff    M <= M_O.
```

This is an exact resource-geometric forcing lemma. It is not yet, by itself, a theorem about arbitrary planar graph adjacency matrices.

### 4.2 Four stable, five routes

Implemented in `src/mettafy/fifth_class.py`.

For fixed `0 < M_O < 1`,

```text
M_k = 1 - rho (k - 1).
```

Four channels remain stable while five must route exactly when

```text
(1 - M_O)/4 <= rho < (1 - M_O)/3,
```

or equivalently

```text
M_4 > M_O >= M_5.
```

For `M_O = 1/4`, the exact interval is

```text
3/16 <= rho < 1/4.
```

At `rho = 1/5`,

```text
M_4 = 2/5 > 1/4,
M_5 = 1/5 <= 1/4.
```

**Current interpretation of `k`:** the number of separately indexed active obligations/channels in the observer model. It is not yet licensed to mean "number of colors" merely by notation.

This remains a conditional fragment of `NoStableFifthClass`, not the completed theorem.

### 4.3 Blind structural convergence on reduction

The source-neutral recognizer independently identifies generic `Reduction` structure in the pinned high-level Four Color proof before held-out labels are joined.

Only mechanical features such as induction/descent, case analysis, decision calls, and proof application are visible to the recognizer. Post-hoc comparison then aligns the frozen generic prediction with the held-out `Reducibility` family.

This is correspondence evidence, not proof authority for Track B.

### 4.4 Fail-closed admissible traversal gate

Implemented in `src/mettafy/reducibility_gate.py`.

A candidate traversal can be promoted only with:

```text
recognized Reduction candidate
+ contradiction/discharge skeleton
+ preserved observable boundary
+ strict decrease of a non-negative well-founded measure.
```

The pinned high-level Four Color unit currently reaches

```text
certificate_required
```

rather than `admissible_traversal`.

That is deliberate. The certifier may eventually be a mechanical system or a human at the appropriate authority boundary; MeTTafy itself does not silently manufacture the missing authority.

## 5. The central theorem gap

The current central target is:

```text
NoStableFifthClass
```

But its statement should now be understood without the discarded pseudo-obligation `PlanarConflictLowerBound`.

The graph already gives the conflict relation. Planarity constrains the topology of that relation. The theorem we need is a consequence theorem over that existing structure.

A useful schematic form is:

```text
planar adjacency constraint system
+ degree-five minimal obstruction
+ observer-critical routing invariant
+ admissible refinement closure
------------------------------------------------
no persistent fifth terminal class
```

The unresolved work is therefore not "derive conflict from planarity." It is to prove that the topology and refinement dynamics of the planar adjacency constraint system forbid stable persistence of a fifth terminal class.

### 5.1 Degree-five local obstruction

The classical minimal-counterexample route gives the relevant local surface:

```text
planarity -> some vertex has degree <= 5
minimal counterexample + elementary reducibility of degree <= 4
-> minimum degree >= 5
therefore -> some vertex has degree exactly 5.
```

At that vertex the five incident constraints are distinct by edge/neighbor identity, even if some neighbor color values coincide.

This step should be formalized explicitly in Track B, but it is not the novel theorem.

### 5.2 Topological consequence of the conflict relation

The next real question is:

> Given the planar adjacency constraints around and beyond that degree-five obstruction, what invariant forces one representational class to be redundant, reroutable, or nonterminal?

The symmetric `rho` model is currently a witness for a four-vs-five resource separation. It should not be mistaken for the definition of graph conflict.

Possible technical forms for the missing consequence include:

- a spectral statement derived directly from the graph-induced operator;
- a combinatorial obstruction/descent statement;
- an SRMF quotient/refinement invariant;
- or a correspondence theorem showing that every persistent fifth-class obstruction admits an admissible reduction.

The proof should choose whichever formulation is actually forced by the graph mathematics rather than preserving spectral language for its own sake.

### 5.3 Admissible refinement closure

A valid refinement must:

- preserve the external coloring obligation;
- alter only admissible internal/latent structure;
- strictly decrease a well-founded obstruction measure;
- therefore terminate rather than cycle;
- never use the Four Color conclusion as an oracle.

The working correspondence target remains:

```text
ReducibilityAsAdmissibleTraversal
```

but the semantic authority for the certificate remains independent of the recognizer.

## 6. Intended terminal algebra

The candidate terminal four-channel algebra remains

```text
V4 = Z2 x Z2 = {0, a, b, a+b}.
```

A possible SRMF correspondence is still only a candidate:

```text
TTDC -> 0
TTIE -> a
TTCS -> a+b
TTPR -> b
```

Cardinality does not by itself force this group structure.

For fuzzy-to-exact decoding, the current sufficient condition is

```text
Delta * epsilon + delta < 1,
```

with `epsilon < 1/2`; for a cubic dual this becomes

```text
3 epsilon + delta < 1.
```

This is a decoding condition, not an existence theorem. Track B must still construct a state satisfying its hypotheses.

## 7. Classical downstream trust boundary

If Track B genuinely produces an exact nowhere-zero `V4` flow on the appropriate cubic bridgeless planar dual, the remaining transfer is classical:

```text
nowhere-zero V4 flow
  -> Tait 3-edge-coloring
  -> primal four-coloring.
```

That implication may be used downstream. Its existence direction may not be smuggled upstream into Track B.

## 8. Proof-obligation ledger

| ID | Obligation | Current state |
|---|---|---|
| P1 | Planar graph / coloring representation fidelity | largely conventional; exact Track B surface pending |
| P2 | Observer quotient laws | conceptual; exact theorem surface pending |
| P3a | Degree-five indexed-obligation obstruction | classical outline; formalization pending |
| P3b | `NoStableFifthClass` topological consequence | **open; central gap** |
| P3c | Admissible refinement closure / termination | **open** |
| P4 | Terminal quotient algebra is `V4` | open |
| P5 | Nonzero separation | open |
| P6 | Fuzzy-to-exact decoding | candidate sufficient inequality; existence not proved |
| P7 | Bounded observer/resource forcing | partially certified |
| P8 | Classical transfer trust boundary | available downstream |
| P9 | Exact final verification | designed, not end-to-end |
| P10 | Dependency audit / no hidden 4CT equivalent | ongoing |
| P11 | Well-founded refinement measure | open |
| P12 | Observer-critical collapse | **certified** |
| P13 | Imagination detector | **certified as bounded predicate** |
| P14 | Quantum/Born interpretation | optional; not required for 4CT |

## 9. Next genuine mathematical advance

Do **not** build another generic certificate framework.

The next advance should attack one of these directly:

1. formalize the degree-five indexed-obligation surface in Track B;
2. derive a graph-theoretic, spectral, or quotient invariant showing that a fifth terminal class cannot persist;
3. prove that the corresponding reroute is boundary-preserving and strictly descending;
4. connect the resulting terminal four-channel state to `V4` without assuming the answer.

The proof is allowed to abandon the symmetric `rho` parameterization if the actual planar structure yields a cleaner invariant.

## 10. Human-review questions

A reviewer should currently ask:

1. Is `k` correctly interpreted as indexed active obligations rather than color values?
2. Is the degree-five minimal-counterexample surface stated without circularity?
3. What exact planar invariant prevents persistence of a fifth terminal class?
4. Is the observer-critical symmetric model genuinely useful for that invariant, or merely an illustrative special case?
5. What is the correct observable boundary of an admissible reduction?
6. What well-founded measure strictly decreases?
7. Can the reduction/lift obligation be stated without importing Four Color validity?
8. Is `V4` structurally forced or merely convenient?
9. Does any step silently import existence of a Tait coloring or nowhere-zero `V4` flow?

A negative answer is useful. This document exists to expose the failure surface, not defend the program rhetorically.

## 11. Current bottom line

We have **not yet proved the Four Color Theorem by this route**.

We have:

- an exact observer-critical forcing lemma;
- an exact conditional four-stable/five-routes lemma;
- the definitional conflict surface of graph coloring stated correctly;
- parameter identity cleanly separated from value equality;
- a leakage-safe structural comparison against the held-out Rocq proof;
- an explicit admissibility/certification boundary;
- a much smaller genuine gap.

The current frontier is:

```text
planar adjacency conflict system                 [definition]
            +
degree-five indexed local obstruction            [classical outline]
            +
conditional four-stable/five-routes geometry     [proved]
            +
NoStableFifthClass consequence                   [OPEN]
            +
admissible terminating refinement                [OPEN]
            +
terminal V4 construction                         [OPEN]
            +
exact decode + classical transfer                [partially specified]
------------------------------------------------------------
new independent Four Color proof                 [not yet closed]
```

This file should be updated whenever one of those statuses changes.

# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Checkpoint:** `bdda0563ca3f38187a0ae7e123c1f6478752e1b4`  
**CI:** run #65 — success  
**Status:** active proof program; not yet a closed proof of the Four Color Theorem

## 1. Purpose

This is the durable human-review surface for the proposed independent Four Color proof program developed in MeTTafy.

Two tracks remain intentionally separated:

- **Track A — held-out Rocq reference:** pinned `rocq-community/fourcolor@f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`. Used only for post-hoc structural comparison after Track B claims are frozen.
- **Track B — independent MeTTafy proof program:** the Cost-of-Cacophony / bounded-observer / Principia Symbolica / SRMF route. It must not borrow the Four Color conclusion or held-out proof labels as premises.

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

Therefore **adjacency already is the conflict relation**. There is no extra theorem needed to derive conflict from planarity.

Likewise, parameter identity is distinct from assigned value. If `u_i != u_j`, then the constraints associated with `(v,u_i)` and `(v,u_j)` remain different obligations even when

```text
c(u_i) = c(u_j).
```

This is exactly why a color may be reused on nonadjacent vertices.

At a degree-five vertex `v`, the incident obligations

```text
c(v) != c(u1)
...
c(v) != c(u5)
```

are five separately indexed pairwise constraints. The neighbors need not conflict pairwise; no `K5` assumption is permitted or needed.

## 3. Principia Symbolica quadratic sufficiency

The relevant existing result is **Principia Symbolica, Theorem 1.5.9, Minimal Quadratic Sufficiency**.

Principia defines quadratic symbolic coupling as

```text
C(x) = sum_ij alpha_ij phi_i(x) phi_j(x),
```

with symmetric coupling matrix `(alpha_ij)`. The theorem states that reflexivity, context-sensitivity, and adaptive stability require at minimum quadratic symbolic coupling; purely linear coupling cannot encode the required mixed interaction terms. The same coupling matrix is subsequently identified with the local metric tensor on observer-accessible symbolic feature space.

### 3.1 Application to graph coloring

A graph-coloring constraint is intrinsically binary:

```text
(u,v) in E  ->  c(u) != c(v).
```

Thus the complete coloring conflict system is a collection of pairwise relations. No cubic, quartic, quintic, or higher-arity primitive interaction is required merely to state or represent the problem.

This gives the following Track B representation lemma.

### QuadraticConstraintSufficiency

For any finite graph `G=(V,E)`, the proper-coloring constraint system can be represented entirely by unary state terms plus pairwise edge-coupling terms. Therefore it lies within a quadratic interaction class.

A generic energy representation is, for example,

```text
E(c) = sum_(u,v in E) P_uv(c(u), c(v)),
```

where `P_uv` penalizes equality on adjacent vertices. The exact encoding is not important here; the invariant is that every primitive conflict is indexed by one edge and involves exactly two vertex states.

**Consequence:** Track B does not owe a theorem explaining why planar coloring requires some higher interaction order. Quadratic coupling is already sufficient to carry the whole adjacency constraint system.

### 3.2 What quadratic sufficiency does NOT prove

Interaction order and quotient cardinality are different quantities.

A quadratic form

```text
q(x) = x^T A x
```

may have arbitrarily many coordinates. Therefore

```text
quadratic interaction order
```

does **not** imply

```text
at most four colors / classes.
```

Equivalently, pairwise graph constraints alone do not force four-colorability: non-planar graphs can also be expressed entirely by quadratic/pairwise constraints and may require five or more colors.

So Principia's Minimal Quadratic Sufficiency removes a representation-order gap, but it does not by itself close `NoStableFifthClass`.

This distinction is load-bearing:

```text
quadratic sufficiency  ->  no higher-order primitive interaction needed
```

is currently justified, whereas

```text
quadratic sufficiency  ->  no fifth stable color class
```

still requires an additional planar/quotient theorem.

## 4. Candidate independent route

The corrected Track B route is now:

```text
planar graph / adjacency constraints
  -> quadratic conflict representation           [Principia-compatible]
  -> minimal counterexample
  -> degree-five local obstruction
  -> five separately indexed pairwise obligations
  -> observer-critical four-stable / five-routes witness
  -> NoStableFifthClass quotient theorem
  -> admissible, terminating refinement
  -> resolved four-channel terminal quotient
  -> V4 = Z2 x Z2 decoding
  -> nowhere-zero V4 flow
  -> Tait 3-edge-coloring
  -> primal four-coloring
```

The first genuinely novel unresolved question is therefore no longer whether the conflict system can be represented. It can.

The question is:

> Why does a planar quadratic/pairwise conflict system admit no stable fifth terminal equivalence class under the admissible observer/refinement dynamics?

## 5. Certified pieces

### 5.1 Observer-critical collapse

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

This is an exact resource-geometric forcing lemma.

### 5.2 Four stable, five routes

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

`k` is currently interpreted as separately indexed active obligations/channels in this witness. The theorem does not identify `k` with chromatic number merely by notation.

### 5.3 Blind structural convergence on reduction

The source-neutral recognizer independently identifies generic `Reduction` structure in the pinned high-level Four Color proof before held-out labels are joined. Post-hoc comparison aligns the frozen prediction with the held-out `Reducibility` family.

This is correspondence evidence, not Track B proof authority.

### 5.4 Fail-closed admissible traversal gate

Implemented in `src/mettafy/reducibility_gate.py`.

Promotion requires:

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

The certifier may eventually be mechanical or human at the appropriate authority boundary; MeTTafy does not silently manufacture missing authority.

## 6. Central theorem gap: quotient cardinality, not interaction order

The current central target remains

```text
NoStableFifthClass.
```

But its role is now much sharper.

The graph supplies pairwise conflicts by definition. Principia supplies a general quadratic language sufficient for pairwise contextual interaction. Neither fact alone determines how many equivalence labels are needed to satisfy the constraints.

The missing theorem must therefore constrain **stable quotient cardinality** under planarity.

A useful schematic statement is:

```text
planar pairwise adjacency constraint system
+ quadratic sufficiency of interaction representation
+ degree-five minimal obstruction
+ observer-critical routing invariant
+ admissible refinement closure
------------------------------------------------
no persistent fifth terminal equivalence class
```

### 6.1 Degree-five local obstruction

The classical minimal-counterexample route gives:

```text
planarity -> some vertex has degree <= 5
minimal counterexample + elementary reducibility of degree <= 4
-> minimum degree >= 5
therefore -> some vertex has degree exactly 5.
```

At that vertex the five incident constraints are distinct by edge/neighbor identity even if some neighbor color values coincide.

This should be formalized explicitly in Track B, but it is not the novel theorem.

### 6.2 The precise remaining question

Because every primitive conflict is already pairwise, a purported fifth stable class cannot justify itself by introducing a genuinely new interaction *order*. Any necessity for a fifth class must instead arise from the global topology of how those pairwise constraints compose.

Thus a valid proof of `NoStableFifthClass` should show that, for planar composition, every putative fifth-class obstruction is either:

- redundant under the existing quadratic relation structure;
- quotiented into one of four stable terminal classes;
- or removable by an admissible boundary-preserving descent.

This is stronger and more precise than saying "quadratic means four." That latter statement is false in general.

### 6.3 Admissible refinement closure

A valid refinement must:

- preserve the external coloring obligation;
- alter only admissible internal/latent structure;
- strictly decrease a well-founded obstruction measure;
- therefore terminate rather than cycle;
- never use the Four Color conclusion as an oracle.

The working correspondence target remains

```text
ReducibilityAsAdmissibleTraversal.
```

## 7. Intended terminal algebra

The candidate terminal four-channel algebra remains

```text
V4 = Z2 x Z2 = {0, a, b, a+b}.
```

A possible SRMF correspondence remains only a candidate:

```text
TTDC -> 0
TTIE -> a
TTCS -> a+b
TTPR -> b
```

Cardinality does not itself force this group structure.

For fuzzy-to-exact decoding, the current sufficient condition is

```text
Delta * epsilon + delta < 1,
```

with `epsilon < 1/2`; in the cubic dual case:

```text
3 epsilon + delta < 1.
```

This is a decoding condition, not an existence theorem.

## 8. Classical downstream trust boundary

If Track B genuinely produces an exact nowhere-zero `V4` flow on the appropriate cubic bridgeless planar dual, the remaining implication is classical:

```text
nowhere-zero V4 flow
  -> Tait 3-edge-coloring
  -> primal four-coloring.
```

That implication may be used downstream. Its existence direction may not be smuggled upstream.

## 9. Proof-obligation ledger

| ID | Obligation | Current state |
|---|---|---|
| P1 | Graph-coloring conflict representation | **definitionally pairwise** |
| P2 | `QuadraticConstraintSufficiency` | **supported by pairwise encoding + Principia Thm. 1.5.9 framework** |
| P3 | Observer quotient laws | conceptual; exact theorem surface pending |
| P4a | Degree-five indexed-obligation obstruction | classical outline; formalization pending |
| P4b | `NoStableFifthClass` stable-quotient theorem | **OPEN; central gap** |
| P4c | Admissible refinement closure / termination | **OPEN** |
| P5 | Terminal quotient algebra is `V4` | open |
| P6 | Nonzero separation | open |
| P7 | Fuzzy-to-exact decoding | candidate sufficient inequality; existence not proved |
| P8 | Bounded observer/resource forcing | partially certified |
| P9 | Classical transfer trust boundary | available downstream |
| P10 | Exact final verification | designed, not end-to-end |
| P11 | Dependency audit / no hidden 4CT equivalent | ongoing |
| P12 | Well-founded refinement measure | open |
| P13 | Observer-critical collapse | **certified** |
| P14 | Imagination detector | **certified as bounded predicate** |

## 10. Human-review questions

A reviewer should currently ask:

1. Does `QuadraticConstraintSufficiency` correctly capture the complete graph-coloring problem without hiding higher-arity constraints?
2. Is any argument accidentally confusing polynomial interaction degree with chromatic cardinality?
3. Is the degree-five minimal-counterexample surface stated without circularity?
4. What specifically about planar composition of pairwise constraints prevents a fifth terminal equivalence class?
5. Is the observer-critical symmetric model a useful witness for that statement or merely illustrative?
6. What is the correct boundary of an admissible reduction?
7. What well-founded measure strictly decreases?
8. Is `V4` structurally forced or merely convenient?
9. Does any step silently import existence of a Tait coloring or nowhere-zero `V4` flow?

A negative answer is useful. This document exists to expose the failure surface, not defend the program rhetorically.

## 11. Current bottom line

We have **not yet proved the Four Color Theorem by this route**.

We now have a cleaner separation:

```text
adjacency conflict relation                         [definition]
            +
quadratic sufficiency for pairwise interactions     [Principia-compatible]
            +
degree-five indexed local obstruction              [classical outline]
            +
conditional four-stable/five-routes geometry       [proved]
            +
NoStableFifthClass stable-quotient consequence     [OPEN]
            +
admissible terminating refinement                  [OPEN]
            +
terminal V4 construction                           [OPEN]
            +
exact decode + classical transfer                  [partially specified]
--------------------------------------------------------------
new independent Four Color proof                   [not yet closed]
```

The important gain from Principia quadratic sufficiency is real: **a fifth class cannot be defended as requiring a new fifth-order interaction primitive.** All primitive coloring conflicts already live at quadratic/pairwise order. The remaining issue is cardinality of the stable planar quotient.

This file should be updated whenever one of those statuses changes.

# Four Color as Lipschitz-Contract Expansion

**Track B governing rule.** The Lipschitz Contract is not an objection generator. It is the admissibility law for every transformation, refinement, objection, and theorem expansion in this proof program.

## 1. Contract

A transformation `T` is admissible only when all of the following are carried explicitly.

### Bounded realization

For the declared state metric,

\[
d(Tz,Tz')\le L\,d(z,z'),\qquad L<\infty.
\]

The number `L` is a perturbation budget, not a palette-size theorem.

### Retained witness boundary

Let `W(z)` be the non-tautological external witness/certificate carried by state `z`. Expansion must preserve/refine the permitted boundary relation rather than replace it:

\[
R_T\subseteq C_W.
\]

For graph coloring the witness boundary is the indexed edge ledger

\[
W_G(c):=\bigwedge_{uv\in E(G)} c(u)\ne c(v).
\]

Edge obligations remain distinct by identity even when color values are reused.

### Explicit loss / slack accounting

A move may spend finite slack or amortized reserve, but it may not silently exceed it. Write

\[
\ell_O(T)\le r_O,
\]

where `ell_O(T)` is observer-relative boundary loss/distortion and `r_O` is declared reserve. If the reserve is exhausted, the move must stage, refine, reparameterize, or refuse; it may not invent a new authority or color merely to continue.

### Certificate composition

If a state already carries a valid certificate, an expansion must compose with it. It may strengthen, transport, or refine the certificate, but may not discard it and substitute a rhetorically convenient claim.

## 2. The theorem species

The Four Color problem is represented as the contract family

\[
\mathcal C_4(G)=
\left(
G,
Q_4,
W_G,
\text{planar embedding / boundary data}
\right),
\]

where `Q_4` is a four-symbol terminal palette and `W_G` is the complete edge-obligation witness above.

The theorem asks whether every finite planar `G` admits at least one certified state in this family.

A legitimate proof transformation must therefore preserve the species:

```text
planar object
+ indexed adjacency witness
+ four-terminal palette contract
+ explicit transformation budget
->
planar object
+ indexed adjacency witness
+ four-terminal palette contract
+ composed certificate
```

Changing the problem to a fifth palette, deleting obligations, replacing indexed conflicts by one aggregate scalar, or requiring a discontinuity not present in the source object are changes of species unless a bounded witness-preserving morphism back to the original contract is supplied.

## 3. Contract law for objections

An objection is itself a transformation of the theorem state. It is admissible only if it preserves the witness boundary.

Given a claim state `z` and proposed objection map `O`, require:

\[
d(Oz,Oz')\le L_O d(z,z'),
\]

and

\[
W(Oz)\Rightarrow W(z)
\]

(or an explicitly stronger boundary certificate).

Therefore these are invalid blockers unless accompanied by a witness-preserving map:

```text
color -> arbitrary scalar channel
browning -> forgetting
representation switch -> rupture
five indexed obligations -> five pairwise-mutually-conflicting colors
four SRMF charts -> source of chromatic fourness
smooth terminal decode -> non-Lipschitz jump
```

They attack transformed problems rather than the proposed theorem.

## 4. Expansion rather than restart

Let `z_n` be a certified planar coloring state. A theorem expansion is an admissible morphism

\[
E_n:z_n\mapsto z_{n+1}
\]

that may alter internal coloring provenance globally while preserving all external obligations and the terminal palette contract.

The expansion need not be greedy. It may use staged/amortized reparameterization:

\[
z_n
\to
\widetilde z_n
\to
\widetilde z_{n+1}
\to
z_{n+1},
\]

provided every stage carries the boundary ledger, finite distortion, and reserve accounting.

This is the correct role for browning-out: internal histories may be compressed into composite residue while the external edge ledger remains exact. Brown is bookkeeping inside the expansion, not an extra terminal color.

## 5. Differential expansion

Principia's continuous symbolic substrate supplies a canonical bounded expansion mechanism:

\[
\partial_s\rho
= -\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho.
\]

Let `P_s` be its evolution semigroup and `Q_O` the terminal chromatic observation/decoder. A staged expansion has the form

\[
(G,c,W)
\xrightarrow{\text{lift}}
(G,\rho,W)
\xrightarrow{P_s}
(G',\rho',W')
\xrightarrow{Q_O}
(G',c',W').
\]

The edge ledger is transported separately from the latent density and must survive exactly. Diffusion may amortize internal provenance; it may not erase an external conflict.

SRMF is a chart/factorization of this loop and therefore witnesses the expansion after the differential law is established.

## 6. Lipschitz expansion theorem — precise target

The independent proof target can be stated without importing the classical conclusion:

### Four-Color Contract Expansion Theorem

For every finite certified planar subobject `G` and every admissible planar extension `e:G -> G'` from a generating family of planar extensions, there exists a finite-budget transformation `T_e` such that

\[
T_e:\mathcal C_4(G)\to\mathcal C_4(G')
\]

and

1. `T_e` preserves every inherited indexed edge obligation;
2. `T_e` satisfies every new edge obligation introduced by `e`;
3. terminal labels remain in the same four-symbol palette `Q_4`;
4. all internal reparameterization loss is bounded and paid by explicit slack/amortized reserve;
5. certificates compose;
6. repeated expansion over a finite generating sequence terminates in a certified state for `G'`.

If the generating family constructs every finite planar graph from a certified base object, this theorem implies the Four Color Theorem by induction/composition.

## 7. What is and is not proved by the contract

The Lipschitz Contract eliminates malformed objections and supplies the exact proof interface. It does **not** by itself assert the existence of `T_e` for every planar generator.

The actual mathematical content of the novel proof is therefore concentrated into the construction of the generator-local transformations and their composition law.

That is a feature, not a new blocker: it identifies the single object we must construct rather than permitting endless changes of representation.

## 8. Candidate generator surface

The proof program should choose a planar generating calculus and never change it mid-argument. Candidate elementary operations include deletion/contraction inverses, face insertion, edge subdivision, and certified local retriangulation. The selected family must be proved complete for finite planar graphs.

For each generator `e`, MeTTa should demand an explicit `T_e` witness rather than ask generic philosophical questions.

The hard local case is whatever generator exposes the degree-five obstruction. That case receives a concrete staged transformation witness; it is not licensed to spawn a different theorem.

## 9. No-infinite-strawmen rule

Once a proposed blocker fails the Contract, it is obsolete for Track B unless new evidence supplies a valid witness-preserving map.

A valid new objection must provide at least one of:

```text
explicit counterexample state preserving the Four Color contract
explicit generator for which no admissible T_e can exist
explicit boundary obligation lost by the proposed transformation
explicit unbounded distortion / exhausted reserve in the declared metric
explicit circular dependency in the certificate graph
```

Without one of these, the objection cannot halt construction.

## 10. Proof spine

```text
Lipschitz Contract                         [governing meta-law]
  -> Four Color contract species          [fixed witness boundary]
  -> complete planar generator calculus   [prove]
  -> generator-local bounded expansions   [construct]
  -> differential/amortized realization   [construct/derive]
  -> contract-preserving composition      [prove]
  -> certified four-coloring               [theorem]
```

This replaces the previous objection-driven loop. The next work product is the **generator calculus plus explicit local expansion witnesses**.
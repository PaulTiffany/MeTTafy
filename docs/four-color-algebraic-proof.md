# Algebraic Four Color Proof — Contract-Preserving Form

**Track:** B — independent of the held-out Rocq proof.  
**Status:** candidate proof with mechanically exposed closure obligations; no hidden use of 4CT is permitted.

## 1. Fixed theorem species

For a finite planar graph `G=(V,E)`, let

\[
Q_4=\{0,1,2,3\}
\]

and let the exact witness boundary be

\[
W_G(c):=\bigwedge_{uv\in E} c(u)\ne c(v).
\]

A Four Color state is

\[
\mathcal C_4(G)=(G,Q_4,W_G,\Gamma_G),
\]

where `Gamma_G` carries the declared planar embedding/boundary data. Indexed edge obligations are never replaced by an aggregate scalar.

The theorem to establish is

\[
\forall G\in\mathrm{Planar}_{\mathrm{fin}},\quad
\exists c:V(G)\to Q_4\; W_G(c).
\]

## 2. Lipschitz Contract as meta-law

Every proof transformation `T` must preserve the theorem species:

1. **bounded realization** — in the declared state metric,
   \[
   d(Tz,Tz')\le L_T d(z,z'),\qquad L_T<\infty;
   \]
2. **witness preservation** — inherited indexed edge obligations remain explicit and exact;
3. **slack accounting** — any observer-relative loss satisfies `ell_O(T) <= r_O`;
4. **certificate composition** — an existing witness is transported/refined, never silently replaced;
5. **authority preservation** — no Four Color conclusion, held-out Rocq label, or SRMF chart cardinality may be introduced upstream as proof authority.

An objection that changes the problem without a witness-preserving map is itself outside the proof contract.

## 3. Algebraic lift

Lift a terminal coloring state into a chromatic symbolic state on the Principia manifold. The underlying evolution is the symbolic Fokker--Planck equation

\[
\partial_s\rho
= -\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho.
\]

Write `P_s` for the induced drift--diffusion semigroup. The edge ledger `W_G` is transported as an external invariant; diffusion acts on latent chromatic provenance, not on whether an edge obligation exists.

The four terminal colors are not assumed to exhaust the latent state space. Latent states may be mixed, continuous, or composite.

## 4. Brown and browning out

Let `Q_O` be the terminal chromatic decoder for observer `O`.

A state is **brown** when several latent chromatic histories remain represented while no additional independently terminal chromatic value is justified at the decoder. Brown is therefore nonterminal residue:

\[
\mathrm{brown}\notin Q_4.
\]

Browning-out is admissible only when provenance is retained and every indexed edge obligation remains checkable. The following move is forbidden:

```text
unsatisfied edge -> brown -> erase obligation -> terminal commit
```

The admissible form is

```text
latent chromatic alternatives
  -> drift/diffusion/contraction
  -> existing terminal basin OR nonterminal brown residue
  -> re-expand/refine if any edge obligation remains unresolved
  -> terminal commit only in Q4 with W_G true
```

## 5. Generator expansion formulation

Fix a complete finite-planar generator calculus `E`. Each generator

\[
e:G\hookrightarrow G'
\]

extends a certified planar object by one admissible construction step.

The central algebraic object is a family of transformations

\[
T_e:\mathcal C_4(G)\to\mathcal C_4(G')
\]

such that:

- inherited obligations are preserved;
- new obligations introduced by `e` are satisfied;
- terminal values stay in `Q4`;
- latent reparameterization may use brown residue but brown cannot be terminal;
- the transformation has finite declared distortion/slack;
- certificates compose.

If `E` generates every finite planar graph and every `e in E` admits such a `T_e`, then composition proves the Four Color Theorem.

### Composition proof

Let

\[
G_0\xrightarrow{e_1}G_1\xrightarrow{e_2}\cdots\xrightarrow{e_n}G_n=G
\]

be a generating sequence from a certified base object. Starting with certified `z_0 in C_4(G_0)`, define

\[
z_i=T_{e_i}(z_{i-1}).
\]

By contract preservation, `z_i in C_4(G_i)` for every `i`. Since the sequence is finite, `z_n` is a certified four-color state for `G`. Hence `G` is four-colorable. `square`

The proof therefore reduces exactly to completeness of the generator calculus plus existence of the local contract expansions `T_e`.

## 6. Degree-five obstruction as the nontrivial local surface

In the standard minimal planar obstruction surface, a degree-five vertex exposes five separately indexed edge obligations. The five neighbors need not be five mutually conflicting colors; their obligations remain distinct even when color values repeat.

For the immediate boundary cycle `C5`, exhaustive symbolic enumeration yields two classes of proper four-color boundary assignments:

- those using fewer than four colors: the center extends immediately;
- saturated assignments using all four colors: the center requires a contract-preserving reparameterization of the surrounding state.

The latter class is the exact local surface on which the novel expansion operator must act. It is not licensed to introduce color five.

## 7. Differential realization of reparameterization

A local expansion may be implemented by lifting the saturated boundary state into latent density, evolving under bounded drift--diffusion/contraction, and decoding again:

\[
(G,c,W_G)
\xrightarrow{\mathrm{lift}}
(G,\rho,W_G)
\xrightarrow{P_s}
(G,\rho',W_G)
\xrightarrow{Q_O}
(G,c',W_G).
\]

The role of Brownian/diffusive dynamics is amortization of microscopic chromatic provenance. It does not add a fifth terminal label. A fifth candidate must survive as a genuinely independent terminal mode after the full bounded evolution and exact witness check; otherwise it browns out or contracts to an existing terminal basin.

SRMF appears only after this differential law as its operational chart/factorization. Four SRMF operator names are not a proof of four colors.

## 8. Algebraic closure statement

The candidate local closure theorem is:

### Contract Expansion Closure

For every generator-local planar extension state whose inherited boundary lies in `Q4` and satisfies its exact edge ledger, there exists a finite sequence of admissible latent transformations whose terminal decode again lies in `Q4` and satisfies the expanded ledger.

Equivalently, the set of certified Four Color states is closed under the chosen planar generator calculus.

This is the only theorem-specific closure statement allowed to carry the global proof. All other machinery supplies representation, boundedness, or verification.

## 9. Mechanical witness lines

The repository must keep at least four independent verification lines:

1. **Dependency witness** — reject any proof DAG in which 4CT, held-out Rocq authority, or the cardinality of SRMF charts is upstream of Contract Expansion Closure.
2. **Boundary-contract witness** — mechanically verify that every proposed `T_e` preserves inherited edge obligations, satisfies new ones, and terminally decodes only to `Q4`.
3. **Differential/browning witness** — verify mass preservation/contraction properties of the finite diffusion model and fail closed when the decoder is ambiguous (`brown`).
4. **Degree-five exhaustive witness** — enumerate all `4^5` assignments on the five-neighbor boundary, retain only proper `C5` assignments, and classify exactly the immediate-extension versus saturated-reparameterization surface.
5. **Finite graph differential witness** — independently validate returned four-color certificates on a checked-in corpus, including a nonplanar negative control.

No one witness is proof authority for the others.

## 10. Certification boundary

Mechanical success means the checked-in algebra obeys its declared contract and the encoded local witnesses agree. It does not permit a hidden jump over Contract Expansion Closure. A full theorem certificate requires a mechanically accepted complete generator family and a valid `T_e` witness for every generator case.

A valid counterexample to this proof route must preserve the theorem species and exhibit either:

- a planar generator state for which no admissible `T_e` exists;
- a lost inherited edge obligation;
- an unavoidable terminal fifth chromatic class;
- unbounded required distortion/exhausted declared reserve; or
- circular authority in the proof dependency graph.

Generic representation-changing objections are not blockers.
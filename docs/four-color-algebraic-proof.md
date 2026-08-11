# Algebraic Four Color Proof — Contract-Preserving Form

**Track:** B — independent of the held-out Rocq proof.  
**Status:** candidate constructive proof with mechanically exposed closure obligations; no hidden use of 4CT is permitted.

## 1. Fixed theorem species

For a finite planar graph `G=(V,E)`, let

\[
Q_4=\{0,1,2,3\}
\]

and let the exact terminal witness be

\[
W_G(c):=\bigwedge_{uv\in E} c(u)\ne c(v).
\]

The theorem to establish is

\[
\forall G\in\mathrm{Planar}_{\mathrm{fin}},\quad
\exists c:V(G)\to Q_4\; W_G(c).
\]

The proof must keep three mathematical species distinct.

### Construction state

A construction state `K` is a partial committed coloring together with the exact graph and edge ledger. Uncolored regions are absent from the committed coloring; they are not assigned a fuzzy terminal value.

For an uncolored region `v`, let

\[
S_K(v)=\{c(u):u\sim v,\;u\text{ already committed}\}.
\]

Its directly admissible terminal colors are exactly

\[
\boxed{A_K(v)=Q_4\setminus S_K(v).}
\]

Thus adjacency restricts the possible new color space from inside the existing four-color palette.

### Brown observer projection

A bounded observer may see an unresolved or composite state as **brown**. Brown is a projection of construction state, not a construction color:

\[
B_O:\mathcal K(G)\to\mathcal B_O.
\]

`B_O` may be many-to-one. Different construction histories may therefore have the same brown observation. Brown cannot determine or authorize the next construction move without additional retained witness information.

### Terminal decode

Only a complete construction state may be decoded to the view-from-nowhere coloring:

\[
D:\mathcal K_{\mathrm{terminal}}(G)\to\operatorname{Col}_4(G).
\]

At this level there is no brown and no unresolved traversal. There is only a proper `Q4` coloring satisfying `W_G`.

## 2. Lipschitz Contract as meta-law

Every proof transformation must preserve the theorem species and direction of authority:

1. **construction first** — traversal acts on `K`, not on its brown projection;
2. **exact witness preservation** — inherited indexed edge obligations remain explicit and exact;
3. **bounded realization** — in the declared construction metric,
   \[
   d(TK,TK')\le L_T d(K,K'),\qquad L_T<\infty;
   \]
4. **observer non-authority** — no fact derived solely from `B_O(K)` may establish a construction transition unless an explicit witness-preserving map back to construction state is supplied;
5. **terminal non-circularity** — no property of the completed four-colored map may be used upstream to define the traversal law;
6. **certificate composition** — an existing construction certificate is transported/refined, never silently replaced;
7. **authority preservation** — no Four Color conclusion, held-out Rocq label, SRMF chart cardinality, or exhaustive enumeration may be introduced upstream as proof authority.

## 3. Traversal/coloration algebra

Let `I` denote the Four-Color construction traversal operator. This is distinct from Principia's ordinary complex phase unit.

The proposed chromatic law is exact nilpotency index four:

\[
I^3\ne0,\qquad I^4=0.
\]

Equivalently, the cyclic construction module generated from a seed has four nonzero stages before annihilation:

\[
e_0,\; Ie_0,\; I^2e_0,\; I^3e_0,\; I^4e_0=0.
\]

This establishes an algebraic ceiling of four independent traversal levels. It does **not** by itself prove that every graph-level dependency can be realized as a legal recoloring.

The construction law therefore consists of both:

- the index-four traversal algebra; and
- the exact adjacency complement `A_K(v)=Q_4\setminus S_K(v)`.

## 4. Degree-five surface

In a minimal planar obstruction, a degree-five vertex exposes five separately indexed adjacency obligations.

If the five committed neighbors use fewer than four distinct colors, then

\[
A_K(v)\ne\varnothing
\]

and the center extends directly.

The nontrivial case is a proper `C5` boundary using all four colors. Its multiplicity pattern is necessarily

\[
2+1+1+1.
\]

Hence two nonadjacent indexed boundary obligations carry the same terminal color. Algebraically, five indexed obligations map into four terminal modes with a forced kernel dependency.

This dependency is real, but it is not yet a recoloring theorem.

## 5. Exact component traversals and composition

A two-color component traversal is an exact graph morphism on construction state. Choose two terminal colors `a,b`, take one connected component of the subgraph induced by vertices colored `a` or `b`, and exchange `a<->b` on that entire component.

Every committed edge remains valid:

- edges inside the component still connect unequal colors after the swap;
- edges outside the component are unchanged;
- an edge from the component to an outside vertex cannot carry the other member of the same two-color pair, or that outside vertex would belong to the same induced component.

Therefore each component traversal is individually ledger-preserving, and finite compositions remain ledger-preserving.

This yields an important refinement of the degree-five target. A saturated state may be **single-move locked**: no one component traversal opens a color at the focus vertex. That does not imply construction failure. A later component traversal may become available after an earlier exact traversal changes the component structure.

The repository contains an explicit mechanically certified planar witness with:

- a saturated degree-five focus;
- no opening one-step two-color component traversal;
- a two-step composition that preserves every committed edge and opens a terminal color;
- an explicit spherical embedding certificate for the witness graph.

This witness is not proof authority. It establishes only that the constructive theorem must quantify over finite compositions rather than single moves.

## 6. Nilpotent desaturation obligation

The exact remaining constructive statement is therefore:

### Nilpotent Desaturation Closure

For every saturated degree-five construction state `K` occurring in a finite planar graph, the forced boundary dependency induced by the index-four traversal algebra admits a **finite composition of exact construction traversals**

\[
K=K_0\xrightarrow{T_1}K_1\xrightarrow{T_2}\cdots\xrightarrow{T_m}K_m=K'
\]

such that:

1. the graph is unchanged throughout;
2. every committed edge obligation remains satisfied at every intermediate state;
3. the center remains uncommitted during the traversal;
4. the final visible neighbor-color image strictly desaturates:
   \[
   |S_{K'}(v)|\le3;
   \]
5. therefore
   \[
   A_{K'}(v)=Q_4\setminus S_{K'}(v)\ne\varnothing;
   \]
6. the composition is generated by the declared construction algebra rather than imported from a completed four-coloring;
7. the traversal length is finite and its required construction distortion is explicitly bounded.

Nilpotency alone, linear dependence alone, brown observation, finite enumeration, and one-step Kempe availability are insufficient substitutes.

The current algebraic problem is now narrower: prove that planarity plus the saturated `C5` dependency prevents an infinite or closed sequence of exact component traversals that remains permanently saturated.

## 7. Brown belongs only to observation

Brown remains useful for Principia's bounded-observer account. A construction state may project to brown when provenance or unresolved alternatives are compressed:

\[
K\xrightarrow{B_O}\mathrm{brown}.
\]

But the constructive proof path is

\[
K_0\xrightarrow{T_1}K_1\xrightarrow{T_2}\cdots\xrightarrow{T_n}K_n,
\]

not

\[
\mathrm{brown}\to\text{new terminal color}.
\]

The observer path and construction path may coexist, but authority flows only from construction witnesses to observer descriptions, not backward.

## 8. Terminal completion

If construction traversal reaches a complete state `K_T`, terminal decoding is sound exactly when the full edge ledger holds:

\[
D(K_T)=c\in\operatorname{Col}_4(G),
\qquad W_G(c)=\mathrm{true}.
\]

The completed four-color map certifies the result. It does not explain or define the traversal that constructed it.

## 9. Global induction once desaturation is proved

Assume Nilpotent Desaturation Closure.

Let `G` be a minimal planar counterexample. By the planar degree bound, `G` has a vertex `v` of degree at most five. Remove `v` and construct a valid four-coloring of `G-v` by minimality.

- If the committed neighbor image of `v` uses at most three colors, `A_K(v)` is nonempty and `v` is committed directly.
- If `v` has degree five and the boundary uses all four colors, apply Nilpotent Desaturation Closure. The finite traversal produces `K'` with at most three visible neighbor colors, so `A_{K'}(v)` is nonempty. Commit `v` with any color in that complement.

The resulting complete construction contradicts minimality. Therefore no minimal counterexample exists.

This induction is valid only after Nilpotent Desaturation Closure is independently established.

## 10. Mechanical witness lines

The repository must keep independent verification lines:

1. **construction-state witness** — partial commits use only `Q4`, preserve committed edge obligations, and compute admissible colors exactly as `Q4 \ S`;
2. **observer-separation witness** — distinct construction states can project to the same brown observation, proving that brown is not sufficient construction authority;
3. **terminal-decode witness** — decoding is refused until construction is complete and the full edge ledger is valid;
4. **nilpotency witness** — `I^3 != 0` and `I^4 = 0`, with four nonzero cyclic stages;
5. **degree-five kernel witness** — every saturated proper `C5` has multiplicity `2+1+1+1` and a forced indexed dependency;
6. **component-traversal witness** — every two-color component swap preserves the exact committed edge ledger;
7. **composition witness** — an explicit planar single-move-locked saturated state desaturates after two exact component traversals;
8. **desaturation certificate witness** — every proposed graph rewrite must explicitly preserve all committed edges and open at least one terminal color at the focus vertex;
9. **dependency witness** — brown observation, completed-map facts, held-out Rocq, exhaustive enumeration, SRMF cardinality, and 4CT itself are forbidden upstream of traversal/desaturation authority.

Computation may falsify or certify declared lemmas. It may not replace the missing algebraic implication.

## 11. Certification boundary

Mechanical success means the checked-in construction algebra and species boundaries obey their declared contract. A full theorem certificate additionally requires an algebraic proof of Nilpotent Desaturation Closure for every admissible saturated planar degree-five construction state.

A valid counterexample to this proof route must preserve the theorem species and exhibit one of:

- a saturated planar construction state whose forced nilpotent dependency admits no finite ledger-preserving desaturation;
- a lost inherited edge obligation;
- an unavoidable fifth independently terminal construction mode;
- unbounded required construction distortion/exhausted reserve; or
- circular authority in the proof dependency graph.

Brown projection and completed-map viewpoints remain valuable for Principia Symbolica, but neither is permitted to masquerade as the coloration construction itself.
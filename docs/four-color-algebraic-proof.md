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

## 4. Plane parameterization as a discrete calculus

Fix one already colored region as a local reference state. Relative to that region, every adjacent region must lie in the three-color complement. Encode the four absolute colors as the Klein four group `V4`; then the three admissible relative differences are exactly the three nonzero `V4` elements.

For a cyclic frontier with colors `q_0,...,q_{n-1}`, define the discrete frontier derivative

\[
\delta_i=q_i-q_{i+1}\in V_4\setminus\{0\}.
\]

Closure of the frontier gives the telescoping integrability law

\[
\sum_i \delta_i=0.
\]

If `n_1,n_2,n_3` count the three nonzero frontier modes, then `V4` closure implies

\[
n_1\equiv n_2\equiv n_3\pmod 2.
\]

This is the first layer of the discrete calculus: local state change is not arbitrary; it is parameterized by a closed planar frontier.

### Degree-five corner law

For a degree-five frontier, the parity law and `n_1+n_2+n_3=5` force

\[
(n_1,n_2,n_3)=(3,1,1)
\]

up to permutation.

Moreover, on every proper three-color `C5` frontier, the two singleton transition edges are adjacent. Therefore there is a unique boundary vertex where the two exceptional transition modes meet, and the remaining three frontier edges carry one dominant mode.

This gives a canonical local shape without recoloring search:

```text
three-edge dominant continuation run
        +
one exceptional two-edge corner
```

The exceptional corner is a geometrically distinguished **inspection locus**. It is not yet a proven recoloring locus.

## 5. Bounded planar continuation

The second layer of the calculus is integrability of proposed state continuations in the plane.

Consider two simple continuation arcs inside a disk whose endpoints lie on one cyclic boundary. If their endpoint pairs alternate in cyclic order, then the arcs are forced to intersect. If the endpoint pairs do not alternate, cyclic order alone does not force an intersection.

Thus a primitive obstruction can be expressed without metric geometry:

\[
\boxed{\text{alternating boundary endpoints}\Rightarrow\text{forbidden intersection}.}
\]

A continuation is therefore operationally admissible only while it preserves the existing cyclic order/incidence relations and does not force an intersection with an already retained trajectory.

This matches the red-team model:

- a state may continue arbitrarily far when nothing constrains it;
- deflection is admissible while cyclic order remains integrable;
- obstruction occurs when the demanded continuation would violate bounded planar coexistence.

Length itself is not the scarce resource. Planar incidence is.

## 6. Exact component traversals remain verification tools

A two-color component traversal is an exact graph morphism on construction state. Choose two terminal colors `a,b`, take one connected component of the subgraph induced by vertices colored `a` or `b`, and exchange `a<->b` on that entire component.

Every committed edge remains valid, so such traversals compose exactly. They remain useful as mechanical witnesses and falsifiers.

However, component traversal search is no longer the source calculus. The source calculus is now:

\[
\text{frontier derivative}
+\text{cyclic closure}
+\text{noncrossing integrability}.
\]

A graph-level component move is admissible as proof authority only when it is derived from, or explicitly mapped back to, that planar continuation structure.

## 7. Remaining constructive obligation

The theorem-specific missing map is now more precise.

### Planar Continuation Closure

For every saturated degree-five construction state `K` occurring in a finite planar graph, let its fixed-region frontier induce the `3,1,1` transition signature and unique exceptional corner. The planar continuation calculus must determine a finite ledger-preserving construction rewrite

\[
K\xrightarrow{T}K'
\]

such that:

1. the graph is unchanged;
2. every committed edge obligation remains satisfied;
3. the center remains uncommitted during the rewrite;
4. `T` is justified by the frontier derivative and noncrossing continuation law, not by search over completed colorings;
5. the final neighbor-color image satisfies
   \[
   |S_{K'}(v)|\le3;
   \]
   and hence `A_{K'}(v)` is nonempty;
6. the construction distortion is finite and explicitly bounded.

The new ingredients narrow the target substantially, but they do **not** yet prove this closure theorem. In particular:

- `3,1,1` alone does not imply recolorability;
- adjacency of the singleton modes alone does not imply recolorability;
- non-alternating endpoints alone do not construct the required graph rewrite;
- component-swap availability cannot be imported as proof authority unless tied back to the continuation calculus.

The next proof step is exactly the map from the exceptional corner plus surrounding planar continuation relations to a legal construction rewrite.

## 8. Brown belongs only to observation

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

## 9. Terminal completion

If construction traversal reaches a complete state `K_T`, terminal decoding is sound exactly when the full edge ledger holds:

\[
D(K_T)=c\in\operatorname{Col}_4(G),
\qquad W_G(c)=\mathrm{true}.
\]

The completed four-color map certifies the result. It does not explain or define the traversal that constructed it.

## 10. Global induction once continuation closure is proved

Assume Planar Continuation Closure.

Let `G` be a minimal planar counterexample. By the planar degree bound, `G` has a vertex `v` of degree at most five. Remove `v` and construct a valid four-coloring of `G-v` by minimality.

- If the committed neighbor image of `v` uses at most three colors, `A_K(v)` is nonempty and `v` is committed directly.
- If `v` has degree five and the boundary uses all four colors, apply Planar Continuation Closure. The rewrite produces `K'` with at most three visible neighbor colors, so `A_{K'}(v)` is nonempty. Commit `v` with any color in that complement.

The resulting complete construction contradicts minimality. Therefore no minimal counterexample exists.

This induction is valid only after Planar Continuation Closure is independently established.

## 11. Certification boundary

Mechanical success means the checked-in construction algebra and species boundaries obey their declared contract. A full theorem certificate additionally requires an algebraic proof of Planar Continuation Closure for every admissible saturated planar degree-five construction state.

A valid counterexample to this proof route must preserve the theorem species and exhibit one of:

- a saturated planar construction state whose exceptional-corner continuation structure admits no ledger-preserving desaturation;
- a lost inherited edge obligation;
- an unavoidable fifth independently terminal construction mode;
- unbounded required construction distortion/exhausted reserve; or
- circular authority in the proof dependency graph.

Brown projection and completed-map viewpoints remain valuable for Principia Symbolica, but neither is permitted to masquerade as the coloration construction itself.

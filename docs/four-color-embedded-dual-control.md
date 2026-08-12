# Embedded Plane-Dual Nonzero Controls at Shared z0

**Status:** graph-native nonzero control realization for witnessed degree-five triangulated
embeddings. This tranche does not by itself prove universal continuation for every planar
degree-five construction.

## 1. Shared zero-point

Let

\[
z_0=s=(G,c)
\]

be the exact Four Color construction state. The Kempe and V4/dual control
parameterizations may correspond at the same zero:

\[
\rho_{\mathrm{Kempe}}(s,0)=s=\rho_{\mathrm{dual}}(s,0).
\]

Changing parameterization at zero is identity on the graph/coloring state. A nonzero
dual parameter is admitted only when an embedding witness derives it.

## 2. Retained embedding witness

`DegreeFiveTriangulatedEmbedding` retains:

- the exact construction state;
- the uncommitted degree-five focus;
- its witnessed cyclic C5 boundary;
- all triangular faces of a spherical embedding.

The witness checks the full edge ledger against the face ledger: every graph edge occurs
twice among spherical face boundaries and Euler characteristic is two. The five
focus-incident triangles are exactly the five triangles cut away when the focus is
deleted. What remains is a triangulated disk with the same C5 boundary.

The embedding is proof evidence. It is not a mutable surface coordinate.

## 3. Deriving the actual dual continuation

For a saturated boundary choose a singleton V4 derivative mode \(\sigma\). On every
properly colored triangular disk face the three edge differences are the three nonzero
V4 modes once each. Excluding \(\sigma\) therefore leaves dual degree two at every disk
triangle.

The implementation constructs that selected-mode network from the retained faces. A
selected boundary edge becomes a terminal; a selected interior primal edge joins the
two incident disk triangles. The four terminals are then followed through the actual
dual network, producing two concrete `DualContinuationPath` witnesses.

Thus the terminal pairing is not chosen from the two abstract noncrossing options. It
is **derived from the supplied embedding**.

## 4. Nonzero domain parameter

Each actual terminal-to-terminal dual path crosses a finite set of primal edges. Removing
those crossed edges from the committed primal disk yields two sides. One side is chosen
canonically and translated by \(\sigma\).

For every internal edge of the translated side, both endpoints move and its V4
difference is unchanged. Every crossed edge has old mode \(m\ne\sigma\), so after
translation

\[
m' = m+\sigma \ne 0.
\]

Therefore the resulting `ConstructionState` preserves the exact graph, committed vertex
identity, genus-zero species, Q4 palette, and every committed edge obligation.

`DualDomainNonzeroCertificate` also checks that the realized boundary derivative is
exactly the `toggle_cut_endpoints` result for the embedding-derived terminal pair.

## 5. Positive and persistent witnesses

The tests carry two explicit maximal-planar degree-five embeddings with the same
saturated boundary word

\[
(0,1,0,2,3).
\]

For translation mode \(\sigma=(0,1)\):

1. one embedding derives terminal pairing
   \[
   ((0,1),(3,4)),
   \]
   and either graph-derived nonzero path parameter produces positive focus slack;

2. the persistent-double-lock embedding derives
   \[
   ((0,4),(1,3)),
   \]
   and either graph-derived nonzero path parameter preserves zero focus slack while
   still producing a legal, nontrivial construction transition.

This is the desired distinction: the embedding chooses the real parameter. The proof
does not manufacture the favorable pairing.

## 6. Proof interface now earned

We now have the executable chain

\[
\boxed{
z_0
\to
\text{corresponding V4/dual parameterization at }z_0
\to
\text{retained embedding}
\to
\text{actual dual path}
\to
\text{certified nonzero domain translation}
\to
z_1.
}
\]

A change of chart is still zero movement. A nonzero move is now graph-native and
embedding-derived.

The remaining theorem work is to integrate persistent zero-slack outcomes with retained
witness staging so that the next corresponding parameterization is derived from the
same physical carrier/history without replay being counted as progress.

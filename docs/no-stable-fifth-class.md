# NoStableFifthClass: what is proved, and what remains

This note separates an exact observer-geometric theorem from the graph-theoretic bridge still required to connect it to the Four Color Theorem.

## 1. Exact four-versus-five observer separation

For the symmetric `k`-constraint Cost-of-Cacophony geometry, define the soft mode

\[
M_k(\rho)=1-\rho(k-1).
\]

Let an observer have a fixed admissible soft-mode floor

\[
0<M_O<1.
\]

The observer treats `k` simultaneous channels as stable exactly when

\[
M_k(\rho)>M_O.
\]

For four channels,

\[
M_4=1-3\rho,
\]

so four remain stable when

\[
\rho<\frac{1-M_O}{3}.
\]

For five channels,

\[
M_5=1-4\rho,
\]

so the fifth configuration reaches the observer routing floor when

\[
\rho\ge\frac{1-M_O}{4}.
\]

Therefore

\[
\boxed{
\frac{1-M_O}{4}\le\rho<\frac{1-M_O}{3}
}
\]

is an exact nonempty interval on which four simultaneous channels remain observer-stable while five cannot remain in the same representation.

Because `0 < M_O < 1`,

\[
\frac{1-M_O}{4}<\frac{1-M_O}{3},
\]

so the interval is always nonempty.

This is the theorem mechanically implemented by `mettafy.fifth_class.ChannelStabilityWindow` and witnessed by `WIT-FOUR-STABLE-FIVE-ROUTES`.

It is **not** the Four Color Theorem. A Cacophony channel is not automatically a graph color, and a single symmetric coupling parameter `rho` does not automatically represent an arbitrary planar conflict graph.

## 2. Why degree five is nevertheless the right graph-theoretic bridge

For a finite simple planar graph with at least three vertices, Euler's formula and the face-degree bound imply

\[
|E|\le 3|V|-6.
\]

Hence the average degree satisfies

\[
\frac{1}{|V|}\sum_{v\in V}\deg(v)
=
\frac{2|E|}{|V|}
<6.
\]

Therefore every such planar graph contains at least one vertex of degree at most five.

Now suppose a smaller graph is already four-colored and we restore a removed vertex `v`.

If

\[
\deg(v)\le 3,
\]

one of four colors is immediately unused by its neighbors.

If

\[
\deg(v)=4,
\]

there are at most four neighbor colors; if fewer than four appear, extension is immediate. The only nontrivial case is when all four colors appear around `v`.

At

\[
\deg(v)=5,
\]

pigeonhole reasoning alone cannot extend the coloring: five neighbors may collectively exhibit all four colors, with one repeated. This is the first local degree at which naive greedy extension necessarily runs out of information.

So planarity reduces the induction bottleneck to local degree at most five, and degree five is the first unresolved local obstruction after trivial color availability is exhausted.

That is a genuine structural correspondence with the observer-geometric theorem:

```text
Cacophony side                     planar-coloring side
-------------------------------    ---------------------------------
four channels stable               four terminal labels available
fifth channel forces rerouting     degree-five case needs restructuring
representation change required     Kempe/reducibility transformation
same endpoint may hide phase       same boundary coloring may admit recoloring
```

The table is a correspondence target, not a proof of identity.

## 3. The missing theorem

A theorem worthy of the name `NoStableFifthClass` must discharge the following bridge without assuming four-colorability:

> Given an admissible planar SRMF conflict object, every local degree-five obstruction can be transformed by an allowed SRMF refinement/recoloring move into a state whose terminal conflict requires at most four independent labels, while preserving already-certified boundary constraints.

Formally, the missing ingredients are:

1. **Conflict-object definition.** Specify exactly what an SRMF vertex/region is.
2. **Adjacency definition.** Specify when two transformations require distinct terminal labels.
3. **Planarity theorem.** Prove that the relevant conflict object is planar under declared hypotheses.
4. **Color/operator map.** Define the correspondence between terminal labels and SRMF channels without assuming four labels in advance.
5. **Degree-five reduction.** Give a constructive permitted refinement for the remaining degree-five case.
6. **Invariant preservation.** Prove the refinement preserves Contract/Blanket/Ledger obligations and does not hide unresolved conflict in an observer quotient.

Only after (5) and (6) are proved does the observer-geometric separation become evidence for `NoStableFifthClass` rather than a parallel analogy.

## 4. Where imaginary traversal may enter

The classical degree-five obstruction is not solved by inventing a fifth color. It is solved by changing the coloring state while retaining the same graph.

That is precisely the kind of situation for which Principia Symbolica's real/imaginary distinction is relevant:

\[
d_O^{\mathrm{Re}}\text{ can remain bounded while }d_O^{\mathrm{Im}}\text{ records a latent orientation change.}
\]

A Kempe-chain-style recoloring can therefore be investigated as an **imaginary traversal candidate**: observable graph incidence remains fixed while latent label orientation changes until a real four-color extension becomes available.

This is still a research hypothesis. The proof obligation is to show that the SRMF imaginary traversal relation contains the required recoloring transformations and that its reintegration map preserves adjacency correctness.

## 5. Amortization

If a finite family of degree-five obstruction types can be compiled into certified refinement moves, then the expensive discovery is paid once:

\[
\text{discover/refute refinement}
\to
\text{certify move}
\to
\text{store Strategy IR}
\to
\text{reuse on future planar instances}.
\]

This is the intended MeTTafy role. Rocq remains proof-validity authority. MeTTafy should extract and replay the transformation strategy without silently inheriting Rocq's authority for a different semantic claim.

## 6. Current claim boundary

Mechanically established now:

\[
\boxed{
\frac{1-M_O}{4}\le\rho<\frac{1-M_O}{3}
\Longleftrightarrow
\text{four stable and five routes}
}
\]

within the declared symmetric observer model.

Not yet established:

\[
\boxed{
\text{planarity + SRMF refinement}
\Longrightarrow
\text{NoStableFifthClass}
}
\]

The next proof work belongs exactly at the degree-five transformation bridge. That is where the Four Color machinery and the SRMF observer dynamics must either coincide mechanically or fail to coincide.
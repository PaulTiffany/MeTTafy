# Graph-Native Staging on the Four Color Control Surface

**Status:** exact finite stage-identity discipline plus a mechanically derived two-stage witness on the persistent planar carrier. This note does not by itself establish universal continuation for every planar degree-five state.

## 1. Stage identity comes from the carrier

A nonzero plane-dual control is no longer named by the caller. For a V4 translation mode

\[
\sigma\in V_4\setminus\{0\}
\]

and an embedding-derived dual path crossing the physical primal edge set \(P\), its proof-stage identity is

\[
\boxed{\operatorname{id}(\sigma,P)=(\sigma,P).}
\]

The implementation canonicalizes the crossed primal edges, so path orientation and traversal direction do not create a new stage identity.

Because every nonzero V4 element is self-inverse, reversing the same domain translation across the same physical cut has the same identifier. The inverse remains a legal graph symmetry; it is simply not counted a second time as proof progress.

## 2. Physical witness and chromatic typing are separate

The history records two different objects:

1. the physical carrier edges already retained as witnesses;
2. the content-addressed mode/cut controls already consumed as proof stages.

This prevents chromatic retyping of an already retained edge set from masquerading as fresh geometry. Retained carrier edges are monotone, but they need not grow strictly on every fresh stage.

## 3. Finiteness is graph-derived

Let the fixed committed carrier contain \(m\) physical edges. A deliberately loose upper bound on all possible nonempty mode/cut identities is

\[
\boxed{3(2^m-1).}
\]

There are three nonzero V4 modes and finitely many nonempty physical edge subsets. Therefore an infinite sequence of pairwise fresh graph-native dual-stage identities is impossible on one fixed finite carrier.

This is a finiteness theorem for stage identity, not yet a theorem that a fresh admissible stage always exists while the focus has zero palette slack.

## 4. Receding-horizon zero-point rebasing

Suppose a certified nonzero dual parameter acts at

\[
z_0=(G,c_0)
\]

and yields

\[
z_1=(G,c_1).
\]

If

\[
A_{c_1}(v)=\varnothing,
\]

the same retained face embedding is re-certified with the new coloring, and the Kempe and V4 dual parameterizations are reconstructed at the actual successor:

\[
\rho_{\mathrm{Kempe}}(z_1,0)=z_1
=\rho_{\mathrm{dual}}(z_1,0).
\]

No future route is carried across the transition. The next controls are derived again from the state actually reached.

## 5. Persistent-carrier two-stage derivation

For the persistent planar carrier with boundary

\[
(0,1,0,2,3),
\]

take the singleton mode

\[
\sigma_1=(0,1).
\]

The retained embedding derives the physical dual path with terminal edges \((0,4)\), crossing

\[
P_1=\{ab,ae\}.
\]

Its graph-native stage is

\[
s_1=((0,1),\{ab,ae\}).
\]

Translating the isolated side gives

\[
(0,1,0,2,3)
\longrightarrow
(2,1,0,2,3),
\]

while the focus still has zero palette slack.

At the new zero-point the old \((0,1)\) cut \(\{ab,ae\}\) is still present and its inverse translation is still legal. But it receives exactly the already-consumed identity \(s_1\), so it cannot be counted again as progress.

The recolored boundary now has singleton modes \((0,1)\) and \((1,1)\). Recomputing the plane-dual continuation for

\[
\sigma_2=(1,1)
\]

derives a fresh physical path with terminal edges \((1,2)\), crossing

\[
P_2=\{bc,cd\}.
\]

Its stage identity

\[
s_2=((1,1),\{bc,cd\})
\]

is fresh. Applying it gives

\[
(2,1,0,2,3)
\longrightarrow
(2,1,3,2,3),
\]

and now

\[
\boxed{A(v)=\{0\}.}
\]

Thus the previously known two-stage focus-slack trajectory is now derived entirely through the plane-dual parameterization, shared zero-points, physical cut witnesses, and graph-native nonreplay history.

## 6. What is now mechanical

The repository mechanically checks that:

- stage identity is invariant under cut-edge order and orientation;
- the first persistent-carrier dual stage is derived from the actual embedding;
- the successor remains a valid genus-zero embedded construction state;
- Kempe and dual control descriptions rebase to the exact successor zero-point;
- the inverse first cut remains a legal coloring symmetry;
- the history rejects that inverse as repeated proof progress;
- a fresh second dual stage is derived from the successor embedding;
- the second stage gives exact positive focus slack while preserving the graph and edge ledger;
- every fresh stage decreases the finite graph-derived stage-capacity bound by one.

## 7. Remaining universal statement

The sharpened global obligation is now:

> For every saturated degree-five genus-zero construction with zero focus slack, repeated receding-horizon derivation of graph-native controls either produces positive focus slack or exposes a fresh admissible mode/cut identity; the process cannot exhaust all graph-native stage identities while the focus remains slackless.

The fixed-carrier finiteness half is now explicit. The remaining theorem-specific content is the **fresh-stage-or-focus-slack implication** for arbitrary retained planar embeddings.

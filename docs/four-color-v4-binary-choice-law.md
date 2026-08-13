# V4 Binary Choice Law for Action-Local Four Color Control

**Status:** exact algebraic/mechanical law for one selected dual-domain action.

The action-local correction has a sharper V4 form.  Fix one nonzero mode
\(\sigma\in V_4\).  Every committed vertex carries one realized binary choice

\[
\chi(v)\in\{0,1\},
\]

with

- \(\chi(v)=0\): stay at the current palette state for this domain action;
- \(\chi(v)=1\): change direction to the unique \(\sigma\)-partner.

The pointwise action is

\[
\boxed{c'(v)=c(v)+\chi(v)\sigma.}
\]

For a fixed choice bit, both maps on \(Q_4\) are exact isometries in the
discrete palette metric.  The zero choice is the identity.  The nonzero choice
is a fixed-point-free involution:

\[
q\mapsto q+\sigma,\qquad
(q+\sigma)+\sigma=q.
\]

Thus every realized palette state has one output under the selected action, and
every state that changes direction has exactly one distinct partner.

## Edge law

For a committed edge \(uv\), write

\[
\delta_{uv}=c(u)+c(v)\in V_4\setminus\{0\}.
\]

After the binary choices at its two endpoints,

\[
\begin{aligned}
\delta'_{uv}
&=c'(u)+c'(v)\\
&=\delta_{uv}+(\chi(u)\oplus\chi(v))\sigma.
\end{aligned}
\]

Therefore

\[
\boxed{
\delta'_{uv}
=
\begin{cases}
\delta_{uv}, & \chi(u)=\chi(v),\\
\delta_{uv}+\sigma, & \chi(u)\ne\chi(v).
\end{cases}}
\]

Only an edge whose endpoint choices differ is affected.  On that pair, exactly
one endpoint changes direction relative to the other endpoint.  This is the
pairwise interaction boundary that the earlier counterfactual-router language
was obscuring.

## Why the selected dual network excludes sigma

If the endpoint choices differ and the original edge mode were
\(\delta_{uv}=\sigma\), then

\[
\delta'_{uv}=\sigma+\sigma=0,
\]

which would violate the edge obligation.  Hence an admissible cut may cross
only edges with mode different from \(\sigma\).

That is exactly the graph-native rule already used by the embedded dual
continuation: the \(\sigma\)-network follows primal edges whose modes are the
other two nonzero V4 elements.  The binary-choice law therefore derives the
local admissibility condition rather than adding another routing heuristic.

## Domain action as a choice mask

For an embedding-derived `DualDomainParameter`, the translated side is the set
of vertices with \(\chi=1\).  The other side has \(\chi=0\).  The physical cut
is recovered exactly as

\[
\boxed{
P=\{uv\in E:\chi(u)\oplus\chi(v)=1\}.
}
\]

`DualDomainBinaryChoiceCertificate` mechanically verifies:

1. every vertex color is exactly `c(v) + chi(v) sigma`;
2. the XOR-choice cut is exactly the retained physical dual-path cut;
3. same-choice edges retain their exact V4 difference;
4. different-choice edges toggle by exactly \(\sigma\);
5. every crossed edge had mode different from \(\sigma\), so every updated
   edge difference remains nonzero;
6. both pointwise palette choices have exact Lipschitz constant \(L=1\).

This makes the previously observed symmetric-difference surgery a consequence
of a more primitive local law: **one selected direction, one binary choice at
each state, one pairwise edge consequence.**

## Composition

Because \(V_4\) has characteristic two, repeating the same choice mask and mode
cancels pointwise:

\[
T_{\sigma,\chi}^2=\operatorname{id}.
\]

This explains why the physical dual move remains a reversible symmetry even
when the graph-native proof-history layer refuses to count the same physical
stage twice as progress.

Different construction stages can still fail to commute because the next
choice mask is derived from the *new* graph/coloring state.  The pointwise V4
translation is flat; the state-dependent reconstruction of admissible controls
is where the already-measured construction holonomy lives.

## CI

The action-local CI boundary now exhaustively verifies, for all three nonzero
V4 modes and all four palette states, that:

- the stay choice is an \(L=1\) isometry;
- the change-direction choice is an \(L=1\) isometry;
- every change-direction choice has one distinct partner;
- applying the same nonzero direction twice returns to the original palette
  state.

The graph-level unit witness then certifies the exact XOR edge law on all four
current dual controls of the persistent degree-five carrier.

# Current Opportunity Totality

**Status:** exact present-state control theorem; no future route.

The cross-direction handoff law yields a sharper statement than bounded
reachability.  After one currently valid dual-domain action, inspect only the
actual successor.

If the exact focus observable satisfies

\[
A(v)\neq\varnothing,
\]

then the local construction may stop by committing one currently admissible
color.

If instead

\[
A(v)=\varnothing,
\]

the successor boundary is again a saturated proper C5.  It therefore has
exactly two singleton V4 modes.  The source direction remains singleton, and
the handoff certificate identifies the other singleton as one member of the
source shared-opportunity pair.

Each current singleton mode has exactly two embedding-derived dual paths.
Consequently the actual zero-slack successor exposes exactly four current
nonzero dual controls:

\[
\boxed{
A(v)=\varnothing
\Longrightarrow
|\mathcal A_{\mathrm{dual}}(z)|=4.
}
\]

Applied after a realized action:

\[
\boxed{
 z\xrightarrow{T}z'
 \Longrightarrow
 \left[
 A_{z'}(v)\neq\varnothing
 \right]
 \;\lor\;
 \left[
 |\mathcal A_{\mathrm{dual}}(z')|=4
 \right].
}
\]

This is **current opportunity totality**, not a route theorem.  No destination,
lookahead tree, or preferred successor is stored.  When zero slack persists,
`CurrentOpportunityTotalityCertificate` rebuilds the dual-defect chart at the
actual successor and derives the four controls there.

The complete 154-member proper-color-preserving flip family exercises this
certificate on all four current controls of every instance, for 616 exact
present-action transitions.  Each transition must certify either immediate
focus admissibility or exactly four current successor controls.

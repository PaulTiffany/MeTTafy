# Current Opportunity Totality

**Status:** exact present-state control theorem; no future route.

After one currently valid dual-domain action, inspect only the actual successor.

If

\[
A(v)=Q_4\setminus c(N(v))\neq\varnothing,
\]

then the Four Color construction has a current **focus color commitment**. This
is not a stop action.

If instead

\[
A(v)=\varnothing,
\]

the successor boundary is again a saturated proper C5. It has exactly two
singleton V4 modes. The source direction remains singleton, and the handoff
certificate identifies the other singleton as one member of the source shared
opportunity pair.

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
\left[A_{z'}(v)\neq\varnothing\right]
\;\lor\;
\left[|\mathcal A_{\mathrm{dual}}(z')|=4\right].
}
\]

This is **current opportunity totality**, not a route theorem. No destination,
lookahead tree, or preferred successor is stored. When zero slack persists,
`CurrentOpportunityTotalityCertificate` rebuilds the dual-defect chart at the
actual successor and derives the four controls there.

The handed-off refinement then retains only the two controls in the actual
successor's resulting other singleton direction.

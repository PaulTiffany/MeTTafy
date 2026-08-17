# Pairwise Consequence and Shared Opportunity

**Status:** local algebraic refinement of the action-local Lipschitz law.

A realized action has one pairwise consequence.  It does not fan out into several realized successor states.

Fix a nonzero V4 direction sigma.  If one palette state q changes direction, the active two-state orbit is

\[
\{q, q+\sigma\}.
\]

That is the realized pairwise consequence.  The other two palette states are not further consequences.  They form the complementary two-state orbit under the same direction and therefore share one structural opportunity:

\[
Q_4
=
\{q,q+\sigma\}
\sqcup
\{r,r+\sigma\}.
\]

The second pair is permission, not realization.

The same distinction is sharper on an affected committed edge.  Its current nonzero mode cannot equal sigma.  Therefore the three nonzero V4 modes split as

\[
V_4\setminus\{0\}
=
\{\sigma\}
\sqcup
\{\mu,\mu+\sigma\}.
\]

If exactly one endpoint changes direction, the one realized edge consequence is

\[
\mu\mapsto\mu+\sigma.
\]

The two non-sigma modes form the shared opportunity orbit.  They are exchanged by the selected direction:

\[
(\mu+\sigma)+\sigma=\mu.
\]

Thus the local accounting is

\[
\boxed{
\text{one realized pairwise consequence}
\;|\;
\text{two complementary states sharing one opportunity}
}
\]

not one action producing several independently realized effects.

This distinction matters for the Lipschitz boundary.  Consequence belongs to the realized morphism.  Opportunity belongs to the permission surface exposed by the resulting local geometry.  A later state may act on that opportunity, but only in a later action after the current successor has been realized and its local permissions recomputed.

`v4_action_lipschitz.py` now certifies both forms of the two-state opportunity orbit:

- complementary palette opportunity: the two Q4 states outside the active sigma-pair;
- edge opportunity modes: the two nonzero edge modes different from sigma.

The graph-level certificate further requires every crossed edge to move exactly between those two opportunity modes while all same-choice edges retain their exact mode.

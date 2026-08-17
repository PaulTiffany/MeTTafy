# Joint Dynamics of a Handed Opportunity Pair

**Status:** exact pair-level law, with scalar one-step descent explicitly not required.

After a zero-slack consequence, let the actual successor hand off its resulting
other singleton direction \(\tau\).  The two current controls in that direction
form one shared opportunity pair

\[
\mathcal H_\tau(z)=\{P_0,P_1\}.
\]

The pair has a stronger joint structure than either member has alone.

## Homogeneous immediate response

The two members have the same focus-admissibility class:

\[
\boxed{
A(T_{P_0}z)\neq\varnothing
\iff
A(T_{P_1}z)\neq\varnothing.
}
\]

Thus the state does not need to inspect two future outcomes to discover which
member is favorable.  Either both currently expose a focus color commitment,
or neither does.

## Persistent pair completion

Suppose neither first action exposes a focus color commitment.  The selected
\(\tau\)-opportunity carrier is invariant under either action, so after
realizing one member the actual successor re-derives the same two physical
\(\tau\)-paths.  The sibling path therefore remains a current opportunity.

Realize the sibling next.  The two possible orders commute at the construction
state:

\[
\boxed{
T_{P_1}T_{P_0}z=T_{P_0}T_{P_1}z.
}
\]

No future path is stored: the second control is re-derived after the first
realized consequence and matched by its retained physical carrier.

At the boundary, the two paths together meet all four non-\(\tau\) terminals.
Consequently the combined action toggles every non-\(\tau\) boundary mode by
\(\tau\).  If the source mode multiplicities are

\[
\tau^1,\quad \alpha^3,\quad \beta^1,
\]

then pair completion gives

\[
\boxed{
\tau^1,\quad \alpha^1,\quad \beta^3.
}
\]

The handed mode stays singleton while the repeated mode and the other
singleton exchange roles.  The boundary remains saturated and focus slack
remains zero.

This is a deterministic **role retyping law**, not a scalar descent law.

## Relation to the kill witness

The previously banked witness

\[
(\mathrm{pivot},10)\to\{(\mathrm{pivot},12),(\mathrm{pivot},12)\}
\]

therefore does not obstruct the pair calculus.  It kills only the attempt to
score either first member by immediate phase descent.  The shared opportunity
object carries information in the pair and its completion, not in a monotone
one-step scalar attached to either branch.

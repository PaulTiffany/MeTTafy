# Construction-Space Holonomy in the Persistent-Lock Carrier

**Status:** exact finite construction witness. This note does not claim a knot invariant, Contract Expansion Closure, or the Four Color Theorem.

## 1. Why stage order must be retained

On the persistent-double-lock carrier, let

- `T_AB` be the exact Kempe swap of the `A/B` component seeded at `a`, and
- `T_BC` be the exact Kempe swap seeded at `b` with the `C` color.

Both are legal graph-level component swaps.  Every intermediate state preserves
all committed edge obligations.  Nevertheless, direct replay gives

\[
T_{BC}T_{AB}(s) \ne T_{AB}T_{BC}(s).
\]

For the canonical boundary `A B A C D = 0 1 0 2 3`, the two staged orders land at

\[
(1,2,1,0,3)
\]

and

\[
(1,2,0,1,3),
\]

respectively.  Therefore a static potential on the boundary alone cannot capture
all construction progress: the path taken through exact component moves matters.

## 2. The order defect is graph-native

The difference between those two endpoints is not an observer phase added by hand.
It is exactly an ordinary `0/1` Kempe component swap on the residual component
`{c,d}`.  Thus the failed square leaves a concrete reversible residue carried by
the graph itself.

This is the minimal sense in which we currently use **construction holonomy**:
a loop/square in the space of admissible staged moves may leave a nontrivial
residual construction transport.

No braid or knot type is inferred from this fact alone.

## 3. Control: not every stage pair has holonomy

The two singleton stages used by the known two-stage opening path commute on the
same carrier.  Replaying them in either order reaches the same open boundary

\[
(2,1,3,2,3),
\]

with color `0` available at the original focus.

So the repository does **not** encode the claim that all stage order matters.
The mechanical witness distinguishes a genuinely noncommuting pair from a
commuting control pair.

## 4. Consequence for the closure program

The immediate theorem target is now more specific than a generic finite-stage
rank.  A faithful closure law must account for the path geometry of admissible
construction moves.

A future invariant may quotient out:

1. exact inverse/replay pairs;
2. commuting squares of independent moves;
3. other graph-native relations that can be mechanically certified.

What remains after these cancellations is a candidate obstruction/holonomy class.
The next research question is whether every saturated degree-five planar state has
an admissible path whose residual class trivializes sufficiently to open the
original center.

This note deliberately stops before identifying that residual with a braid,
trefoil, or other knot type.  Such a promotion requires a mechanically derived
encoding of stage trajectories and equivalence moves.

# Four Stable, Five Routes

This note isolates the part of `NoStableFifthClass` that follows exactly from the observer-critical Cost-of-Cacophony geometry, without borrowing the Four Color Theorem.

## Conditional theorem

Let the symmetric `k`-channel soft mode be

\[
M_k = 1-\rho(k-1),
\]

and let a bounded observer route/change representation whenever

\[
M_k \le M_O,
\qquad 0<M_O<1.
\]

Then four channels remain stable while a fifth must route exactly when

\[
M_4 > M_O \ge M_5.
\]

Substituting the soft modes gives

\[
1-3\rho > M_O \ge 1-4\rho,
\]

hence

\[
\boxed{
\frac{1-M_O}{4}\le \rho < \frac{1-M_O}{3}
}.
\]

Because `0 < M_O < 1`, the interval is nonempty:

\[
\frac{1-M_O}{4}<\frac{1-M_O}{3}.
\]

Therefore every admissible observer floor has a nonempty conflict regime in which a four-channel representation is still solvent but adding a fifth simultaneous mutually conflicting channel crosses the observer floor.

## Reference case

For the previous observer-critical witness with

\[
k=4,\qquad \tau=m=1,\qquad B_O=4,
\]

we had

\[
M_O=\frac14.
\]

The exact four/five separation window is therefore

\[
\frac{3}{16}\le\rho<\frac14.
\]

At `rho = 1/5`,

\[
M_4=1-3/5=2/5>1/4,
\]

while

\[
M_5=1-4/5=1/5\le1/4.
\]

So four remains stable and five routes.

## What this proves

The theorem establishes a real observer-relative **fifth-channel obstruction** inside the symmetric Cacophony model. It is not merely that the fifth channel is more expensive: there exists an exact regime where four is admissible and five is not.

This is a conditional theorem, not yet the Four Color Theorem.

## Missing bridge to planarity

To obtain `NoStableFifthClass` for planar coloring, we still need a theorem connecting planar conflict structure to the channel geometry. In particular, at least one of the following must be established rather than assumed:

1. a planar local conflict requiring a fifth terminal color induces five simultaneous constraints represented by the same or a lower-bounded effective `rho`;
2. admissible SRMF refinement preserves a lower bound placing that effective conflict in the four/five separation window;
3. reducibility/Kempe/discharging structure guarantees that whenever a putative fifth class appears, an imaginary/refinement traversal can merge or reroute it before terminal stabilization.

Euler planarity alone is insufficient. It guarantees a vertex of degree at most five, which supports the Five Color Theorem reduction but does not by itself eliminate the fifth color. Any proof that jumps directly from planarity to this Cacophony interval would be circular unless the missing structural bound is derived independently.

## Working theorem stack

```text
ObserverCriticalCollapse
    ↓
FourStableFiveRoutes          # proved conditionally here
    ↓
PlanarConflictLowerBound      # open
    ↓
AdmissibleRefinementClosure   # open
    ↓
NoStableFifthClass            # target
    ↓
Four terminal channels suffice
```

The mechanistic strategy is therefore not to re-prove Four Color by naming four operators. It is to show that a fifth terminal distinction cannot remain simultaneously necessary, observer-stable, and planar after admissible SRMF refinement.

# Four Color Immediate Control Access

**Status:** exact one-step construction law on the fixed genus-zero Four Color species.

This note records the control semantics used by Track B.  A coloration agent is
not required to possess an eventual target coloring or a precomputed route.
Control authority is receding-horizon: the current graph/coloring determines the
controls available now; after one exact control is applied, the next control is
derived again from the resulting construction state.

## 1. Fixed construction species

A construction state is

\[
s=(G,c)
\]

inside the fixed sphere/plane species with palette

\[
Q_4=\{0,1,2,3\}.
\]

For an uncommitted focus vertex `v`, the exact local observable is

\[
A_s(v)=Q_4\setminus c(N(v)).
\]

No future target, route, surface genus, or theorem-evaluation bit is a mutable
coordinate of the state.

## 2. Current controls

For two distinct colors `p,q`, every connected component of the subgraph induced
by vertices colored in `{p,q}` defines an exact Kempe control: exchange `p` and
`q` on the whole component.

Every such control preserves every committed edge inequality.  Therefore the
current control set

\[
\mathcal A(s)
\]

is derived directly from the current graph and coloring.

## 3. Immediate Control Accessibility

Suppose

\[
A_s(v)=\varnothing.
\]

Then all four palette values occur among the committed neighbors of `v`.  Choose
one committed neighbor `u`, let `p=c(u)`, and choose any `q\in Q_4\setminus\{p\}`.
The `{p,q}` component containing `u` exists by construction.  Swapping that
component gives a distinct state

\[
s' = T_{u,p,q}(s)
\]

with the same graph carrier, the same committed vertex identities, the same
sphere/plane species, and a valid indexed edge ledger.

Hence

\[
\boxed{
A_s(v)=\varnothing
\Longrightarrow
\mathcal A(s)\ne\varnothing.
}
\]

This is an access theorem, not a lookahead theorem.

## 4. Receding-horizon construction

The lawful construction loop is

\[
s_t
\xrightarrow{T_t\in\mathcal A(s_t)}
s_{t+1},
\]

followed by recomputation of

\[
A_{s_{t+1}}(v)
\quad\text{and}\quad
\mathcal A(s_{t+1}).
\]

The agent need not certify `s_n` while acting at `s_t`.  The next state is the
only state that must be currently accessible.

This matches the graph-native control surface already implemented in
`construction_control_surface.py`: the admissible controls themselves generate
the navigation surface, and noncommuting controls generate path-dependent
construction geometry.

## 5. Mechanical witness

`ImmediateControlCertificate` contains exactly

```text
before
focus
move
after
```

and deliberately contains no target path, route, or future-goal coordinate.
Its validity replays the declared component move and checks:

- zero current focus slack requires a control;
- the graph carrier is unchanged;
- committed vertex identity is unchanged;
- genus remains zero;
- every committed edge remains proper;
- the one-step state actually changes.

The exhaustive local test constructs this certificate for all 120 saturated
proper `C5` boundary assignments.  A separate test applies the same law on the
persistent-double-lock exterior carrier and then derives the next control from
the actual resulting state.

## 6. Relation to staging

Immediate access supplies the lawful next action.  Retained witness/history
supplies the proof discipline for staged continuation: a later step is justified
from the state and witness then present, not from an imagined eventual route.

Thus the control semantics are

\[
\boxed{
\text{current carrier}
\to
\text{current controls}
\to
\text{one exact state transition}
\to
\text{recompute access}.
}
\]

The construction surface is generated online by the same parameters the
coloration agent is permitted to navigate.

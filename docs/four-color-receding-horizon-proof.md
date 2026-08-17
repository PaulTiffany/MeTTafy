# Four Color Receding-Horizon Proof Spine

## Status

This note integrates the current graph-native Four Color construction around one rule:

> The coloration agent is entitled to the control that is accessible from the present certified state. After applying one exact control, access is recomputed from the resulting state.

No future route, target state, or theorem verdict is a coordinate of the construction state.

## 1. Fixed theorem species

The mutable construction state is `(G,c)` on the fixed genus-zero Four Color species with palette

\[
Q_4=\{0,1,2,3\}.
\]

For an uncommitted focus vertex `v`, the exact local observable is

\[
A_c(v)=Q_4\setminus c(N(v)).
\]

The construction may commit `v` whenever `A_c(v)` is nonempty.

## 2. Degree-five hard state

After minimal-counterexample reduction to a degree-five focus, the only nontrivial boundary case is a proper `C5` using all four colors. Up to palette and cyclic symmetry its role word is

\[
A\;B\;A\;C\;D.
\]

Its `V4` edge derivative has the forced multiplicity signature

\[
(3,1,1),
\]

with the two singleton derivative modes separated.

## 3. Immediate control accessibility

If `A_c(v)` is empty, every palette color occurs among the committed neighbors. For any committed seed neighbor and any second palette color, the exact two-color component containing the seed exists. Swapping that component is a current graph-derived control and preserves every committed edge inequality.

Thus

\[
A_c(v)=\varnothing
\quad\Longrightarrow\quad
\mathcal A(c)\ne\varnothing.
\]

This is an access statement, not a future-path statement.

## 4. Receding-horizon construction

At stage `t` the agent observes only the current certified state and chooses

\[
T_t\in\mathcal A(c_t).
\]

It then forms

\[
c_{t+1}=T_t(c_t)
\]

and recomputes both `A_{c_{t+1}}(v)` and the graph-derived control set `\mathcal A(c_{t+1})`.

The persistent exterior witness demonstrates why this staging is necessary: one lawful control can preserve zero focus slack while changing the chromatic typing of the same physical carrier, after which a newly computed control produces positive focus slack.

## 5. Finite control audit

For a fixed finite carrier with `n` committed vertices there are at most

\[
4^n
\]

color assignments. Exact Kempe-component controls preserve the carrier, committed vertex identity, palette, and edge ledger. Therefore exhaustive breadth-first traversal of the current Kempe control component terminates.

The mechanical audit has exactly two proof-relevant outcomes:

1. a finite `FocusSlackPathCertificate`, replayable one current control at a time, whose final state satisfies `A(v) != empty`; or
2. a `SlacklessControlComponentCertificate`, proving that the currently declared Kempe-control family has been exhaustively traversed on the retained carrier while every reachable state still has `A(v) = empty`.

The second certificate is not a theorem-level stopping condition. Under the Lipschitz Contract it is retained evidence requiring the admissible control description or witness boundary to expand rather than permitting the construction to forget the obstruction.

## 6. Current demonstrated instances

The mechanical suite establishes:

- all 120 saturated proper bare `C5` colorings have a one-stage exact focus-slack certificate;
- the explicit persistent exterior carrier has no one-stage slack-producing move but has a two-stage receding-horizon certificate;
- every replayed stage is recomputed from the state actually reached and preserves the fixed genus-zero carrier and edge ledger.

## 7. Proof obligation in its present form

The remaining proof work is not an omniscient global-route oracle. It is to prove **control totality across admissible witness expansion**:

> whenever the current control family is exhausted with zero focus slack, the retained planar witness determines a strictly richer graph-native control description, and this expansion cannot repeat indefinitely on a finite genus-zero construction.

The already implemented retained-witness stage rank supplies the finite-history mechanism once the admissible graph-native expansion stages are derived from the planar carrier rather than supplied by the caller.

The plane-dual `V4` continuation calculus and the demonstrated construction holonomy are the current candidates for deriving those stages.

## 8. Inductive completion once control totality is established

For a minimum planar counterexample, delete a degree-five vertex `v` and four-color the smaller graph by minimality. Run the certified receding-horizon construction at `v`.

- If `A(v)` is nonempty, commit any color in it.
- If `A(v)` is empty, take the currently accessible certified control.
- If the local control family is exhausted, retain that exact certificate and derive the next admissible planar control layer.

Control totality plus finite non-replay then yields a finite state with `A(v)` nonempty. Commit `v`, contradicting minimality.

The theorem-specific task is therefore concentrated in the graph-native witness-expansion law; the local state ontology, degree-five algebra, immediate access rule, receding-horizon semantics, finite control audit, and exact replay discipline are already mechanical.

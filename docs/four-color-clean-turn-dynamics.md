# Clean-Turn Dynamics on the Saturated Degree-Five Frontier

**Status:** direct boundary/planar consequences of the clean-turn calculus.  The
only remaining global step stated here is physical-shape growth across a full
persistent orbit.

## 1. Canonical saturated word

Write the proper four-state frontier as

\[
\boxed{A\;B\;A\;C\;D}
\]

on cyclic positions `0,1,2,3,4`.

A clean turn changes exactly one boundary position because the entire chosen
bichromatic component meets the frontier only at its seed.

If the seed has a singleton color, that color disappears from the frontier and
the focus can commit it immediately.  Therefore every clean turn that remains
nonterminal must act at one of the two repeated `A` positions.

Boundary properness leaves no color choice at either repeated position:

- position `0` is adjacent to `D,B`, so its only nontrivial clean replacement is
  `C`;
- position `2` is adjacent to `B,C`, so its only nontrivial clean replacement is
  `D`.

Thus the only persistent boundary-level turns are

\[
A_0\to C
\qquad\text{or}\qquad
A_2\to D.
\]

The graph determines whether the corresponding whole component is clean; the
boundary algebra does not guess.

## 2. If no singleton finishes, both repeated turns are clean

### Repeated-Turn Pair Lemma

If no singleton-colored boundary vertex has a clean turn in the saturated word
`A B A C D`, then **both** repeated `A` positions have clean turns.

### Proof for position 0

The candidate turn at position `0` uses colors `{A,C}`.
The `{A,C}` boundary terminals are

\[
a,c,d,
\]

and `c,d` are adjacent on the boundary, hence already lie in one `{A,C}`
component.

If `a` were not clean for `{A,C}`, it would join that component, so one
`{A,C}` component would contain all three `a,c,d`.

Because singleton turns are assumed unavailable, the singleton `B,D` boundary
vertices `b,e` must lie in one `{B,D}` component; otherwise either singleton
component would itself be a clean terminal turn.

Choose a tree in the `{A,C}` component spanning `a,c,d`.  At least one of the
tree paths `a--c` or `a--d` avoids the remaining third boundary terminal in its
interior.  Either path is a crosscut separating boundary points `b` and `e`.
But a `{B,D}` path joins `b` to `e`, and the color sets

\[
\{A,C\}\cap\{B,D\}=\varnothing
\]

make the two paths vertex-disjoint.  This contradicts planar separation.

Therefore the `{A,C}` component at `a` meets the frontier only at `a`: position
`0` is clean.

### Proof for position 2

The argument is symmetric.  The `{A,D}` boundary terminals are `a,c,e`, with
`a,e` already adjacent.  If `c` joined their component, a spanning tree would
supply an `a--c` or `c--e` crosscut separating `b` from `d`.  No terminal clean
turn implies that `b,d` lie in one `{B,C}` component, giving a disjoint
`b--d` path.  Contradiction.

Hence position `2` is also clean.  \(\square\)

## 3. Turn-based rule; no lookahead

Suppose one persistent clean turn is realized and the focus still has zero
slack.

In the successor, the just-used component remains a clean component for the
inverse color swap.  That is the move back.

But the Repeated-Turn Pair Lemma applies again to the actual successor: if no
singleton clean turn is currently available, **both** occurrences of the new
repeated state are clean.  Therefore the other repeated occurrence supplies a
current clean turn that is not the inverse.

So a proof-relevant controller needs no future search:

```text
if a singleton clean turn exists:
    take it and commit the freed state at the focus
else:
    take the repeated clean turn at the occurrence not used on the preceding turn
```

Each whole component is derived from the actual current coloring before the
turn is applied.

## 4. Pure boundary orbit under persistent noninverse play

Assume, only for contradiction analysis, that no singleton clean turn ever
appears.  Choose position `0` first.  The noninverse rule then forces seed
positions

\[
0,3,1,4,2,0,3,1,4,2,\ldots
\]

so

\[
\boxed{i_t=3t\pmod 5.}
\]

The repeated-state transition is simultaneously forced through the four-cycle

\[
\boxed{A\to C\to B\to D\to A\to\cdots.}
\]

Equivalently the unordered bichromatic turn pairs repeat as

\[
AC,\;BC,\;BD,\;AD,\;AC,\ldots
\]

with period four.

The boundary position phase has period five and the state-pair phase has period
four.  Therefore the complete boundary turn phase has exact period

\[
\boxed{\operatorname{lcm}(5,4)=20.}
\]

After twenty persistent noninverse clean turns, the boundary coloring returns
exactly to its starting word.  Choosing the other repeated occurrence first
gives the reflected orientation of the same 20-turn law.

This is a boundary arithmetic orbit only.  It does **not** change the physical
surface species or introduce a toroidal construction.

## 5. The remaining theorem is now tiny

A counterexample to Four Color continuation through this calculus would have to
support an indefinitely repeated 20-turn boundary orbit while every turn is a
real graph-native clean component and no singleton ever becomes clean.

Thus the remaining target can be stated directly on physical component shape.

### Persistent-Orbit Shape Growth — OPEN

If one complete 20-turn noninverse clean orbit occurs with zero focus slack
throughout, then when the same boundary seed and same bichromatic pair recur,
the newly derived physical component must strictly contain new retained planar
shape relative to the preceding occurrence.

A proof of this statement would finish the turn-level termination argument:
repeating 20-turn blocks would force an infinite strict growth chain of physical
shapes inside one finite planar carrier, impossible.

The theorem should be proved or killed directly.  No Bellman value, phase rank,
SRMF cycle, or future-route coordinate is required.
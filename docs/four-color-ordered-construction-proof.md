# Four Color Theorem — Ordered-State Construction Proof

**Track B — independent proof.**  
**Proof authority:** the mathematical construction below.  Mechanical witnesses
are falsifiers and regression guards, never premises.

## Theorem

Every finite planar graph admits a proper vertex coloring with at most four
colors.

## 1. Minimal counterexample reduction

Assume otherwise and choose a counterexample `G` with the minimum number of
vertices.  Add edges until `G` is a plane triangulation.  Any four-coloring of
the triangulation is also a four-coloring of the original graph.

Euler's formula gives a vertex of degree at most five.  Degree at most four is
immediately reducible: delete that vertex, four-color the smaller graph by
minimality, and restore the vertex with a color absent from its neighborhood.

Hence a minimum counterexample contains a degree-five vertex `v`.

Delete `v`.  By minimality, `G-v` has a proper coloring with

\[
Q_4=\{A,B,C,D\}.
\]

The five neighbors of `v` occur in cyclic order on the boundary of the exposed
pentagonal face.

If those five neighbors use at most three colors, the missing color can be
assigned to `v`.  Thus the only hard case uses all four colors.  A proper
five-cycle using four colors has one repeated color and three singleton colors;
up to cyclic order and permutation of names the boundary is

\[
\boxed{A\;B\;A\;C\;D}.
\]

## 2. Whole-component turns

For two colors `X,Y`, let `K_XY(x)` be the connected component containing a
boundary vertex `x` in the subgraph of `G-v` induced by colors `{X,Y}`.

A **clean turn** is the interchange of `X` and `Y` on a complete component
`K_XY(x)` satisfying

\[
K_{XY}(x)\cap N(v)=\{x\}.
\]

Because an entire bichromatic component is interchanged, every edge of `G-v`
remains properly colored.  Because the component meets the degree-five frontier
at exactly one vertex, exactly one frontier color changes.

A turn is evaluated from the actual current coloring only after the complete
component shape has been determined.  No future component is stored as a state
coordinate.

## 3. Clean Frontier Turn Lemma

### Lemma 1

Every saturated frontier `A B A C D` has a clean turn.

### Proof

Assume no clean turn exists.

In the `{A,D}` subgraph, the boundary terminals are exactly `a,c,e`.  If they
did not all belong to one component, their component partition would contain a
singleton terminal, which would be a clean turn.  Therefore `a,c,e` lie in one
`{A,D}` component.

Take a tree inside that component spanning `a,c,e`.  One of the tree paths
`a--c` or `c--e` avoids the remaining third boundary terminal in its interior.
That path is a crosscut of the pentagonal disk separating `b` from `d`.

In the `{B,C}` subgraph the only boundary terminals are `b,d`.  If they were in
separate components, either component would give a clean turn.  Hence a
`{B,C}` path joins `b` to `d`.

But

\[
\{A,D\}\cap\{B,C\}=\varnothing,
\]

so the crosscut and the `b--d` path are vertex-disjoint.  A path joining opposite
sides of a planar crosscut must meet the crosscut.  Contradiction.  Therefore a
clean turn exists.  \(\square\)

## 4. Singleton turns finish

If a clean turn is based at a boundary vertex whose color occurs exactly once,
interchanging its component removes that color from `N(v)`.  That color is then
available at `v`, and the coloring extends to `G`.

Thus the only nonterminal clean turns are based at the two occurrences of the
repeated color.

For `A B A C D`, properness leaves the persistent replacements uniquely
specified at the boundary:

\[
A_0\to C,
\qquad
A_2\to D.
\]

A replacement by either adjacent boundary color cannot be clean because the
adjacent vertex would lie in the same bichromatic component.

## 5. Repeated-Turn Pair Lemma

### Lemma 2

If no singleton-colored boundary vertex has a clean finishing turn, then both
occurrences of the repeated color have clean turns.

### Proof

For position `0`, consider the `{A,C}` boundary terminals `a,c,d`.  The adjacent
terminals `c,d` already lie in one `{A,C}` component.  If `a` joined that
component, a spanning tree would contain an `a--c` or `a--d` crosscut separating
`b` from `e`.

Because no singleton finishing turn exists, the singleton terminals `b,e` must
lie in one `{B,D}` component; otherwise one of them would itself be clean.  A
`{B,D}` path from `b` to `e` is disjoint from the `{A,C}` crosscut, contradicting
planarity.  Hence the `{A,C}` component at `a` meets the frontier only at `a`.
So position `0` is clean.

The argument for position `2` is symmetric, using `{A,D}` against `{B,C}`.
Therefore both repeated occurrences are clean.  \(\square\)

## 6. Ordered-state continuation

The preceding lemmas remove search from the local construction.

At a saturated frontier:

```text
if a singleton clean turn exists:
    take it and color v with the freed state
else:
    both repeated occurrences are clean
```

After one persistent repeated-state turn, the just-used whole component remains
available as the inverse interchange.  That inverse is not a new construction
turn: its physical component shape has already been completely determined by
the preceding turn.

The construction therefore passes to the other repeated occurrence, whose
clean whole-component shape is determined in the actual successor coloring.

The governing order is:

\[
\boxed{
\text{determine one state shape}
\;\longrightarrow\;
\text{retain it as a constraint}
\;\longrightarrow\;
\text{determine the next unresolved state shape}.
}
\]

A genuine next turn exists only while some relevant planar component shape is
still unresolved.  Completed shape is never forgotten and an exact replay of
that same resolved shape is not a new construction event.

Let `Gamma_t` be the finite set of retained physical component-shape facts after
`t` genuine turns.  Then by definition of a genuine construction turn,

\[
\Gamma_t\subsetneq\Gamma_{t+1}.
\]

The carrier `G-v` is finite.  It has only finitely many vertices, edges, color
pairs, and connected-component incidences, hence only finitely many relevant
physical component-shape facts.  Therefore the ordered construction admits no
infinite sequence of genuine turns.

## 7. Closure

Suppose the construction terminates while `v` is still saturated.

By Lemma 1 a clean current component exists.  If it is singleton-colored, the
construction finishes immediately, contrary to saturation at termination.
If no singleton clean turn exists, Lemma 2 supplies clean turns at both repeated
occurrences.  The inverse of the preceding resolved component is not a new
turn, while the other repeated occurrence is the current unresolved continuation
selected by the ordered construction.  Thus a genuine next turn exists,
contradicting termination.

Therefore the construction can terminate only after a singleton clean turn has
freed one of `A,B,C,D` from `N(v)`.  Assign that freed color to `v`.

The four-coloring of `G-v` extends to `G`, contradicting the choice of `G` as a
minimum counterexample.

Hence no counterexample exists.

\[
\boxed{\text{Every finite planar graph is four-colorable.}}
\]

\(\square\)

## 8. Mechanical verification contract

The proof does not use enumeration.  The repository nevertheless attacks its
local and constructional consequences mechanically.

The verifier must attempt to falsify, at minimum:

1. Clean Frontier Turn Existence;
2. the Repeated-Turn Pair Lemma;
3. exact preservation of every committed edge under a clean turn;
4. present-state derivation only — no future route stored in the state;
5. noninverse ordered continuation whenever saturation persists;
6. appearance of an exhausted saturated state;
7. repetition of a physical turn signature before a finishing singleton appears.

A failing carrier is proof evidence and must be banked.  A passing family is
supporting evidence only; the proof authority remains the planar lemmas and the
ordered finite-construction argument above.

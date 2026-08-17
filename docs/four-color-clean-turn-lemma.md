# Clean Frontier Turn Lemma

**Status:** direct planar lemma; no Four Color conclusion imported.

## 1. Setup

Let `v` be the uncommitted degree-five focus.  After deleting `v`, retain the
closed genus-zero carrier as a disk whose boundary neighbors occur in cyclic
order

\[
a,b,c,d,e.
\]

In the saturated four-state case, relabel the boundary

\[
\boxed{A\;B\;A\;C\;D}.
\]

For two colors `X,Y`, let `K_XY(x)` denote the connected component containing
boundary vertex `x` in the subgraph induced by colors `{X,Y}`.

A **clean turn** is a complete bichromatic component swap for which

\[
K_{XY}(x)\cap\{a,b,c,d,e\}=\{x\}.
\]

Because the whole component is known before the turn is applied, a clean turn
changes exactly one frontier state and leaves the other four indexed frontier
obligations untouched.

## 2. Lemma

### Clean Frontier Turn Existence

Every saturated proper degree-five frontier `A B A C D` on a planar disk has at
least one clean turn.

## 3. Proof

Assume, for contradiction, that no clean turn exists.

Consider the subgraph induced by colors `{A,D}`.  Its boundary terminals are
exactly

\[
a,c,e.
\]

If these three terminals did not all lie in the same `{A,D}` component, their
component partition would contain a singleton block: a partition of three
objects with no singleton block can only be the one-block partition.  That
singleton terminal would itself define a clean turn, contrary to assumption.

Hence

\[
\boxed{a,c,e\text{ lie in one connected }\{A,D\}\text{ component}.}
\]

Take a tree inside that component spanning `a,c,e`.  Among the two unique tree
paths `a--c` and `c--e`, at least one avoids the remaining third boundary
terminal in its interior.  Call that path `P`.

- if `P` joins `a` to `c`, the boundary points `b` and `d` lie on opposite arcs
  of the disk boundary cut by `a,c`;
- if `P` joins `c` to `e`, the boundary points `d` and `b` again lie on opposite
  arcs cut by `c,e`.

Thus `P` is a planar crosscut separating `b` from `d`.

Now consider the subgraph induced by colors `{B,C}`.  Its only boundary
terminals are

\[
b,d.
\]

Under the assumption that no clean turn exists, `b` and `d` cannot lie in
separate components; either singleton component would be clean.  Therefore
there is a `{B,C}` path `Q` joining `b` to `d`.

But the color sets are disjoint:

\[
\{A,D\}\cap\{B,C\}=\varnothing.
\]

So `P` and `Q` are vertex-disjoint.  This is impossible because `Q` joins two
boundary points separated by the crosscut `P`.

Contradiction.  Therefore a clean turn exists.  \(\square\)

## 4. Immediate turn law

A saturated proper `C5` uses one repeated color and three singleton colors.

If a clean turn is seeded at a singleton-colored boundary vertex, that color
disappears from the frontier after the turn.  The focus therefore has a current
legal color immediately.

If zero focus slack persists after a clean turn, the seed must have carried the
repeated color.  Properness of the `C5` then forces the new boundary color: at
that repeated position the two adjacent frontier colors exclude two singleton
states, so the only nontrivial clean replacement is the third singleton state.

Hence every nonterminal clean turn has the simple form

\[
\boxed{
\text{repeated state}\longrightarrow\text{the unique non-neighbor singleton state}.
}
\]

There are no additional boundary-level choices hidden in that turn.

## 5. What remains

The earlier open problem was too large:

```text
some global admissible traversal must eventually succeed
```

The direct planar lemma reduces it to:

```text
while the focus remains saturated,
there is always at least one clean whole-component turn.
```

The remaining theorem is now termination/selection at the **turn** level:

### Sequential Clean-Turn Termination — OPEN

Starting from a saturated degree-five frontier, repeated turn-by-turn use of
clean components can be selected so that a singleton state becomes clean in
finitely many turns, after which the focus commits that freed state.

The existing hard witnesses show this cannot be replaced by a one-turn claim:
one retained three-interior planar carrier requires three clean turns under the
current exact component calculus.

The proof task is therefore to derive the finite turn law from how each realized
component shape constricts the next one, not to invent a micro-action progress
scalar.
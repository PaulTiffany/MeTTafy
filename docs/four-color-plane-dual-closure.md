# Plane-Dual Continuation for Witness-Expansion Closure

**Status:** exact local/planar calculus plus explicit negative guards. This note does not claim Witness-Expansion Closure or the Four Color Theorem.

## 1. Start from the actual construction boundary

Let the saturated degree-five boundary have V4 derivative word

\[
(\delta_0,\ldots,\delta_4),\qquad \delta_i\in V_4\setminus\{0\}.
\]

The established C5 law gives multiplicities `3,1,1`. Choose one singleton mode
\(\sigma\). The other two nonzero modes will be called the selected modes.

This choice is not a new color and not an observer projection. It is a
parameterization of the existing committed coloring.

## 2. Triangle continuation law

For any properly colored triangular face with vertex colors `x,y,z`, its three
edge differences are

\[
x-y,\quad y-z,\quad z-x.
\]

In `V4`, three distinct vertex colors force these to be exactly the three
nonzero elements of `V4`, once each.

Therefore, after excluding one mode \(\sigma\), every interior triangular face
is incident to exactly two selected-mode edges.

In the embedded dual this gives degree two at every interior triangle. The
selected-mode continuation is consequently a disjoint union of paths and
cycles. Boundary occurrences of the selected modes are path terminals.

For a saturated C5 and singleton \(\sigma\), exactly four boundary edges are
selected. Their four terminals can be paired by the embedded degree-two network.
Planarity allows only the two noncrossing perfect matchings in cyclic order.

This is the first exact plane-derived restriction on the operational move.

## 3. Domain translation law

Let a simple dual continuation path cut the disk into two sides and suppose all
primal edges crossed by the cut carry modes different from \(\sigma\). Translate
every color on one side by \(\sigma\in V_4\).

- An edge with both ends on the same side retains its difference.
- A cut edge of old mode `m` receives new mode

\[
m' = m+\sigma.
\]

Because the cut contains no \(\sigma\)-mode edge, `m != sigma`, and hence
`m+sigma` is another nonzero V4 mode. No cut edge becomes monochromatic.

Thus the translation is an exact ledger-preserving coloring transformation.
Its boundary effect occurs only at the two boundary edges where the dual path
terminates; their modes are toggled by \(\sigma\).

This turns an operational recoloring from an assumed Kempe move into a
consequence of the plane parameterization plus an embedding witness.

## 4. Opening versus locked pairings

For every saturated C5 and either singleton choice \(\sigma\), the two
noncrossing terminal pairings split exactly into:

1. one **opening pairing**: translating either path makes the two singleton
   derivative edges adjacent, so the boundary becomes a three-color C5 and the
   center opens;
2. one **locked pairing**: translating either path leaves the singleton defects
   separated, so the boundary remains saturated.

The repository checks this classification over all 120 saturated proper C5
assignments. Enumeration is a falsifier/witness here; the structural source is
the triangle degree-two continuation law and planar noncrossing.

## 5. Two failed descent measures, retained as guards

### Boundary-only potential fails

A locked domain translation is an involution at the V4 boundary level: applying
the same translation across the same cut twice returns the original derivative
word because \(\sigma+\sigma=0\).

Hence a potential depending only on the five boundary modes cannot justify
strict monotone descent under all legal locked transformations. A locked
boundary can participate in a 2-cycle.

The missing termination quantity must therefore retain more state than the
C5 derivative word: at minimum the traversed continuation/witness history or an
irreversible construction resource.

### Jordan interior cardinality fails

The existing explicit planar lock witness already contains lock paths whose
closure with a boundary arc is a face. Such a Jordan domain has zero interior
vertices while the original center is still locked.

Therefore `number of vertices strictly inside the current Jordan domain` is not
a general strict-descent measure either.

These are useful failures: they narrow Witness-Expansion Closure without
silently changing theorem species.

## 6. Revised closure target

The locked branch now has a sharper form.

Given the actual embedded degree-two continuation network for either singleton
mode, either its pairing is opening, or it is the locked noncrossing pairing.
In the locked case a valid proof must enlarge the retained witness and define a
construction transformation whose state includes enough information to prevent
reversible cycling.

The remaining theorem therefore cannot be merely

\[
\text{locked C5}\to\text{another C5}.
\]

It must be of the form

\[
(K,W,h)\longrightarrow(K',W',h')
\]

where `h` records an explicitly bounded construction resource/history and some
well-founded quantity on the expanded state decreases, or an index-four
nilpotent action consumes one stage without allowing the inverse move as an
admissible construction step.

This is the exact place where the candidate nilpotent traversal
\(\mathfrak I^4=0\) may become relevant. It is not yet connected: an explicit
action of \(\mathfrak I\) on the embedded continuation witness is still required.

## 7. Certification boundary

The new code may certify:

- every proper V4 triangle realizes all three nonzero modes;
- excluding one mode gives local dual degree two;
- four selected C5 terminals have exactly two noncrossing pairing types;
- those pairing types split into opening and locked boundary effects;
- cut translation by the excluded mode preserves nonzero edge differences when
  the cut crosses only selected modes;
- the locked boundary operation is reversible, refuting boundary-only descent.

It may not certify:

- that an arbitrary abstract pairing is realized by a supplied embedding;
- Witness-Expansion Closure in the locked branch;
- a nilpotent action on expanded planar witnesses;
- a completed Four Color proof.

# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Branch:** `agent/ordered-state-construction`  
**Status:** active independent proof program; not yet a closed proof of the Four Color Theorem

## 1. Canonical proof species

Track B is now an **ordered state construction**.

A turn is not one micro-action and not a simultaneous future branch.  A turn
traces one complete graph-native bichromatic component until its physical shape
is known, applies that whole component transformation once, and only then
derives the next turn from the realized successor.

The fixed theorem species remains one finite closed genus-zero planar carrier,
one exact edge ledger, and the four terminal states

\[
Q_4=\{0,1,2,3\}.
\]

No future route, theorem verdict, opening/closure flag, observer state, or
held-out Four Color label is a construction coordinate.

## 2. Easy facts now isolated

- adjacency is definitionally the pairwise conflict relation;
- a minimum planar counterexample reduces to the degree-five local case;
- a saturated proper degree-five frontier has role word `A B A C D` up to
  cyclic/color symmetry;
- the fifth indexed obligation must reuse one of four states by pigeonhole;
- the hard issue is the planar geometry of that reuse, not interaction order or
  palette arithmetic.

Principia quadratic sufficiency, V4 derivatives, SRMF, observer quotients,
Bellman values, phase ranks, holonomy, and browning-out are therefore not
premises of the current theorem.

## 3. New direct planar theorem

`docs/four-color-clean-turn-lemma.md` proves:

### Clean Frontier Turn Existence — PROVED

For every saturated planar degree-five frontier `A B A C D`, at least one
bichromatic connected component meets the frontier in exactly one vertex.
Swapping that entire component therefore changes exactly one frontier state
while preserving all other indexed frontier obligations.

The proof is a direct planar separation argument.  Assuming no such component
forces one `{A,D}` component to span the three boundary terminals `a,c,e` and
one disjoint `{B,C}` component to connect `b,d`; a crosscut extracted from the
first separates the endpoints of the second, contradiction.

## 4. Stronger turn law

`docs/four-color-clean-turn-dynamics.md` proves:

### Repeated-Turn Pair Lemma — PROVED

If no singleton-colored frontier vertex has a clean terminal turn, then **both**
occurrences of the repeated state have clean turns.

Therefore after any persistent clean turn, if the focus is still saturated:

1. the just-used component supplies the inverse turn;
2. the other occurrence of the new repeated state supplies a current clean
   noninverse turn.

No future search is required.  The present-state rule is:

```text
if a singleton clean turn exists:
    take it and commit the freed state
else:
    take the repeated clean turn at the occurrence not used on the preceding turn
```

## 5. Exact boundary calculus

Under the hypothetical condition that no singleton clean turn ever appears,
the noninverse rule is forced.

Choosing one orientation, seed positions follow

\[
0,3,1,4,2,0,\ldots
\]

with period five, while the repeated-state transitions follow

\[
A\to C\to B\to D\to A\to\cdots
\]

with period four.

Hence the nominal saturated boundary phase has exact period

\[
\boxed{\operatorname{lcm}(5,4)=20.}
\]

After twenty persistent noninverse turns the boundary coloring returns exactly
to its starting word.  This is arithmetic on the fixed planar boundary, not a
change of surface topology.

## 6. Mechanical enforcement

`src/mettafy/sequential_frontier.py` now certifies a **clean frontier turn** as
one whole two-color component whose frontier intersection is exactly its seed.
It also provides a bounded exhaustive audit helper; enumeration remains a
falsifier/witness layer and is not part of the proof-state semantics.

`tests/test_sequential_frontier.py` banks two hard instances:

- the persistent double lock resolves in two clean turns;
- the retained three-interior kill witness has no clean route within two turns
  but has an exact three-turn route.

Thus the simplified calculus does not erase the known hard witness.

## 7. Current central theorem gap

The remaining proof target is no longer a global search/descent theorem.

### Persistent-Orbit Shape Growth — OPEN

Assume one full 20-turn persistent noninverse boundary orbit occurs with zero
focus slack throughout.  When the same boundary seed and same bichromatic pair
recur, prove that the newly derived physical component contains strictly more
retained planar shape than at the preceding occurrence.

If this holds, repeated 20-turn blocks would force an infinite strict growth
chain inside one finite planar carrier, impossible.  A singleton clean turn
must therefore appear after finitely many turns, freeing a state for the focus.

This statement should be proved or killed directly.  No substitute progress
scalar is needed.

## 8. Existing machinery retained only as witness bank

The repository's older dual, V4, staged, handoff, phase, holonomy, SRMF, and
observer constructions remain available to falsify or illuminate the small
turn theorem.  They are no longer in the canonical proof dependency chain.

Track A remains the pinned held-out Rocq Four Color development and may be used
only for post-hoc structural comparison after Track-B claims are frozen.

## 9. Bottom line

We do **not** yet have a new proof of the Four Color Theorem.

We do now have a materially smaller proof spine:

```text
degree-five saturated frontier
-> clean whole-component turn exists                  [PROVED]
-> if no singleton finishes, both repeated turns clean [PROVED]
-> noninverse present-state continuation exists       [PROVED]
-> persistent boundary phase has period 20            [PROVED]
-> recurring physical component strictly grows        [OPEN]
-> finite carrier forces a singleton finishing turn
-> commit focus
```

The one open arrow is now physical shape growth under a completely explicit
turn law.
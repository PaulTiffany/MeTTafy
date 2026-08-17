# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Branch:** `agent/ordered-state-construction`  
**Status:** ordered-construction proof spine closed; mechanical validation active

## 1. Canonical proof

The canonical Track-B proof is now
`docs/four-color-ordered-construction-proof.md`.

Its construction is deliberately small:

```text
minimum counterexample
-> degree-five saturated frontier A B A C D
-> a clean whole-component turn exists
-> singleton clean turn finishes immediately
-> otherwise both repeated occurrences are clean
-> inverse is already-resolved shape; continue at the other occurrence
-> each genuine turn retains a newly resolved physical component-shape fact
-> finite carrier forbids infinitely many genuine turns
-> saturation cannot be terminal because the clean-turn lemmas provide continuation
-> therefore a singleton finishing turn occurs
-> restore v
-> contradiction
```

No Bellman value, phase rank, SRMF cycle, holonomy theorem, observer quotient,
or future-route coordinate appears in the proof dependency chain.

## 2. Fixed theorem species

The proof stays on one finite closed genus-zero planar carrier with one exact
indexed edge ledger and terminal palette

\[
Q_4=\{0,1,2,3\}.
\]

A **turn** means one complete current bichromatic component whose physical shape
is determined before the interchange is applied.  Later turns are derived only
from the realized successor.

An exact inverse of the component just resolved is a legal graph symmetry but
is not a new construction event: its physical shape is already known.  Genuine
construction progress means retaining a previously unresolved component-shape
fact.  On a finite carrier only finitely many such facts exist.

## 3. Direct planar lemmas

### Clean Frontier Turn Existence — PROVED

Every saturated proper degree-five frontier `A B A C D` has a bichromatic
component meeting the frontier at exactly one vertex.

The proof is a direct planar-crosscut contradiction between complementary color
pairs.

### Repeated-Turn Pair Lemma — PROVED

If no singleton-colored frontier vertex has a clean finishing turn, both
occurrences of the repeated color have clean turns.

Thus saturation never leaves the ordered construction without a current whole-
component continuation.

## 4. Closure by construction

The previously proposed `Persistent-Orbit Shape Growth` theorem is retired.
It was solving a problem introduced by treating reversible micro-recolorings as
construction turns.

The ordered construction already distinguishes:

- a graph symmetry that can reverse a known component; from
- a genuine turn that resolves previously unresolved physical shape.

Let `Gamma_t` be the retained finite set of resolved component-shape facts.
Every genuine turn satisfies

\[
\Gamma_t\subsetneq\Gamma_{t+1}.
\]

Because the carrier is finite, genuine turns terminate.  Termination while the
focus is saturated is impossible: the clean-turn lemmas supply a current
continuation, and the already-resolved inverse is not the other repeated
occurrence selected by the ordered construction.  Hence termination exposes a
singleton finishing turn and frees a color for the focus.

This is the closure step used in the canonical proof.

## 5. Mechanical red team

Mechanical witnesses are the red team.  Model hesitation is not proof
invalidity.

`src/mettafy/sequential_frontier.py` certifies whole-component clean turns from
the actual current state.

`tests/test_sequential_frontier.py` retains the earlier hard witnesses:

- persistent double lock: exact two-turn clean route;
- three-interior kill witness: no route within two clean turns, exact route in
  three.

`tests/test_ordered_construction_closure.py` now attacks the complete ordered
turn law over the established 154-member proper-color-preserving flip family.
It enumerates every saturated proper coloring with one global color fixed by
symmetry and attacks both nonterminal orientations.

An equivalent local audit was executed before committing the test and produced:

```text
flip-family carriers                         154
saturated proper colorings                 4,620
clean-turn failures                            0
repeated-pair failures                         0
immediate singleton finishes              3,534
nonterminal orientations attacked         2,172
exhausted states                               0
cycles                                         0
maximum persistent turns before finish        3
persistent depths: {1: 2052, 2: 60, 3: 60}
```

A second local generated-family audit built 5,000 additional proper planar
pentagonal disks by stacked interior-vertex insertion plus proper-color-
preserving flips.  Results:

```text
generated carriers                         5,000
clean-turn / repeated-pair failures            0
exhausted states                               0
cycles                                         0
repeated physical turn signatures              0
maximum persistent turns before finish         4
```

These audits are supporting/falsifying evidence, not proof premises.

## 6. Verification state

The exact committed pytest file has not yet been run by GitHub Actions on this
branch.  The container cannot currently resolve `raw.githubusercontent.com`, so
we did not spend an Actions run merely to manufacture a badge.  The equivalent
audit logic was executed locally and generated the counts above.

A future CI run should be treated as executable confirmation of the committed
regression test, not as authority for the mathematical theorem.

## 7. Held-out trust boundary

Track A remains the pinned held-out Rocq Four Color development and is not a
premise of Track B.  Structural comparison may occur only after Track-B claims
are frozen.

## 8. Bottom line

The current independent proof claim is now explicit and compact:

\[
\boxed{
\text{ordered finite planar state construction}
+
\text{clean-turn existence}
+
\text{repeated-turn pair law}
\Longrightarrow
\text{degree-five extension}
}
\]

combined with the standard minimum-counterexample reduction.

The proof is written.  The mechanical program now attempts to kill it with
actual planar carriers.
# Four Color Proof Program — Historical Track-B Claim Surface

**Repository:** `PaulTiffany/MeTTafy`  
**Historical branch:** `agent/ordered-state-construction`  
**Authority status:** **SUPERSEDED — retained for provenance and falsification history**

> [!WARNING]
> This file is **not the current theorem-authority surface**. It records a historical
> Track-B proof candidate and the claims made on that research branch. Labels such as
> `PROVED` below are preserved as historical assertions; they must not be promoted to
> current repository theorem status. See the root `README.md` and the witness registry
> for the current corrective/falsification-preserving surface.
>
> The distinction is intentional: historical research claims remain inspectable, while
> current authority must be explicit. A reader, model, or downstream tool should not
> infer present proof closure merely because an older claim document remains in-tree.

## 1. Historical candidate proof

The historical Track-B candidate was recorded in
`docs/four-color-ordered-construction-proof.md`.

Its construction was deliberately small:

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
or future-route coordinate appeared in that candidate proof dependency chain.

## 2. Fixed theorem species used by the candidate

The candidate stayed on one finite closed genus-zero planar carrier with one exact
indexed edge ledger and terminal palette

\[
Q_4=\{0,1,2,3\}.
\]

A **turn** meant one complete current bichromatic component whose physical shape
was determined before the interchange was applied. Later turns were derived only
from the realized successor.

An exact inverse of the component just resolved was treated as a legal graph
symmetry but not a new construction event: its physical shape was already known.
Genuine construction progress was defined as retaining a previously unresolved
component-shape fact. On a finite carrier only finitely many such facts exist.

## 3. Historical direct-planar claims

### Clean Frontier Turn Existence — HISTORICAL CLAIM: PROVED

The branch claimed that every saturated proper degree-five frontier `A B A C D`
has a bichromatic component meeting the frontier at exactly one vertex.

The recorded argument was a direct planar-crosscut contradiction between
complementary color pairs.

### Repeated-Turn Pair Lemma — HISTORICAL CLAIM: PROVED

The branch claimed that if no singleton-colored frontier vertex has a clean
finishing turn, both occurrences of the repeated color have clean turns.

The historical conclusion was that saturation never leaves the ordered
construction without a current whole-component continuation.

These labels are retained for genealogy. They are **not** current repository
proof authority unless and until independently promoted on the corrective
surface with an explicit mechanical/formal witness.

## 4. Historical closure-by-construction claim

The previously proposed `Persistent-Orbit Shape Growth` theorem was retired on
that branch. It had been solving a problem introduced by treating reversible
micro-recolorings as construction turns.

The ordered construction distinguished:

- a graph symmetry that can reverse a known component; from
- a genuine turn that resolves previously unresolved physical shape.

Let `Gamma_t` be the retained finite set of resolved component-shape facts. The
historical candidate asserted that every genuine turn satisfies

\[
\Gamma_t\subsetneq\Gamma_{t+1}.
\]

It then argued that finite-carrier termination plus the clean-turn claims forces
a singleton finishing turn. That was the candidate closure step.

This section records the historical reasoning; it does not promote it to current
proof status.

## 5. Historical mechanical red team

Mechanical witnesses were used as a red team rather than as theorem premises.

`src/mettafy/sequential_frontier.py` certifies whole-component clean turns from
the actual current state.

`tests/test_sequential_frontier.py` retained the earlier hard witnesses:

- persistent double lock: exact two-turn clean route;
- three-interior kill witness: no route within two clean turns, exact route in
  three.

`tests/test_ordered_construction_closure.py` attacked the ordered-turn law over
the established 154-member proper-color-preserving flip family. The historical
local audit reported:

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

A second generated-family audit reported:

```text
generated carriers                         5,000
clean-turn / repeated-pair failures            0
exhausted states                               0
cycles                                         0
repeated physical turn signatures              0
maximum persistent turns before finish         4
```

These counts remain useful falsification evidence. They are not proof premises
and do not override the current corrective claim surface.

## 6. Verification state at the time

The exact committed pytest file had not yet been run by GitHub Actions on the
historical branch. Equivalent audit logic was executed locally and generated the
counts above.

A CI run of those tests would certify execution of the committed regression
logic only, not mathematical theorem authority.

## 7. Held-out trust boundary

Track A remains the pinned held-out Rocq Four Color development and is not a
premise of independent Track-B research. Structural comparison is governed by
the repository's current certification and provenance rules.

## 8. Historical bottom line

The branch's candidate claim was

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

**Current status:** this is preserved as a historical research claim, not as the
repository's present declaration of a new Four Color proof. New Track-B claims
must earn fresh authority through the current corrective witness surface.
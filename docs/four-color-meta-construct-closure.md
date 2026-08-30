# Four Color Two-Meta-Construct Closure Surface

**Status:** active independent Track-B research surface; **not a new Four Color proof claim**.

This note records the corrected closure target after separating **test time** from **game time** and, more sharply, separating **imaginary structure** from **realized authority**.

## Core correction

A realized partial coloring is not required to execute every recoloring considered during search. Counterfactual branches may cycle, reverse, become uglier, terminate early, restart, or be represented in an entirely different internal language. They are imaginary research objects, not construction history.

The stronger interface is therefore:

```text
RealizedMap + Focus
  -> open imagination box
arbitrary caller-defined imaginary witness structure
  -> sound projection / abstention
V4 | None
  -> actual-map admissibility check
CertifiedInstantiation
  -> instantiate exactly one void
RealizedMap
```

The box is **not** a search-depth bound. It is an authority boundary.

The executable implementation still handles only finite concrete data at runtime, of course. The claim is narrower and more important: proof authority does not depend on first forcing imagination into a fixed finite route, path length, rollout depth, or monotone trajectory representation.

## Unbounded within the box

`ImaginationBox` fixes only two things:

- the unchanged realized map;
- the unchanged void focus.

It deliberately carries no `path`, `route`, `depth`, `max_depth`, `steps`, `max_steps`, or finite-state schema.

An `ImaginaryProjection` may inspect any caller-supplied witness object. That object can encode red-team patterns, alternating interactions, nested counterfactuals, reversals, repeated states, transformed coordinates, symbolic summaries, or another useful representation.

The projection returns either:

```text
None
```

which remains wholly imaginary, or a proposed `V4` color.

A proposed color still has **zero authority** until it validates as a `CertifiedInstantiation` against the unchanged realized map and focus. Thus:

```text
rich imaginary witness
        ↓ compression
      V4 proposal
        ↓ actual-map check
CertifiedInstantiation
```

The witness itself does not cross the wall.

This is the formal version of the methodological claim:

> do not bound imagination; formalize the compression of imagination.

## Current two-family research ontology

The present local degree-five hypothesis has two meta-construct families:

1. **red-team** — the three-upward-state / `A-B-A` family already formalized by `RedTeamComposition.lean`;
2. **alternating pair** — the two-upward-running-state family with alternating horizontal state interactions.

The repository represents these as `MetaConstructFamily.redTeam` and `MetaConstructFamily.alternatingPair`.

That two-constructor type is **not** an exhaustiveness proof. The actual mathematical statement remains explicit:

> Every relevant planar continuation at the precommit frontier classifies into one of the two families.

In Lean this obligation is named `PlanarTwoFamilyExhaustive`. No inhabitant is supplied.

## Reachability is also explicit

The claim that "the answer is in imagination space" is represented as a separate proposition rather than assumed by the type system.

In Lean, `ProjectionReachable` means:

```text
there exists some imaginary witness
and some V4 color
such that the projection returns that color.
```

No depth bound appears in that proposition. But neither does the existence of an arbitrary witness type prove reachability by itself.

`ProjectionSound` is the complementary authority condition:

```text
if the projection returns a color,
that color is admissible on the unchanged realized map.
```

Together they yield a real `CertifiedInstantiation`:

```text
ProjectionReachable + ProjectionSound
-> CertifiedInstantiation
```

and the existing construction theorem then gives exactly one realized void consumption.

This is the sharper remaining bridge:

```text
find the right quotient/projection of imagination
rather than force imagination itself to descend monotonically.
```

## Restart versus void/end

The local semantic endpoints remain intentionally asymmetric.

### Restart

A restart means only:

> this observed imaginary prefix did not authorize the next realized move.

Restart carries no color, no route, no predicted response, and no construction authority. It leaves the realized map unchanged and consumes zero voids.

### Void/end

A void/end is allowed to cross the authority boundary only when it contains a `CertifiedInstantiation` checked against the unchanged realized map.

Therefore:

```text
imagined opening != void/end
```

and

```text
valid actual-map certificate -> void/end -> exactly one realized void consumed
```

This preserves the earlier correction that an already saturated realized `A B A C D` focus cannot be repaired merely because an imagined recoloring exposes slack.

## What changed in the proof burden

The earlier historical construction attempted to prove progress by accumulating an ever-growing ledger of resolved shape facts. That was solving a problem created by treating reversible imagined or exploratory transformations as if they were construction turns.

The corrected target does **not** require a Lyapunov function over counterfactual dynamics. Test-time reasoning may revisit states, stutter, branch, reverse, change representation, or restart.

The remaining burden is sharper:

```text
planar two-family exhaustiveness
+
sound imagination-projection reachability from every strategy-safe nonterminal state
-> one safe realized void instantiation
```

The second clause refines the existing precommit target captured by `StrategyIRComplete` and `EveryStrategySafeStateHasSafeInstantiation` in `TestTimeActiveInference.lean`.

## Mechanical implementation

`src/mettafy/meta_construct_closure.py` now provides:

- the two-family ontology;
- finite-prefix restart semantics;
- `ImaginationBox`, which fixes authority without fixing search shape;
- `ImaginaryProjection`, which compresses arbitrary witness objects to `V4 | None`;
- fail-closed actual-map checking before any projected answer can become a certificate;
- explicit two-family coverage with a separately supplied `exhaustive` premise;
- typed `Restart` and `VoidEnd` endpoints;
- a mechanical void-delta check;
- a `ClosureObligation` ledger that refuses to report closure unless both planar exhaustiveness and sound imagination-projection reachability are present.

`tests/test_meta_construct_closure.py` checks that:

- a partial red-team prefix may stop without advancing construction;
- the imagination box has no route/depth/step budget fields;
- arbitrarily structured witness data compresses to certificate-only authority;
- 10,000 repeated imaginary labels do not become construction history;
- abstention leaves the realized map untouched;
- an unsound projected color cannot cross the authority wall;
- observing both named families does not silently prove planar exhaustiveness;
- a blocked realized `ABACD` focus cannot be promoted to void/end;
- an unrelated certificate cannot close another obligation;
- a valid actual-map certificate consumes exactly one realized void.

`examples/four_color/MetaConstructClosure.lean` formalizes the same distinction with an arbitrary witness type, `ProjectionSound`, `ProjectionReachable`, `compressImagination`, and a theorem that successful compression consumes exactly one realized void regardless of the internal witness representation.

## Current bottom line

The corrected candidate shape is now:

```text
minimum-counterexample / precommit reduction
-> open imaginary reasoning inside a fixed authority box
-> every relevant continuation falls into one of two meta-construct families     [OPEN]
-> arbitrary imaginary structure may branch / stutter / reverse / restart
-> some witness projects to a V4 answer                                         [OPEN]
-> every projected answer is sound on the actual map                            [PROOF OBLIGATION]
-> erase the imaginary witness
-> CertifiedInstantiation
-> instantiate exactly one void
-> repeat on the realized successor
```

The repo therefore no longer needs to demand monotone progress from imagination space. It needs to prove the right compression theorem and the two explicitly named open bridges.
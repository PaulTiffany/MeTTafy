# Four Color Two-Meta-Construct Closure Surface

**Status:** active independent Track-B research surface; **not a new Four Color proof claim**.

This note records the corrected closure target after separating **test time** from **game time**.

## Core correction

A realized partial coloring is not required to execute every recoloring considered during search. Counterfactual branches may cycle, reverse, become uglier, terminate early, or be discarded. They are inference artifacts, not construction history.

The construction boundary is therefore:

```text
RealizedMap
  -> inspect / roleplay / branch / restart
InferenceEpisode
  -> actual-map admissibility proof
CertifiedInstantiation
  -> instantiate exactly one void
RealizedMap
```

A test-time branch may stop at any finite prefix. In particular, a red-team pattern does not need to grow into a canonical complete picture before the branch can terminate. Ending the branch as **restart** changes no realized state.

## Current two-family research ontology

The present local degree-five hypothesis has two meta-construct families:

1. **red-team** — the three-upward-state / `A-B-A` family already formalized by `RedTeamComposition.lean`;
2. **alternating pair** — the two-upward-running-state family with alternating horizontal state interactions.

The repository now represents these as `MetaConstructFamily.redTeam` and `MetaConstructFamily.alternatingPair`.

That two-constructor type is **not** an exhaustiveness proof. The actual mathematical statement remains explicit:

> Every relevant planar continuation at the precommit frontier classifies into one of the two families.

In Lean this obligation is named `PlanarTwoFamilyExhaustive`. No inhabitant is supplied.

## Restart versus void/end

The local semantic endpoints are intentionally asymmetric.

### Restart

A restart means only:

> this finite imagined prefix did not authorize the next realized move.

Restart carries no color, no route, no predicted response, and no construction authority. It leaves the realized map byte-for-byte conceptually unchanged and consumes zero voids.

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

The corrected target does **not** require a Lyapunov function over counterfactual dynamics. Test-time reasoning may revisit states.

The remaining burden is sharper:

```text
planar two-family exhaustiveness
+
sound certified-instantiation reachability from every strategy-safe nonterminal state
-> one safe realized void instantiation
```

The second clause is the existing precommit target captured by `StrategyIRComplete` and `EveryStrategySafeStateHasSafeInstantiation` in `TestTimeActiveInference.lean`.

## Mechanical implementation

`src/mettafy/meta_construct_closure.py` provides:

- the two-family ontology;
- finite-prefix semantics;
- explicit two-family coverage with a separately supplied `exhaustive` premise;
- typed `Restart` and `VoidEnd` endpoints;
- a mechanical void-delta check;
- a `ClosureObligation` ledger that refuses to report closure unless both planar exhaustiveness and certified reachability are present.

`tests/test_meta_construct_closure.py` checks that:

- a partial red-team prefix may stop without advancing construction;
- observing both named families does not silently prove planar exhaustiveness;
- planar classification alone does not create construction authority;
- a blocked realized `ABACD` focus cannot be promoted to void/end;
- a valid actual-map certificate consumes exactly one realized void.

`examples/four_color/MetaConstructClosure.lean` checks the same authority boundary formally and names the missing planar theorem directly.

## Current bottom line

The corrected candidate shape is now:

```text
minimum-counterexample / precommit reduction
-> finite local test-time inference
-> every continuation falls into one of two meta-construct families        [OPEN]
-> branches may restart without construction progress
-> at least one branch yields a sound actual-map CertifiedInstantiation    [OPEN]
-> instantiate exactly one void
-> repeat on the realized successor
```

The repo therefore no longer needs to demand monotone progress from imagination space. It needs to prove the two explicitly named open bridges.

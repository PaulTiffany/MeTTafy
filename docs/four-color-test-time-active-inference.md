# Four Color Test-Time Active Inference

**Status:** current control interpretation; bounded Lean and Python witnesses only.

The independent Four Color lane is not a one-step reducibility argument for the isolated degree-five star.

The map-maker operates receding-horizon:

```text
observe current realized map
-> derive current legal actions
-> imagine consequences / responses
-> select one current action
-> realize exactly that action
-> discard the old counterfactual bundle
-> re-observe the actual successor
```

Only the selected action enters construction history. Imagined cross-cuts, replies, and later possibilities are test-time inference, not intermediate realized maps and not stored future-route coordinates.

## Hard -> hard is allowed

For canonical

```text
A B A C D
```

a proper one-site rewrite of the repeated `A` can produce

```text
A B D C D
```

while the frontier still uses all four colors. `TestTimeActiveInference.lean` banks this as a negative witness.

Therefore the target is **not**

```text
every hard state -> opens in one move.
```

The existing red-team theorem is intentionally weaker and compatible with the negative witness:

```text
one realized proper hard-state action
-> focus opens now
   OR
-> actual successor is hard again.
```

In the second case the controller does not replay an old plan. It re-observes the successor and derives its current action surface again.

## Graph-native implementation

`src/mettafy/construction_control_surface.py` already implements this discipline.

`ImmediateControlCertificate` derives one current Kempe-component control from the actual current construction and certifies exactly one realized successor. It contains no later target or route.

`ColorationControlSurface` derives controls from each current `ConstructionState`. After a step, any later control is recomputed from the resulting state. Its bounded breadth-first search is an audit/falsification tool, not proof-relevant lookahead.

Thus the control interpretation is:

```text
lawful now != terminal now != globally closing
```

## Viability and the actual closure debt

Current actionability is only the first target:

```text
nonterminal current state -> at least one current legal action.
```

That still does not prove eventual opening. The stronger failure object is a reachable **closed nonterminal action class**: a nonempty set of realized states such that

1. no state in the set is terminal/open; and
2. every currently available action from every state in the set realizes another state in the same set.

`TestTimeActiveInference.lean` names this object as `ClosedNonterminalClass` and the desired exclusion as `NoClosedNonterminalClass`. The exclusion is deliberately **not proved** yet.

A successful adaptive proof must rule out such a trap for the actual graph-derived action relation, or establish an equivalent theorem. This need not take the form of a monotone scalar or predetermined route.

## Relation to PR #68

The superseded imagined-exchange experiment typed the hypothetical opposite response as already carrying a clean `B` or `D` escape. That made the useful response part of the interface rather than deriving it from weaker current-map facts.

The correction is:

```text
imagined response = inference input
not
imagined response = proof of future success.
```

Counterfactual evaluation may guide which current action to realize. Once the action is realized, the old hypothetical bundle is discarded and the actual map is observed again.

## Proof boundary

This lane currently claims:

- exact V4 hard-frontier algebra;
- whole-turn properness preservation;
- hard-state action can open or re-enter the hard species;
- hard -> hard genuinely occurs in the canonical finite frontier witness;
- receding-horizon/current-state control is represented explicitly;
- the no-trap theorem is visible as an open obligation.

It does **not** claim:

- one-step degree-five reducibility;
- that every clean carrier is singleton/color-freeing;
- that current actionability implies eventual success;
- a monotone progress ranking;
- a stored future route;
- `NoClosedNonterminalClass` for arbitrary planar maps;
- a new proof of the Four Color Theorem.

The research target is now sharper:

```text
current-map actionability
+ realize-one / re-observe control
+ no reachable closed nonterminal action class
+ construction/map-completion wrapper
-> independent closure candidate.
```

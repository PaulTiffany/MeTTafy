# Four Color Two-Meta-Construct Closure Surface

**Status:** active independent Track-B research surface; **not a new Four Color proof claim**.

This note records the corrected closure target after separating **test time** from **game time**, separating **imaginary structure** from **realized authority**, and reconnecting projection reachability to the earlier **Decision Reachability** pattern: a deciding result is reached through an admissible chain of refinements rather than postulated as a bare existential.

## Core correction

A realized partial coloring is not required to execute every recoloring considered during search. Counterfactual branches may cycle, reverse, become uglier, terminate early, restart, or be represented in an entirely different internal language. They are imaginary research objects, not construction history.

The interface is:

```text
RealizedMap + Focus
  -> open imagination box
arbitrary imaginary work
  -> finite witnessed Decision Reachability residue
if-this -> then-this -> ... -> deciding endpoint
  -> sound projection / abstention
V4 | None
  -> actual-map admissibility check
CertifiedInstantiation
  -> instantiate exactly one void
RealizedMap
```

The box is **not** a search-depth bound. It is an authority boundary.

The successful proof residue is finite because it must be transferable and auditable. That does **not** impose a fixed bound on imagination. Search may branch, restart, stutter, revisit a representation, or run arbitrarily far before one finite deciding chain is retained.

This is the same raw/generated/witnessed discipline used elsewhere in the research program: semantic possibility is larger than the finite witness surface. Here the specialization is concrete: imagination may be open; a claim crossing into construction must leave a finite inspectable chain.

## Unbounded within the box

`ImaginationBox` fixes only two things:

- the unchanged realized map;
- the unchanged void focus.

It deliberately carries no `path`, `route`, `depth`, `max_depth`, `steps`, `max_steps`, or finite-state schema.

An `ImaginaryProjection` may inspect any caller-supplied witness object. That object can encode red-team patterns, alternating interactions, nested counterfactuals, reversals, repeated states, transformed coordinates, symbolic summaries, or another useful representation.

The projection returns either `None`, which remains wholly imaginary, or a proposed `V4` color. A proposed color still has **zero authority** until it validates as a `CertifiedInstantiation` against the unchanged realized map and focus.

```text
rich imaginary work
        ↓ retain one deciding residue
finite admissible Decision Reachability chain
        ↓ endpoint projection
      V4 proposal
        ↓ actual-map check
CertifiedInstantiation
```

The imaginary workspace does not cross the wall.

> do not bound imagination; formalize the compression of imagination.

## Decision Reachability is the missing connection

The earlier `ProjectionReachable` definition said only:

```text
there exists some imaginary witness
and some V4 color
such that the projection returns that color.
```

That was extensionally correct but operationally thin. The repository now gives it a witnessed meaning.

`AdmissibleRefinementChain step seed endpoint` is a finite proof object whose adjacent states satisfy a caller-supplied admissible refinement relation:

```text
seed
  -- admissible --> s1
  -- admissible --> s2
  ...
  -- admissible --> endpoint
```

`DecisionWitness` adds the deciding fact:

```text
projection(endpoint) = some color
```

and `DecisionReachable` is the existence of such a witness.

There is deliberately no maximum chain length. One can prove a chain of length 3, 10,000, or any other finite length without changing the interface. The theorem

```text
decisionReachable_implies_projectionReachable
```

shows that the old existential is now only the extensional shadow of the stronger auditable object.

This is a direct reuse of the earlier **Decision Reachability** research pattern: a deciding refinement must be reachable through the admissible refinement structure, not merely exist from a God's-eye view. The Four Color formalization specializes that pattern to imagination without claiming that the forcing correspondence itself proves the graph-theoretic premise.

## Current two-family research ontology

The present local degree-five hypothesis has two meta-construct families:

1. **red-team** — the three-upward-state / `A-B-A` family already formalized by `RedTeamComposition.lean`;
2. **alternating pair** — the two-upward-running-state family with alternating horizontal state interactions.

The repository represents these as `MetaConstructFamily.redTeam` and `MetaConstructFamily.alternatingPair`.

That two-constructor type is **not** an exhaustiveness proof. The actual mathematical statement remains explicit:

> Every relevant planar continuation at the precommit frontier classifies into one of the two families.

In Lean this obligation is named `PlanarTwoFamilyExhaustive`. No global inhabitant is supplied.

## The two missing pieces now compose

Previously the repository carried planar exhaustiveness and projection reachability beside one another. It now contains an explicit bridge.

A caller supplies `ContinuationAdvance`, meaning that one imaginary refinement was generated by one relevant planar continuation. Forgetting the continuation label gives `ContinuationGeneratedStep`.

`TwoFamilyGeneratedStep` retains the same refinement while additionally recording that its generating continuation classifies as red-team or alternating-pair.

Then:

```text
PlanarTwoFamilyExhaustive
+
ContinuationGeneratedStep
->
TwoFamilyGeneratedStep
```

and the chain-level transport theorem gives:

```text
DecisionReachable over continuation-generated steps
+
PlanarTwoFamilyExhaustive
->
DecisionReachable over two-family-generated steps
```

The Lean names are:

- `planarExhaustiveness_upgrades_generated_step`;
- `DecisionWitness.upgradeToTwoFamilies`;
- `planarExhaustive_upgrades_decisionReachable`.

So the two-family theorem is no longer a detached taxonomy claim. When supplied, it upgrades every witnessed implication in a deciding chain into the claimed two-family local ontology.

## Projection soundness remains the authority wall

`ProjectionSound` says:

```text
if the deciding endpoint projects a color,
that color is admissible on the unchanged realized map.
```

Decision Reachability plus projection soundness yields construction authority:

```text
DecisionReachable
+
ProjectionSound
->
CertifiedInstantiation
```

via `decisionReachable_sound_has_certificate`.

The chain is erased at the wall. `compressDecision` retains only the actual map, focus, color, and admissibility proof. `compressedDecision_consumes_one_void` proves that however much imagination preceded the residue, successful realization consumes exactly one real void.

## Restart versus void/end

The local semantic endpoints remain intentionally asymmetric.

### Restart

A restart means only:

> this observed imaginary work did not authorize the next realized move.

Restart carries no color, no route, no predicted response, and no construction authority. It leaves the realized map unchanged and consumes zero voids.

### Void/end

A void/end is allowed to cross the authority boundary only when it contains a `CertifiedInstantiation` checked against the unchanged realized map.

```text
imagined opening != void/end
```

```text
witnessed deciding chain
+ sound actual-map projection
-> void/end
-> exactly one realized void consumed
```

This preserves the earlier correction that an already saturated realized `A B A C D` focus cannot be repaired merely because an imagined recoloring exposes slack.

## Connection to the existing precommit target

`TestTimeActiveInference.lean` already banks the construction-level obligation:

```text
EveryStrategySafeStateHasSafeInstantiation safe
```

The new definition

```text
DecisionReachabilityComplete safe
```

states the same burden in transferable imagination language:

> for every strategy-safe nonterminal realized map, there exists one focus, one sound imagination interface, and one finite witnessed admissible decision chain whose compressed successor remains strategy-safe.

The bridge theorem

```text
decisionReachabilityComplete_implies_safe_instantiation
```

proves that this directly discharges the already-banked construction obligation.

This is the key simplification. We no longer need a separate mysterious "projection reachability" theorem plus a separate construction theorem. The transferable proof object is the Decision Reachability chain itself.

## Mechanical implementation

`src/mettafy/meta_construct_closure.py` provides:

- the two-family ontology;
- finite-prefix restart semantics;
- `ImaginationBox`, which fixes authority without fixing search shape;
- `ImaginaryProjection`, which compresses arbitrary witness objects to `V4 | None`;
- `DecisionReachability`, a finite auditable `if-this-then-this` chain with no maximum-length field;
- fail-closed checking of every adjacent refinement step;
- fail-closed checking that the endpoint actually decides;
- fail-closed actual-map checking before the endpoint can become a certificate;
- `end_from_decision`, the only direct chain-to-void/end helper;
- explicit two-family coverage with a separately supplied `exhaustive` premise;
- typed `Restart` and `VoidEnd` endpoints;
- a mechanical void-delta check.

`tests/test_meta_construct_closure.py` checks that:

- a partial red-team prefix may stop without advancing construction;
- the imagination box has no route/depth/step budget fields;
- arbitrary imaginary structure compresses to certificate-only authority;
- 10,000 repeated imaginary labels do not become construction history;
- a Decision Reachability chain records an auditable implication spine;
- a 10,000-step deciding chain is accepted without introducing a maximum-depth parameter;
- one unsupported implication makes the chain fail closed;
- a valid chain with a nondeciding endpoint fails closed;
- an unsound projected color cannot cross the authority wall;
- observing both named families does not silently prove planar exhaustiveness;
- a blocked realized `ABACD` focus cannot be promoted to void/end;
- an unrelated certificate cannot close another obligation;
- local closure can be supplied through witnessed Decision Reachability.

`examples/four_color/MetaConstructClosure.lean` formalizes the same structure with `AdmissibleRefinementChain`, `DecisionWitness`, `DecisionReachable`, two-family chain transport, `compressDecision`, and the bridge to `EveryStrategySafeStateHasSafeInstantiation`.

## Current bottom line

The candidate proof surface is now:

```text
minimum-counterexample / precommit reduction
-> open imaginary reasoning inside a fixed authority box
-> retain one finite admissible if-this-then-this chain
-> endpoint decides a V4 proposal
-> planar exhaustiveness upgrades continuation-generated links into the two families
-> projection soundness checks the endpoint against the unchanged actual map
-> erase the imaginary chain
-> CertifiedInstantiation
-> instantiate exactly one void
-> remain inside the strategy-safe class
-> repeat on the realized successor
```

What remains to earn globally is now sharply named rather than structurally mysterious:

```text
DecisionReachabilityComplete safe
```

plus the planar classification theorem needed to justify the claimed two-family interpretation of the admissible continuation steps.

No Lyapunov law over imagination space is assumed. Imagination remains open inside the box; the proof becomes transferable by retaining only a finite admissible deciding residue.
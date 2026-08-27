# Four Color Test-Time Active Inference

**Status:** authoritative world model for the independent Four Color construction lane. The Four Color Theorem is not proved here.

The controlling distinctions are:

> **Test time is not game time.**

> **Sequential imagination is not sequential construction.**

> **Imagine many. Instantiate one. Re-observe.**

The operational loop is:

```text
realized partial map
-> inspect
-> roleplay hypothetical moves / responses / counter-responses
-> quotient repeated concrete positions into proof-relevant strategy classes
-> amortize the surviving first move
-> certify one admissible V4 state at one current void
-> instantiate exactly that void
-> discard the old imagination episode
-> re-observe the new realized partial map
```

## Three spaces

### REALIZED — construction space

A realized map contains the actual partial coloring. Construction time advances only when one currently void region is instantiated:

```text
void -> V4
```

Already-realized regions are preserved by that construction event. If `V(M)` counts void regions, every realized turn must satisfy

```text
V(M_next) = V(M) - 1.
```

### INFERENCE — imagination space

Kempe swaps, cross-cuts, opposite responses, alternative colorings, red-team branches, hypothetical future commitments, hard-to-hard transformations, mirrors, restarts, and longer levels of thinking live here by default.

They may branch, cycle, revisit a proof-relevant state, contradict one another, or fail. None of those events advances construction time, and no monotone ranking is required inside imagination space.

An imagined state is not a historical successor of the realized map.

A hypothetical future commitment may reduce the number of unresolved vertices **inside that imagined line** while the actual void count remains unchanged. This models game-style reasoning such as:

```text
if I do this,
  and the map answers this,
    then I do this,
      and the map answers that ...
```

Only the first move of such a line is ever eligible to cross back into reality. Deeper imagined commitments are discarded with the episode.

### TERMINAL — result space

Terminal verification accepts only a completed map. A partial map cannot be promoted to the Four Color result interface.

## Three clocks

The model distinguishes:

```text
construction turn t
inference / observation order sigma
level-of-thinking depth d
```

Several counterfactual states may belong to the same construction turn even if a bounded MapMaker inspects them sequentially:

```text
same realized antecedent M_t
-> observe state A at sigma_1
-> observe state B at sigma_2
-> observe state C at sigma_3
```

Construction time is still `t` throughout.

Likewise, a depth-three hypothetical line does not mean three construction moves happened. It means the MapMaker considered three nested possible commitments before deciding whether the depth-zero move should happen at all.

## The authority boundary

The formal authority flow is:

```text
RealizedMap
   -> inspect / roleplay
InferenceEpisode + StrategyIR
   -> explicit soundness derivation
CertifiedInstantiation
   -> instantiate
ConstructionStep
   -> RealizedMap
```

Forbidden shortcuts include:

```text
ImaginedState -> RealizedMap
HypotheticalMap -> RealizedMap
PredictedResponse -> ProofOfSuccess
Depth>0 imagined move -> skip directly across construction turns
```

A successful imagined branch can guide inference, but it cannot acquire proof authority merely by existing.

In Lean, `CertifiedInstantiation` carries only a V4 color and a proof that the color is admissible at the actual void focus. `instantiate` is the only realized execution boundary and proves preservation of non-focus sites plus the one-void construction monotone.

In Python, `src/mettafy/active_inference_boundary.py` mirrors the same separation. `src/mettafy/strategy_ir.py` adds legal hypothetical future commitments and the human MapMaker roleplay vocabulary. `amortize_first_move` permits only a depth-zero imagined commitment to reach the existing `amortize` bridge, which rechecks it against the unchanged actual map.

## Correction: a realized saturated focus is too late

Under the current construction authority, existing realized colors are never rewritten. Therefore if an **actual** void focus is already adjacent to all four V4 colors, then

```text
A_M(v) = empty
```

and there is no lawful `void -> color` instantiation at that focus.

Counterfactual recoloring can expose useful structure in imagination, but it cannot retroactively make a color admissible on the unchanged realized map. The retained negative tests enforce exactly this.

Therefore the central induction target is **not**:

```text
EveryBlockedFocusResolvable
```

for arbitrary already-blocked realized focuses.

The strategy must operate before such a trap is committed.

## Strategy-safe construction target

Let `StrategySafe(M)` mean that the current realized partial map remains inside the class for which the MapMaker policy can continue without rewriting realized history.

The construction target is conceptually:

```text
EveryStrategySafeStateHasSafeInstantiation
```

meaning:

```text
for every strategy-safe nonterminal realized map M,
there exists one actual void focus v and one admissible color c
such that instantiating v := c produces another strategy-safe realized map.
```

This is the induction shape:

```text
StrategySafe(M_0)
StrategySafe(M_t)
  -> exists one certified void -> color move
  -> StrategySafe(M_{t+1})
V(M_{t+1}) = V(M_t) - 1
```

Finiteness of the realized map then supplies the construction clock. The mathematical debt is discovering and proving a sufficiently broad `StrategySafe` class and a complete strategy for remaining inside it.

## Strategy IR: roleplay the bounded MapMaker

The current lowest-level vocabulary is intentionally small:

```text
SEE
ASK
ANSWER
COMMIT-OR-NOT
```

A roleplay transcript records only:

1. what the bounded MapMaker can observe;
2. which proof-relevant question is asked;
3. which response class the map supplies in imagination;
4. which options remain;
5. whether the depth-zero candidate is committed, rejected, or still undecided.

Inherited Four Color vocabulary is not automatically trusted as the ontology. Kempe chains, reducible configurations, discharging language, and other historical abstractions may re-enter only when the roleplay procedure reconstructs a need for them.

The intended workflow is:

```text
counterexample
-> missing proof-relevant distinction
-> minimal new observable / probe / response class
-> refined Strategy IR
```

This is Unweave -> Ribosome: start with mechanically checkable atoms, then rebuild only the strategy language forced by successful and failing roleplay.

## Strategy equivalence and compression

Two concrete imaginary positions are candidates for the same strategy class when the bounded MapMaker has the same proof-relevant view of them:

```text
same observables
same available probes
same response classes
same relevant options
```

The Python `StrategySignature` deliberately leaves this vocabulary open rather than pretending the correct quotient is already known.

A concrete transcript such as

```text
x1 -> x2 -> x3 -> x4 -> x5 -> ...
```

may therefore compress to a small strategy automaton such as

```text
A -> B -> C -> B
```

where the repeated `B` closes a proof-relevant loop instead of requiring indefinite unrolling.

The working empirical hypothesis is:

> **Strategy Compression Hypothesis:** the number of proof-relevant MapMaker response classes is dramatically smaller than the number of concrete coloring configurations required by extensional case checking.

This is a hypothesis to test against historical hard configurations, not a theorem already established.

## Reclassification of the hard-to-hard witness

The canonical frontier

```text
A B A C D
```

admits a proper counterfactual one-site rewrite to

```text
A B D C D
```

that remains hard.

This is retained as an **INFERENCE / NEGATIVE** witness:

```text
one imagined intervention
!=
immediate resolution
```

and, under the corrected construction frame:

```text
an already saturated realized focus
!=
a state that imagination can directly repair
```

The witness is useful primarily as a red-team strategy position: a policy considering an earlier commitment must be able to predict, classify, avoid, or otherwise account for this kind of future trap before reality crosses into it.

## PR #68 lesson

The superseded response type encoded the useful escape directly in the hypothetical response. That supplied the desired conclusion as interface data.

The permanent rule is:

```text
imagined response = inference data
not
imagined response = theorem payload
```

Facts such as `clean`, `open`, `escape`, or `safe` may cross the authority boundary only when derived from weaker premises by an explicit theorem.

## PR #69 lesson

PR #69 correctly banked several negative facts: hard-to-hard hypothetical behavior exists, current actionability is not progress, and one-step reducibility is not assumed.

Its mistake was category placement: frontier recoloring successors were presented as realized construction successors. Those witnesses are now reclassified as counterfactual transformations. The realized construction event remains only `void -> V4` at the focus.

## Open proof obligations

The current proof debt has at least these independent parts:

```text
InferenceSound
StrategyIRCompleteness
EveryStrategySafeStateHasSafeInstantiation
```

`InferenceSound` says a strategy claim promoted to construction is actually admissible on the unchanged realized map.

`StrategyIRCompleteness` says the chosen roleplay/strategy vocabulary is rich enough that every strategy-safe nonterminal realized state yields a strategy-certified first move that remains strategy-safe after real instantiation.

`EveryStrategySafeStateHasSafeInstantiation` is the construction-level existence consequence needed by the finite void-count induction.

The repository intentionally supplies no proof of those universal claims yet.

## Test discipline

New tests and theorem comments should identify their category:

- `REALIZED:` actual partial-map construction facts;
- `INFERENCE:` counterfactual reasoning and strategy-class facts;
- `ROLEPLAY:` bounded `SEE / ASK / ANSWER / COMMIT-OR-NOT` records;
- `BRIDGE:` authority-transfer/soundness facts;
- `TERMINAL:` completed-map facts;
- `NEGATIVE:` falsifiers or category-error guards.

If a test crosses categories without an explicit bridge, its design is invalid.

## Working audit

When uncertain, ask:

> **Did this happen to the map, or only in the MapMaker's imagination?**

If it happened only in imagination, ask:

> **Did this concrete difference change the proof-relevant strategy state?**

If not, quotient it away.

If a strategy wants to affect reality, ask:

> **What exact theorem lets the depth-zero candidate collapse into one lawful instantiation on the unchanged actual map?**

Then instantiate one, discard the old imagination episode, and re-observe.

# Four Color Test-Time Active Inference

**Status:** authoritative world model for the independent Four Color construction lane. The Four Color Theorem is not proved here.

The controlling distinction is:

> **Test time is not game time.**

The operational loop is:

```text
realized partial map
-> inspect
-> imagine interventions / responses
-> amortize reasoning
-> certify one admissible V4 state at the current void focus
-> instantiate exactly that void
-> re-observe the new realized partial map
```

Shortest checksum:

> **Imagine many. Instantiate one. Re-observe.**

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

Kempe swaps, cross-cuts, opposite responses, alternative colorings, red-team branches, hard-to-hard transformations, restarts, and longer hypothetical sequences live here by default.

They may branch, cycle, contradict one another, or fail. None of those events advances construction time, and no monotone ranking is required inside imagination space.

An imagined coloring is not a historical successor of the realized map.

### TERMINAL — result space

Terminal verification accepts only a completed map. A partial map cannot be promoted to the Four Color result interface.

## The authority boundary

The formal authority flow is:

```text
RealizedMap
   -> inspect
InferenceEpisode
   -> explicit soundness derivation
CertifiedInstantiation
   -> instantiate
ConstructionStep
   -> RealizedMap
```

Forbidden shortcuts include:

```text
ImaginedState -> RealizedMap
PredictedResponse -> ProofOfSuccess
```

A successful imagined branch can guide inference, but it cannot acquire proof authority merely by existing.

In Lean, `CertifiedInstantiation` carries only a V4 color and a proof that the color is admissible at the actual void focus. `instantiate` is the only realized execution boundary and proves preservation of non-focus sites plus the one-void construction monotone.

In Python, `src/mettafy/active_inference_boundary.py` mirrors the same separation. `amortize` rechecks the selected color against the unchanged realized `ConstructionState`; an imagined branch with apparent slack cannot self-promote into a realized commit.

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
immediate resolution.
```

It is **not** interpreted as

```text
realized construction history contains ABACD -> ABDCD.
```

The witness refutes naive one-step reducibility. It does not by itself refute adaptive test-time reasoning, and adaptive test-time reasoning does not by itself prove the theorem.

## PR #68 lesson

The superseded response type encoded the useful escape directly in the hypothetical response. That supplied the desired conclusion as interface data.

The permanent rule is:

```text
imagined response = inference data
not
imagined response = theorem payload
```

Facts such as `clean`, `open`, or `escape` may cross the authority boundary only when derived from weaker premises by an explicit theorem.

## PR #69 lesson

PR #69 correctly banked several negative facts: hard-to-hard hypothetical behavior exists, current actionability is not progress, and one-step reducibility is not assumed.

Its mistake was category placement: frontier recoloring successors were presented as realized construction successors. Those witnesses are now reclassified as counterfactual transformations. The realized construction event remains only `void -> V4` at the focus.

The old `NoClosedNonterminalClass` framing is therefore not the central construction theorem. Realized construction consumes voids rather than wandering among recolored historical states.

## Genuine open theorem

The remaining local mathematical obligation is represented without an inhabitant:

```text
EveryBlockedFocusResolvable
```

Conceptually:

```text
for every actual partial map M and blocked void focus v,
there exists test-time reasoning that certifies one color c in V4
that is admissible on M at v.
```

Soundness is a separate obligation:

```text
InferenceSound
```

A complete local bridge requires both resolution and soundness. Resolution without soundness cannot authorize construction; soundness without resolution does not solve blocked focuses.

Only after those obligations are proved can the global monotone construction argument consume voids to completion.

## Richer geometry

The five-ring signature `ABACD` is a projection, not the full map. Two realized maps may share that frontier signature while exposing different second-neighborhood, chain-connectivity, ring-extension, or composed-construct information.

Such richer data belongs to inspection/inference unless and until a theorem derives a `CertifiedInstantiation` from it. Frontier-state recurrence must never be promoted to full-state recurrence without proof.

## Test discipline

New tests and theorem comments should identify their category:

- `REALIZED:` actual partial-map construction facts;
- `INFERENCE:` counterfactual reasoning facts;
- `BRIDGE:` authority-transfer/soundness facts;
- `TERMINAL:` completed-map facts;
- `NEGATIVE:` falsifiers or category-error guards.

If a test crosses categories without an explicit bridge, its design is invalid.

## Working audit

When uncertain, ask:

> **Did this happen to the map, or only in the map-maker's imagination?**

If it happened only in imagination, ask:

> **What exact theorem lets that reasoning collapse into one lawful instantiation?**

That theorem is the current frontier.

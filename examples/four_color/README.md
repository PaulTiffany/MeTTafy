# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, boundary-edge V4 differences, and atomic bichromatic turn preservation.
- `ImaginaryColorDirections.lean` — the step-3 decision surface: relative to any anchor coloration there are exactly three nonidentity V4 directions, i.e. `total colors - 1 = 3`; every distinct imagined coloration has one unique such direction, and arbitrarily long imaginary words normalize to identity or one of those three directions.
- `C2ContactVoid.lean` — in-game contact/void semantics, Brown's embedded coarse interface, canonical `A B A C D` boundary/carrier incidence, and the contact-void reduction.
- `C2ForcedThird.lean` — the forced-third law on the same three-direction surface: fixing one reference state leaves exactly three upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `C2CrossCutAffordance.lean` — operational cross-cut semantics: restricting one upward opportunity forces escape to the unique third upward state once the cross-cut event is present.
- `BrownAffordance.lean` — embedded-player relevance: Brown distinguishes occupancy (`void` versus `colored`) and is present in the game, but its coarse interface cannot reconstruct the color-dependent affordance profile, so it is not color-relevant to local play.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game plus the finite step-3 stop law: two distinct upward states and their forced third exhaust the three-direction action surface; if all three have acted and void blocks replay, the local game is stopped. The five realized boundary slots participate in the same V4 surface; they do not add another decision dimension.
- `TestTimeActiveInference.lean` — test-time/receding-horizon control semantics. Imaginary action is not construction history; only a certified actual-map choice crosses into realized construction.
- `MetaConstructClosure.lean` — open imagination and Decision Reachability as a transferable audit residue. `ProjectionSound` gates an imagined endpoint against the unchanged actual map and `compressDecision` erases the imaginary residue into one `CertifiedInstantiation`.
- `MapMakerPareto.lean` — the complete MapMaker operational product and its preserved order: `Do:Observe -> Imagine:Observe -> Imagine:Act* -> Do:Act`. The four primitive modes are exactly `Do/Imagine × Observe/Act`. Phase 3 is not an additional open completeness theorem: its decision surface is the already-banked three nonidentity V4 directions. Proper boundary-edge differences are nonzero V4 differences and therefore lie on that same surface. Any all-maps safe-successor package is named separately as realization closure rather than decision completeness.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites; terminal inspection remains outside intermediate play.

## Current operational frame

The MapMaker strategy surface is the full product

```text
{Do, Imagine} × {Observe, Act}
```

with the preserved order

```text
1. Do: Observe
2. Imagine: Observe
3. Imagine: Act*
4. Do: Act
```

or, using the implementation names,

```text
overview ; local-expansion ; counter-play* ; draw
```

Phase 3 is the decision-complete surface. For the four-color palette:

```text
total colors - 1 = 3
```

because a fixed reference/anchor removes the identity direction and leaves exactly the three nonzero V4 differences. `ImaginaryColorDirections.lean` proves the exact three-direction cover and uniqueness; `C2ForcedThird.lean` proves that two distinct upward directions force the unique third; `RedTeamComposition.lean` proves that those three exhaust the local upward action surface under the void-blocked stop rule.

The boundary is not outside this count. `FourColorCore.lean` represents each cyclic boundary contact by a V4 difference. On a proper boundary each adjacent pair differs, so each boundary-edge mode is nonzero and therefore belongs to the same three-direction decision surface. Five boundary locations can reuse those three directions; locations are not additional colors or additional decision dimensions.

Imagination may still branch, reverse, stutter, restart, or run arbitrarily far. The finite Decision Reachability chain is only the transferable record of one consequence chain inside phase 3. It does not create a new strategy phase and it does not enlarge the three-direction surface.

The authority order remains:

```text
Do:Observe
-> Imagine:Observe
-> Imagine:Act* over the three-direction surface
-> sound projection
-> Do:Act with no perception during the write
-> re-observe the realized successor
```

## Status discipline

These witnesses remain separated by what they establish rather than by inventing duplicate completeness targets.

- **Primitive strategy completeness is banked:** the four MapMaker modes uniquely cover the `Do/Imagine × Observe/Act` product.
- **Step-3 decision completeness is banked:** the minimal shared V4 decision surface has exactly three nonidentity directions (`4 - 1`), including proper boundary-edge differences.
- **Consequence exhaustion is banked:** pair + forced third exhausts the three upward states, and the existing acted/void-blocked theorem supplies the local stop condition.
- **Decision Reachability is a transfer/audit representation, not another completeness obligation.**
- **Construction authority remains separate:** only a sound actual-map `CertifiedInstantiation` can become `Do:Act`.
- `SafeOrderedRealizationComplete` is the name for any global all-maps safe-realization package; it is deliberately not called decision completeness.

No monotone law over imagination is required, and no stored future route is admitted as construction state.

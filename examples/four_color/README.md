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
- `MapMakerPareto.lean` — the complete MapMaker operational product and its preserved order: `Do:Observe -> Imagine:Observe -> Imagine:Act* -> Do:Act`. The four primitive modes are exactly `Do/Imagine × Observe/Act`. Phase 3 is the decision-complete surface: the already-banked three nonidentity V4 directions.
- `ProofFrontierReduction.lean` — composition-only theorem spine. It introduces no new premise: the ordered MapMaker product fixes phases 1, 2, and 4; all repeatable strategic variation is phase 3; every proper boundary contact lies on the same nonzero V4 surface; arbitrary retained imaginary traversal reduces to identity or one of the three directions; and pair + forced third exhausts the upward surface.
- `Phase3ConstraintCollapse.lean` — constraint-collapse algebra inside phase 3. A fixed reference exposes exactly three nonidentity shifts; realized colored neighbors can only remove candidates from that surface, giving the `3 -> 2 -> 1 -> 0` collapse. Two distinct phase shifts interface by forcing the unique third. Three distinct realized neighbor colors force the fourth; all four block direct instantiation without creating a fourth imaginary direction.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites; terminal inspection remains outside intermediate play.

## Proof-frontier reduction

The novelty carried by the MapMaker formulation is a reduction, not another search procedure.

The strategy surface is the full product

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

or

```text
overview ; local-expansion ; counter-play* ; draw
```

`MapMakerParetoComplete` proves that these four modes uniquely cover the operational product. `ProofFrontierReduction.lean` then makes the downshift explicit: phases 1, 2, and 4 have fixed operational roles, so the only repeatable strategic part of an ordered residue is phase 3.

For the four-color palette, phase 3 has the minimal shared surface

```text
total colors - 1 = 4 - 1 = 3
```

because a fixed reference/anchor removes the identity direction and leaves exactly the three nonzero V4 differences.

The boundary is inside this count, not beside it. Each proper boundary edge is a nonzero V4 difference, so five boundary locations reuse the same three directions. Location count is not decision dimension.

Arbitrary sequential imagination does not enlarge the surface. A retained phase-3 word may be arbitrarily long, but `imaginary_word_has_small_algebraic_normal_form` proves its net V4 result is either identity or one of the three nonzero directions. This is compression of the transferable residue, not a bound on imagination itself.

Finally, for any fixed reference, two distinct upward states determine the unique forced third and the three together exhaust every upward state. Under the existing acted/void-blocked rule, once those three have acted the local phase-3 game is stopped.

The central theorem is:

```text
mapMakerPareto_reduces_proof_frontier_to_step3
```

It is deliberately a composition theorem over existing results. It adds no new completeness premise.

## Phase-3 constraint collapse

`Phase3ConstraintCollapse.lean` records why three is not merely a palette count. It is the maximal nonidentity imagination surface once one current/reference state is fixed.

```text
reference fixed
-> 3 possible phase shifts
-> one additional realized color excludes one shift: 2 remain
-> a second additional realized color excludes another: 1 remains
-> the third additional realized color exhausts the surface: 0 remain
```

Equivalently, realized information can only collapse the phase-3 possibility space:

```text
3 -> 2 -> 1 -> 0
```

The implementation connects this directly to `AdmissibleAt`: an admissible candidate must differ from every realized colored neighbor. Therefore one realized neighbor places the candidate on the existing three-direction surface; two distinct realized neighbor colors leave only a two-state residue; three distinct realized neighbor colors force the unique fourth palette state; and if that fourth state is also realized at the boundary, direct instantiation is impossible.

Two distinct imaginary phase shifts do not open a new direction when they interface. Their V4 composition determines the unique third nonidentity direction. The interface closes the surface:

```text
x, y -> x + y = z
{x, y, z} = V4 \ {0}
```

When direct placement collapses to zero because all four colors are represented around the void, phase 3 may continue as counter-play on surrounding relations. That continuation still uses the same three nonidentity V4 directions; obstruction does not create a fourth phase shift.

## Authority is implementation around the frontier

The authority order remains:

```text
Do:Observe
-> Imagine:Observe
-> Imagine:Act* on the three-direction surface
-> sound projection
-> Do:Act with no perception during the write
-> re-observe the realized successor
```

Decision Reachability is an audit/transfer representation of one finite consequence chain inside phase 3. It is not a second decision-completeness requirement.

`CertifiedInstantiation`, `BlindDraw`, carrier constructions, projection functions, and particular cross-cut realizations are implementation or authority mechanisms around the reduced frontier. A specialized route can still owe a witness of its own geometric or projection interface; that does not create another strategic dimension or undo the MapMaker reduction.

## Status discipline

- **Primitive operational completeness is banked:** the four modes uniquely cover `Do/Imagine × Observe/Act`.
- **Proof-frontier reduction is banked:** in an ordered MapMaker residue, all repeatable strategic variation is phase 3.
- **Step-3 decision completeness is banked:** the shared V4 surface has exactly three nonidentity directions (`4 - 1`).
- **Constraint collapse is explicit:** realized neighbor colors remove possibilities from that fixed surface in the `3 -> 2 -> 1 -> 0` pattern.
- **Three-color forcing is explicit on the realized map:** three distinct realized neighbor colors force the fourth admissible candidate.
- **Four-color blockage is explicit:** if all four palette states occur around a void, no direct admissible instantiation exists; counter-play remains imaginary rather than creating another direction.
- **Boundary inclusion is banked:** every proper boundary-edge difference lies on the same surface.
- **Arbitrary retained imaginary traversal is algebraically compressed:** identity or one of the three directions.
- **Consequence exhaustion is banked:** pair + forced third exhausts all upward states; acted + void-blocked stops the local surface.
- **Authority remains separate:** only a sound actual-map certificate can become `Do:Act`.

No monotone law over imagination is required, and no stored future route is admitted as construction state.

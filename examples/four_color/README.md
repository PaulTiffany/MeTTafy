# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, and atomic bichromatic turn preservation.
- `C2ContactVoid.lean` — in-game contact/void semantics, Brown's embedded coarse interface, canonical `A B A C D` carrier incidence, and the earlier stronger reduction through an explicit physical carrier-interaction premise. That intersection route is retained as a legacy/falsification surface; it is no longer the current C2 authority.
- `C2ForcedThird.lean` — the red-team forced-third law: fixing one lower/reference state leaves three nontrivial upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `C2CrossCutAffordance.lean` — an older realized-turn shadow model of cross-cut restriction/freedom. It remains useful for checking what would follow if such an affordance bundle were realized, but it is not the current C2 deliberation semantics.
- `C2CrossCutOpportunity.lean` — current C2 authority. During inspection the map-maker instantiates an already-realized state in imagination, imagines one terminal-avoiding `a--c` or `c--e` A/D cross-cut, then imagines an opposite B/C response conditioned on that cut. Cut and response are stored as one simultaneous `CanonicalC2ImaginedExchange`; neither is a realized intermediate map. The fully locked incidence is incompatible with any legal imagined exchange, so Lean proves that a clean carrier opportunity already exists. `amortizeC2` discards all imagined steps and retains only that single clean next-move opportunity.
- `BrownAffordance.lean` — embedded-player relevance: Brown distinguishes occupancy (`void` versus `colored`) and is present in the game, but its coarse interface cannot reconstruct the color-dependent affordance profile, so it is not color-relevant to local play.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game: a proper one-site frontier rewrite either re-enters the same hard/A-B-A red-team normal form or removes the old seed color from the frontier and thereby opens a concrete focus-color opportunity. A successor that remains blocked therefore re-enters the same normal form. The same file also banks the finite stop condition: relative to one fixed reference there are exactly three upward states, and once all three have acted, a void rule that makes acted states unavailable leaves no upward action on that local surface; any later action must be a fresh start/restart elsewhere.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum. Compatible coherent primitives compose coherently; regrouping a composition tree preserves its game projection; and the existing B/C/D void-stop theorem lifts into the generic surface semantics.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites. `TerminalResult` accepts only a `CompletedMap`, so partial maps and intermediate turns cannot be fed to the terminal verifier by type. The same map-maker may pause play and inspect the partial map; the distinction is an operational mode boundary, not a permanent identity split.

The game is constructed from inside: realized color states and their contacts determine legal opportunities. The same map-maker may alternate between embedded play and inspection of the partial map. In inspection mode, hypothetical state moves and hypothetical responses can be evaluated together, but they do not become construction history. Only the amortized chosen move is later realized. Brown is an embedded coarse player that may remain present while becoming irrelevant to color-dependent play.

## Current C2 boundary

At the game-theoretic proof layer, C2 clean-turn **opportunity** existence is closed for the declared canonical planar-disk geometry:

```text
no clean carrier
-> all A/D terminals are locked together and B/D are locked together
-> inspect the spanning A/D carrier
-> imagine a terminal-avoiding A/D cross-cut
-> imagine an opposite B/C response to that cut
-> evaluate cut + response as one simultaneous counterfactual exchange
-> the exchange is incompatible with the claimed B/C lock
-> contradiction
-> amortize the whole imagined exchange into one clean next-move opportunity
```

There is no realized intermediate cross-cut state and no realized response state. The imagined response is dependent on the imagined cut for deliberation, but both belong to one simultaneous counterfactual bundle from the perspective of the actual construction turn.

The disk laws used by `CanonicalC2DiskGeometry` are the declared cross-cut mechanics of the theorem's planar-disk domain: a connected A/D span exposes a terminal-avoiding cut probe; that probe admits an opposite response; and a legal cut-response bundle cannot coexist with an untouched B/C lock across the separated terminals. The Lean theorem does **not** claim a from-first-principles formalization of the Jordan curve theorem or Euclidean plane topology. A later substrate theorem may show that another formal representation of planar disks instantiates this contract; that is a ground-representation transport question rather than the old C2-specific physical carrier-intersection premise.

These files still do not, by themselves, claim a new proof of the Four Color Theorem. C2 establishes a current clean-turn opportunity; `FourColorCore.lean` separately proves what a supplied clean atomic turn does. The remaining program must connect the declared planar-map substrate to this disk contract and compose the local construction through map completion without importing hidden route or observer authority. The construct grammar does not claim that the current primitive families generate every planar map or provide an automatic decomposition algorithm.

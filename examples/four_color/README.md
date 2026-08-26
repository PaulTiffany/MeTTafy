# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, and atomic bichromatic turn preservation.
- `C2ContactVoid.lean` — in-game contact/void semantics, Brown's embedded coarse interface, canonical `A B A C D` carrier incidence, and the earlier stronger reduction through an explicit physical carrier-interaction premise. That intersection route is retained as a legacy/falsification surface; it is no longer the current C2 authority.
- `C2ForcedThird.lean` — the red-team forced-third law: fixing one lower/reference state leaves three nontrivial upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `C2CrossCutAffordance.lean` — realized cross-cut-turn semantics. A taken cross-cut consumes a previously available cut-state opportunity and offers an escape-state opportunity on the successor surface. In the V4 specialization the escape is the unique forced third state; canonically, with `A=0`, a C-carried cut of B restricts B and offers D.
- `C2CrossCutOpportunity.lean` — current C2 authority. It separates an inspection-mode imagined cross-cut from a realized turn. `CanonicalC2DiskGeometry` declares the two ground disk facts used by the paper-map argument: one connected A/D carrier spanning `a,c,e` exposes a terminal-avoiding `a--c` or `c--e` cross-cut opportunity, and either such cross-cut restricts the opposite B/C continuation across the separated `b,d` terminals. Lean then proves that the fully locked incidence is impossible and therefore at least one canonical clean carrier/turn opportunity exists. No physical A/D–B/C vertex intersection is assumed.
- `BrownAffordance.lean` — embedded-player relevance: Brown distinguishes occupancy (`void` versus `colored`) and is present in the game, but its coarse interface cannot reconstruct the color-dependent affordance profile, so it is not color-relevant to local play.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game: a proper one-site frontier rewrite either re-enters the same hard/A-B-A red-team normal form or removes the old seed color from the frontier and thereby opens a concrete focus-color opportunity. A successor that remains blocked therefore re-enters the same normal form. The same file also banks the finite stop condition: relative to one fixed reference there are exactly three upward states, and once all three have acted, a void rule that makes acted states unavailable leaves no upward action on that local surface; any later action must be a fresh start/restart elsewhere.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum. Compatible coherent primitives compose coherently; regrouping a composition tree preserves its game projection; and the existing B/C/D void-stop theorem lifts into the generic surface semantics.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites. `TerminalResult` accepts only a `CompletedMap`, so partial maps and intermediate turns cannot be fed to the terminal verifier by type. The same map-maker may of course pause play and inspect the partial map; the distinction is an operational mode boundary, not a permanent identity split.

The game is constructed from inside: realized color states and their contacts determine legal opportunities. The map-maker may alternate between embedded play and inspection of the partial map, but facts do not silently inherit powers across that mode switch. Brown is an embedded coarse player that may remain present while becoming irrelevant to color-dependent play.

## Current C2 boundary

At the game-theoretic proof layer, C2 clean-turn **opportunity** existence is now closed for the declared canonical planar-disk geometry:

```text
no clean carrier
-> all A/D terminals are locked together and B/D are locked together
-> the spanning A/D geometry exposes an imagined terminal-avoiding cross-cut
-> by cross-cut mechanics, that cut restricts the opposite B/C continuation
-> contradiction
-> some clean carrier opportunity exists
```

The cross-cut response is part of the declared disk geometry of the theorem's domain, just as cyclic boundary order is part of that domain; it is not a hidden observer or a future route. The Lean theorem does **not** claim a from-first-principles formalization of the Jordan curve theorem or Euclidean plane topology. A later substrate theorem may show that another formal representation of planar disks instantiates `CanonicalC2DiskGeometry`; that transport is a ground-representation question, not an open C2-specific carrier-intersection premise.

These files still do not, by themselves, claim a new proof of the Four Color Theorem. C2 establishes a current clean-turn opportunity; `FourColorCore.lean` separately proves what a supplied clean atomic turn does. The remaining program must connect the declared planar-map substrate to this disk contract and compose the local construction through map completion without importing hidden route or observer authority. The construct grammar does not claim that the current primitive families generate every planar map or provide an automatic decomposition algorithm.

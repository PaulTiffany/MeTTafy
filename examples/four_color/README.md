# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, and atomic bichromatic turn preservation.
- `C2ContactVoid.lean` — in-game contact/void semantics, Brown's embedded coarse interface, canonical `A B A C D` carrier incidence, and the reduction of clean-carrier existence to one explicit planar carrier-interaction premise.
- `C2ForcedThird.lean` — the red-team forced-third law: fixing one lower/reference state leaves three nontrivial upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `C2CrossCutAffordance.lean` — a bounded realized cross-cut affordance model. It records what follows from a supplied cut/escape bundle; it does not establish that actual planar geometry supplies a useful one-step escape.
- `BrownAffordance.lean` — embedded-player relevance: Brown distinguishes occupancy (`void` versus `colored`) and is present in the game, but its coarse interface cannot reconstruct the color-dependent affordance profile, so it is not color-relevant to local play.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game: a proper one-site frontier rewrite either re-enters the same hard/A-B-A red-team normal form or removes the old seed color from the frontier and thereby opens a concrete focus-color opportunity. A successor that remains blocked therefore re-enters the same normal form. The separate finite-stop theorem remains conditional on the declared acted/void-blocked action surface; it is not a proof that actual Kempe play necessarily exhausts those actions.
- `TestTimeActiveInference.lean` — test-time/receding-horizon control semantics. A current action is selected from the current realized state, exactly one successor is realized, and that actual successor is re-observed. The canonical `A B A C D -> A B D C D` witness proves that a proper repeated-color action can remain hard and blocked, so one-step reducibility is explicitly rejected. The remaining target is precommit strategy safety: every strategy-safe nonterminal realized map must admit one certified instantiation that remains strategy-safe.
- `MetaConstructClosure.lean` — two-family closure and imagination-compression boundary. The current research ontology names red-team and alternating-pair, while `ImaginationBox` leaves the internal witness type arbitrary: authority is bounded by the unchanged realized map/focus rather than by a path/depth budget. `ProjectionSound` gates every projected color against the actual map, `ProjectionReachable` names the open existence claim, and successful compression erases the imaginary witness into one `CertifiedInstantiation`. The separate planar bridge `PlanarTwoFamilyExhaustive` is also intentionally left open.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum. Compatible coherent primitives compose coherently; regrouping a composition tree preserves its game projection; and the existing conditional B/C/D void-stop theorem lifts into the generic surface semantics.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites. `TerminalResult` accepts only a `CompletedMap`, so partial maps and intermediate turns cannot be fed to the terminal verifier by type. The same map-maker may pause play to inspect the partial map; this is a mode boundary, not a permanent identity split.

## Current operational frame

The map-maker alternates between embedded play and inspection. In inspection mode, hypothetical moves and responses may be evaluated, but they are not realized construction history. The selected current move is realized once; then all permissions are recomputed from the actual successor.

```text
observe current realized map
-> open imagination inside the current authority box
-> branch / reverse / stutter / transform representation / restart as useful
-> project or abstain
-> validate any projected color on the unchanged actual map
-> realize exactly one certified action
-> re-observe the actual successor
```

A hard successor is therefore a legitimate observation, not evidence that the realized action was invalid. The proof does **not** require every hard state to open in one move, nor does it require imaginary dynamics to descend monotonically.

The existing Python `ImmediateControlCertificate` / `ColorationControlSurface` already follows this receding-horizon discipline on graph-native Kempe controls: immediate access is derived from the current construction, one control is realized, and any later control is recomputed from the resulting state. Bounded path search remains an audit/falsification surface rather than a proof-relevant future route.

## Current proof debt

These files do not claim a new proof of the Four Color Theorem. In particular:

- clean carrier existence is weaker than one-step color freeing;
- the canonical hard-to-hard witness mechanically blocks any silent promotion of a proper/clean current move into one-step reducibility;
- test-time actionability alone is not global closure;
- the current two-meta-construct candidate still owes the actual planar theorem that every relevant continuation classifies as red-team or alternating-pair;
- it also owes `ProjectionReachable` plus `ProjectionSound` for every strategy-safe nonterminal realized state;
- declaring an arbitrary imagination witness type does not prove that a useful witness exists;
- no monotone progress scalar is assumed necessary;
- no stored future route is admitted as proof state;
- the construct grammar still does not prove that current primitives generate every planar map or that arbitrary map completion follows.

PR #68's stronger imagined-escape contract is not part of this authority surface: an imagined response may guide test-time choice, but it may not carry the missing success theorem as an assumption.

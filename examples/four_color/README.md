# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, and atomic bichromatic turn preservation.
- `C2ContactVoid.lean` — in-game contact/void semantics, Brown's embedded coarse interface, canonical `A B A C D` carrier incidence, and the reduction of clean-carrier existence to one explicit planar carrier-interaction premise.
- `C2ForcedThird.lean` — the red-team forced-third law: fixing one lower/reference state leaves three nontrivial upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `C2CrossCutAffordance.lean` — a bounded realized cross-cut affordance model. It records what follows from a supplied cut/escape bundle; it does not establish that actual planar geometry supplies a useful one-step escape.
- `BrownAffordance.lean` — embedded-player relevance: Brown distinguishes occupancy (`void` versus `colored`) and is present in the game, but its coarse interface cannot reconstruct the color-dependent affordance profile, so it is not color-relevant to local play.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game: a proper one-site frontier rewrite either re-enters the same hard/A-B-A red-team normal form or removes the old seed color from the frontier and thereby opens a concrete focus-color opportunity. A successor that remains blocked therefore re-enters the same normal form. The separate finite-stop theorem remains conditional on the declared acted/void-blocked action surface; it is not a proof that actual Kempe play necessarily exhausts those actions.
- `TestTimeActiveInference.lean` — test-time/receding-horizon control semantics. A current action is selected from the current realized state, exactly one successor is realized, and that actual successor is re-observed. The canonical `A B A C D -> A B D C D` witness proves that a proper repeated-color action can remain hard and blocked, so one-step reducibility is explicitly rejected. The remaining target is precommit strategy safety: every strategy-safe nonterminal realized map must admit one certified instantiation that remains strategy-safe.
- `MetaConstructClosure.lean` — two-family closure, open imagination, and Decision Reachability. Arbitrary test-time reasoning leaves a finite admissible `if-this -> then-this` residue; `ProjectionSound` gates the deciding endpoint against the unchanged actual map; `compressDecision` erases the imaginary residue into one `CertifiedInstantiation`; and `decisionReachabilityComplete_implies_safe_instantiation` connects that transferable proof object to the existing precommit construction target. `PlanarTwoFamilyExhaustive` remains an explicit planar classification obligation.
- `MapMakerPareto.lean` — SRMF-specialized MapMaker strategy algebra. The primitive Pareto frontier is: global overview; local neighbor/expansion imagination; interactive reaction/counter-play imagination; and blind draw. The first three generate Decision Reachability refinements and cannot write reality. Draw is the only write-capable primitive and has no perception/imagination capability. The four modes are pairwise non-dominating on their declared irreducible capability axes and jointly capability-complete. The stronger behavioral theorem that every admissible MapMaker strategy reduces to a composition of the four modes is named `MapMakerParetoComplete` and remains explicit rather than being inferred from the enum.
- `ConstructGrammar.lean` — open game-theoretic composition grammar. Primitive construct and fact types are caller-supplied, so stripes, red-team patches, alternating structures, and future local constructs can enter as atoms without extending a closed picture enum. Compatible coherent primitives compose coherently; regrouping a composition tree preserves its game projection; and the existing conditional B/C/D void-stop theorem lifts into the generic surface semantics.
- `ConstructionTerminalFrame.lean` — separates construction from result inspection. A map-maker step can only instantiate one previously void site with a V4 state while preserving the other realized sites. `TerminalResult` accepts only a `CompletedMap`, so partial maps and intermediate turns cannot be fed to the terminal verifier by type. The same map-maker may pause play to inspect the partial map; this is a mode boundary, not a permanent identity split.

## Current operational frame

The MapMaker control alphabet is now explicitly separated into three precommit reasoning modes and one authority-crossing mode:

```text
overview
  | local expansion
  | counter-play
  ... repeat / branch / restart in imagination as useful ...
  -> finite Decision Reachability residue
  -> sound projection
  -> draw, with no perception during the write
  -> re-observe the realized successor
```

Equivalently, the transferable control word has the normal form:

```text
(overview | local-expansion | counter-play)* ; draw
```

The star is not a search bound. Imagination may range freely inside the authority box. The finite word is the auditable residue retained after a deciding chain is found.

A hard successor is therefore a legitimate observation, not evidence that the realized action was invalid. The proof does **not** require every hard state to open in one move, nor does it require imaginary dynamics to descend monotonically.

The existing Python `ImmediateControlCertificate` / `ColorationControlSurface` already follows this receding-horizon discipline on graph-native Kempe controls: immediate access is derived from the current construction, one control is realized, and any later control is recomputed from the resulting state. Bounded path search remains an audit/falsification surface rather than a proof-relevant future route.

## Current proof debt

These files do not claim a new proof of the Four Color Theorem. In particular:

- clean carrier existence is weaker than one-step color freeing;
- the canonical hard-to-hard witness mechanically blocks any silent promotion of a proper/clean current move into one-step reducibility;
- test-time actionability alone is not global closure;
- `DecisionReachabilityComplete` remains the strategy-level theorem target: every strategy-safe nonterminal realized state must have a finite admissible deciding residue whose sound projection yields a safe successor;
- the current two-meta-construct candidate still owes the actual planar theorem that every relevant continuation classifies as red-team or alternating-pair;
- `MapMakerParetoComplete` remains the behavioral reduction target: every admissible MapMaker strategy must be shown reducible, without loss of relevant capability/decision behavior, to compositions of overview, local expansion, counter-play, and blind draw;
- capability coverage of the four declared axes is not by itself behavioral completeness;
- no monotone progress scalar is assumed necessary;
- no stored future route is admitted as proof state;
- the construct grammar still does not prove that current primitives generate every planar map or that arbitrary map completion follows.

PR #68's stronger imagined-escape contract is not part of this authority surface: an imagined response may guide test-time choice, but it may not carry the missing success theorem as an assumption.

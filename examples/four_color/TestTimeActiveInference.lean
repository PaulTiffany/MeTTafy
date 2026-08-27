import examples.four_color.ConstructionTerminalFrame
import examples.four_color.RedTeamComposition

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Test-time active inference for the independent Four Color research lane.

AUTHORITATIVE FRAME CONTRACT
----------------------------
Test time is not game time. Sequential imagination is not sequential construction.

A realized partial map may be inspected through arbitrarily many counterfactual
frontier states, hypothetical future commitments, and response classes. Those
objects may branch, cycle, restart, or remain blocked. None of them is
construction history.

The only authority boundary is:

  RealizedMap
      -> inspect / imagine / roleplay
  InferenceEpisode
      -> derive under an explicit soundness theorem
  CertifiedInstantiation
      -> instantiate one void
  RealizedMap

This file therefore treats the canonical

  A B A C D -> A B D C D

hard-to-hard transition only as an INFERENCE/NEGATIVE witness. It proves that a
candidate one-step recoloring can remain hard. It does not assert that the
realized construction ever performs that recoloring.

A further correction is now explicit: an already saturated realized focus is too
late for inference-only recoloring to repair, because the authority boundary does
not rewrite realized colors. The open induction target is therefore precommit
strategy safety: every strategy-safe nonterminal realized map must admit one
certified instantiation that remains strategy-safe.
-/

namespace MeTTafy.FourColor

universe u

/-! ## Inference-only state and move types -/

/-- A counterfactual five-frontier state considered during inspection. -/
structure ImaginedState where
  frontier : Boundary5

/--
One counterfactual frontier transformation. Its `after` state remains in
`ImaginedState`; there is deliberately no authority edge to `RealizedMap`.
-/
structure CounterfactualMove (before : ImaginedState) where
  turn : OneSiteBoundaryTurn before.frontier
  properAfter : ProperPentagon turn.after

namespace CounterfactualMove

/-- The result of a counterfactual move is another imagined state. -/
def after {before : ImaginedState}
    (move : CounterfactualMove before) : ImaginedState :=
  ⟨move.turn.after⟩

end CounterfactualMove

/--
One test-time reasoning episode over one actual map and one actual focus.
The list may contain any sequence of counterfactual states; it is not a stored
future construction route.
-/
structure InferenceEpisode {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  imaginedStates : List ImaginedState

/--
An inference method may declare that an episode certifies a color. This relation
has no construction authority by itself; `InferenceSound` is the required bridge.
-/
structure InferenceMethod (Vertex : Type u) where
  certifies :
    {map : RealizedMap Vertex} →
    {focus : Focus Vertex} →
    InferenceEpisode map focus →
    V4 → Prop

/--
Soundness is the exact collapse theorem: if test-time reasoning claims a color,
that color must be admissible on the actual realized map at the actual focus.
-/
def InferenceSound {Vertex : Type u}
    (method : InferenceMethod Vertex) : Prop :=
  ∀ {map : RealizedMap Vertex} {focus : Focus Vertex}
      (episode : InferenceEpisode map focus) (color : V4),
    method.certifies episode color →
    AdmissibleAt map focus color

/--
Explicit authority bridge from an inference claim to a construction certificate.
The imagined states are discarded; only the derived color and actual-map
admissibility proof cross the boundary.
-/
def amortize
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (method : InferenceMethod Vertex)
    (sound : InferenceSound method)
    (episode : InferenceEpisode map focus)
    (color : V4)
    (certified : method.certifies episode color) :
    CertifiedInstantiation map focus :=
  ⟨color, sound episode color certified⟩

/--
After amortization, realized execution is exactly one `void -> V4` instantiation.
No counterfactual intermediate state is executed.
-/
def realizeInference
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (method : InferenceMethod Vertex)
    (sound : InferenceSound method)
    (episode : InferenceEpisode map focus)
    (color : V4)
    (certified : method.certifies episode color) :
    RealizedMap Vertex :=
  instantiate (amortize method sound episode color certified)

/-- REALIZED: the collapse boundary advances construction by exactly one void. -/
theorem realizeInference_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (method : InferenceMethod Vertex)
    (sound : InferenceSound method)
    (episode : InferenceEpisode map focus)
    (color : V4)
    (certified : method.certifies episode color) :
    voidCount roster (realizeInference method sound episode color certified) =
      voidCount roster map - 1 := by
  exact voidCount_instantiate roster
    (amortize method sound episode color certified)

/-! ## Canonical INFERENCE / NEGATIVE witness -/

/-- Canonical hard frontier A B A C D in the gauge A=0, B=a, C=b, D=c. -/
def canonicalABACD : Boundary5 :=
  ⟨V4.zero, V4.a, V4.zero, V4.b, V4.c⟩

/-- The canonical frontier as an inspection-only state. -/
def canonicalImaginedABACD : ImaginedState :=
  ⟨canonicalABACD⟩

/--
INFERENCE: imagine recoloring the second A occurrence to D.
This is not a realized construction step.
-/
def imaginedRepeatedAtoD : CounterfactualMove canonicalImaginedABACD where
  turn := {
    slot := .s2
    replacement := V4.c
    changed := by simp [canonicalImaginedABACD, canonicalABACD, boundaryAt]
  }
  properAfter := by
    simp [canonicalImaginedABACD, canonicalABACD,
      OneSiteBoundaryTurn.after, replaceBoundary, ProperPentagon]

@[simp] theorem imaginedRepeatedAtoD_after :
    imaginedRepeatedAtoD.after.frontier =
      (⟨V4.zero, V4.a, V4.c, V4.b, V4.c⟩ : Boundary5) := rfl

/-- INFERENCE: the canonical source is a hard 2:1:1:1 frontier. -/
theorem canonicalABACD_hard : HardDegreeFiveFrontier canonicalABACD := by
  simp [canonicalABACD, HardDegreeFiveFrontier, ProperPentagon,
    UsesAllFourColors, BoundaryContains]

/--
NEGATIVE: the imagined repeated-A recoloring remains hard. Therefore one
counterfactual intervention need not immediately free a focus color.
-/
theorem imaginedRepeatedAtoD_stays_hard :
    HardDegreeFiveFrontier imaginedRepeatedAtoD.after.frontier := by
  simp [imaginedRepeatedAtoD_after, HardDegreeFiveFrontier, ProperPentagon,
    UsesAllFourColors, BoundaryContains]

/-- NEGATIVE: that imagined branch still exposes no focus color. -/
theorem imaginedRepeatedAtoD_does_not_open :
    ¬ HasFocusOpportunity imaginedRepeatedAtoD.after.frontier :=
  hard_frontier_has_no_focus_opportunity
    imaginedRepeatedAtoD.after.frontier imaginedRepeatedAtoD_stays_hard

/--
INFERENCE: the red-team one-site dichotomy is valid inside imagination space.
The theorem says nothing about construction history.
-/
theorem imagined_redTeam_step_reenters_or_opens
    (before : ImaginedState)
    (normal : RedTeamNormalForm before.frontier)
    (move : CounterfactualMove before) :
    HasFocusOpportunity move.after.frontier ∨
      RedTeamNormalForm move.after.frontier := by
  rcases redTeam_turn_composes_or_opens
      before.frontier normal move.turn move.properAfter with hardAgain | openNow
  · exact Or.inr hardAgain
  · exact Or.inl openNow

/-! ## Explicit remaining precommit strategy obligation -/

/-- REALIZED: a partial map is nonterminal exactly when at least one site is void. -/
def HasVoid {Vertex : Type u} (map : RealizedMap Vertex) : Prop :=
  ∃ vertex, map.state vertex = .void

/-- Caller-supplied meaning of the strategy-safe realized construction class. -/
abbrev StrategySafePredicate (Vertex : Type u) :=
  RealizedMap Vertex → Prop

/--
The construction-level open target. It does not claim that an arbitrary already
blocked focus can be repaired. Instead, every strategy-safe nonterminal realized
map must have one certified actual instantiation whose successor is still safe.

No inhabitant is supplied here.
-/
def EveryStrategySafeStateHasSafeInstantiation
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex) : Prop :=
  ∀ (map : RealizedMap Vertex),
    safe map →
    HasVoid map →
    ∃ (focus : Focus Vertex) (cert : CertifiedInstantiation map focus),
      safe (instantiate cert)

/--
The strategy-level completeness target for one particular inference method.
A bounded roleplay procedure may inspect many same-turn states and nested
hypothetical commitments, but it must eventually certify a depth-zero move whose
realized successor remains inside `safe`.

The soundness proof is explicit because the imagined strategy claim itself has no
construction authority.
-/
def StrategyIRComplete
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex)
    (method : InferenceMethod Vertex)
    (sound : InferenceSound method) : Prop :=
  ∀ (map : RealizedMap Vertex),
    safe map →
    HasVoid map →
    ∃ (focus : Focus Vertex)
      (episode : InferenceEpisode map focus)
      (color : V4)
      (certified : method.certifies episode color),
      safe (realizeInference method sound episode color certified)

/--
BRIDGE: a complete and sound Strategy IR yields the construction-level safe
instantiation obligation. The counterfactual transcript itself is discarded.
-/
theorem strategyIRComplete_implies_safe_instantiation
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex)
    (method : InferenceMethod Vertex)
    (sound : InferenceSound method)
    (complete : StrategyIRComplete safe method sound) :
    EveryStrategySafeStateHasSafeInstantiation safe := by
  intro map safeMap hasVoid
  rcases complete map safeMap hasVoid with
    ⟨focus, episode, color, certified, safeAfter⟩
  refine ⟨focus, amortize method sound episode color certified, ?_⟩
  simpa [realizeInference] using safeAfter

end MeTTafy.FourColor

import examples.four_color.RedTeamComposition

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Test-time / active-inference semantics for the independent Four Color game.

FRAME CONTRACT
--------------
A blocked construction is not required to admit a one-step color-freeing move.
The map-maker acts receding-horizon:

  observe current realized state
  -> derive current legal actions
  -> imagine consequences/responses
  -> choose one current action
  -> realize exactly that action
  -> discard the old counterfactual bundle
  -> re-observe the actual successor

Imagined futures never become construction history.  A hard successor is not a
failed turn; it is a new test-time observation from which the current action
surface must be derived again.

This file deliberately proves the canonical negative witness

  A B A C D -> A B D C D

for a proper one-site repeated-A rewrite: both source and successor are hard.
Thus one-step reducibility is not the theorem being pursued.

The remaining global obligation is stated, not assumed: a successful test-time
proof must rule out a reachable closed class of nonterminal states under the
actual graph-derived action relation.  No monotone progress scalar or stored
future route is introduced here.
-/

namespace MeTTafy.FourColor

universe u v

/--
Generic current-state controller. `available` is recomputed from the current
realized state; `realize` applies one selected current action.
-/
structure TestTimeController (State : Type u) (Action : Type v) where
  available : State → Action → Prop
  realize : State → Action → State

/-- One actually realized test-time step. It carries only current permission. -/
structure TestTimeStep
    {State : Type u} {Action : Type v}
    (controller : TestTimeController State Action) where
  before : State
  action : Action
  permitted : controller.available before action

namespace TestTimeStep

/-- The unique realized successor of one selected current action. -/
def after
    {State : Type u} {Action : Type v}
    {controller : TestTimeController State Action}
    (step : TestTimeStep controller) : State :=
  controller.realize step.before step.action

end TestTimeStep

/-- Current actionability is an extensional property of the current state only. -/
def TestTimeActionable
    {State : Type u} {Action : Type v}
    (controller : TestTimeController State Action)
    (state : State) : Prop :=
  ∃ action, controller.available state action

/--
A nonterminal closed action class is the actual failure object for an adaptive
receding-horizon proof: once entered, every available action stays inside it and
no member is terminal.
-/
def ClosedNonterminalClass
    {State : Type u} {Action : Type v}
    (controller : TestTimeController State Action)
    (terminal : State → Prop)
    (inside : State → Prop) : Prop :=
  (∃ state, inside state) ∧
  (∀ state, inside state → ¬ terminal state) ∧
  (∀ state action,
    inside state →
    controller.available state action →
    inside (controller.realize state action))

/--
A test-time viability target: every nonterminal current state exposes at least
one current action. This is intentionally weaker than one-step success.
-/
def TestTimeViable
    {State : Type u} {Action : Type v}
    (controller : TestTimeController State Action)
    (terminal : State → Prop) : Prop :=
  ∀ state, ¬ terminal state → TestTimeActionable controller state

/-! ## Frontier-level specialization: observe -> act -> re-observe -/

/-- A realized proper one-site frontier action, with no future route attached. -/
structure FrontierTestTimeAction (before : Boundary5) where
  turn : OneSiteBoundaryTurn before
  properAfter : ProperPentagon turn.after

/-- The realized successor is inspected only after the selected turn occurs. -/
def FrontierTestTimeAction.after
    {before : Boundary5}
    (action : FrontierTestTimeAction before) : Boundary5 :=
  action.turn.after

/--
Test-time red-team law: after one realized proper current action, inspect the
actual successor. It is either open now or is another hard/red-team state to be
re-observed. No later action is selected or stored by this theorem.
-/
theorem redTeam_realize_then_reobserve
    (before : Boundary5)
    (normal : RedTeamNormalForm before)
    (action : FrontierTestTimeAction before) :
    HasFocusOpportunity action.after ∨ RedTeamNormalForm action.after := by
  rcases redTeam_turn_composes_or_opens
      before normal action.turn action.properAfter with hardAgain | openNow
  · exact Or.inr hardAgain
  · exact Or.inl openNow

/-- A hard successor is explicitly a valid re-observation outcome, not failure. -/
def RequiresReobservation (boundary : Boundary5) : Prop :=
  RedTeamNormalForm boundary ∧ ¬ HasFocusOpportunity boundary

/-- Any hard frontier is blocked and therefore genuinely requires re-observation. -/
theorem hard_frontier_requires_reobservation
    (boundary : Boundary5)
    (hard : HardDegreeFiveFrontier boundary) :
    RequiresReobservation boundary :=
  ⟨hard_frontier_is_redTeam boundary hard,
    hard_frontier_has_no_focus_opportunity boundary hard⟩

/-! ## Canonical negative witness: one proper action need not open in one step -/

/-- Canonical hard frontier A B A C D in the gauge A=0, B=a, C=b, D=c. -/
def canonicalABACD : Boundary5 :=
  ⟨V4.zero, V4.a, V4.zero, V4.b, V4.c⟩

/-- Recolor the second A occurrence to D: A B A C D -> A B D C D. -/
def repeatedAtoD : OneSiteBoundaryTurn canonicalABACD where
  slot := .s2
  replacement := V4.c
  changed := by simp [canonicalABACD, boundaryAt]

@[simp] theorem repeatedAtoD_after :
    repeatedAtoD.after =
      (⟨V4.zero, V4.a, V4.c, V4.b, V4.c⟩ : Boundary5) := rfl

/-- The canonical source really is a hard 2:1:1:1 frontier. -/
theorem canonicalABACD_hard : HardDegreeFiveFrontier canonicalABACD := by
  simp [canonicalABACD, HardDegreeFiveFrontier, ProperPentagon,
    UsesAllFourColors, BoundaryContains]

/-- The repeated-A rewrite is proper as a one-site frontier action. -/
theorem repeatedAtoD_proper : ProperPentagon repeatedAtoD.after := by
  simp [repeatedAtoD_after, ProperPentagon]

/-- The actual successor is still hard: one-step opening is false. -/
theorem repeatedAtoD_successor_hard : HardDegreeFiveFrontier repeatedAtoD.after := by
  simp [repeatedAtoD_after, HardDegreeFiveFrontier, ProperPentagon,
    UsesAllFourColors, BoundaryContains]

/-- Consequently the repeated-A action does not expose a focus color. -/
theorem repeatedAtoD_does_not_open :
    ¬ HasFocusOpportunity repeatedAtoD.after :=
  hard_frontier_has_no_focus_opportunity
    repeatedAtoD.after repeatedAtoD_successor_hard

/--
The negative witness composes exactly as test-time control predicts: the move is
lawful at the frontier level, the successor stays hard, and the correct next
operation is re-observation rather than declaring the action or proof failed.
-/
theorem repeatedAtoD_requires_reobservation :
    RequiresReobservation repeatedAtoD.after :=
  hard_frontier_requires_reobservation
    repeatedAtoD.after repeatedAtoD_successor_hard

/-! ## Explicit remaining proof obligation -/

/--
No-trap is the stronger closure target required beyond current actionability.
It is intentionally a predicate, not a theorem here: the actual graph-derived
Four Color controller still has to prove it.
-/
def NoClosedNonterminalClass
    {State : Type u} {Action : Type v}
    (controller : TestTimeController State Action)
    (terminal : State → Prop) : Prop :=
  ∀ inside : State → Prop,
    ¬ ClosedNonterminalClass controller terminal inside

end MeTTafy.FourColor

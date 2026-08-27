import examples.four_color.StrategyColorProjection

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Forcing and strategy-phase reduction for bounded Four Color MapMaker play.

The central distinction is deliberate:

* `colorPhase` is the retained V4 invariant from StrategyColorProjection;
* `responseRank` is the number of live proof-relevant response classes.

A supported forcing step may preserve color phase while strictly reducing response
rank.  Thus a move can be strategically decisive without being a color phase
transition.  Rank one is a forcing line; rank zero is checkmate.

Everything in this file is INFERENCE-only.  No forcing witness is construction
authority and no theorem here produces `CertifiedInstantiation`.
-/

namespace MeTTafy.FourColor

/--
The live-response quotient already factors out concrete replies that are strategically
equivalent.  `nodup` means its cardinality is the number of live response classes,
not the number of serialized opponent actions.
-/
structure StrategyResponseQuotient where
  classes : List Nat
  nodup : classes.Nodup

/-- Number of strategically live response classes. -/
def responseRank (responses : StrategyResponseQuotient) : Nat :=
  responses.classes.length

/-- Checkmate: no strategically live response class remains. -/
def StrategyCheckmate (responses : StrategyResponseQuotient) : Prop :=
  responses.classes = []

/-- Forcing line: exactly one strategically live response class remains. -/
def StrategyForced (responses : StrategyResponseQuotient) : Prop :=
  ∃ response, responses.classes = [response]

/-- Pair one boundary-labelled Strategy tangle with its current response quotient. -/
structure StrategyGameState where
  tangle : StrategyTangle
  responses : StrategyResponseQuotient

/-- A forcing step strictly reduces the proof-relevant response quotient. -/
def StrategyForcingStep (before after : StrategyGameState) : Prop :=
  responseRank after.responses < responseRank before.responses

/--
A mechanically supported forcing step must also be a supported Strategy/color
simulation.  The color projection may stutter or uncross; forcing is measured in
response space, not inferred from color motion.
-/
structure SupportedStrategyForcingStep (before after : StrategyGameState) : Prop where
  simulation : StrategyColorSimulation before.tangle after.tangle
  forces : StrategyForcingStep before after

/-- Checkmate is exactly response rank zero. -/
theorem strategyCheckmate_iff_responseRank_zero
    (responses : StrategyResponseQuotient) :
    StrategyCheckmate responses ↔ responseRank responses = 0 := by
  simp [StrategyCheckmate, responseRank]

/-- A forced line has exactly one live response class. -/
theorem strategyForced_responseRank_one
    {responses : StrategyResponseQuotient}
    (forced : StrategyForced responses) :
    responseRank responses = 1 := by
  rcases forced with ⟨response, rfl⟩
  rfl

/-- Every forcing step removes at least one live response class. -/
theorem StrategyForcingStep.succ_after_le_before
    {before after : StrategyGameState}
    (step : StrategyForcingStep before after) :
    responseRank after.responses + 1 ≤ responseRank before.responses := by
  exact Nat.succ_le_of_lt step

/-- Strict response-rank descent cannot immediately run backward. -/
theorem StrategyForcingStep.not_reverse
    {before after : StrategyGameState}
    (step : StrategyForcingStep before after) :
    ¬ StrategyForcingStep after before := by
  intro reverse
  exact (Nat.not_lt_of_ge (Nat.le_of_lt step)) reverse

/-- Checkmate admits no further forcing step because rank cannot fall below zero. -/
theorem strategyCheckmate_no_forcing
    {before after : StrategyGameState}
    (mate : StrategyCheckmate before.responses) :
    ¬ StrategyForcingStep before after := by
  intro step
  have zero : responseRank before.responses = 0 :=
    (strategyCheckmate_iff_responseRank_zero before.responses).1 mate
  rw [zero] at step
  exact Nat.not_lt_zero _ step

/--
If a position is already a forcing line (rank one), any further forcing step reaches
checkmate (rank zero).  This is the finite-response analogue of the final move in a
forcing game line.
-/
theorem forcing_from_forced_reaches_checkmate
    {before after : StrategyGameState}
    (forced : StrategyForced before.responses)
    (step : StrategyForcingStep before after) :
    StrategyCheckmate after.responses := by
  have one : responseRank before.responses = 1 :=
    strategyForced_responseRank_one forced
  have belowOne : responseRank after.responses < 1 := by
    simpa [one] using step
  have zero : responseRank after.responses = 0 := by
    omega
  exact (strategyCheckmate_iff_responseRank_zero after.responses).2 zero

/--
A supported forcing step can change strategy phase while preserving the retained
V4 color phase.  This is the formal separation between strategic forcing and a
color phase transition.
-/
theorem SupportedStrategyForcingStep.preservesColorPhase
    {before after : StrategyGameState}
    (step : SupportedStrategyForcingStep before after) :
    colorPhase (projectStrategyTangle before.tangle) =
      colorPhase (projectStrategyTangle after.tangle) :=
  step.simulation.preservesColorPhase

/--
One supported move can therefore simultaneously preserve color phase and strictly
reduce strategy phase rank.
-/
theorem SupportedStrategyForcingStep.color_stable_strategy_descent
    {before after : StrategyGameState}
    (step : SupportedStrategyForcingStep before after) :
    colorPhase (projectStrategyTangle before.tangle) =
        colorPhase (projectStrategyTangle after.tangle) ∧
      responseRank after.responses < responseRank before.responses :=
  ⟨step.preservesColorPhase, step.forces⟩

/--
If a supported forcing step starts from a forcing line, its destination is checkmate
while the retained color phase is unchanged.
-/
theorem supported_forced_step_reaches_color_stable_checkmate
    {before after : StrategyGameState}
    (forced : StrategyForced before.responses)
    (step : SupportedStrategyForcingStep before after) :
    StrategyCheckmate after.responses ∧
      colorPhase (projectStrategyTangle before.tangle) =
        colorPhase (projectStrategyTangle after.tangle) := by
  exact ⟨forcing_from_forced_reaches_checkmate forced step.forces,
    step.preservesColorPhase⟩

/-!
Interpretation:

  many concrete replies
      -> quotient by strategic equivalence
      -> live response classes
      -> forcing step strictly lowers responseRank
      -> rank 1: forced line
      -> rank 0: checkmate.

The richer Strategy state can therefore undergo a genuine strategic phase reduction
while the color projection stutters or performs a phase-preserving uncrossing.
This is not a claim that all game choices are physically absent; only that they no
longer survive as distinct proof-relevant response classes.
-/

end MeTTafy.FourColor

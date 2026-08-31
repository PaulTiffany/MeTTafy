import examples.four_color.MetaConstructClosure

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

MapMaker operational strategy surface for the independent Four Color research lane.

The previous ordering is preserved as the complete operational 2 x 2 product:

1. Do: Observe       -- view the realized map globally;
2. Imagine: Observe  -- imagine one state, perceive its neighbors, imagine expansion;
3. Imagine: Act      -- imagine reactions and counter-plays through consequence chains;
4. Do: Act           -- commit one certified state with no perception during the write.

The first three phases are test-time reasoning. The fourth is the sole authority
crossing. The consequence chain in phase 3 may be arbitrarily long; a successful
run leaves a finite auditable residue.

This file proves primitive operational completeness directly: the four modes are
exactly the Do/Imagine x Observe/Act product. The remaining Four Color burden is
downstream: every strategy-safe nonterminal realized state must admit an ordered
phase-1/2/3 decision whose sound projection authorizes phase 4.
-/

namespace MeTTafy.FourColor

universe u v

/-! ## Complete operational product -/

/-- Whether the primitive operates on realized state or imaginary state. -/
inductive MapMakerDomain where
  | do
  | imagine
  deriving DecidableEq, Repr

/-- Whether the primitive observes or acts. -/
inductive MapMakerOperation where
  | observe
  | act
  deriving DecidableEq, Repr

/-- The four primitive MapMaker modes. -/
inductive MapMakerMode where
  | overview
  | localExpansion
  | counterPlay
  | draw
  deriving DecidableEq, Repr

/-- One cell of Do/Imagine x Observe/Act. -/
abbrev OperationalCell := MapMakerDomain × MapMakerOperation

/-- Each mode is exactly one cell of the operational product. -/
def modeCell : MapMakerMode → OperationalCell
  | .overview => (.do, .observe)
  | .localExpansion => (.imagine, .observe)
  | .counterPlay => (.imagine, .act)
  | .draw => (.do, .act)

/-- Every operational product cell has one named primitive. -/
def modeOfCell : OperationalCell → MapMakerMode
  | (.do, .observe) => .overview
  | (.imagine, .observe) => .localExpansion
  | (.imagine, .act) => .counterPlay
  | (.do, .act) => .draw

@[simp] theorem modeOfCell_modeCell (mode : MapMakerMode) :
    modeOfCell (modeCell mode) = mode := by
  cases mode <;> rfl

@[simp] theorem modeCell_modeOfCell (cell : OperationalCell) :
    modeCell (modeOfCell cell) = cell := by
  rcases cell with ⟨domain, operation⟩
  cases domain <;> cases operation <;> rfl

/-- Every product cell is occupied by a primitive mode. -/
theorem modeCell_surjective (cell : OperationalCell) :
    ∃ mode : MapMakerMode, modeCell mode = cell := by
  exact ⟨modeOfCell cell, modeCell_modeOfCell cell⟩

/-- The cell map is injective: two primitive names cannot occupy one product cell. -/
theorem modeCell_injective : Function.Injective modeCell := by
  intro lhs rhs same
  calc
    lhs = modeOfCell (modeCell lhs) := (modeOfCell_modeCell lhs).symm
    _ = modeOfCell (modeCell rhs) := congrArg modeOfCell same
    _ = rhs := modeOfCell_modeCell rhs

/--
Primitive Pareto completeness: every Do/Imagine x Observe/Act cell is represented
by exactly one MapMaker mode. There is no fifth primitive operational cell.
-/
theorem MapMakerParetoComplete (cell : OperationalCell) :
    ∃ mode : MapMakerMode,
      modeCell mode = cell ∧
        ∀ other : MapMakerMode, modeCell other = cell → other = mode := by
  refine ⟨modeOfCell cell, modeCell_modeOfCell cell, ?_⟩
  intro other same
  apply modeCell_injective
  exact same.trans (modeCell_modeOfCell cell).symm

/-! ## Pareto capability surface -/

/-- The irreducible capability axes used for the local Pareto comparison. -/
inductive MapMakerCapability where
  | globalOverview
  | localNeighborExpansion
  | interactiveCounterPlay
  | blindRealizedWrite
  deriving DecidableEq, Repr

/-- Each primitive owns one irreducible capability axis. -/
def primaryCapability : MapMakerMode → MapMakerCapability
  | .overview => .globalOverview
  | .localExpansion => .localNeighborExpansion
  | .counterPlay => .interactiveCounterPlay
  | .draw => .blindRealizedWrite

/-- The primitive capability assignment is injective: no two modes own one axis. -/
theorem primaryCapability_injective : Function.Injective primaryCapability := by
  intro lhs rhs same
  cases lhs <;> cases rhs <;> simp [primaryCapability] at same ⊢

/-- Primitive capability profile. -/
def HasModeCapability (mode : MapMakerMode) (capability : MapMakerCapability) : Prop :=
  capability = primaryCapability mode

/-- Weak Pareto dominance between primitive modes on the declared capability axes. -/
def ModeDominates (lhs rhs : MapMakerMode) : Prop :=
  ∀ capability, HasModeCapability rhs capability → HasModeCapability lhs capability

/-- No primitive mode dominates a distinct primitive mode. -/
theorem modeDominates_iff_eq (lhs rhs : MapMakerMode) :
    ModeDominates lhs rhs ↔ lhs = rhs := by
  constructor
  · intro dominates
    apply primaryCapability_injective
    have owned : HasModeCapability rhs (primaryCapability rhs) := rfl
    exact (dominates (primaryCapability rhs) owned).symm
  · intro same
    subst same
    intro capability owned
    exact owned

/-- The four primitive modes are therefore a Pareto antichain. -/
theorem distinct_modes_are_pareto_incomparable
    {lhs rhs : MapMakerMode}
    (different : lhs ≠ rhs) :
    ¬ ModeDominates lhs rhs ∧ ¬ ModeDominates rhs lhs := by
  constructor
  · intro dominates
    exact different ((modeDominates_iff_eq lhs rhs).mp dominates)
  · intro dominates
    exact different (((modeDominates_iff_eq rhs lhs).mp dominates).symm)

/-- Only Do:Act / draw owns realized-write capability. -/
theorem draw_is_only_writer (mode : MapMakerMode) :
    HasModeCapability mode .blindRealizedWrite ↔ mode = .draw := by
  constructor
  · intro writes
    apply primaryCapability_injective
    simpa [HasModeCapability, primaryCapability] using writes.symm
  · intro same
    subst same
    rfl

/-- Do:Act / draw has no perception or imagination capability. -/
theorem draw_has_no_perception :
    ¬ HasModeCapability .draw .globalOverview ∧
    ¬ HasModeCapability .draw .localNeighborExpansion ∧
    ¬ HasModeCapability .draw .interactiveCounterPlay := by
  simp [HasModeCapability, primaryCapability]

/-- The three test-time modes cannot write the realized map. -/
theorem nonDraw_modes_cannot_write
    {mode : MapMakerMode}
    (notDraw : mode ≠ .draw) :
    ¬ HasModeCapability mode .blindRealizedWrite := by
  intro writes
  exact notDraw ((draw_is_only_writer mode).mp writes)

/-! ## Preserved operational order -/

/-- The three reasoning phases admitted before authority crossing. -/
inductive PrecommitMode where
  | overview
  | localExpansion
  | counterPlay
  deriving DecidableEq, Repr

/-- Embed a precommit phase into the full MapMaker alphabet. -/
def PrecommitMode.toMapMakerMode : PrecommitMode → MapMakerMode
  | .overview => .overview
  | .localExpansion => .localExpansion
  | .counterPlay => .counterPlay

/-- A precommit mode can never silently become Do:Act. -/
theorem precommit_ne_draw (mode : PrecommitMode) :
    mode.toMapMakerMode ≠ .draw := by
  cases mode <;> simp [PrecommitMode.toMapMakerMode]

/-- A MapMaker program is a finite transferable residue over the modes. -/
abbrev MapMakerProgram := List MapMakerMode

/-- The one-pass canonical product ordering. -/
def canonicalParetoProgram : MapMakerProgram :=
  [.overview, .localExpansion, .counterPlay, .draw]

/-- The canonical ordering is literally Do:Observe, Imagine:Observe, Imagine:Act, Do:Act. -/
theorem canonicalProgram_preserves_product_order :
    canonicalParetoProgram.map modeCell =
      [(.do, .observe), (.imagine, .observe), (.imagine, .act), (.do, .act)] := by
  rfl

/-- Ordered precommit residue: phase 1, then phase 2, then phase-3 consequence chain. -/
def orderedPrecommitProgram (counterSteps : Nat) : MapMakerProgram :=
  [.overview, .localExpansion] ++ List.replicate counterSteps .counterPlay

/-- Full ordered authority-crossing residue: O ; L ; C* ; D. -/
def orderedOperationalProgram (counterSteps : Nat) : MapMakerProgram :=
  orderedPrecommitProgram counterSteps ++ [.draw]

/-- The full normal-form predicate. -/
def IsOrderedOperationalProgram (program : MapMakerProgram) : Prop :=
  ∃ counterSteps, program = orderedOperationalProgram counterSteps

/-- A program has a capability when one of its primitive modes has it. -/
def ProgramHasCapability
    (program : MapMakerProgram)
    (capability : MapMakerCapability) : Prop :=
  ∃ mode, mode ∈ program ∧ HasModeCapability mode capability

/-- The canonical program covers every declared capability axis. -/
theorem canonicalProgram_capability_complete
    (capability : MapMakerCapability) :
    ProgramHasCapability canonicalParetoProgram capability := by
  cases capability with
  | globalOverview =>
      exact ⟨.overview, by simp [canonicalParetoProgram], by simp [HasModeCapability, primaryCapability]⟩
  | localNeighborExpansion =>
      exact ⟨.localExpansion, by simp [canonicalParetoProgram], by simp [HasModeCapability, primaryCapability]⟩
  | interactiveCounterPlay =>
      exact ⟨.counterPlay, by simp [canonicalParetoProgram], by simp [HasModeCapability, primaryCapability]⟩
  | blindRealizedWrite =>
      exact ⟨.draw, by simp [canonicalParetoProgram], by simp [HasModeCapability, primaryCapability]⟩

/-! ## Ordered Decision Reachability -/

/-- A precommit refinement step is labelled by one of the three non-writing phases. -/
abbrev PrecommitAdvance (Witness : Type v) :=
  Witness → Witness → PrecommitMode → Prop

/-- Forget the phase label while retaining the admissible refinement relation. -/
def PrecommitGeneratedStep
    {Witness : Type v}
    (advance : PrecommitAdvance Witness) :
    Witness → Witness → Prop :=
  fun before after => ∃ mode, advance before after mode

/--
The exact preserved phase order as a transferable deciding residue:

Do:Observe -> Imagine:Observe -> Imagine:Act* -> deciding endpoint.

The phase-3 chain may have any finite length; `stay` represents zero counter-play
steps when local imagined observation already decides the move.
-/
structure OrderedMapMakerDecision
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness) where
  afterOverview : box.Witness
  afterLocalObservation : box.Witness
  endpoint : box.Witness
  color : V4
  overviewStep : advance seed afterOverview .overview
  localObservationStep : advance afterOverview afterLocalObservation .localExpansion
  consequenceChain : AdmissibleRefinementChain
    (fun before after => advance before after .counterPlay)
    afterLocalObservation endpoint
  hit : projection.project endpoint = some color

/-- Every phase-3 counter-play step is also a generic precommit-generated step. -/
theorem counterPlayStep_is_precommitGenerated
    {Witness : Type v}
    (advance : PrecommitAdvance Witness)
    {before after : Witness}
    (step : advance before after .counterPlay) :
    PrecommitGeneratedStep advance before after := by
  exact ⟨.counterPlay, step⟩

/--
Erase the phase labels only after the ordered structure has been witnessed,
recovering the generic Decision Reachability certificate machinery.
-/
def OrderedMapMakerDecision.toDecisionWitness
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness)
    (decision : OrderedMapMakerDecision box projection seed advance) :
    DecisionWitness box projection seed (PrecommitGeneratedStep advance) :=
  {
    endpoint := decision.endpoint
    color := decision.color
    chain := .advance
      ⟨.overview, decision.overviewStep⟩
      (.advance
        ⟨.localExpansion, decision.localObservationStep⟩
        (decision.consequenceChain.mono
          (fun step => counterPlayStep_is_precommitGenerated advance step)))
    hit := decision.hit
  }

/-- The ordered phase-1/2/3 residue plus projection soundness yields authority. -/
theorem orderedMapMakerDecision_sound_has_certificate
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness)
    (decision : OrderedMapMakerDecision box projection seed advance) :
    Nonempty (CertifiedInstantiation map focus) := by
  exact ⟨compressDecision box projection sound
    (decision.toDecisionWitness box projection seed advance)⟩

/--
Do:Act is not another reasoning step. It exists only after the ordered decision
residue crosses the sound projection wall.
-/
structure BlindDraw
    {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  certificate : CertifiedInstantiation map focus

/-- Construct the final Do:Act from an ordered and sound phase-1/2/3 decision. -/
def blindDrawFromOrderedDecision
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness)
    (decision : OrderedMapMakerDecision box projection seed advance) :
    BlindDraw map focus :=
  ⟨compressDecision box projection sound
    (decision.toDecisionWitness box projection seed advance)⟩

/-- The final Do:Act consumes exactly one realized void. -/
theorem blindDraw_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (draw : BlindDraw map focus) :
    voidCount roster (instantiate draw.certificate) = voidCount roster map - 1 := by
  exact voidCount_instantiate roster draw.certificate

/-! ## Remaining Four Color completeness target -/

/--
The remaining theorem is now stated only where the actual Four Color burden lies:
every strategy-safe nonterminal realized state admits the preserved ordered
phase-1/2/3 decision, with a sound projection whose phase-4 draw stays safe.

Primitive operational completeness is already proved above by the 2 x 2 product.
-/
def OrderedMapMakerDecisionComplete
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex) : Prop :=
  ∀ (map : RealizedMap Vertex),
    safe map →
    HasVoid map →
    ∃ (focus : Focus Vertex)
      (box : ImaginationBox.{u, 0} Vertex map focus)
      (projection : ImaginaryProjection box)
      (seed : box.Witness)
      (advance : PrecommitAdvance box.Witness)
      (sound : ProjectionSound box projection)
      (decision : OrderedMapMakerDecision box projection seed advance),
      safe (instantiate (blindDrawFromOrderedDecision
        box projection sound seed advance decision).certificate)

/--
BRIDGE: proving ordered MapMaker decision completeness discharges the existing
construction-level safe-instantiation obligation.
-/
theorem orderedMapMakerDecisionComplete_implies_safe_instantiation
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex)
    (complete : OrderedMapMakerDecisionComplete safe) :
    EveryStrategySafeStateHasSafeInstantiation safe := by
  intro map safeMap hasVoid
  rcases complete map safeMap hasVoid with
    ⟨focus, box, projection, seed, advance, sound, decision, safeAfter⟩
  let draw := blindDrawFromOrderedDecision box projection sound seed advance decision
  exact ⟨focus, draw.certificate, safeAfter⟩

end MeTTafy.FourColor

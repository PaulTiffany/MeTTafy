import examples.four_color.MetaConstructClosure

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

MapMaker Pareto strategy surface for the independent Four Color research lane.

The four primitive modes specialize the SRMF cycle into the map-making task:

1. overview: view the realized map globally;
2. local expansion: imagine one state, perceive its neighbors, imagine expansion;
3. counter-play: imagine reactions and counter-plays among states;
4. draw: commit one certified state with no perception during the write.

The formalization distinguishes three claims:

* the four declared primitive capabilities are pairwise non-redundant;
* together they cover the declared MapMaker capability axes;
* the stronger theorem that every admissible MapMaker strategy is behaviorally
  reducible to a composition of these modes is an explicit open premise rather
  than a consequence of declaring a four-constructor enum.

This keeps the Pareto-completeness claim transferable without laundering the
remaining mathematical work.
-/

namespace MeTTafy.FourColor

universe u v

/-- The four primitive MapMaker modes. -/
inductive MapMakerMode where
  | overview
  | localExpansion
  | counterPlay
  | draw
  deriving DecidableEq, Repr

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

/-- Only draw owns realized-write capability. -/
theorem draw_is_only_writer (mode : MapMakerMode) :
    HasModeCapability mode .blindRealizedWrite ↔ mode = .draw := by
  constructor
  · intro writes
    apply primaryCapability_injective
    simpa [HasModeCapability, primaryCapability] using writes.symm
  · intro same
    subst same
    rfl

/-- Draw has no perception/imagination capability in the primitive profile. -/
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

/-- The perception/imagination modes admitted before authority crossing. -/
inductive PrecommitMode where
  | overview
  | localExpansion
  | counterPlay
  deriving DecidableEq, Repr

/-- Embed a precommit mode into the full MapMaker alphabet. -/
def PrecommitMode.toMapMakerMode : PrecommitMode → MapMakerMode
  | .overview => .overview
  | .localExpansion => .localExpansion
  | .counterPlay => .counterPlay

/-- A precommit mode can never silently become draw. -/
theorem precommit_ne_draw (mode : PrecommitMode) :
    mode.toMapMakerMode ≠ .draw := by
  cases mode <;> simp [PrecommitMode.toMapMakerMode]

/-- A MapMaker program is an arbitrary finite transferable residue over the modes. -/
abbrev MapMakerProgram := List MapMakerMode

/-- The canonical four-mode capability cover. -/
def canonicalParetoProgram : MapMakerProgram :=
  [.overview, .localExpansion, .counterPlay, .draw]

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

/--
Capability-level Pareto completeness is mechanically banked: any strategy whose
observable capability profile is expressed on these axes is weakly covered by
the canonical four-mode program.
-/
def StrategyHasCapability (Strategy : Type v) := Strategy → MapMakerCapability → Prop

def ProgramWeaklyCoversStrategy
    {Strategy : Type v}
    (strategyHas : StrategyHasCapability Strategy)
    (program : MapMakerProgram)
    (strategy : Strategy) : Prop :=
  ∀ capability, strategyHas strategy capability → ProgramHasCapability program capability

theorem canonicalProgram_weakly_covers_every_profile
    {Strategy : Type v}
    (strategyHas : StrategyHasCapability Strategy)
    (strategy : Strategy) :
    ProgramWeaklyCoversStrategy strategyHas canonicalParetoProgram strategy := by
  intro capability _used
  exact canonicalProgram_capability_complete capability

/-! ## Behavioral Pareto completeness: explicit theorem target -/

/--
`Implements` says that one program over the four primitive modes reproduces the
relevant behavior of an external MapMaker strategy. The exact behavioral notion
is caller-supplied so that capability enumeration cannot masquerade as the
substantive reduction theorem.
-/
abbrev Implements (Strategy : Type v) := Strategy → MapMakerProgram → Prop

/--
OPEN PREMISE / THEOREM TARGET: every admissible MapMaker strategy is represented
by some composition over overview, local expansion, counter-play, and blind draw.

This is the substantive Pareto-completeness claim. No global inhabitant is
supplied merely from the four-constructor ontology.
-/
def MapMakerParetoComplete
    {Strategy : Type v}
    (admissible : Strategy → Prop)
    (implements : Implements Strategy) : Prop :=
  ∀ strategy, admissible strategy → ∃ program, implements strategy program

/-! ## SRMF / Decision Reachability specialization -/

/--
A precommit refinement step is labelled by one of the three non-writing SRMF
modes. Overview, local expansion, and counter-play may repeat without bound at
search time; the transferred proof residue records only the finite deciding spine.
-/
abbrev PrecommitAdvance (Witness : Type v) :=
  Witness → Witness → PrecommitMode → Prop

/-- Forget the mode label while retaining the admissible refinement relation. -/
def PrecommitGeneratedStep
    {Witness : Type v}
    (advance : PrecommitAdvance Witness) :
    Witness → Witness → Prop :=
  fun before after => ∃ mode, advance before after mode

/-- Decision Reachability specialized to the three non-writing MapMaker modes. -/
def MapMakerDecisionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness) : Prop :=
  DecisionReachable box projection seed (PrecommitGeneratedStep advance)

/--
The three-mode imagination spine plus projection soundness yields exactly the
same authority-bearing certificate as generic Decision Reachability.
-/
theorem mapMakerDecisionReachable_sound_has_certificate
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (seed : box.Witness)
    (advance : PrecommitAdvance box.Witness)
    (reachable : MapMakerDecisionReachable box projection seed advance) :
    Nonempty (CertifiedInstantiation map focus) := by
  exact decisionReachable_sound_has_certificate
    box projection sound seed (PrecommitGeneratedStep advance) reachable

/--
Blind draw is not another inference step. It is the typed realization payload
that exists only after Decision Reachability has crossed the sound projection wall.
-/
structure BlindDraw
    {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  certificate : CertifiedInstantiation map focus

/-- Construct blind draw authority from a witnessed and sound precommit chain. -/
def blindDrawFromDecision
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    {seed : box.Witness}
    {advance : PrecommitAdvance box.Witness}
    (decision : DecisionWitness box projection seed (PrecommitGeneratedStep advance)) :
    BlindDraw map focus :=
  ⟨compressDecision box projection sound decision⟩

/-- A blind draw realizes exactly one certified void. -/
theorem blindDraw_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (draw : BlindDraw map focus) :
    voidCount roster (instantiate draw.certificate) = voidCount roster map - 1 := by
  exact voidCount_instantiate roster draw.certificate

end MeTTafy.FourColor

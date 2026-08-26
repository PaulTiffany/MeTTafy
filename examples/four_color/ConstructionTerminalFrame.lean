import Std.Data.Finset.Basic
import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Construction/result frame for the independent Four Color research lane.

AUTHORITATIVE FRAME CONTRACT
----------------------------
Construction history contains only realized partial maps. One construction turn
instantiates exactly one previously void focus with one V4 state and preserves
all other realized site states.

Counterfactual recolorings do not live here. They belong to inspection/inference
space and acquire no authority over construction unless an explicit soundness
bridge derives a `CertifiedInstantiation` for the current realized map.

Terminal verification is a separate type boundary and accepts only a completed
map. Thus:

  imagine many -> certify one -> instantiate one -> re-observe

and construction time advances only at the `instantiate` boundary.
-/

namespace MeTTafy.FourColor

universe u

/-- Properness of the currently realized colored contacts. Void sites impose no
color constraint until the map-maker instantiates them. -/
def RealizedProper {Vertex : Type u}
    (adjacent : Vertex → Vertex → Prop)
    (state : Vertex → SiteState) : Prop :=
  ∀ u v cu cv,
    adjacent u v →
    state u = .colored cu →
    state v = .colored cv →
    cu ≠ cv

/-- One partially realized map during construction play. -/
structure ConstructionMap (Vertex : Type u) where
  adjacent : Vertex → Vertex → Prop
  state : Vertex → SiteState
  proper : RealizedProper adjacent state

/-- Authority-facing name for the actual partial map. -/
abbrev RealizedMap (Vertex : Type u) := ConstructionMap Vertex

/-- A named current void under consideration. This is a realized-map focus, not
an imagined frontier state. -/
structure Focus (Vertex : Type u) where
  vertex : Vertex

/--
The exact local fact required to instantiate `color` at `focus` without changing
any already-realized site.

The neighbor condition is orientation-neutral so the construction layer does not
silently assume a symmetry theorem about the caller's adjacency relation.
-/
structure AdmissibleAt {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex)
    (color : V4) : Prop where
  focus_was_void : map.state focus.vertex = .void
  no_self_contact : ¬ map.adjacent focus.vertex focus.vertex
  differs_from_realized_neighbors :
    ∀ neighbor neighborColor,
      (map.adjacent focus.vertex neighbor ∨ map.adjacent neighbor focus.vertex) →
      map.state neighbor = .colored neighborColor →
      color ≠ neighborColor

/--
The only object allowed to cross from inference into realized construction.
It carries a color plus a proof that this color is admissible on the actual map.
No imagined state or predicted response is itself construction authority.
-/
structure CertifiedInstantiation {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  color : V4
  admissible : AdmissibleAt map focus color

/-- Point update used only by the certified construction boundary. -/
def instantiatedState {Vertex : Type u} [DecidableEq Vertex]
    (map : RealizedMap Vertex)
    (focus : Focus Vertex)
    (color : V4)
    (vertex : Vertex) : SiteState :=
  if vertex = focus.vertex then .colored color else map.state vertex

/--
Execute exactly one certified `void -> V4` event. No recoloring route, imagined
intermediate frontier, or future construction move is executed here.
-/
def instantiate {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (cert : CertifiedInstantiation map focus) : RealizedMap Vertex where
  adjacent := map.adjacent
  state := instantiatedState map focus cert.color
  proper := by
    intro left right leftColor rightColor adjacent leftRealized rightRealized
    by_cases leftFocus : left = focus.vertex
    · subst left
      by_cases rightFocus : right = focus.vertex
      · subst right
        exact False.elim (cert.admissible.no_self_contact adjacent)
      · have leftColorEq : cert.color = leftColor := by
          have sameColored :
              SiteState.colored cert.color = SiteState.colored leftColor := by
            simpa [instantiatedState] using leftRealized
          cases sameColored
          rfl
        have rightBefore : map.state right = .colored rightColor := by
          simpa [instantiatedState, rightFocus] using rightRealized
        have different := cert.admissible.differs_from_realized_neighbors
          right rightColor (Or.inl adjacent) rightBefore
        simpa [leftColorEq] using different
    · by_cases rightFocus : right = focus.vertex
      · subst right
        have rightColorEq : cert.color = rightColor := by
          have sameColored :
              SiteState.colored cert.color = SiteState.colored rightColor := by
            simpa [instantiatedState] using rightRealized
          cases sameColored
          rfl
        have leftBefore : map.state left = .colored leftColor := by
          simpa [instantiatedState, leftFocus] using leftRealized
        have different := cert.admissible.differs_from_realized_neighbors
          left leftColor (Or.inr adjacent) leftBefore
        have reverse : leftColor ≠ cert.color := Ne.symm different
        simpa [rightColorEq] using reverse
      · have leftBefore : map.state left = .colored leftColor := by
          simpa [instantiatedState, leftFocus] using leftRealized
        have rightBefore : map.state right = .colored rightColor := by
          simpa [instantiatedState, rightFocus] using rightRealized
        exact map.proper left right leftColor rightColor
          adjacent leftBefore rightBefore

/-- Realized execution preserves every non-focus site exactly. -/
theorem instantiate_preserves_elsewhere
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (cert : CertifiedInstantiation map focus)
    (vertex : Vertex)
    (notFocus : vertex ≠ focus.vertex) :
    (instantiate cert).state vertex = map.state vertex := by
  simp [instantiate, instantiatedState, notFocus]

/-- The realized focus is exactly the certified V4 state. -/
theorem instantiate_realizes_focus
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (cert : CertifiedInstantiation map focus) :
    (instantiate cert).state focus.vertex = .colored cert.color := by
  simp [instantiate, instantiatedState]

/-- One map-maker action in the legacy construction interface. -/
structure MapMakerStep {Vertex : Type u}
    (before after : ConstructionMap Vertex) where
  focus : Vertex
  color : V4
  same_adjacency : before.adjacent = after.adjacent
  focus_was_void : before.state focus = .void
  focus_is_realized : after.state focus = .colored color
  unchanged_elsewhere : ∀ vertex, vertex ≠ focus → after.state vertex = before.state vertex

namespace MapMakerStep

/-- A map-maker step instantiates a genuine palette state at its focus. -/
theorem instantiates_palette_state
    {Vertex : Type u}
    {before after : ConstructionMap Vertex}
    (step : MapMakerStep before after) :
    ∃ color : V4, after.state step.focus = .colored color := by
  exact ⟨step.color, step.focus_is_realized⟩

/-- The focus was not already a realized color before this step. -/
theorem focus_not_colored_before
    {Vertex : Type u}
    {before after : ConstructionMap Vertex}
    (step : MapMakerStep before after) :
    ∀ color : V4, before.state step.focus ≠ .colored color := by
  intro color equal
  rw [step.focus_was_void] at equal
  cases equal

end MapMakerStep

/--
A proof-relevant realized construction step. Its only executable authority is the
`CertifiedInstantiation` for the current realized map and focus.
-/
structure ConstructionStep (Vertex : Type u) where
  before : RealizedMap Vertex
  focus : Focus Vertex
  certificate : CertifiedInstantiation before focus

namespace ConstructionStep

/-- Execute the single certified construction event. -/
def after {Vertex : Type u} [DecidableEq Vertex]
    (step : ConstructionStep Vertex) : RealizedMap Vertex :=
  instantiate step.certificate

/-- Compatibility bridge to the older `MapMakerStep` witness. -/
def toMapMakerStep {Vertex : Type u} [DecidableEq Vertex]
    (step : ConstructionStep Vertex) :
    MapMakerStep step.before step.after where
  focus := step.focus.vertex
  color := step.certificate.color
  same_adjacency := rfl
  focus_was_void := step.certificate.admissible.focus_was_void
  focus_is_realized := by
    simp [after, instantiate, instantiatedState]
  unchanged_elsewhere := by
    intro vertex notFocus
    exact instantiate_preserves_elsewhere
      step.certificate vertex notFocus

end ConstructionStep

/-- The finite set of currently uninstantiated sites. -/
def voidSites {Vertex : Type u} [Fintype Vertex] [DecidableEq Vertex]
    (map : RealizedMap Vertex) : Finset Vertex :=
  Finset.univ.filter (fun vertex => map.state vertex = .void)

/-- Construction time is measured by the remaining uninstantiated sites. -/
def voidCount {Vertex : Type u} [Fintype Vertex] [DecidableEq Vertex]
    (map : RealizedMap Vertex) : Nat :=
  (voidSites map).card

/-- A certified instantiation removes exactly its focus from the void set. -/
theorem voidSites_instantiate
    {Vertex : Type u} [Fintype Vertex] [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (cert : CertifiedInstantiation map focus) :
    voidSites (instantiate cert) = (voidSites map).erase focus.vertex := by
  ext vertex
  by_cases atFocus : vertex = focus.vertex
  · subst vertex
    simp [voidSites, instantiate, instantiatedState]
  · simp [voidSites, instantiate, instantiatedState, atFocus]

/-- Every realized construction turn consumes exactly one void. -/
theorem voidCount_instantiate
    {Vertex : Type u} [Fintype Vertex] [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (cert : CertifiedInstantiation map focus) :
    voidCount (instantiate cert) = voidCount map - 1 := by
  change (voidSites (instantiate cert)).card = (voidSites map).card - 1
  rw [voidSites_instantiate]
  exact Finset.card_erase_of_mem (by
    simp [voidSites, cert.admissible.focus_was_void])

/-- A completed map is a construction state with no remaining void sites. -/
structure CompletedMap (Vertex : Type u) extends ConstructionMap Vertex where
  complete : ∀ vertex, ∃ color : V4, state vertex = .colored color

/--
The terminal result exposed after construction. This contains no move policy,
no intermediate route, and no authority to alter the completed map.
-/
structure TerminalResult (Vertex : Type u) where
  completed : CompletedMap Vertex

/-- Terminal verification is defined only on a completed map. -/
def verifyTerminalResult {Vertex : Type u}
    (completed : CompletedMap Vertex) : TerminalResult Vertex :=
  ⟨completed⟩

/-- Every finished site realizes one of the four V4 states. -/
theorem terminal_result_uses_only_v4
    {Vertex : Type u}
    (result : TerminalResult Vertex) :
    ∀ vertex, ∃ color : V4, result.completed.state vertex = .colored color := by
  exact result.completed.complete

/-- The finished result retains properness of every realized adjacency. -/
theorem terminal_result_is_proper
    {Vertex : Type u}
    (result : TerminalResult Vertex) :
    RealizedProper result.completed.adjacent result.completed.state :=
  result.completed.proper

end MeTTafy.FourColor

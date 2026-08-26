import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Construction/result frame for the Four Color research lane.

FRAME CONTRACT
--------------
The game is instantiated from inside construction. A map-maker realizes one
previously void site as one of the four V4 palette states while preserving every
other realized site. No terminal verifier participates in that move.

Terminal verification is intentionally a different type boundary. A verifier
accepts only a `CompletedMap`, whose every site has already been realized as a
palette state. Thus a partial construction cannot be passed to the terminal
result interface by construction.

The theorem proved here is deliberately small: a completed map uses only V4
states because those are exactly the states the map-maker was allowed to
instantiate. This file does not prove that a legal completion always exists or
that every construction strategy completes a planar map.
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

/-- One partially realized map during play. -/
structure ConstructionMap (Vertex : Type u) where
  adjacent : Vertex → Vertex → Prop
  state : Vertex → SiteState
  proper : RealizedProper adjacent state

/--
One map-maker action: exactly one named void becomes one V4 state and every
other site is left as realized before the action.
-/
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

/--
The terminal verifier's four-color observation: every realized site of the
finished map has one of the V4 palette states.
-/
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

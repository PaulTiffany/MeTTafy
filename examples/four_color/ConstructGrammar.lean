import examples.four_color.RedTeamComposition

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A generic composition grammar for Four Color game constructs.

FRAME CONTRACT
--------------
Named pictures such as stripes or the red-team A-B-A construction are not the
ontology.  They are concrete primitive witnesses that may be embedded into an
open construct grammar.  Larger game-theoretic meta-constructs are built by
composition.

The grammar is intentionally polymorphic in its primitive construct type and in
its geometry/contact fact type.  Adding a new useful picture therefore does not
require adding a new constructor to the meta-language.

The shared game projection records only:

* realized facts (geometry/contact evidence supplied by the primitive layer),
* actions that have already occurred on the local surface, and
* actions that are currently available on that local surface.

Two constructs may compose only when an action consumed by either side is not
advertised as available by the other.  Local coherence is therefore preserved
under compatible composition.

Void/end remains a local boundary condition: a stopped surface has no available
action in its declared action domain.  Restart is a fresh construct elsewhere,
not another action inside the exhausted surface.
-/

namespace MeTTafy.FourColor

universe u v w

/--
A minimal primitive example.  A basic stripe is two distinct palette states in
an ordered local relation.  It is an example atom, not an exhaustive list of
possible primitive construct kinds.
-/
structure BasicStripe where
  lower : V4
  upper : V4
  distinct : lower ≠ upper

/--
Open syntax for game constructs.  `Primitive` is deliberately supplied by the
caller, so the grammar never needs an enum of every recognizable picture.
-/
inductive MetaConstruct (Primitive : Type u) where
  | atom (primitive : Primitive)
  | compose (left right : MetaConstruct Primitive)

namespace MetaConstruct

/-- Any primitive construct embeds directly into the meta-construct language. -/
def embed {Primitive : Type u} (primitive : Primitive) : MetaConstruct Primitive :=
  .atom primitive

/-- Basic stripes are ordinary atoms of the same generic grammar. -/
def stripe (primitive : BasicStripe) : MetaConstruct BasicStripe :=
  embed primitive

end MetaConstruct

/--
The game-theoretic projection of a construct.

`Fact` deliberately remains abstract: it may encode contacts, boundary pieces,
carrier incidence, stripe orientation, or another mechanically meaningful local
fact without changing the composition calculus.
-/
structure GameSurface (Fact : Type v) (Action : Type w) where
  realizes : Fact → Prop
  acted : Action → Prop
  available : Action → Prop

namespace GameSurface

/-- An acted route cannot simultaneously remain available on one local surface. -/
def Coherent {Fact : Type v} {Action : Type w}
    (surface : GameSurface Fact Action) : Prop :=
  ∀ action, surface.acted action → ¬ surface.available action

/-- No action remains available on the declared local surface. -/
def Stopped {Fact : Type v} {Action : Type w}
    (surface : GameSurface Fact Action) : Prop :=
  ∀ action, ¬ surface.available action

/--
Pointwise composition of two construct projections.  Composition accumulates
realized facts, acted routes, and still-advertised opportunities.
-/
def compose {Fact : Type v} {Action : Type w}
    (left right : GameSurface Fact Action) : GameSurface Fact Action where
  realizes := fun fact => left.realizes fact ∨ right.realizes fact
  acted := fun action => left.acted action ∨ right.acted action
  available := fun action => left.available action ∨ right.available action

/--
Cross-compatibility required for coherent composition: neither side may offer
an action that the other side has already consumed.
-/
def Compatible {Fact : Type v} {Action : Type w}
    (left right : GameSurface Fact Action) : Prop :=
  (∀ action, left.acted action → ¬ right.available action) ∧
  (∀ action, right.acted action → ¬ left.available action)

/-- Compatible coherent game surfaces compose into another coherent surface. -/
theorem coherent_compose
    {Fact : Type v} {Action : Type w}
    (left right : GameSurface Fact Action)
    (leftCoherent : Coherent left)
    (rightCoherent : Coherent right)
    (compatible : Compatible left right) :
    Coherent (compose left right) := by
  intro action actedHere availableHere
  rcases actedHere with actedLeft | actedRight
  · rcases availableHere with availableLeft | availableRight
    · exact leftCoherent action actedLeft availableLeft
    · exact compatible.1 action actedLeft availableRight
  · rcases availableHere with availableLeft | availableRight
    · exact compatible.2 action actedRight availableLeft
    · exact rightCoherent action actedRight availableRight

/--
Observational equality at the game layer.  Syntax trees may differ while their
realized facts and action affordances are the same.
-/
def Equivalent {Fact : Type v} {Action : Type w}
    (left right : GameSurface Fact Action) : Prop :=
  (∀ fact, left.realizes fact ↔ right.realizes fact) ∧
  (∀ action, left.acted action ↔ right.acted action) ∧
  (∀ action, left.available action ↔ right.available action)

/-- Grouping of composition does not change the game-theoretic projection. -/
theorem compose_associative
    {Fact : Type v} {Action : Type w}
    (first second third : GameSurface Fact Action) :
    Equivalent
      (compose (compose first second) third)
      (compose first (compose second third)) := by
  constructor
  · intro fact
    constructor
    · intro observed
      rcases observed with observed12 | observed3
      · rcases observed12 with observed1 | observed2
        · exact Or.inl observed1
        · exact Or.inr (Or.inl observed2)
      · exact Or.inr (Or.inr observed3)
    · intro observed
      rcases observed with observed1 | observed23
      · exact Or.inl (Or.inl observed1)
      · rcases observed23 with observed2 | observed3
        · exact Or.inl (Or.inr observed2)
        · exact Or.inr observed3
  · constructor
    · intro action
      constructor
      · intro actedHere
        rcases actedHere with acted12 | acted3
        · rcases acted12 with acted1 | acted2
          · exact Or.inl acted1
          · exact Or.inr (Or.inl acted2)
        · exact Or.inr (Or.inr acted3)
      · intro actedHere
        rcases actedHere with acted1 | acted23
        · exact Or.inl (Or.inl acted1)
        · rcases acted23 with acted2 | acted3
          · exact Or.inl (Or.inr acted2)
          · exact Or.inr acted3
    · intro action
      constructor
      · intro availableHere
        rcases availableHere with available12 | available3
        · rcases available12 with available1 | available2
          · exact Or.inl available1
          · exact Or.inr (Or.inl available2)
        · exact Or.inr (Or.inr available3)
      · intro availableHere
        rcases availableHere with available1 | available23
        · exact Or.inl (Or.inl available1)
        · rcases available23 with available2 | available3
          · exact Or.inl (Or.inr available2)
          · exact Or.inr available3

end GameSurface

/--
Interpretation of primitive constructs into game semantics.  Each primitive must
already be locally coherent before it enters the composition grammar.
-/
structure PrimitiveSemantics
    (Primitive : Type u) (Fact : Type v) (Action : Type w) where
  surface : Primitive → GameSurface Fact Action
  coherent : ∀ primitive, GameSurface.Coherent (surface primitive)

/-- Evaluate a meta-construct by recursively composing primitive game surfaces. -/
def evaluate
    {Primitive : Type u} {Fact : Type v} {Action : Type w}
    (semantics : PrimitiveSemantics Primitive Fact Action) :
    MetaConstruct Primitive → GameSurface Fact Action
  | .atom primitive => semantics.surface primitive
  | .compose left right =>
      GameSurface.compose (evaluate semantics left) (evaluate semantics right)

/--
A meta-construct is well formed when each recursive composition is compatible.
No finite catalogue of named visual patterns occurs in this definition.
-/
def WellFormed
    {Primitive : Type u} {Fact : Type v} {Action : Type w}
    (semantics : PrimitiveSemantics Primitive Fact Action) :
    MetaConstruct Primitive → Prop
  | .atom _ => True
  | .compose left right =>
      WellFormed semantics left ∧
      WellFormed semantics right ∧
      GameSurface.Compatible (evaluate semantics left) (evaluate semantics right)

/-- Every well-formed construct tree has a coherent game-theoretic projection. -/
theorem wellFormed_evaluates_coherently
    {Primitive : Type u} {Fact : Type v} {Action : Type w}
    (semantics : PrimitiveSemantics Primitive Fact Action)
    (construct : MetaConstruct Primitive)
    (wellFormed : WellFormed semantics construct) :
    GameSurface.Coherent (evaluate semantics construct) := by
  induction construct with
  | atom primitive =>
      exact semantics.coherent primitive
  | compose left right leftIH rightIH =>
      rcases wellFormed with ⟨leftWellFormed, rightWellFormed, compatible⟩
      exact GameSurface.coherent_compose
        (evaluate semantics left)
        (evaluate semantics right)
        (leftIH leftWellFormed)
        (rightIH rightWellFormed)
        compatible

/--
The existing void-stop semantics is exactly a stopped game surface when the
action domain is restricted to the three non-reference upward states.
-/
def UpwardSurfaceStopped
    (reference : V4)
    {Fact : Type v}
    (surface : GameSurface Fact V4) : Prop :=
  ∀ state, UpwardFrom reference state → ¬ surface.available state

/-- Lift the already-banked local void stop into the generic construct semantics. -/
theorem canonical_BCD_void_stop_is_construct_stop
    {Fact : Type v}
    (surface : GameSurface Fact V4)
    (bActed : surface.acted V4.a)
    (cActed : surface.acted V4.b)
    (dActed : surface.acted V4.c)
    (voidBlocks : VoidBlocksActed surface.acted surface.available) :
    UpwardSurfaceStopped V4.zero surface := by
  exact canonical_BCD_acted_and_void_blocked_stop_game
    surface.acted surface.available bActed cActed dActed voidBlocks

end MeTTafy.FourColor

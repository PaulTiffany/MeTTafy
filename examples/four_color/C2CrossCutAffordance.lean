import examples.four_color.ConstructGrammar

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Operational cross-cut semantics for the Four Color research lane.

FRAME CONTRACT
--------------
A cross-cut is treated first as a game move, not as a generic Jordan object.
By definition it has an asymmetric affordance effect:

* the state it cuts was available and is restricted afterward;
* the state it escapes to is available afterward.

This immediately makes a cross-cut a non-dead-end game event.  In the V4 lane,
when one fixed reference and two distinct upward states determine the move, the
escape state is the already-banked unique third state `reference + cut + mover`.

This file does not prove that every canonical alternating planar boundary forces
such a cross-cut event to exist.  It therefore does not, by itself, discharge
`crosscut_meets_opposite` or unconditional C2.  It formalizes what a cross-cut
means operationally once the move is present.
-/

namespace MeTTafy.FourColor

universe u v

/--
One operational cross-cut turn between two game surfaces.

`cut` is a state whose prior opportunity is removed by the turn.
`escape` is a state for which the successor surface offers an opportunity.
No geometric path is baked into this definition.
-/
structure CrossCutTurn (Fact : Type u) (State : Type v) where
  before : GameSurface Fact State
  after : GameSurface Fact State
  cut : State
  escape : State
  cut_was_available : before.available cut
  restricts_cut : ¬ after.available cut
  offers_escape : after.available escape

namespace CrossCutTurn

/-- The cut state and escape state cannot coincide. -/
theorem cut_ne_escape
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State) :
    turn.cut ≠ turn.escape := by
  intro equal
  apply turn.restricts_cut
  rw [equal]
  exact turn.offers_escape

/-- A cross-cut genuinely removes an opportunity that existed before the move. -/
theorem cut_is_genuinely_restricted
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State) :
    turn.before.available turn.cut ∧ ¬ turn.after.available turn.cut := by
  exact ⟨turn.cut_was_available, turn.restricts_cut⟩

/-- The escape opportunity is present on the realized successor surface. -/
theorem escape_is_free
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State) :
    turn.after.available turn.escape :=
  turn.offers_escape

/-- A cross-cut cannot itself leave the successor surface completely stopped. -/
theorem after_not_stopped
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State) :
    ¬ GameSurface.Stopped turn.after := by
  intro stopped
  exact stopped turn.escape turn.offers_escape

/--
Optional stronger notion: the escape state was unavailable before the turn and
is newly available afterward.  Basic cross-cut semantics only requires offered
freedom, not novelty of that freedom.
-/
def NewlyFrees
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State) : Prop :=
  ¬ turn.before.available turn.escape

/-- If the escape was previously blocked, the cross-cut is a strict affordance transfer. -/
theorem newly_frees_effect
    {Fact : Type u} {State : Type v}
    (turn : CrossCutTurn Fact State)
    (fresh : NewlyFrees turn) :
    (turn.before.available turn.cut ∧ ¬ turn.after.available turn.cut) ∧
    (¬ turn.before.available turn.escape ∧ turn.after.available turn.escape) := by
  exact ⟨⟨turn.cut_was_available, turn.restricts_cut⟩, ⟨fresh, turn.offers_escape⟩⟩

end CrossCutTurn

/-! ## V4 forced-escape specialization -/

/--
A V4 cross-cut whose escape state is determined by one fixed reference, the
state being cut, and the distinct upward state carrying the move.
-/
structure ForcedV4CrossCut (Fact : Type u) where
  turn : CrossCutTurn Fact V4
  reference : V4
  mover : V4
  cut_upward : UpwardFrom reference turn.cut
  mover_upward : UpwardFrom reference mover
  mover_ne_cut : mover ≠ turn.cut
  escape_forced : turn.escape = forcedThirdFrom reference turn.cut mover

namespace ForcedV4CrossCut

/-- The forced escape remains a non-reference/upward state. -/
theorem escape_upward
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact) :
    UpwardFrom crosscut.reference crosscut.turn.escape := by
  rw [crosscut.escape_forced]
  exact forcedThird_ne_reference
    crosscut.reference crosscut.turn.cut crosscut.mover
    crosscut.cut_upward crosscut.mover_upward crosscut.mover_ne_cut.symm

/-- The forced escape is not the state being cut. -/
theorem escape_ne_cut
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact) :
    crosscut.turn.escape ≠ crosscut.turn.cut := by
  rw [crosscut.escape_forced]
  exact forcedThird_ne_left
    crosscut.reference crosscut.turn.cut crosscut.mover
    crosscut.cut_upward crosscut.mover_upward crosscut.mover_ne_cut.symm

/-- The forced escape is not the upward state carrying the move. -/
theorem escape_ne_mover
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact) :
    crosscut.turn.escape ≠ crosscut.mover := by
  rw [crosscut.escape_forced]
  exact forcedThird_ne_right
    crosscut.reference crosscut.turn.cut crosscut.mover
    crosscut.cut_upward crosscut.mover_upward crosscut.mover_ne_cut.symm

/--
The operational effect specialized to V4: the cut opportunity is removed while
the uniquely forced third state is available on the successor surface.
-/
theorem restricts_cut_and_frees_forced_third
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact) :
    ¬ crosscut.turn.after.available crosscut.turn.cut ∧
    crosscut.turn.after.available
      (forcedThirdFrom crosscut.reference crosscut.turn.cut crosscut.mover) := by
  constructor
  · exact crosscut.turn.restricts_cut
  · rw [← crosscut.escape_forced]
    exact crosscut.turn.offers_escape

/-- Canonical A=0, B=a, C=b specialization: the forced escape state is D=c. -/
theorem canonical_B_cut_C_move_escapes_to_D
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact)
    (reference_is_A : crosscut.reference = V4.zero)
    (cut_is_B : crosscut.turn.cut = V4.a)
    (mover_is_C : crosscut.mover = V4.b) :
    crosscut.turn.escape = V4.c := by
  rw [crosscut.escape_forced, reference_is_A, cut_is_B, mover_is_C]
  rfl

/-- Canonically, a B-cut/C-move cross-cut restricts B. -/
theorem canonical_B_is_restricted
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact)
    (cut_is_B : crosscut.turn.cut = V4.a) :
    ¬ crosscut.turn.after.available V4.a := by
  rw [← cut_is_B]
  exact crosscut.turn.restricts_cut

/-- Canonically, that same cross-cut offers freedom to D. -/
theorem canonical_D_is_free
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact)
    (reference_is_A : crosscut.reference = V4.zero)
    (cut_is_B : crosscut.turn.cut = V4.a)
    (mover_is_C : crosscut.mover = V4.b) :
    crosscut.turn.after.available V4.c := by
  have escape_is_D := canonical_B_cut_C_move_escapes_to_D
    crosscut reference_is_A cut_is_B mover_is_C
  rw [← escape_is_D]
  exact crosscut.turn.offers_escape

/--
Canonical operational cross-cut law: B is restricted and D is free after a
C-carried cross-cut move relative to A.
-/
theorem canonical_crosscut_restricts_B_and_frees_D
    {Fact : Type u}
    (crosscut : ForcedV4CrossCut Fact)
    (reference_is_A : crosscut.reference = V4.zero)
    (cut_is_B : crosscut.turn.cut = V4.a)
    (mover_is_C : crosscut.mover = V4.b) :
    (¬ crosscut.turn.after.available V4.a) ∧
    crosscut.turn.after.available V4.c := by
  exact ⟨
    canonical_B_is_restricted crosscut cut_is_B,
    canonical_D_is_free crosscut reference_is_A cut_is_B mover_is_C
  ⟩

end ForcedV4CrossCut

end MeTTafy.FourColor

import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

The algebraic half of the red-team C2 crosscut sketch.

FRAME CONTRACT
--------------
One palette state is fixed as a lower/reference state.  The other three states
are the only possible nontrivial relative states above that reference.  If two
distinct upward states are brought into one typed crosscut interaction, their
pair determines the unique third upward state.

This file proves only that V4 forcing law.  It does not prove that planar
geometry actually forces a crossing, nor does it replace the still-open
`crosscut_meets_opposite` premise in `C2ContactVoid.lean`.
-/

namespace MeTTafy.FourColor

/-- A nontrivial state relative to one fixed lower/reference palette state. -/
def UpwardFrom (reference state : V4) : Prop := state ≠ reference

/--
The state forced by a fixed reference and two interacting upward states.

In characteristic two this is `reference + left + right`.  After gauging the
reference to `zero`, it becomes the familiar `left + right`.
-/
def forcedThirdFrom (reference left right : V4) : V4 :=
  add reference (add left right)

/-- Gauging the reference to zero recovers the simple `left + right` rule. -/
theorem forcedThirdFrom_zero (left right : V4) :
    forcedThirdFrom .zero left right = add left right := by
  rfl

/-- The forced state is not the fixed lower/reference state. -/
theorem forcedThird_ne_reference
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    forcedThirdFrom reference left right ≠ reference := by
  cases reference <;> cases left <;> cases right <;>
    simp_all [UpwardFrom, forcedThirdFrom, add]

/-- The forced state is different from the first interacting upward state. -/
theorem forcedThird_ne_left
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    forcedThirdFrom reference left right ≠ left := by
  cases reference <;> cases left <;> cases right <;>
    simp_all [UpwardFrom, forcedThirdFrom, add]

/-- The forced state is different from the second interacting upward state. -/
theorem forcedThird_ne_right
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    forcedThirdFrom reference left right ≠ right := by
  cases reference <;> cases left <;> cases right <;>
    simp_all [UpwardFrom, forcedThirdFrom, add]

/--
There is exactly one palette state left after fixing the lower/reference state
and two distinct upward states: `reference + left + right`.
-/
theorem forcedThird_unique
    (reference left right candidate : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right)
    (candidate_ne_reference : candidate ≠ reference)
    (candidate_ne_left : candidate ≠ left)
    (candidate_ne_right : candidate ≠ right) :
    candidate = forcedThirdFrom reference left right := by
  cases reference <;> cases left <;> cases right <;> cases candidate <;>
    simp_all [UpwardFrom, forcedThirdFrom, add]

/--
Packaged forcing law without hiding the witness behind chooser language: the
forced state exists, has all three required distinctions, and every state with
those distinctions is equal to it.
-/
theorem two_upward_states_force_unique_third
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    ∃ third,
      UpwardFrom reference third ∧
      third ≠ left ∧
      third ≠ right ∧
      ∀ candidate,
        UpwardFrom reference candidate →
        candidate ≠ left →
        candidate ≠ right →
        candidate = third := by
  refine ⟨forcedThirdFrom reference left right, ?_, ?_, ?_, ?_⟩
  · exact forcedThird_ne_reference reference left right leftUp rightUp different
  · exact forcedThird_ne_left reference left right leftUp rightUp different
  · exact forcedThird_ne_right reference left right leftUp rightUp different
  · intro candidate candidateUp candidate_ne_left candidate_ne_right
    exact forcedThird_unique reference left right candidate
      leftUp rightUp different candidateUp candidate_ne_left candidate_ne_right

/--
Canonical C2 gauge: with `A = zero`, the interaction of `B = a` and `C = b`
forces `D = c`.  The violated/remaining color is therefore not a free choice.
-/
theorem canonical_BC_interaction_forces_D :
    forcedThirdFrom V4.zero V4.a V4.b = V4.c := by
  rfl

/-- The same canonical fact stated as uniqueness among upward states. -/
theorem canonical_D_is_unique_remaining_upward :
    ∀ candidate : V4,
      candidate ≠ V4.zero →
      candidate ≠ V4.a →
      candidate ≠ V4.b →
      candidate = V4.c := by
  intro candidate candidate_ne_A candidate_ne_B candidate_ne_C
  exact forcedThird_unique V4.zero V4.a V4.b candidate
    (by simp [UpwardFrom])
    (by simp [UpwardFrom])
    (by simp)
    candidate_ne_A candidate_ne_B candidate_ne_C

end MeTTafy.FourColor

import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A deliberately small Four Color witness for observer-relative playability.

FRAME CONTRACT
--------------
The formal game may inspect the actual palette state presented at contact.
A coherent local player must be able to recover the legal color affordances of
that contact from its observation alone.

Brown remains a legitimate external occupancy observer: it distinguishes
`void` from `colored`.  But every realized palette state projects to the same
`brown` value.  This file proves that the game's color-dependent local move
opportunities therefore do not factor through Brown's observation.

This is not a claim that Brown changes or destroys the underlying distinctions.
It is exactly the opposite: the operational distinctions remain present in the
game while Brown lacks the interface required to use them coherently.
-/

namespace MeTTafy.FourColor

/-! ## Local color-contact affordances -/

/--
A candidate palette state is locally legal against one exposed contact exactly
when the two states differ.  This is the atomic Four Color contact rule, not a
chooser or a global search policy.
-/
def legalAgainst (exposed candidate : V4) : Bool :=
  if exposed = candidate then false else true

/-- The complete local move-opportunity profile induced by one exposed color. -/
structure ContactAffordance where
  allowZero : Bool
  allowA : Bool
  allowB : Bool
  allowC : Bool
  deriving DecidableEq, Repr

/-- All four candidate opportunities available at one colored contact. -/
def contactAffordances (exposed : V4) : ContactAffordance where
  allowZero := legalAgainst exposed .zero
  allowA := legalAgainst exposed .a
  allowB := legalAgainst exposed .b
  allowC := legalAgainst exposed .c

/-- A direct color observation is sufficient to recover the local affordance profile. -/
def directColorProjection (color : V4) : V4 := color

/--
A projection supports coherent local play when the exact legal affordance
profile factors through that projection.
-/
def AffordancesFactorThrough {View : Type}
    (projection : V4 → View) : Prop :=
  ∃ decode : View → ContactAffordance,
    ∀ exposed, decode (projection exposed) = contactAffordances exposed

/-- Direct color contact carries enough information to play the local rule coherently. -/
theorem direct_color_supports_coherent_play :
    AffordancesFactorThrough directColorProjection := by
  refine ⟨contactAffordances, ?_⟩
  intro exposed
  rfl

/-! ## Brown sees occupancy but loses move opportunity -/

/-- Brown distinguishes a void site from a colored site. -/
theorem brown_observes_occupancy :
    brownObserve .void ≠ brownObserve (.colored V4.zero) := by
  simp [brownObserve]

/--
The same Brown observation can hide opposite answers to a concrete move
question: candidate `a` is legal against `zero` and illegal against `a`.
-/
theorem brown_same_view_different_a_opportunity :
    brownColorProjection V4.zero = brownColorProjection V4.a ∧
    legalAgainst V4.zero V4.a = true ∧
    legalAgainst V4.a V4.a = false := by
  simp [brownColorProjection, legalAgainst]

/-- The full local affordance profiles for exposed `zero` and exposed `a` differ. -/
theorem zero_and_a_have_different_affordances :
    contactAffordances V4.zero ≠ contactAffordances V4.a := by
  intro equal
  have sameA := congrArg ContactAffordance.allowA equal
  simp [contactAffordances, legalAgainst] at sameA

/--
Brown cannot recover exact legal move opportunities from its observation alone.
Two formal states collapse to the same Brown view while requiring different
local affordance profiles.
-/
theorem brown_affordances_do_not_factor :
    ¬ AffordancesFactorThrough brownColorProjection := by
  intro factors
  rcases factors with ⟨decode, commutes⟩
  have zeroProfile := commutes V4.zero
  have aProfile := commutes V4.a
  apply zero_and_a_have_different_affordances
  calc
    contactAffordances V4.zero = decode (brownColorProjection V4.zero) := zeroProfile.symm
    _ = decode (brownColorProjection V4.a) := by rfl
    _ = contactAffordances V4.a := aProfile

/--
Operational statement of the Brown-observer limitation: Brown is an occupancy
observer but not a sufficient interface for coherent participation in a game
whose legal moves depend on color identity.
-/
theorem brown_cannot_coherently_play_local_contact_rule :
    ¬ AffordancesFactorThrough brownColorProjection :=
  brown_affordances_do_not_factor

end MeTTafy.FourColor

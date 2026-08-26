import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A deliberately small Four Color witness for player-relative playability.

FRAME CONTRACT
--------------
To participate in the game, a player is embedded in the realized construction
and receives local contact observations. A coherent color-relevant player must
be able to recover the legal color affordances of that contact from its own
interface.

Brown is such an embedded player: it distinguishes `void` from `colored`.
But every realized palette state appears as the same `brown` value. Brown is
therefore present in the game while functionally left behind by the distinctions
that determine color-dependent moves.

This is not a claim that Brown changes or destroys the underlying distinctions.
The distinctions remain operational for the color-capable players; Brown simply
cannot use them to alter the legal color-action surface.
-/

namespace MeTTafy.FourColor

/-! ## Local color-contact affordances -/

/--
A candidate palette state is locally legal against one exposed contact exactly
when the two states differ. This is the atomic Four Color contact rule, not a
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

/-! ## Embedded players and color relevance -/

/-- An embedded player receives an observation from each realized local site. -/
structure EmbeddedPlayer (View : Type) where
  observe : SiteState → View

/-- Brown is an embedded player with a coarse local interface. -/
def brownPlayer : EmbeddedPlayer BrownView where
  observe := brownObserve

/-- A direct color-capable player preserves the realized site state itself. -/
def directSitePlayer : EmbeddedPlayer SiteState where
  observe := id

/--
Color relevance means that a player's colored-contact interface is sufficient
to reconstruct the legal local color affordances.
-/
def ColorRelevant {View : Type} (player : EmbeddedPlayer View) : Prop :=
  AffordancesFactorThrough (fun color => player.observe (.colored color))

/-! ## Brown is present but strategically irrelevant to color play -/

/-- Brown distinguishes a void site from a colored site. -/
theorem brown_observes_occupancy :
    brownPlayer.observe .void ≠ brownPlayer.observe (.colored V4.zero) := by
  simp [brownPlayer, brownObserve]

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
Two realized color states collapse to the same Brown view while requiring
different local affordance profiles.
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

/-- Brown is embedded in the game but is not color-relevant to its local move rule. -/
theorem brown_embedded_not_color_relevant :
    ¬ ColorRelevant brownPlayer := by
  simpa [ColorRelevant, brownPlayer, brownObserve, brownColorProjection] using
    brown_affordances_do_not_factor

/--
Compatibility name retained for existing references: Brown cannot coherently
play the color-dependent contact rule from its coarse interface alone.
-/
theorem brown_cannot_coherently_play_local_contact_rule :
    ¬ AffordancesFactorThrough brownColorProjection :=
  brown_affordances_do_not_factor

end MeTTafy.FourColor

import examples.four_color.C2ForcedThird

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A bounded composition theorem for the red-team degree-five game.

FRAME CONTRACT
--------------
The proof world is still the formal global Four Color frame.  A clean carrier
turn has already been banked elsewhere as changing exactly one frontier seed
while preserving proper coloring.  This file studies only the induced
five-frontier rewrite.

The key claim is a dichotomy, not termination:

* if a one-site proper frontier rewrite still uses all four palette states, the
  successor is again the same hard degree-five / A-B-A red-team species;
* otherwise the color formerly occupying the changed site has disappeared from
  the frontier, so the deleted focus has a concrete color opportunity.

Thus a blocked successor composes back into the same red-team normal form.  No
ledger monotonicity, no non-replay theorem, and no global Four Color closure are
claimed here.
-/

namespace MeTTafy.FourColor

/-- The five concrete positions of the degree-five frontier. -/
inductive BoundarySlot where
  | s0
  | s1
  | s2
  | s3
  | s4
  deriving DecidableEq, Repr

/-- Read one concrete frontier position. -/
def boundaryAt (boundary : Boundary5) : BoundarySlot → V4
  | .s0 => boundary.c0
  | .s1 => boundary.c1
  | .s2 => boundary.c2
  | .s3 => boundary.c3
  | .s4 => boundary.c4

/-- Replace exactly one concrete frontier position. -/
def replaceBoundary
    (boundary : Boundary5)
    (slot : BoundarySlot)
    (replacement : V4) : Boundary5 :=
  match slot with
  | .s0 => ⟨replacement, boundary.c1, boundary.c2, boundary.c3, boundary.c4⟩
  | .s1 => ⟨boundary.c0, replacement, boundary.c2, boundary.c3, boundary.c4⟩
  | .s2 => ⟨boundary.c0, boundary.c1, replacement, boundary.c3, boundary.c4⟩
  | .s3 => ⟨boundary.c0, boundary.c1, boundary.c2, replacement, boundary.c4⟩
  | .s4 => ⟨boundary.c0, boundary.c1, boundary.c2, boundary.c3, replacement⟩

/--
The frontier-level image of a supplied clean atomic turn: one site changes and
all other frontier sites are retained.
-/
structure OneSiteBoundaryTurn (before : Boundary5) where
  slot : BoundarySlot
  replacement : V4
  changed : replacement ≠ boundaryAt before slot

namespace OneSiteBoundaryTurn

/-- The realized successor frontier of one declared one-site turn. -/
def after {before : Boundary5} (turn : OneSiteBoundaryTurn before) : Boundary5 :=
  replaceBoundary before turn.slot turn.replacement

end OneSiteBoundaryTurn

/-- A focus color opportunity exists exactly when some palette state is absent from the frontier. -/
def HasFocusOpportunity (boundary : Boundary5) : Prop :=
  ∃ color : V4, ¬ BoundaryContains boundary color

/--
The red-team normal form used by the C2 construction lane: a proper degree-five
hard frontier together with its mechanically implied A-B-A window.
-/
def RedTeamNormalForm (boundary : Boundary5) : Prop :=
  HardDegreeFiveFrontier boundary ∧ HasABAWindow boundary

/-- Every hard degree-five frontier canonically re-enters the red-team normal form. -/
theorem hard_frontier_is_redTeam
    (boundary : Boundary5)
    (hard : HardDegreeFiveFrontier boundary) :
    RedTeamNormalForm boundary :=
  ⟨hard, hard_degree_five_has_ABA_window boundary hard⟩

/-- A hard frontier has no focus opportunity: all four palette states occur. -/
theorem hard_frontier_has_no_focus_opportunity
    (boundary : Boundary5)
    (hard : HardDegreeFiveFrontier boundary) :
    ¬ HasFocusOpportunity boundary := by
  intro opportunity
  rcases opportunity with ⟨color, absent⟩
  exact absent (usesAllFour_contains boundary color hard.2)

/--
Changing one slot cannot erase a different color that was already present.
This is the small structural fact behind the composition dichotomy.
-/
theorem replaceBoundary_preserves_other_color
    (before : Boundary5)
    (slot : BoundarySlot)
    (replacement color : V4)
    (present : BoundaryContains before color)
    (notOld : color ≠ boundaryAt before slot) :
    BoundaryContains (replaceBoundary before slot replacement) color := by
  have oldNe : boundaryAt before slot ≠ color := Ne.symm notOld
  rcases before with ⟨c0, c1, c2, c3, c4⟩
  cases slot <;>
    simp_all [BoundaryContains, boundaryAt, replaceBoundary]

/--
One-site composition dichotomy.

Start from the hard 2,1,1,1 frontier, change exactly one site, and require the
realized successor frontier to remain proper.  Then either all four colors still
occur, so the successor is another hard frontier, or the old seed color is now
absent.  The latter is exactly a newly exposed focus opportunity.
-/
theorem one_site_hard_turn_reenters_or_frees_seed
    (before : Boundary5)
    (hard : HardDegreeFiveFrontier before)
    (turn : OneSiteBoundaryTurn before)
    (properAfter : ProperPentagon turn.after) :
    HardDegreeFiveFrontier turn.after ∨
      ¬ BoundaryContains turn.after (boundaryAt before turn.slot) := by
  let old := boundaryAt before turn.slot
  by_cases oldPresent : BoundaryContains turn.after old
  · left
    refine ⟨properAfter, ?_⟩
    have containsAfter : ∀ color : V4, BoundaryContains turn.after color := by
      intro color
      by_cases sameOld : color = old
      · simpa [sameOld] using oldPresent
      · have presentBefore : BoundaryContains before color :=
          usesAllFour_contains before color hard.2
        simpa [OneSiteBoundaryTurn.after] using
          (replaceBoundary_preserves_other_color before turn.slot turn.replacement color
            presentBefore sameOld)
    exact ⟨containsAfter .zero, containsAfter .a, containsAfter .b, containsAfter .c⟩
  · right
    exact oldPresent

/--
A red-team turn either composes into the same red-team species or opens a color
for the focus.  This is the reusable one-step induction interface.
-/
theorem redTeam_turn_composes_or_opens
    (before : Boundary5)
    (normal : RedTeamNormalForm before)
    (turn : OneSiteBoundaryTurn before)
    (properAfter : ProperPentagon turn.after) :
    RedTeamNormalForm turn.after ∨ HasFocusOpportunity turn.after := by
  rcases one_site_hard_turn_reenters_or_frees_seed before normal.1 turn properAfter with
    hardAfter | freed
  · exact Or.inl (hard_frontier_is_redTeam turn.after hardAfter)
  · exact Or.inr ⟨boundaryAt before turn.slot, freed⟩

/--
If the successor remains blocked (no color opportunity), the turn necessarily
re-enters the same red-team normal form.  This is the literal closure-under-turn
statement needed for repeated composition.
-/
theorem blocked_redTeam_turn_reenters
    (before : Boundary5)
    (normal : RedTeamNormalForm before)
    (turn : OneSiteBoundaryTurn before)
    (properAfter : ProperPentagon turn.after)
    (stillBlocked : ¬ HasFocusOpportunity turn.after) :
    RedTeamNormalForm turn.after := by
  rcases redTeam_turn_composes_or_opens before normal turn properAfter with
    normalAfter | opportunity
  · exact normalAfter
  · exact False.elim (stillBlocked opportunity)

end MeTTafy.FourColor

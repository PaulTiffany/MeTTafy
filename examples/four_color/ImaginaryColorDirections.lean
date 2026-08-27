import examples.four_color.FourColorCore

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Algebraic imaginary-color directions for the independent Four Color research lane.

The realized palette is V4 = Z2 x Z2.  Relative to any fixed anchor coloration,
there are exactly three non-identity color differences.  This file formalizes
that fact without introducing construction authority or geometric assumptions.

The intended reading is inference-only:

  anchor coloration
    -> choose one nonzero V4 difference
    -> imagine the corresponding alternative coloration

Arbitrarily long sequential imagination may compose these differences, but it
cannot create a fourth non-identity algebraic direction.
-/

namespace MeTTafy.FourColor

/-- An irreducible imaginary color direction is exactly a nonzero V4 element. -/
abbrev ImaginaryDirection := { direction : V4 // direction ≠ V4.zero }

namespace ImaginaryDirection

/-- Forget the nonzero witness and expose the underlying V4 difference. -/
def toV4 (direction : ImaginaryDirection) : V4 := direction.1

/-- The three concrete nonzero V4 directions. -/
def dirA : ImaginaryDirection := ⟨V4.a, by decide⟩
def dirB : ImaginaryDirection := ⟨V4.b, by decide⟩
def dirC : ImaginaryDirection := ⟨V4.c, by decide⟩

/-- Explicit finite cover of the non-identity direction space. -/
def all : List ImaginaryDirection := [dirA, dirB, dirC]

@[simp] theorem all_length : all.length = 3 := rfl

/-- Every nonzero V4 direction is one of the three explicit directions. -/
theorem mem_all (direction : ImaginaryDirection) : direction ∈ all := by
  rcases direction with ⟨value, nonzero⟩
  cases value with
  | zero => exact False.elim (nonzero rfl)
  | a => simp [all, dirA, dirB, dirC]
  | b => simp [all, dirA, dirB, dirC]
  | c => simp [all, dirA, dirB, dirC]

/-- Equality of directions is exactly equality of their underlying V4 values. -/
theorem ext {left right : ImaginaryDirection}
    (equal : toV4 left = toV4 right) : left = right := by
  apply Subtype.ext
  exact equal

end ImaginaryDirection

/-- Apply one imaginary relative-color direction to an anchor coloration. -/
def imaginedColor (anchor : V4) (direction : ImaginaryDirection) : V4 :=
  add anchor direction.1

/-- Adding the anchor to its own difference recovers the imagined coloration. -/
theorem add_difference_left (anchor imagined : V4) :
    add anchor (difference anchor imagined) = imagined := by
  calc
    add anchor (difference anchor imagined) = add anchor (add anchor imagined) := rfl
    _ = add (add anchor anchor) imagined := (add_assoc anchor anchor imagined).symm
    _ = add V4.zero imagined := by rw [add_self]
    _ = imagined := zero_add imagined

/-- Taking the anchor difference after applying a direction recovers that direction. -/
theorem difference_add_left_cancel (anchor delta : V4) :
    difference anchor (add anchor delta) = delta := by
  calc
    difference anchor (add anchor delta) = add anchor (add anchor delta) := rfl
    _ = add (add anchor anchor) delta := (add_assoc anchor anchor delta).symm
    _ = add V4.zero delta := by rw [add_self]
    _ = delta := zero_add delta

/-- Repeating one characteristic-two direction cancels around any suffix. -/
theorem add_left_self_cancel (direction suffix : V4) :
    add direction (add direction suffix) = suffix := by
  calc
    add direction (add direction suffix) = add (add direction direction) suffix :=
      (add_assoc direction direction suffix).symm
    _ = add V4.zero suffix := by rw [add_self]
    _ = suffix := zero_add suffix

/-- Any nonzero imaginary direction changes the anchor coloration. -/
theorem imaginedColor_ne_anchor
    (anchor : V4) (direction : ImaginaryDirection) :
    imaginedColor anchor direction ≠ anchor := by
  intro equal
  have collapsed : direction.1 = V4.zero := by
    calc
      direction.1 = difference anchor (imaginedColor anchor direction) :=
        (difference_add_left_cancel anchor direction.1).symm
      _ = difference anchor anchor := congrArg (difference anchor) equal
      _ = V4.zero := by
        simp [difference, add_self]
  exact direction.2 collapsed

/--
Relative to one anchor, every distinct coloration has a unique nonzero V4
imaginary direction.  This is the exact algebraic form of "three alternatives".
-/
theorem distinct_imagined_color_has_unique_direction
    (anchor imagined : V4)
    (different : imagined ≠ anchor) :
    ∃! direction : ImaginaryDirection,
      imagined = imaginedColor anchor direction := by
  have anchorDifferent : anchor ≠ imagined := by
    intro equal
    exact different equal.symm
  have nonzeroDifference : difference anchor imagined ≠ V4.zero :=
    (difference_nonzero_iff_ne anchor imagined).2 anchorDifferent
  let witness : ImaginaryDirection :=
    ⟨difference anchor imagined, nonzeroDifference⟩
  refine ⟨witness, ?_, ?_⟩
  · exact (add_difference_left anchor imagined).symm
  · intro other otherEq
    apply Subtype.ext
    have recovered : difference anchor imagined = other.1 := by
      calc
        difference anchor imagined =
            difference anchor (imaginedColor anchor other) :=
          congrArg (difference anchor) otherEq
        _ = other.1 := difference_add_left_cancel anchor other.1
    exact recovered.symm

/-- The three explicit imagined alternatives relative to one anchor. -/
def imaginaryAlternatives (anchor : V4) : List V4 :=
  ImaginaryDirection.all.map (imaginedColor anchor)

@[simp] theorem imaginaryAlternatives_length (anchor : V4) :
    (imaginaryAlternatives anchor).length = 3 := by
  simp [imaginaryAlternatives, ImaginaryDirection.all]

/-- The explicit three alternatives are exactly the palette states unequal to the anchor. -/
theorem mem_imaginaryAlternatives_iff
    (anchor color : V4) :
    color ∈ imaginaryAlternatives anchor ↔ color ≠ anchor := by
  constructor
  · intro member equal
    rcases List.mem_map.mp member with ⟨direction, _, directionEq⟩
    exact imaginedColor_ne_anchor anchor direction (directionEq.trans equal)
  · intro different
    rcases distinct_imagined_color_has_unique_direction anchor color different with
      ⟨direction, directionEq, _⟩
    exact List.mem_map.mpr
      ⟨direction, ImaginaryDirection.mem_all direction, directionEq.symm⟩

/-- Compose a sequential imaginary direction word to its net V4 difference. -/
def netDirection : List ImaginaryDirection → V4
  | [] => V4.zero
  | direction :: rest => add direction.1 (netDirection rest)

/-- Net direction distributes over concatenation. -/
theorem netDirection_append
    (left right : List ImaginaryDirection) :
    netDirection (left ++ right) =
      add (netDirection left) (netDirection right) := by
  induction left with
  | nil => simp [netDirection, zero_add]
  | cons head tail ih =>
      simp [netDirection, ih, add_assoc]

/-- A repeated imaginary direction is algebraically trivial. -/
theorem repeated_direction_cancels (direction : ImaginaryDirection) :
    netDirection [direction, direction] = V4.zero := by
  simp [netDirection, add_zero, add_self]

/-- Fuse two distinct directions into their unique third nonzero V4 direction. -/
def fuseDirection
    (left right : ImaginaryDirection)
    (different : left ≠ right) : ImaginaryDirection := by
  have valuesDifferent : left.1 ≠ right.1 := by
    intro equal
    exact different (Subtype.ext equal)
  have nonzero : add left.1 right.1 ≠ V4.zero := by
    simpa [difference] using
      (difference_nonzero_iff_ne left.1 right.1).2 valuesDifferent
  exact ⟨add left.1 right.1, nonzero⟩

/-- Distinct nonzero V4 directions compose to one unique nonzero third direction. -/
theorem distinct_directions_have_unique_third
    (left right : ImaginaryDirection)
    (different : left ≠ right) :
    ∃! third : ImaginaryDirection,
      add left.1 right.1 = third.1 := by
  refine ⟨fuseDirection left right different, rfl, ?_⟩
  intro other equal
  apply Subtype.ext
  exact equal.symm

/--
Arbitrarily deep sequential four-color imagination has only four algebraic net
outcomes: identity, or one of the three nonzero imaginary directions.
-/
theorem imaginary_word_has_small_algebraic_normal_form
    (word : List ImaginaryDirection) :
    netDirection word = V4.zero ∨
      ∃! direction : ImaginaryDirection,
        netDirection word = direction.1 := by
  by_cases zeroPhase : netDirection word = V4.zero
  · exact Or.inl zeroPhase
  · refine Or.inr ⟨⟨netDirection word, zeroPhase⟩, rfl, ?_⟩
    intro other equal
    apply Subtype.ext
    exact equal.symm

end MeTTafy.FourColor

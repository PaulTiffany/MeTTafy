import Lean.Elab.Tactic.Omega
import examples.four_color.ImaginaryColorDirections
import examples.four_color.ReidemeisterStaging

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Color-level Reidemeister uncrossing for Four Color imagination.

This file does not identify a map coloring with a literal knot.  It isolates the
algebraic correspondence suggested by Reidemeister staging:

* a serialized imaginary color word is a projected presentation;
* its net V4 difference is the color phase;
* repeated equal directions cancel locally;
* two distinct directions fuse to their unique third direction;
* both rewrites preserve color phase while shortening the presentation.

All objects remain INFERENCE-only.  No theorem here produces a
CertifiedInstantiation or changes a RealizedMap.
-/

namespace MeTTafy.FourColor

/-- A serialized same-turn sequence of nonzero imaginary color directions. -/
abbrev ColorWord := List ImaginaryDirection

/-- The algebraic phase retained after forgetting the projected word presentation. -/
def colorPhase (word : ColorWord) : V4 := netDirection word

/--
One local color-uncrossing rewrite.  `cancel` is the characteristic-two trivial
uncrossing `[d,d] -> []`.  `fuse` replaces two distinct adjacent directions by
their unique nonzero V4 sum.
-/
inductive ColorUncrossingStep : ColorWord → ColorWord → Prop where
  | cancel
      (pre suffix : ColorWord)
      (direction : ImaginaryDirection) :
      ColorUncrossingStep
        (pre ++ (direction :: direction :: suffix))
        (pre ++ suffix)
  | fuse
      (pre suffix : ColorWord)
      (left right : ImaginaryDirection)
      (different : left ≠ right) :
      ColorUncrossingStep
        (pre ++ (left :: right :: suffix))
        (pre ++ (fuseDirection left right different :: suffix))

/-- Reflexive/transitive closure of local same-turn color uncrossings. -/
inductive ColorUncrossingClosure : ColorWord → ColorWord → Prop where
  | refl (word : ColorWord) : ColorUncrossingClosure word word
  | step {before middle after : ColorWord} :
      ColorUncrossingStep before middle →
      ColorUncrossingClosure middle after →
      ColorUncrossingClosure before after

/-- Every local uncrossing preserves the net V4 color phase. -/
theorem ColorUncrossingStep.preserves_phase
    {before after : ColorWord}
    (step : ColorUncrossingStep before after) :
    colorPhase before = colorPhase after := by
  cases step with
  | cancel pre suffix direction =>
      simp [colorPhase, netDirection_append, netDirection,
        add_left_self_cancel]
  | fuse pre suffix left right different =>
      simp [colorPhase, netDirection_append, netDirection,
        fuseDirection, add_assoc]

/-- Phase preservation composes through any finite uncrossing pass. -/
theorem ColorUncrossingClosure.preserves_phase
    {before after : ColorWord}
    (path : ColorUncrossingClosure before after) :
    colorPhase before = colorPhase after := by
  induction path with
  | refl => rfl
  | step head tail ih =>
      exact Eq.trans head.preserves_phase ih

/-- Every local uncrossing strictly shortens the serialized imaginary word. -/
theorem ColorUncrossingStep.decreases_length
    {before after : ColorWord}
    (step : ColorUncrossingStep before after) :
    after.length < before.length := by
  cases step <;> simp <;> omega

/-- A color phase transition means that the net V4 relation changed. -/
def RequiresColorPhaseTransition (before after : ColorWord) : Prop :=
  colorPhase before ≠ colorPhase after

/-- Reidemeister-like color uncrossing never requires a color phase transition. -/
theorem uncrossing_requires_no_color_phase_transition
    {before after : ColorWord}
    (step : ColorUncrossingStep before after) :
    ¬ RequiresColorPhaseTransition before after := by
  intro changed
  exact changed step.preserves_phase

/-- The smallest explicit trivial projected crossing for one direction. -/
def trivialColorCrossing (direction : ImaginaryDirection) : ColorWord :=
  [direction, direction]

/-- The trivial projected crossing has identity color phase. -/
theorem trivialColorCrossing_phase_zero (direction : ImaginaryDirection) :
    colorPhase (trivialColorCrossing direction) = V4.zero := by
  exact repeated_direction_cancels direction

/-- One local cancellation unknots the trivial color crossing. -/
theorem trivialColorCrossing_uncrosses (direction : ImaginaryDirection) :
    ColorUncrossingStep (trivialColorCrossing direction) [] := by
  simpa [trivialColorCrossing] using
    (ColorUncrossingStep.cancel ([] : ColorWord) ([] : ColorWord) direction)

/-- The trivial crossing is a one-step, zero-phase-transition uncrossing. -/
theorem trivialColorCrossing_uncrosses_without_phase_transition
    (direction : ImaginaryDirection) :
    colorPhase (trivialColorCrossing direction) = colorPhase [] ∧
      ColorUncrossingStep (trivialColorCrossing direction) [] := by
  constructor
  · simp [trivialColorCrossing, colorPhase, netDirection, add_zero, add_self]
  · exact trivialColorCrossing_uncrosses direction

/--
Semantic normal form of a color word: identity if the net phase is zero,
otherwise the unique singleton nonzero direction carrying that phase.
-/
def colorNormalForm (word : ColorWord) : ColorWord :=
  if zeroPhase : colorPhase word = V4.zero then
    []
  else
    [⟨colorPhase word, zeroPhase⟩]

/-- A semantic color normal form contains at most one irreducible direction. -/
theorem colorNormalForm_length_le_one (word : ColorWord) :
    (colorNormalForm word).length ≤ 1 := by
  unfold colorNormalForm
  split <;> simp

/-- Semantic normalization preserves exactly the net V4 color phase. -/
theorem colorNormalForm_preserves_phase (word : ColorWord) :
    colorPhase word = colorPhase (colorNormalForm word) := by
  unfold colorNormalForm
  split
  · simp_all [colorPhase, netDirection]
  · simp [colorPhase, netDirection, add_zero]

/-- The semantic normal form is either identity or one singleton direction. -/
theorem colorNormalForm_shape (word : ColorWord) :
    colorNormalForm word = [] ∨
      ∃ direction : ImaginaryDirection,
        colorNormalForm word = [direction] := by
  unfold colorNormalForm
  split
  · exact Or.inl rfl
  · exact Or.inr ⟨_, rfl⟩

/--
Constructive local normalization: every serialized imaginary color word can be
uncrossed, by repeated local cancellation/fusion, to a word of length at most one.
-/
theorem every_color_word_uncrosses_to_small_normal_form :
    ∀ word : ColorWord,
      ∃ normal : ColorWord,
        ColorUncrossingClosure word normal ∧ normal.length ≤ 1
  | [] => ⟨[], ColorUncrossingClosure.refl [], by simp⟩
  | [direction] =>
      ⟨[direction], ColorUncrossingClosure.refl [direction], by simp⟩
  | left :: right :: rest => by
      by_cases same : left = right
      · subst right
        rcases every_color_word_uncrosses_to_small_normal_form rest with
          ⟨normal, path, small⟩
        refine ⟨normal, ColorUncrossingClosure.step ?_ path, small⟩
        simpa using
          (ColorUncrossingStep.cancel ([] : ColorWord) rest left)
      · let fused := fuseDirection left right same
        rcases every_color_word_uncrosses_to_small_normal_form (fused :: rest) with
          ⟨normal, path, small⟩
        refine ⟨normal, ColorUncrossingClosure.step ?_ path, small⟩
        simpa [fused] using
          (ColorUncrossingStep.fuse ([] : ColorWord) rest left right same)
termination_by word => word.length
decreasing_by all_goals simp_all <;> omega

/--
The local normalizer reaches a small presentation without changing the retained
color phase.  Long imagination therefore contributes presentation length, not new
algebraic phase classes.
-/
theorem every_color_word_uncrosses_without_phase_transition
    (word : ColorWord) :
    ∃ normal : ColorWord,
      ColorUncrossingClosure word normal ∧
      normal.length ≤ 1 ∧
      colorPhase word = colorPhase normal := by
  rcases every_color_word_uncrosses_to_small_normal_form word with
    ⟨normal, path, small⟩
  exact ⟨normal, path, small, path.preserves_phase⟩

/-- One trivial color crossing contributes one R2-like cancellation witness. -/
def trivialColorCrossingComplexity : ReidemeisterComplexityWitness where
  r1Loops := 0
  r2Cancellations := 1
  r3Reorders := 0
  periodicFolds := 0

@[simp] theorem trivialColorCrossingComplexity_total :
    trivialColorCrossingComplexity.total = 1 := rfl

/-!
The correspondence proved here is deliberately algebraic and local:

  projected imaginary word --uncross--> shorter word
  colorPhase                  =           colorPhase

A later geometric theorem may identify which StrategyTangle crossings project to
these color-word rewrites.  That correspondence is not assumed here.
-/

end MeTTafy.FourColor

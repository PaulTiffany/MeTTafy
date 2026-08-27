import examples.four_color.ColorReidemeisterUncrossing
import examples.four_color.ReidemeisterStaging

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

One-way StrategyTangle -> ColorWord projection for the Four Color imagination lane.

This file formalizes the shared-world-model bridge conservatively:

* an introduced role projects to its relative V4 difference from the anchor;
* an oriented geometric crossing projects to the V4 difference of its two roles;
* crossing orientation is forgotten at the color-algebra layer;
* extend/return/probe/periodic operations explicitly stutter;
* opposite-sign crossings of the same two distinct roles project to [d,d] and
  therefore simulate the phase-preserving color uncrossing already proved in
  ColorReidemeisterUncrossing.lean.

The correspondence is one-way.  Nothing here says every color uncrossing has a
geometric StrategyTangle realization, and nothing here grants construction authority.
-/

namespace MeTTafy.FourColor

/-- The nonzero V4 direction witnessed by two distinct roles. -/
def directionOfDistinct
    (left right : V4)
    (different : left ≠ right) : ImaginaryDirection :=
  ⟨difference left right, (difference_nonzero_iff_ne left right).2 different⟩

/--
Project a role pair to zero or one color direction. Equal roles are identity and
therefore stutter; distinct roles emit their grounded V4 difference.
-/
def projectPair (left right : V4) : ColorWord :=
  if different : left ≠ right then
    [directionOfDistinct left right different]
  else
    []

@[simp] theorem projectPair_self (role : V4) : projectPair role role = [] := by
  simp [projectPair]

/-- Every emitted pair direction is grounded in one actual nonzero V4 difference. -/
theorem mem_projectPair_grounded
    {left right : V4}
    {direction : ImaginaryDirection}
    (member : direction ∈ projectPair left right) :
    left ≠ right ∧ direction.1 = difference left right := by
  unfold projectPair at member
  split at member
  case isTrue different =>
    have equalDirection : direction = directionOfDistinct left right different := by
      simpa using member
    subst direction
    exact ⟨different, rfl⟩
  case isFalse same =>
    simp at member

/-- Primitive operations that are intentionally silent at the color-word layer. -/
inductive ProjectionStutterOp : StrategyPrimitiveOp → Prop where
  | extend (role : V4) : ProjectionStutterOp (.extend role)
  | returnTo (role : V4) : ProjectionStutterOp (.returnTo role)
  | periodic (roles : List V4) : ProjectionStutterOp (.periodic roles)
  | probe (roles : List V4) : ProjectionStutterOp (.probe roles)

/-- One-way projection of an Unweaved Strategy primitive into color algebra. -/
def projectPrimitive (anchor : V4) : StrategyPrimitiveOp → ColorWord
  | .introduce role => projectPair anchor role
  | .cross left right _ => projectPair left right
  | .extend _ => []
  | .returnTo _ => []
  | .periodic _ => []
  | .probe _ => []

/-- Explicit stuttering theorem: these operations change presentation, not color word. -/
theorem projectionStutterOp_projects_empty
    (anchor : V4)
    {op : StrategyPrimitiveOp}
    (stutter : ProjectionStutterOp op) :
    projectPrimitive anchor op = [] := by
  cases stutter <;> rfl

/-- Crossing sign belongs to geometry and is deliberately forgotten by color projection. -/
theorem cross_orientation_projects_same
    (anchor left right : V4) :
    projectPrimitive anchor (.cross left right true) =
      projectPrimitive anchor (.cross left right false) := rfl

/-- Serialize the projected color contribution of one same-turn Strategy trace. -/
def projectOperations
    (anchor : V4) : List (StrategyStageFrame × StrategyPrimitiveOp) → ColorWord
  | [] => []
  | (_, op) :: rest => projectPrimitive anchor op ++ projectOperations anchor rest

/-- Projection respects concatenation, so local geometric rewrites stay local in the word. -/
theorem projectOperations_append
    (anchor : V4)
    (left right : List (StrategyStageFrame × StrategyPrimitiveOp)) :
    projectOperations anchor (left ++ right) =
      projectOperations anchor left ++ projectOperations anchor right := by
  induction left with
  | nil => rfl
  | cons head tail ih =>
      simp [projectOperations, ih, List.append_assoc]

/-- The bounded one-way transducer from a StrategyTangle into a color word. -/
def projectStrategyTangle (tangle : StrategyTangle) : ColorWord :=
  projectOperations tangle.raw.anchor tangle.raw.operations

/--
A supported geometric step may either stutter at color level or simulate one
actual local color uncrossing. This is deliberately not an equivalence relation.
-/
inductive StrategyColorSimulation : StrategyTangle → StrategyTangle → Prop where
  | stutter {before after : StrategyTangle} :
      projectStrategyTangle before = projectStrategyTangle after →
      StrategyColorSimulation before after
  | uncross {before after : StrategyTangle} :
      ColorUncrossingStep
        (projectStrategyTangle before)
        (projectStrategyTangle after) →
      StrategyColorSimulation before after

/-- Both allowed simulation modes preserve the retained V4 color phase. -/
theorem StrategyColorSimulation.preservesColorPhase
    {before after : StrategyTangle}
    (simulation : StrategyColorSimulation before after) :
    colorPhase (projectStrategyTangle before) =
      colorPhase (projectStrategyTangle after) := by
  cases simulation with
  | stutter same => exact congrArg colorPhase same
  | uncross step => exact step.preserves_phase

/-- Small geometric presentation containing one opposite-sign crossing pair. -/
def trivialStrategyCrossing
    (anchor left right : V4) : StrategyTangle :=
  {
    raw := {
      anchor := anchor
      operations := [
        (StrategyStageFrame.analysis, StrategyPrimitiveOp.cross left right true),
        (StrategyStageFrame.analysis, StrategyPrimitiveOp.cross left right false)
      ]
    }
    boundary := [left, right]
  }

/-- Same local presentation after removing the geometrically trivial crossing pair. -/
def trivialStrategyUncrossed
    (anchor left right : V4) : StrategyTangle :=
  {
    raw := {
      anchor := anchor
      operations := []
    }
    boundary := [left, right]
  }

/-- A distinct role pair projects to one explicit nonzero direction. -/
theorem projectPair_of_ne
    (left right : V4)
    (different : left ≠ right) :
    projectPair left right = [directionOfDistinct left right different] := by
  simp [projectPair, different, directionOfDistinct]

/-- Opposite geometric crossings project to the same repeated color direction. -/
theorem trivialStrategyCrossing_projects_repeated_direction
    (anchor left right : V4)
    (different : left ≠ right) :
    projectStrategyTangle (trivialStrategyCrossing anchor left right) =
      [directionOfDistinct left right different,
       directionOfDistinct left right different] := by
  simp [projectStrategyTangle, trivialStrategyCrossing, projectOperations,
    projectPrimitive, projectPair, different, directionOfDistinct]

@[simp] theorem trivialStrategyUncrossed_projects_empty
    (anchor left right : V4) :
    projectStrategyTangle (trivialStrategyUncrossed anchor left right) = [] := rfl

/--
The first geometric/color correspondence theorem: a trivial opposite-sign
Strategy crossing simulates the local `[d,d] -> []` color uncrossing.
-/
theorem trivial_strategy_crossing_simulates_color_uncrossing
    (anchor left right : V4)
    (different : left ≠ right) :
    StrategyColorSimulation
      (trivialStrategyCrossing anchor left right)
      (trivialStrategyUncrossed anchor left right) := by
  apply StrategyColorSimulation.uncross
  rw [trivialStrategyCrossing_projects_repeated_direction anchor left right different]
  rw [trivialStrategyUncrossed_projects_empty]
  exact ColorUncrossingStep.cancel
    ([] : ColorWord)
    ([] : ColorWord)
    (directionOfDistinct left right different)

/-- The geometric trivial crossing therefore uncrosses with no color phase transition. -/
theorem trivial_strategy_crossing_preserves_color_phase
    (anchor left right : V4)
    (different : left ≠ right) :
    colorPhase (projectStrategyTangle (trivialStrategyCrossing anchor left right)) =
      colorPhase (projectStrategyTangle (trivialStrategyUncrossed anchor left right)) :=
  (trivial_strategy_crossing_simulates_color_uncrossing
    anchor left right different).preservesColorPhase

/-!
The proved bridge is intentionally asymmetric:

  StrategyTangle move
      -> stutter OR ColorUncrossingStep
      -> equal retained color phase.

No theorem here turns `StrategyColorSimulation` into `CertifiedInstantiation`,
`StrategyIRComplete`, or a realized construction step.  A later theorem may bound
or compare geometric and color Reidemeister complexity, but equality is not assumed.
-/

end MeTTafy.FourColor

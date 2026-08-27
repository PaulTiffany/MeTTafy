import examples.four_color.TestTimeActiveInference

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Reidemeister staging for Four Color MapMaker imagination.

This file does NOT identify a counterfactual coloring with a literal knot and does
NOT grant construction authority to a normal form. It records only the inference
architecture needed to test the hypothesis that long roleplay traces are projected
presentations of a much smaller boundary-labelled strategy tangle.

The intended lane is:

  RoleplayTranscript
    -> RawStrategyTrace
    -> StrategyTangle
    -> interface-preserving staging
    -> StrategyNormalForm
    -> NormalFormCompleteness
    -> StrategyIRCompleteness

Everything in this file is INFERENCE-only. The existing `InferenceSound` /
`CertifiedInstantiation` boundary remains the only route into realized construction.
-/

namespace MeTTafy.FourColor

/-! ## Typed staging objects -/

inductive StrategyStageFrame where
  | reasoning
  | analysis
  | inspection
  deriving DecidableEq, Repr

/-- Lowest-level operations exposed by Unweave before any quotient is assumed. -/
inductive StrategyPrimitiveOp where
  | introduce : V4 -> StrategyPrimitiveOp
  | extend : V4 -> StrategyPrimitiveOp
  | returnTo : V4 -> StrategyPrimitiveOp
  | cross : V4 -> V4 -> Bool -> StrategyPrimitiveOp
  | periodic : List V4 -> StrategyPrimitiveOp
  | probe : List V4 -> StrategyPrimitiveOp
  deriving DecidableEq, Repr

/-- Sequential observation record. Its order is inference time, not construction time. -/
structure RawStrategyTrace where
  anchor : V4
  operations : List (StrategyStageFrame × StrategyPrimitiveOp)
  deriving DecidableEq, Repr

/-- Boundary-labelled local tangle considered while the realized map remains fixed. -/
structure StrategyTangle where
  raw : RawStrategyTrace
  boundary : List V4
  deriving DecidableEq, Repr

/--
Proof-relevant surface that staging is allowed to preserve. Coordinates and raw
trace length are deliberately absent.
-/
structure StagedStrategyInterface where
  remainingRoles : List V4
  boundary : List V4
  periodicCycles : List (List V4)
  responseClasses : List Nat
  options : List Nat
  deriving DecidableEq, Repr

abbrev StrategyInterfaceExtractor := StrategyTangle -> StagedStrategyInterface
abbrev StrategyStagingRelation := StrategyTangle -> StrategyTangle -> Prop

/-- One local R-like staging relation is sound only if it preserves the interface. -/
def StagingPreservesInterface
    (interfaceOf : StrategyInterfaceExtractor)
    (stage : StrategyStagingRelation) : Prop :=
  ∀ {before after}, stage before after -> interfaceOf before = interfaceOf after

/-- Reflexive/transitive closure of same-turn staging rewrites. -/
inductive StrategyStagingClosure
    (stage : StrategyStagingRelation) : StrategyTangle -> StrategyTangle -> Prop where
  | refl (tangle : StrategyTangle) : StrategyStagingClosure stage tangle tangle
  | step {before middle after : StrategyTangle} :
      stage before middle ->
      StrategyStagingClosure stage middle after ->
      StrategyStagingClosure stage before after

/-- Local interface preservation composes through an arbitrarily long staging pass. -/
theorem StrategyStagingClosure.preservesInterface
    {interfaceOf : StrategyInterfaceExtractor}
    {stage : StrategyStagingRelation}
    (preserves : StagingPreservesInterface interfaceOf stage)
    {before after : StrategyTangle}
    (path : StrategyStagingClosure stage before after) :
    interfaceOf before = interfaceOf after := by
  induction path with
  | refl => rfl
  | step head tail ih =>
      exact Eq.trans (preserves head) ih

/-- A normal form is simply irreducible under the chosen explicit staging relation. -/
structure StrategyNormalForm (stage : StrategyStagingRelation) where
  tangle : StrategyTangle
  irreducible : ∀ after, ¬ stage tangle after

/-- The raw tangle stages to this normal form without advancing construction. -/
def Normalizes
    (stage : StrategyStagingRelation)
    (raw : StrategyTangle)
    (normal : StrategyNormalForm stage) : Prop :=
  StrategyStagingClosure stage raw normal.tangle

/--
OPEN INFERENCE OBLIGATION: every generated strategy tangle has some irreducible
representative under the selected staging rules. No inhabitant is supplied here.
-/
def EveryStrategyTangleNormalizes (stage : StrategyStagingRelation) : Prop :=
  ∀ raw, ∃ normal : StrategyNormalForm stage, Normalizes stage raw normal

/--
OPEN INFERENCE OBLIGATION: a finite response-complete cover of normal forms exists.
This is the formal target behind the empirical "perhaps nine or ten classes"
hypothesis; no class count is encoded here.
-/
def FiniteResponseCompleteNormalForms
    (interfaceOf : StrategyInterfaceExtractor)
    (stage : StrategyStagingRelation) : Prop :=
  ∃ normals : List StrategyTangle,
    (∀ normal, normal ∈ normals -> ∀ after, ¬ stage normal after) ∧
    (∀ raw, ∃ normal,
      normal ∈ normals ∧
      StrategyStagingClosure stage raw normal ∧
      interfaceOf raw = interfaceOf normal)

/-- Measured staging work, not a construction-time ranking function. -/
structure ReidemeisterComplexityWitness where
  r1Loops : Nat
  r2Cancellations : Nat
  r3Reorders : Nat
  periodicFolds : Nat
  deriving DecidableEq, Repr

namespace ReidemeisterComplexityWitness

/-- Total number of recorded normalization operations in one inference episode. -/
def total (witness : ReidemeisterComplexityWitness) : Nat :=
  witness.r1Loops + witness.r2Cancellations +
    witness.r3Reorders + witness.periodicFolds

end ReidemeisterComplexityWitness

/-!
`FiniteResponseCompleteNormalForms` is intentionally not converted directly into
`CertifiedInstantiation`. A future completeness proof must still explain how each
response-complete normal form supplies a sound depth-zero strategy claim, thereby
establishing `StrategyIRComplete`; only the existing soundness/amortization bridge
may then affect the realized map.
-/

end MeTTafy.FourColor

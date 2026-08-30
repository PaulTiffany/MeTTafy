import examples.four_color.TestTimeActiveInference
import examples.four_color.ConstructGrammar

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Two-meta-construct closure surface for the independent Four Color research lane.

AUTHORITY CONTRACT
------------------
This file formalizes the corrected shape of the candidate argument without
promoting the missing planar theorem.

* test time is not game time;
* the current research ontology has two named local meta-construct families;
* any finite observed prefix may stop and restart without changing the map;
* void/end carries construction authority only when it contains an actual-map
  CertifiedInstantiation;
* restart consumes zero realized voids;
* void/end consumes exactly one realized void.

The non-tautological mathematical burden is named explicitly as
`PlanarTwoFamilyExhaustive`: every relevant planar continuation must actually
classify into one of the two research families. No inhabitant of that premise is
supplied here. Likewise, this file does not prove global Four Color closure.
-/

namespace MeTTafy.FourColor

universe u v

/-- The two current local research families. This is an ontology, not a theorem. -/
inductive MetaConstructFamily where
  | redTeam
  | alternatingPair
  deriving DecidableEq, Repr

/-- The declared ontology itself has exactly the two named constructors. -/
theorem metaConstructFamily_cases (family : MetaConstructFamily) :
    family = .redTeam ∨ family = .alternatingPair := by
  cases family with
  | redTeam => exact Or.inl rfl
  | alternatingPair => exact Or.inr rfl

/--
An external continuation domain and classifier. The domain remains abstract so
that the missing planar bridge cannot be confused with the two-constructor type.
-/
abbrev ContinuationClassifier (Continuation : Type v) :=
  Continuation → MetaConstructFamily → Prop

/--
OPEN PREMISE: every relevant planar continuation projects into one of the two
current meta-construct families.

This proposition is intentionally separate from `metaConstructFamily_cases`.
The latter is a trivial fact about an enum; this is the mathematical theorem the
candidate proof still has to earn.
-/
def PlanarTwoFamilyExhaustive
    {Continuation : Type v}
    (classifies : ContinuationClassifier Continuation) : Prop :=
  ∀ continuation,
    classifies continuation .redTeam ∨
      classifies continuation .alternatingPair

/--
A local test-time branch may end either by restart, which has no construction
authority, or by carrying a checked actual-map instantiation certificate.
-/
inductive LocalInferenceEnd
    {Vertex : Type u}
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  | restart
  | voidEnd (certificate : CertifiedInstantiation map focus)

/--
Interpret a local inference end at construction time. Restart returns the actual
map unchanged. Void/end realizes exactly the supplied certificate.
-/
def realizeLocalEnd
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex} :
    LocalInferenceEnd map focus → RealizedMap Vertex
  | .restart => map
  | .voidEnd certificate => instantiate certificate

/-- Restart is literally zero construction progress. -/
@[simp] theorem realizeLocalEnd_restart
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex} :
    realizeLocalEnd (LocalInferenceEnd.restart (map := map) (focus := focus)) = map := rfl

/-- Void/end is exactly one certified `void -> V4` construction event. -/
@[simp] theorem realizeLocalEnd_voidEnd
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (certificate : CertifiedInstantiation map focus) :
    realizeLocalEnd (LocalInferenceEnd.voidEnd certificate) = instantiate certificate := rfl

/-- Restart consumes no realized void. -/
theorem restart_preserves_voidCount
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex} :
    voidCount roster
        (realizeLocalEnd (LocalInferenceEnd.restart (map := map) (focus := focus))) =
      voidCount roster map := by
  rfl

/-- Void/end consumes exactly one realized void, independent of test-time length. -/
theorem voidEnd_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (certificate : CertifiedInstantiation map focus) :
    voidCount roster
        (realizeLocalEnd (LocalInferenceEnd.voidEnd certificate)) =
      voidCount roster map - 1 := by
  exact voidCount_instantiate roster certificate

/--
A finite prefix may stop by restart without any claim about whether its local
pattern is complete. This is the formal test-time/game-time separation used by
the red-team prefix argument.
-/
def stopPrefixAsRestart
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (_episode : InferenceEpisode map focus) :
    LocalInferenceEnd map focus :=
  .restart

/-- Stopping an arbitrary finite episode as restart leaves the realized map unchanged. -/
theorem stoppedPrefix_does_not_advance_construction
    {Vertex : Type u} [DecidableEq Vertex]
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (episode : InferenceEpisode map focus) :
    realizeLocalEnd (stopPrefixAsRestart episode) = map := by
  rfl

end MeTTafy.FourColor

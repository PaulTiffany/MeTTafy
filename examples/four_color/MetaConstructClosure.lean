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
* imagination is not construction history;
* theorem machinery does not impose a finite path/depth schema on imagination;
* the current research ontology has two named local meta-construct families;
* any finite observed prefix may stop and restart without changing the map;
* arbitrary imaginary structure may be compressed only through an explicit
  sound projection to an actual-map CertifiedInstantiation;
* void/end carries construction authority only when it contains that certificate;
* restart consumes zero realized voids;
* void/end consumes exactly one realized void.

The non-tautological mathematical burdens are named explicitly:

* `PlanarTwoFamilyExhaustive`: every relevant planar continuation must actually
  classify into one of the two research families;
* `ProjectionReachable`: the open imagination space contains some witness whose
  projection returns a color.

Neither premise is inhabited globally here. Likewise, this file does not prove
global Four Color closure.
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

/-! ## Open imagination, bounded authority -/

/--
An imagination box fixes only the realized authority target.

Its witness space is an arbitrary caller-supplied type. No `List`, `Fin`, path,
depth, or step budget is built into this interface. This does not make concrete
execution literally infinite; it means proof authority does not depend on first
forcing counterfactual reasoning into a bounded trajectory representation.
-/
structure ImaginationBox
    (Vertex : Type u)
    (map : RealizedMap Vertex)
    (focus : Focus Vertex) where
  Witness : Type v

/--
A projection may inspect any witness in the imagination box and either abstain
or propose one V4 color. The proposal still has no construction authority.
-/
structure ImaginaryProjection
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus) where
  project : box.Witness → Option V4

/--
Soundness is the authority wall: every projected color must already be
admissible on the unchanged realized map at the unchanged focus.
-/
def ProjectionSound
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box) : Prop :=
  ∀ witness color,
    projection.project witness = some color →
      AdmissibleAt map focus color

/--
OPEN PREMISE: some imaginary witness projects to an answer.

No search-depth bound occurs in the proposition. Finding or proving such a
witness is the research problem; declaring an arbitrary witness type does not
silently establish reachability.
-/
def ProjectionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box) : Prop :=
  ∃ witness color, projection.project witness = some color

/--
Compress one successful imaginary witness across the authority wall. The
witness itself disappears; only a V4 color plus its actual-map admissibility
proof becomes a `CertifiedInstantiation`.
-/
def compressImagination
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (witness : box.Witness)
    (color : V4)
    (hit : projection.project witness = some color) :
    CertifiedInstantiation map focus :=
  ⟨color, sound witness color hit⟩

/-- Sound reachable imagination yields an actual construction certificate. -/
theorem projectionReachable_sound_has_certificate
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (reachable : ProjectionReachable box projection) :
    Nonempty (CertifiedInstantiation map focus) := by
  rcases reachable with ⟨witness, color, hit⟩
  exact ⟨compressImagination box projection sound witness color hit⟩

/--
Whatever happened inside imagination, a successful compression realizes exactly
one void. Imaginary complexity does not become construction-time complexity.
-/
theorem compressedImagination_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (witness : box.Witness)
    (color : V4)
    (hit : projection.project witness = some color) :
    voidCount roster
        (instantiate (compressImagination box projection sound witness color hit)) =
      voidCount roster map - 1 := by
  exact voidCount_instantiate roster
    (compressImagination box projection sound witness color hit)

/-! ## Local restart / void-end authority -/

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

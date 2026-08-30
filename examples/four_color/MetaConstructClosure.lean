import examples.four_color.TestTimeActiveInference
import examples.four_color.ConstructGrammar

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Two-meta-construct closure surface for the independent Four Color research lane.

AUTHORITY CONTRACT
------------------
This file formalizes the corrected shape of the candidate argument without
promoting the remaining global completeness theorem.

* test time is not game time;
* imagination is not construction history;
* theorem machinery does not impose a finite path/depth schema on imagination;
* successful reasoning may leave a finite witnessed refinement chain without
  imposing any a-priori bound on how long imagination was allowed to search;
* the current research ontology has two named local meta-construct families;
* arbitrary imaginary structure may be compressed only through an explicit
  sound projection to an actual-map CertifiedInstantiation;
* void/end carries construction authority only when it contains that certificate;
* restart consumes zero realized voids;
* void/end consumes exactly one realized void.

The old bare `ProjectionReachable` existential is no longer treated as a
mysterious primitive. `DecisionReachable` supplies its operational content: a
finite witnessed chain of admissible "if this, then this" refinements reaches a
witness whose projection returns a color. No global chain-length bound is built
into the definition.

The planar classification obligation remains explicit as
`PlanarTwoFamilyExhaustive`. This file proves how that theorem upgrades a
continuation-generated Decision Reachability chain into the two-family relation.
The remaining global burden is therefore the existence of such a successful
admissible decision chain for every strategy-safe nonterminal realized state,
together with projection soundness. No global inhabitant is supplied here.
-/

namespace MeTTafy.FourColor

universe u v w

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
abbrev ContinuationClassifier (Continuation : Type w) :=
  Continuation → MetaConstructFamily → Prop

/--
OPEN PREMISE: every relevant planar continuation projects into one of the two
current meta-construct families.

This proposition is intentionally separate from `metaConstructFamily_cases`.
The latter is a trivial fact about an enum; this is the mathematical theorem the
candidate proof still has to earn.
-/
def PlanarTwoFamilyExhaustive
    {Continuation : Type w}
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
Extensional endpoint property: some imaginary witness projects to an answer.

This remains useful as a small interface theorem, but Decision Reachability below
now supplies its witnessed operational content.
-/
def ProjectionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box) : Prop :=
  ∃ witness color, projection.project witness = some color

/-! ## Decision Reachability: if-this-then-this refinement -/

/--
A finite witnessed admissible refinement chain with no a-priori length bound.

This is the transferable residue of an imagination episode. The search that found
the chain may have branched, restarted, revisited representations, or run for an
arbitrary amount of test time. The proof object records only one finite chain that
can be audited after the fact.
-/
inductive AdmissibleRefinementChain
    {Witness : Type v}
    (step : Witness → Witness → Prop) :
    Witness → Witness → Prop where
  | stay (state : Witness) :
      AdmissibleRefinementChain step state state
  | advance {start next finish : Witness} :
      step start next →
      AdmissibleRefinementChain step next finish →
      AdmissibleRefinementChain step start finish

namespace AdmissibleRefinementChain

/-- A refinement chain can be transported along any pointwise strengthening. -/
theorem mono
    {Witness : Type v}
    {weak strong : Witness → Witness → Prop}
    {start finish : Witness}
    (lift : ∀ {before after}, weak before after → strong before after)
    (chain : AdmissibleRefinementChain weak start finish) :
    AdmissibleRefinementChain strong start finish := by
  induction chain with
  | stay state => exact .stay state
  | advance one rest ih => exact .advance (lift one) ih

end AdmissibleRefinementChain

/--
One audited Decision Reachability witness.

`chain` is the "if this, then this" spine. `hit` says the endpoint is a deciding
state for the projection. The endpoint still has no construction authority until
`ProjectionSound` is supplied.
-/
structure DecisionWitness
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (refines : box.Witness → box.Witness → Prop) where
  endpoint : box.Witness
  color : V4
  chain : AdmissibleRefinementChain refines seed endpoint
  hit : projection.project endpoint = some color

/--
Decision Reachability is the existence of one witnessed admissible refinement
chain to a deciding endpoint. There is no fixed maximum chain length.
-/
def DecisionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (refines : box.Witness → box.Witness → Prop) : Prop :=
  Nonempty (DecisionWitness box projection seed refines)

/-- Decision Reachability entails the old bare endpoint existential. -/
theorem decisionReachable_implies_projectionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    (refines : box.Witness → box.Witness → Prop)
    (reachable : DecisionReachable box projection seed refines) :
    ProjectionReachable box projection := by
  rcases reachable with ⟨decision⟩
  exact ⟨decision.endpoint, decision.color, decision.hit⟩

/--
A continuation advance is an admissible imaginary refinement together with the
relevant planar continuation that generated it.
-/
abbrev ContinuationAdvance
    (Witness : Type v)
    (Continuation : Type w) :=
  Witness → Witness → Continuation → Prop

/-- Forget the continuation label while retaining the admissible refinement. -/
def ContinuationGeneratedStep
    {Witness : Type v}
    {Continuation : Type w}
    (advance : ContinuationAdvance Witness Continuation) :
    Witness → Witness → Prop :=
  fun before after => ∃ continuation, advance before after continuation

/--
The same generated refinement, now explicitly classified into one of the two
current meta-construct families.
-/
def TwoFamilyGeneratedStep
    {Witness : Type v}
    {Continuation : Type w}
    (advance : ContinuationAdvance Witness Continuation)
    (classifies : ContinuationClassifier Continuation) :
    Witness → Witness → Prop :=
  fun before after =>
    ∃ continuation,
      advance before after continuation ∧
        (classifies continuation .redTeam ∨
          classifies continuation .alternatingPair)

/--
Planar two-family exhaustiveness upgrades every continuation-generated step to a
two-family generated step. This is the local analogue of upgrading a merely
reachable refinement into one generated by the admissible obligation structure.
-/
theorem planarExhaustiveness_upgrades_generated_step
    {Witness : Type v}
    {Continuation : Type w}
    (advance : ContinuationAdvance Witness Continuation)
    (classifies : ContinuationClassifier Continuation)
    (exhaustive : PlanarTwoFamilyExhaustive classifies) :
    ∀ {before after},
      ContinuationGeneratedStep advance before after →
      TwoFamilyGeneratedStep advance classifies before after := by
  intro before after generated
  rcases generated with ⟨continuation, oneStep⟩
  exact ⟨continuation, oneStep, exhaustive continuation⟩

/--
Therefore a whole continuation-generated decision chain can be transported into
the two-family relation without changing its deciding endpoint.
-/
def DecisionWitness.upgradeToTwoFamilies
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    {Continuation : Type w}
    (advance : ContinuationAdvance box.Witness Continuation)
    (classifies : ContinuationClassifier Continuation)
    (exhaustive : PlanarTwoFamilyExhaustive classifies)
    (decision : DecisionWitness box projection seed
      (ContinuationGeneratedStep advance)) :
    DecisionWitness box projection seed
      (TwoFamilyGeneratedStep advance classifies) :=
  {
    endpoint := decision.endpoint
    color := decision.color
    chain := decision.chain.mono
      (planarExhaustiveness_upgrades_generated_step advance classifies exhaustive)
    hit := decision.hit
  }

/--
The two previously separate gaps now compose: a witnessed continuation-generated
decision chain plus planar two-family exhaustiveness yields a two-family Decision
Reachability witness.
-/
theorem planarExhaustive_upgrades_decisionReachable
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (seed : box.Witness)
    {Continuation : Type w}
    (advance : ContinuationAdvance box.Witness Continuation)
    (classifies : ContinuationClassifier Continuation)
    (exhaustive : PlanarTwoFamilyExhaustive classifies)
    (reachable : DecisionReachable box projection seed
      (ContinuationGeneratedStep advance)) :
    DecisionReachable box projection seed
      (TwoFamilyGeneratedStep advance classifies) := by
  rcases reachable with ⟨decision⟩
  exact ⟨decision.upgradeToTwoFamilies
    box projection seed advance classifies exhaustive⟩

/-! ## Compression through the authority wall -/

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

/-- Compress the deciding endpoint of one witnessed refinement chain. -/
def compressDecision
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    {seed : box.Witness}
    {refines : box.Witness → box.Witness → Prop}
    (decision : DecisionWitness box projection seed refines) :
    CertifiedInstantiation map focus :=
  compressImagination box projection sound
    decision.endpoint decision.color decision.hit

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
Decision Reachability plus projection soundness is the stronger witnessed bridge
to construction authority.
-/
theorem decisionReachable_sound_has_certificate
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    (seed : box.Witness)
    (refines : box.Witness → box.Witness → Prop)
    (reachable : DecisionReachable box projection seed refines) :
    Nonempty (CertifiedInstantiation map focus) := by
  rcases reachable with ⟨decision⟩
  exact ⟨compressDecision box projection sound decision⟩

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

/-- A successful Decision Reachability chain also consumes exactly one void. -/
theorem compressedDecision_consumes_one_void
    {Vertex : Type u} [DecidableEq Vertex]
    (roster : VertexRoster Vertex)
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    (box : ImaginationBox Vertex map focus)
    (projection : ImaginaryProjection box)
    (sound : ProjectionSound box projection)
    {seed : box.Witness}
    {refines : box.Witness → box.Witness → Prop}
    (decision : DecisionWitness box projection seed refines) :
    voidCount roster (instantiate (compressDecision box projection sound decision)) =
      voidCount roster map - 1 := by
  exact voidCount_instantiate roster
    (compressDecision box projection sound decision)

/-! ## Global precommit completeness target -/

/--
The transferable strategy-level target expressed directly in Decision
Reachability language.

For every strategy-safe nonterminal realized map, there must exist one focus and
one sound imagination interface containing a finite witnessed admissible chain to
a deciding endpoint whose realized successor remains strategy-safe.

The chain has no a-priori length bound. No inhabitant is supplied globally here.
-/
def DecisionReachabilityComplete
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex) : Prop :=
  ∀ (map : RealizedMap Vertex),
    safe map →
    HasVoid map →
    ∃ (focus : Focus Vertex)
      (box : ImaginationBox Vertex map focus)
      (projection : ImaginaryProjection box)
      (seed : box.Witness)
      (refines : box.Witness → box.Witness → Prop)
      (sound : ProjectionSound box projection)
      (decision : DecisionWitness box projection seed refines),
      safe (instantiate (compressDecision box projection sound decision))

/--
BRIDGE: Decision Reachability completeness discharges the existing construction-
level safe-instantiation obligation. This connects the imagination proof object
directly to the already-banked precommit induction target.
-/
theorem decisionReachabilityComplete_implies_safe_instantiation
    {Vertex : Type u} [DecidableEq Vertex]
    (safe : StrategySafePredicate Vertex)
    (complete : DecisionReachabilityComplete safe) :
    EveryStrategySafeStateHasSafeInstantiation safe := by
  intro map safeMap hasVoid
  rcases complete map safeMap hasVoid with
    ⟨focus, box, projection, seed, refines, sound, decision, safeAfter⟩
  exact ⟨focus, compressDecision box projection sound decision, safeAfter⟩

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

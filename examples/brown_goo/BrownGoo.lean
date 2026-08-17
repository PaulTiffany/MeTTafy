/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A tiny MeTTafy architecture witness for distinction-preserving transport.
The deliberately playful name "brown goo" denotes a precise failure mode:
a transport collapses a distinction that its fidelity contract, or an admissible
future continuation, still requires it to preserve.
-/

namespace MeTTafy.BrownGoo

universe u v w

/--
A transport contract identifies source distinctions that must survive translation.

`Required x y` is stronger than merely observing `x ≠ y`: the contract says this
particular distinction matters to the semantics we promise to preserve.
-/
structure DistinctionContract (α : Type u) where
  Required : α → α → Prop
  required_distinct : ∀ {x y}, Required x y → x ≠ y

/-- A transport is faithful when every contract-required distinction survives. -/
def Faithful
    {α : Type u} {β : Type v}
    (contract : DistinctionContract α)
    (transport : α → β) : Prop :=
  ∀ {x y}, contract.Required x y → transport x ≠ transport y

/--
A witnessed first-order instance of "brown goo": two source objects that the
contract requires us to keep distinguishable are mapped to the same target object.
-/
def BrownGoo
    {α : Type u} {β : Type v}
    (contract : DistinctionContract α)
    (transport : α → β) : Prop :=
  ∃ x y, contract.Required x y ∧ transport x = transport y

/-- Exact recovery means that `recover` is a left inverse of `transport`. -/
def ExactRecovery
    {α : Type u} {β : Type v}
    (recover : β → α)
    (transport : α → β) : Prop :=
  ∀ x, recover (transport x) = x

/-- A witnessed required collapse mechanically refutes faithfulness. -/
theorem brownGoo_refutes_faithful
    {α : Type u} {β : Type v}
    {contract : DistinctionContract α}
    {transport : α → β}
    (goo : BrownGoo contract transport) :
    ¬ Faithful contract transport := by
  intro faithful
  rcases goo with ⟨x, y, required, collapsed⟩
  exact faithful required collapsed

/-- Any transport admitting exact recovery preserves every required distinction. -/
theorem exactRecovery_implies_faithful
    {α : Type u} {β : Type v}
    {contract : DistinctionContract α}
    {transport : α → β}
    {recover : β → α}
    (exact : ExactRecovery recover transport) :
    Faithful contract transport := by
  intro x y required collapsed
  apply contract.required_distinct required
  calc
    x = recover (transport x) := (exact x).symm
    _ = recover (transport y) := congrArg recover collapsed
    _ = y := exact y

/--
The first-order teethed statement: once a required distinction has been collapsed,
there is no exact decoder that can recover every source object.
-/
theorem brownGoo_forbids_exactRecovery
    {α : Type u} {β : Type v}
    {contract : DistinctionContract α}
    {transport : α → β}
    (goo : BrownGoo contract transport) :
    ¬ ∃ recover : β → α, ExactRecovery recover transport := by
  intro recoverable
  rcases recoverable with ⟨recover, exact⟩
  exact brownGoo_refutes_faithful goo
    (exactRecovery_implies_faithful (contract := contract) exact)

/--
Non-injectivity alone is not first-order "brown goo". If a contract requires no
distinctions, then any transport is faithful to that deliberately empty contract.

This is only a first-order escape hatch. The contextual definitions below close
the pseudo-arbitrary loophole: a distinction cannot be made harmless merely by
omitting it from the immediate contract if an admissible future continuation can
still make it operationally observable.
-/
def NoRequiredDistinctions (α : Type u) : DistinctionContract α where
  Required := fun _ _ => False
  required_distinct := by
    intro x y required
    contradiction

theorem arbitraryTransport_faithful_to_empty_contract
    {α : Type u} {β : Type v}
    (transport : α → β) :
    Faithful (NoRequiredDistinctions α) transport := by
  intro x y required
  contradiction

/-! ## Contextual / higher-order distinction preservation -/

/--
A family of admissible future continuations. An element `observe : α → γ` may
represent a later observer, policy, action, provenance query, reward function, or
an arbitrarily long composition summarized by its eventual observable result.
-/
def ContextuallyDistinct
    {α : Type u} {γ : Type w}
    (contexts : (α → γ) → Prop)
    (x y : α) : Prop :=
  ∃ observe, contexts observe ∧ observe x ≠ observe y

/--
A genuinely arbitrary distinction, relative to a declared continuation family,
is one that every admissible continuation treats identically.
-/
def ContextuallyArbitrary
    {α : Type u} {γ : Type w}
    (contexts : (α → γ) → Prop)
    (x y : α) : Prop :=
  ∀ observe, contexts observe → observe x = observe y

/-- A distinction cannot be both contextually arbitrary and contextually visible. -/
theorem contextuallyArbitrary_excludes_contextualDifference
    {α : Type u} {γ : Type w}
    {contexts : (α → γ) → Prop}
    {x y : α}
    (arbitrary : ContextuallyArbitrary contexts x y) :
    ¬ ContextuallyDistinct contexts x y := by
  intro distinguished
  rcases distinguished with ⟨observe, admissible, differs⟩
  exact differs (arbitrary observe admissible)

/--
`observe` factors through `transport` when the transported representation retains
enough information for some downstream function to reproduce that continuation
exactly for every source object.
-/
def FactorsThrough
    {α : Type u} {β : Type v} {γ : Type w}
    (transport : α → β)
    (observe : α → γ) : Prop :=
  ∃ downstream : β → γ, ∀ x, downstream (transport x) = observe x

/--
If a transport collapses a pair that a continuation distinguishes, that
continuation cannot factor exactly through the transported representation.
-/
theorem contextualDifference_forbids_factorization
    {α : Type u} {β : Type v} {γ : Type w}
    {transport : α → β}
    {observe : α → γ}
    {x y : α}
    (distinguished : observe x ≠ observe y)
    (collapsed : transport x = transport y) :
    ¬ FactorsThrough transport observe := by
  intro factors
  rcases factors with ⟨downstream, commutes⟩
  apply distinguished
  calc
    observe x = downstream (transport x) := (commutes x).symm
    _ = downstream (transport y) := congrArg downstream collapsed
    _ = observe y := commutes y

/--
Contextual Brown Goo: the immediate representation collapses a pair that at least
one admissible future continuation can still distinguish.
-/
def ContextualBrownGoo
    {α : Type u} {β : Type v} {γ : Type w}
    (contexts : (α → γ) → Prop)
    (transport : α → β) : Prop :=
  ∃ x y, ContextuallyDistinct contexts x y ∧ transport x = transport y

/--
The higher-order teeth: contextual Brown Goo always exhibits an admissible future
continuation that can no longer be implemented exactly from the transported state.
-/
theorem contextualBrownGoo_exhibits_unfactorable_context
    {α : Type u} {β : Type v} {γ : Type w}
    {contexts : (α → γ) → Prop}
    {transport : α → β}
    (goo : ContextualBrownGoo contexts transport) :
    ∃ observe, contexts observe ∧ ¬ FactorsThrough transport observe := by
  rcases goo with ⟨x, y, distinguished, collapsed⟩
  rcases distinguished with ⟨observe, admissible, differs⟩
  exact ⟨observe, admissible, contextualDifference_forbids_factorization differs collapsed⟩

/--
A pseudo-arbitrary distinction is absent from the immediate fidelity contract but
is nevertheless distinguishable by an admissible future continuation.
-/
def PseudoArbitrary
    {α : Type u} {γ : Type w}
    (contract : DistinctionContract α)
    (contexts : (α → γ) → Prop)
    (x y : α) : Prop :=
  ¬ contract.Required x y ∧ ContextuallyDistinct contexts x y

/--
If a pseudo-arbitrary pair is collapsed, the result is contextual Brown Goo even
though the immediate first-order contract did not require that pair.
-/
theorem pseudoArbitraryCollapse_is_contextualBrownGoo
    {α : Type u} {β : Type v} {γ : Type w}
    {contract : DistinctionContract α}
    {contexts : (α → γ) → Prop}
    {transport : α → β}
    {x y : α}
    (pseudo : PseudoArbitrary contract contexts x y)
    (collapsed : transport x = transport y) :
    ContextualBrownGoo contexts transport := by
  exact ⟨x, y, pseudo.2, collapsed⟩

/-! ## Concrete blob → goo witness -/

inductive BlobKind where
  | binaryImage
  | text
  | receipt

/-- At this boundary, blob kinds are declared semantically distinct. -/
def blobBoundaryContract : DistinctionContract BlobKind where
  Required := fun x y => x ≠ y
  required_distinct := fun required => required

/-- The bad boundary operation: erase every blob kind to the same undifferentiated unit. -/
def smearBlobKind : BlobKind → Unit := fun _ => ()

/-- Binary image and text were distinct blobs; `smearBlobKind` turns them into goo. -/
theorem smearBlobKind_is_brownGoo :
    BrownGoo blobBoundaryContract smearBlobKind := by
  refine ⟨BlobKind.binaryImage, BlobKind.text, ?_, rfl⟩
  intro collapsed
  cases collapsed

/-- Therefore no decoder from the smeared output can exactly recover all blob kinds. -/
theorem smearBlobKind_has_no_exactRecovery :
    ¬ ∃ recover : Unit → BlobKind, ExactRecovery recover smearBlobKind :=
  brownGoo_forbids_exactRecovery smearBlobKind_is_brownGoo

/-! ## Pseudo-arbitrary blob witness -/

/--
A later routing decision. The immediate representation may pretend image-vs-text is
irrelevant, but a downstream intent to route images differently makes the source
distinction operationally real.
-/
def routeBlob : BlobKind → Bool
  | BlobKind.binaryImage => true
  | BlobKind.text => false
  | BlobKind.receipt => false

/-- The admissible future-context family containing that routing intent. -/
def blobRoutingContexts : (BlobKind → Bool) → Prop :=
  fun observe => observe = routeBlob

theorem blobImageText_contextuallyDistinct :
    ContextuallyDistinct blobRoutingContexts BlobKind.binaryImage BlobKind.text := by
  refine ⟨routeBlob, rfl, ?_⟩
  intro collapsed
  cases collapsed

/--
Under an empty immediate contract the image/text distinction looks "arbitrary",
but the routing continuation reveals that it was only pseudo-arbitrary.
-/
theorem blobImageText_pseudoArbitrary_under_emptyContract :
    PseudoArbitrary
      (NoRequiredDistinctions BlobKind)
      blobRoutingContexts
      BlobKind.binaryImage
      BlobKind.text := by
  constructor
  · intro required
    contradiction
  · exact blobImageText_contextuallyDistinct

/-- First-order contract checking alone would accept the total smear. -/
theorem smearBlobKind_firstOrderFaithful_to_emptyContract :
    Faithful (NoRequiredDistinctions BlobKind) smearBlobKind :=
  arbitraryTransport_faithful_to_empty_contract smearBlobKind

/-- But the admissible routing intent makes the same smear contextual Brown Goo. -/
theorem smearBlobKind_is_contextualBrownGoo :
    ContextualBrownGoo blobRoutingContexts smearBlobKind := by
  exact pseudoArbitraryCollapse_is_contextualBrownGoo
    blobImageText_pseudoArbitrary_under_emptyContract rfl

/--
Therefore some admissible downstream behavior cannot be reconstructed from the
smeared representation. The supposedly arbitrary distinction becomes actual.
-/
theorem smearBlobKind_breaks_admissible_routing :
    ∃ observe, blobRoutingContexts observe ∧ ¬ FactorsThrough smearBlobKind observe :=
  contextualBrownGoo_exhibits_unfactorable_context smearBlobKind_is_contextualBrownGoo

end MeTTafy.BrownGoo

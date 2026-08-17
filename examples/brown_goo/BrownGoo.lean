/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A tiny MeTTafy architecture witness for distinction-preserving transport.
The deliberately playful name "brown goo" denotes a precise failure mode:
a transport collapses a source distinction that its declared contract required
it to preserve.
-/

namespace MeTTafy.BrownGoo

universe u v

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
A witnessed instance of "brown goo": two source objects that the contract requires
us to keep distinguishable are mapped to the same target object.
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
The teethed statement: once a required distinction has been collapsed, there is
no exact decoder that can recover every source object.
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
Non-injectivity alone is not "brown goo". If a contract requires no distinctions,
then any transport is faithful to that deliberately empty contract. This is the
formal escape hatch for honest quotienting or declared lossy abstraction.
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

end MeTTafy.BrownGoo

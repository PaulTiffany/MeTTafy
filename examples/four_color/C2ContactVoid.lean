import examples.four_color.FourColorCore

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A deliberately narrow C2 reduction for the Four Color research game.

FRAME CONTRACT
--------------
The Four Color proof continues to reason from the declared formal global frame.
This file does not add asynchronous observers or subjective dynamics.

It does make one distinction explicit:

* a color is operational inside the game where contact can distinguish palette
  states;
* `void` means no color is present at that site;
* an external brown projection may collapse all four colors and therefore lacks
  the separating interface needed to enforce color-contact obligations.

For C2 itself, the file banks only the finite component-incidence reduction and
the reduction from a planar crosscut-intersection law to that incidence fact.
The Jordan/crosscut intersection law itself remains an explicit topology debt;
it is not proved or smuggled in here.
-/

namespace MeTTafy.FourColor

/-! ## Operational color, void, and the brown projection -/

/-- A site is either uncolored/void or realizes one of the four palette states. -/
inductive SiteState where
  | void
  | colored (color : V4)
  deriving DecidableEq, Repr

/-- The color exposed by a site, if one is operationally present. -/
def colorOf? : SiteState → Option V4
  | .void => none
  | .colored color => some color

@[simp] theorem void_has_no_color : colorOf? .void = none := rfl
@[simp] theorem colored_exposes_color (color : V4) : colorOf? (.colored color) = some color := rfl

/--
A contact-color interface must preserve the four distinctions used by the game.
The direct palette view has such an interface; a constant brown projection does
not.
-/
structure ContactColorInterface (View : Type) where
  observe : V4 → View
  separates : Function.Injective observe

/-- The four game states can distinguish the palette state presented at contact. -/
def directColorContact : ContactColorInterface V4 where
  observe := id
  separates := by
    intro left right equal
    exact equal

/-- The external coarse view used to witness distinction collapse. -/
inductive BrownView where
  | void
  | brown
  deriving DecidableEq, Repr

/-- Brown sees whether color is present, but not which of the four colors it is. -/
def brownObserve : SiteState → BrownView
  | .void => .void
  | .colored _ => .brown

/-- Restrict the brown observation to colored states. -/
def brownColorProjection (_ : V4) : BrownView := .brown

/-- The brown projection cannot serve as the game's operational color-contact interface. -/
theorem brownColorProjection_not_injective :
    ¬ Function.Injective brownColorProjection := by
  intro injective
  have collapsed : V4.zero = V4.a := injective rfl
  cases collapsed

/-- Different formal colors can be observationally identical to Brown. -/
theorem brown_collapses_distinct_colors :
    V4.zero ≠ V4.a ∧
    brownObserve (.colored V4.zero) = brownObserve (.colored V4.a) := by
  constructor
  · intro equal
    cases equal
  · rfl

/-! ## C2 as contact/component incidence plus one planar law -/

/--
The only boundary-component information needed by the canonical `A B A C D`
C2 argument.

`adA`, `adC`, and `adE` are the `{A,D}` component identities seen at boundary
positions `a`, `c`, and `e`.  `bcB` and `bcD` are the `{B,C}` component
identities at `b` and `d`.

Component equality is the operational contact fact: two terminals with the same
identifier lie in the same complete current bichromatic carrier.
-/
structure CanonicalC2Incidence (ADComponent BCComponent : Type) where
  adA : ADComponent
  adC : ADComponent
  adE : ADComponent
  bcB : BCComponent
  bcD : BCComponent

/-- The `{A,D}` carrier at `a` meets no other `{A,D}` boundary terminal. -/
def ADCleanAtA {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  frame.adA ≠ frame.adC ∧ frame.adA ≠ frame.adE

/-- The `{A,D}` carrier at `c` meets no other `{A,D}` boundary terminal. -/
def ADCleanAtC {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  frame.adC ≠ frame.adA ∧ frame.adC ≠ frame.adE

/-- The `{A,D}` carrier at `e` meets no other `{A,D}` boundary terminal. -/
def ADCleanAtE {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  frame.adE ≠ frame.adA ∧ frame.adE ≠ frame.adC

/-- The `{B,C}` carrier at `b` is boundary-clean. -/
def BCCleanAtB {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  frame.bcB ≠ frame.bcD

/-- The `{B,C}` carrier at `d` is boundary-clean. -/
def BCCleanAtD {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  frame.bcD ≠ frame.bcB

/-- At least one of the five canonical C2 boundary terminals has a clean carrier. -/
def HasCanonicalCleanCarrier {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  ADCleanAtA frame ∨
  ADCleanAtC frame ∨
  ADCleanAtE frame ∨
  BCCleanAtB frame ∨
  BCCleanAtD frame

/--
The incidence consequence of the planar C2 argument: the three `{A,D}`
terminals cannot all be in one component while the two `{B,C}` terminals are
also in one component.
-/
def AlternatingCrosscutExclusion {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) : Prop :=
  ¬ (frame.adA = frame.adC ∧
     frame.adC = frame.adE ∧
     frame.bcB = frame.bcD)

/--
Finite C2 reduction: once the planar alternating-crosscut exclusion is supplied,
at least one canonical boundary carrier is clean.

No topology is hidden in this proof.  The proof only performs the finite
component-partition reasoning from the frozen C2 argument.
-/
theorem c2_clean_carrier_from_crosscut
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (planar : AlternatingCrosscutExclusion frame) :
    HasCanonicalCleanCarrier frame := by
  classical
  by_cases hac : frame.adA = frame.adC
  · by_cases hce : frame.adC = frame.adE
    · have hbd : frame.bcB ≠ frame.bcD := by
        intro equal
        exact planar ⟨hac, hce, equal⟩
      exact Or.inr (Or.inr (Or.inr (Or.inl hbd)))
    · have hea : frame.adE ≠ frame.adA := by
        intro equal
        apply hce
        calc
          frame.adC = frame.adA := hac.symm
          _ = frame.adE := equal.symm
      have hec : frame.adE ≠ frame.adC := Ne.symm hce
      exact Or.inr (Or.inr (Or.inl ⟨hea, hec⟩))
  · by_cases hae : frame.adA = frame.adE
    · have hca : frame.adC ≠ frame.adA := Ne.symm hac
      have hce : frame.adC ≠ frame.adE := by
        intro equal
        apply hac
        calc
          frame.adA = frame.adE := hae
          _ = frame.adC := equal.symm
      exact Or.inr (Or.inl ⟨hca, hce⟩)
    · exact Or.inl ⟨hac, hae⟩

/-- The two `{B,C}` clean predicates are equivalent by symmetry of inequality. -/
theorem bc_clean_symmetry
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) :
    BCCleanAtB frame ↔ BCCleanAtD frame := by
  constructor <;> intro different <;> exact Ne.symm different

/-! ## Exposing the remaining topology debt as forced carrier intersection -/

/--
In the canonical naming `A=zero`, `B=a`, `C=b`, `D=c`, the two C2 color pairs
`{A,D}` and `{B,C}` are disjoint.  No operationally colored vertex can belong
to both pairs.
-/
theorem canonical_c2_pairs_disjoint (color : V4) :
    ¬ (InPair V4.zero V4.c color ∧ InPair V4.a V4.b color) := by
  cases color <;> simp [InPair]

universe v

/--
A carrier-level world for the canonical C2 crosscut argument.

The deleted degree-five focus is retained only as an explicit `void` site: it
has no palette state and cannot lie on either bichromatic carrier.  The
`crosscut_meets_opposite` field is the one still-unproved planar theorem: if the
three `{A,D}` boundary terminals collapse into one current carrier and `b,d`
collapse into one `{B,C}` carrier, the crosscut through the exposed pentagonal
void forces the two carriers to meet.

Everything else in this structure is operational contact data visible from the
formal global proof frame.
-/
structure CanonicalC2CarrierWorld
    (Vertex : Type v)
    (ADComponent BCComponent : Type) where
  state : Vertex → SiteState
  focus : Vertex
  focus_void : state focus = .void
  frame : CanonicalC2Incidence ADComponent BCComponent
  adCarrier : ADComponent → Vertex → Prop
  bcCarrier : BCComponent → Vertex → Prop
  ad_uses_pair : ∀ {component vertex}, adCarrier component vertex →
    ∃ color, state vertex = .colored color ∧ InPair V4.zero V4.c color
  bc_uses_pair : ∀ {component vertex}, bcCarrier component vertex →
    ∃ color, state vertex = .colored color ∧ InPair V4.a V4.b color
  crosscut_meets_opposite :
    frame.adA = frame.adC →
    frame.adC = frame.adE →
    frame.bcB = frame.bcD →
    ∃ vertex, adCarrier frame.adA vertex ∧ bcCarrier frame.bcB vertex

/-- The explicit void focus cannot belong to an `{A,D}` carrier. -/
theorem c2_void_not_in_ad_carrier
    {Vertex : Type v}
    {ADComponent BCComponent : Type}
    (world : CanonicalC2CarrierWorld Vertex ADComponent BCComponent)
    (component : ADComponent) :
    ¬ world.adCarrier component world.focus := by
  intro onCarrier
  rcases world.ad_uses_pair onCarrier with ⟨color, stateEqual, _⟩
  rw [world.focus_void] at stateEqual
  cases stateEqual

/-- The explicit void focus cannot belong to a `{B,C}` carrier. -/
theorem c2_void_not_in_bc_carrier
    {Vertex : Type v}
    {ADComponent BCComponent : Type}
    (world : CanonicalC2CarrierWorld Vertex ADComponent BCComponent)
    (component : BCComponent) :
    ¬ world.bcCarrier component world.focus := by
  intro onCarrier
  rcases world.bc_uses_pair onCarrier with ⟨color, stateEqual, _⟩
  rw [world.focus_void] at stateEqual
  cases stateEqual

/-- The two canonical bichromatic carrier families are vertex-disjoint by color. -/
theorem c2_carrier_families_disjoint
    {Vertex : Type v}
    {ADComponent BCComponent : Type}
    (world : CanonicalC2CarrierWorld Vertex ADComponent BCComponent)
    (adComponent : ADComponent)
    (bcComponent : BCComponent)
    (vertex : Vertex) :
    ¬ (world.adCarrier adComponent vertex ∧ world.bcCarrier bcComponent vertex) := by
  intro both
  rcases world.ad_uses_pair both.1 with ⟨adColor, adState, adPair⟩
  rcases world.bc_uses_pair both.2 with ⟨bcColor, bcState, bcPair⟩
  have coloredEqual : SiteState.colored adColor = SiteState.colored bcColor :=
    adState.symm.trans bcState
  have colorEqual : adColor = bcColor := by
    injection coloredEqual
  subst bcColor
  exact canonical_c2_pairs_disjoint adColor ⟨adPair, bcPair⟩

/--
The positive planar intersection law plus operational color disjointness yields
the abstract alternating-crosscut exclusion used by the finite C2 reduction.
-/
theorem c2_crosscut_exclusion_from_contact_void
    {Vertex : Type v}
    {ADComponent BCComponent : Type}
    (world : CanonicalC2CarrierWorld Vertex ADComponent BCComponent) :
    AlternatingCrosscutExclusion world.frame := by
  intro blocked
  rcases world.crosscut_meets_opposite blocked.1 blocked.2.1 blocked.2.2 with
    ⟨vertex, onAD, onBC⟩
  exact c2_carrier_families_disjoint world world.frame.adA world.frame.bcB vertex
    ⟨onAD, onBC⟩

/--
C2 reduced to its remaining topology theorem: in any canonical contact/void
world satisfying the crosscut-intersection law, at least one boundary carrier
is clean.
-/
theorem c2_clean_carrier_from_contact_void
    {Vertex : Type v}
    {ADComponent BCComponent : Type}
    (world : CanonicalC2CarrierWorld Vertex ADComponent BCComponent) :
    HasCanonicalCleanCarrier world.frame :=
  c2_clean_carrier_from_crosscut world.frame
    (c2_crosscut_exclusion_from_contact_void world)

end MeTTafy.FourColor

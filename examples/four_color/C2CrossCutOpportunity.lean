import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

C2 cross-cut opportunity semantics for the Four Color construction game.

FRAME CONTRACT
--------------
This file formalizes the paper-map argument at the exact point where geometry
answers a counterfactual question.

The map-maker may inspect the realized partial map and imagine a cross-cut inside
one already connected carrier.  The imagined cut is not itself a realized turn.
It is an opportunity supplied by the disk geometry.  By the game meaning of a
cross-cut, that opportunity restricts the opposite continuation across the cut.

For the canonical A B A C D boundary there are only two relevant terminal-avoiding
cross-cut shapes from an A/D carrier spanning a,c,e: an a--c cut or a c--e cut.
Either separates b from d in the cyclic pentagonal boundary.  The disk geometry
contract below says exactly two things and nothing stronger:

* if the three A/D terminals lie in one carrier, one of those cross-cut
  opportunities is exposed;
* an exposed cross-cut restricts the opposite B/C continuation, so b and d
  cannot remain in one B/C carrier.

It does NOT assert that the two differently typed carriers meet at a vertex.
That older intersection formulation was stronger than the game requires.
-/

namespace MeTTafy.FourColor

/-- The two terminal-avoiding cross-cut shapes used by the canonical A B A C D argument. -/
inductive CanonicalCrossCutChoice where
  | ac
  | ce
  deriving DecidableEq, Repr

/--
The exact planar-disk response interface needed by C2.

`offered cut` means that inspection of the current realized geometry exposes the
named counterfactual cut.  `spanning_ad_offers_crosscut` is the elementary tree
fact used by the paper proof: a connected A/D carrier spanning a,c,e contains a
terminal-avoiding a--c or c--e cross-cut.  `crosscut_restricts_opposite` is the
operational cross-cut law: because b and d lie on opposite boundary arcs of
either such cut, the B/C continuation cannot remain one untouched component.

This is the declared geometry of the theorem's domain, not an observer and not
a future-route oracle.
-/
structure CanonicalC2DiskGeometry
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) where
  offered : CanonicalCrossCutChoice → Prop
  spanning_ad_offers_crosscut :
    frame.adA = frame.adC →
    frame.adC = frame.adE →
    ∃ cut, offered cut
  crosscut_restricts_opposite :
    ∀ cut, offered cut → frame.bcB ≠ frame.bcD

/-- One inspection-mode cross-cut opportunity exposed by the current disk geometry. -/
structure CanonicalC2CrossCutOpportunity
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) where
  choice : CanonicalCrossCutChoice
  offered : geometry.offered choice

/-- Every exposed canonical cross-cut opportunity restricts the B/C continuation. -/
theorem crosscut_opportunity_restricts_bc
    {ADComponent BCComponent : Type}
    {frame : CanonicalC2Incidence ADComponent BCComponent}
    {geometry : CanonicalC2DiskGeometry frame}
    (opportunity : CanonicalC2CrossCutOpportunity frame geometry) :
    frame.bcB ≠ frame.bcD :=
  geometry.crosscut_restricts_opposite opportunity.choice opportunity.offered

/--
If all three A/D terminals are in one carrier, the disk exposes a concrete
counterfactual cross-cut opportunity.
-/
theorem spanning_ad_exposes_crosscut
    {ADComponent BCComponent : Type}
    {frame : CanonicalC2Incidence ADComponent BCComponent}
    (geometry : CanonicalC2DiskGeometry frame)
    (hac : frame.adA = frame.adC)
    (hce : frame.adC = frame.adE) :
    ∃ opportunity : CanonicalC2CrossCutOpportunity frame geometry, True := by
  rcases geometry.spanning_ad_offers_crosscut hac hce with ⟨choice, offered⟩
  exact ⟨⟨choice, offered⟩, trivial⟩

/--
The counterfactual cross-cut response rules out the only fully locked canonical
incidence: all A/D terminals connected AND b,d still connected in B/C.
-/
theorem c2_crosscut_response_exclusion
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    AlternatingCrosscutExclusion frame := by
  intro locked
  rcases geometry.spanning_ad_offers_crosscut locked.1 locked.2.1 with
    ⟨choice, offered⟩
  exact geometry.crosscut_restricts_opposite choice offered locked.2.2

/--
C2 clean-carrier existence on the declared planar-disk game geometry.

No carrier-intersection witness is assumed.  If the finite incidence pattern
were fully locked, the A/D span would expose a cross-cut opportunity; the
geometry's own response to that imagined cut would restrict B/C, contradicting
the claimed B/C lock.  Therefore at least one canonical boundary carrier is
clean.
-/
theorem c2_clean_carrier_from_disk_geometry
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    HasCanonicalCleanCarrier frame :=
  c2_clean_carrier_from_crosscut frame
    (c2_crosscut_response_exclusion frame geometry)

/--
Equivalent contradiction form matching the paper-map red-team argument: if no
clean carrier existed, the locked incidence would violate the cross-cut response
of the disk geometry.
-/
theorem no_canonical_clean_carrier_impossible
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    ¬ (¬ HasCanonicalCleanCarrier frame) := by
  intro noClean
  exact noClean (c2_clean_carrier_from_disk_geometry frame geometry)

end MeTTafy.FourColor

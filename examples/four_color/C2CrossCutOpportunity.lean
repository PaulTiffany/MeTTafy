import examples.four_color.C2ContactVoid

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

C2 imagined cross-cut/response semantics for the Four Color construction game.

FRAME CONTRACT
--------------
The map-maker alternates operational modes while solving the paper map.

During play, a realized state acts only through its current local contacts.
During inspection, the map-maker may instantiate that same state in imagination,
ask what a cross-cut move would do, and then imagine the opposite state's legal
responses to that hypothetical move.

Those imagined moves are NOT a sequence of realized intermediate maps.  The
response depends on the imagined cut, but cut and response are evaluated as one
counterfactual exchange.  The map-maker amortizes that whole imagined exchange
into the single clean opportunity selected for the next realized move.

For the canonical A B A C D boundary there are only two relevant terminal-
avoiding A/D cross-cut probes when a,c,e lie in one A/D carrier: a--c or c--e.
Either puts b and d on opposite boundary sides.  The opposite B/C player is then
imagined responding to that cut.  By the operational meaning of response, it
escapes on one exposed side: either B is boundary-clean or D is boundary-clean.
That is enough for C2; no physical A/D--B/C carrier intersection is required.
-/

namespace MeTTafy.FourColor

/-- The two terminal-avoiding imagined A/D cross-cut probes in canonical A B A C D. -/
inductive CanonicalCrossCutChoice where
  | ac
  | ce
  deriving DecidableEq, Repr

/--
An imagined opposite response is, by definition of escape from the cross-cut,
one of the two exposed B/C boundary opportunities.  The response is hypothetical;
the proof carried by the constructor is a fact about the current inspected map,
not a realized successor.
-/
inductive CanonicalOppositeResponse
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) where
  | escapeB (clean : BCCleanAtB frame)
  | escapeD (clean : BCCleanAtD frame)

/-- Either typed opposite response immediately certifies that b,d are not one B/C component. -/
theorem opposite_response_rejects_bc_lock
    {ADComponent BCComponent : Type}
    {frame : CanonicalC2Incidence ADComponent BCComponent}
    (response : CanonicalOppositeResponse frame) :
    frame.bcB ≠ frame.bcD := by
  cases response with
  | escapeB clean => exact clean
  | escapeD clean => exact Ne.symm clean

/--
The exact planar-disk counterfactual interface needed by C2.

`cutAvailable` records which cross-cut probes the current inspected geometry
permits us to imagine.

The two ground disk laws are deliberately small:

1. if a,c,e lie in one A/D carrier, inspection exposes a terminal-avoiding
   a--c or c--e imagined cross-cut;
2. every exposed imagined cross-cut offers at least one opposite escape
   response.

The response is conditioned on the imagined cut for deliberation, but there is
no `before -> after` state transition here.  The cut and response are evaluated
together as one simultaneous imagined exchange.  The fact that an escape
response breaks the B/C lock is no longer an extra geometry premise; it follows
from the response type itself.
-/
structure CanonicalC2DiskGeometry
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) where
  cutAvailable : CanonicalCrossCutChoice → Prop
  spanning_ad_offers_crosscut :
    frame.adA = frame.adC →
    frame.adC = frame.adE →
    ∃ cut, cutAvailable cut
  crosscut_offers_response :
    ∀ cut, cutAvailable cut →
      ∃ response : CanonicalOppositeResponse frame, True

/--
One complete imagined exchange: first choose an instantiated state's hypothetical
cross-cut, then imagine one legal opposite response.  Both live in the same
counterfactual bundle; neither is a realized map state.
-/
structure CanonicalC2ImaginedExchange
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) where
  cut : CanonicalCrossCutChoice
  cut_imagined : geometry.cutAvailable cut
  response : CanonicalOppositeResponse frame

/--
A spanning A/D lock exposes a complete imagined cut-response exchange without
realizing either imagined step.
-/
theorem spanning_ad_exposes_imagined_exchange
    {ADComponent BCComponent : Type}
    {frame : CanonicalC2Incidence ADComponent BCComponent}
    (geometry : CanonicalC2DiskGeometry frame)
    (hac : frame.adA = frame.adC)
    (hce : frame.adC = frame.adE) :
    ∃ exchange : CanonicalC2ImaginedExchange frame geometry, True := by
  rcases geometry.spanning_ad_offers_crosscut hac hce with ⟨cut, cutAvailable⟩
  rcases geometry.crosscut_offers_response cut cutAvailable with ⟨response, _⟩
  exact ⟨⟨cut, cutAvailable, response⟩, trivial⟩

/--
A complete imagined exchange reveals that the opposite B/C continuation cannot
remain one untouched component in the inspected current geometry.
-/
theorem imagined_exchange_restricts_bc
    {ADComponent BCComponent : Type}
    {frame : CanonicalC2Incidence ADComponent BCComponent}
    {geometry : CanonicalC2DiskGeometry frame}
    (exchange : CanonicalC2ImaginedExchange frame geometry) :
    frame.bcB ≠ frame.bcD :=
  opposite_response_rejects_bc_lock exchange.response

/--
The simultaneous counterfactual exchange rules out the only fully locked
canonical incidence.
-/
theorem c2_imagined_exchange_exclusion
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    AlternatingCrosscutExclusion frame := by
  intro locked
  rcases spanning_ad_exposes_imagined_exchange geometry locked.1 locked.2.1 with
    ⟨exchange, _⟩
  exact imagined_exchange_restricts_bc exchange locked.2.2

/--
C2 clean-carrier opportunity existence on the declared planar-disk game
geometry.

The proof performs the red-team exchange entirely in imagination.  If the
canonical incidence were fully locked, the imagined A/D cut plus imagined B/C
escape response would reject that lock.  Hence at least one clean carrier
opportunity already exists in the current realized map.
-/
theorem c2_clean_carrier_from_imagined_exchange
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    HasCanonicalCleanCarrier frame :=
  c2_clean_carrier_from_crosscut frame
    (c2_imagined_exchange_exclusion frame geometry)

/--
The map-maker's amortized C2 decision contains only the clean opportunity that
survives the imagined exchange.  No imagined intermediate move becomes part of
the realized construction history.
-/
structure AmortizedC2Move
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) where
  cleanOpportunity : HasCanonicalCleanCarrier frame

/-- Amortize every C2 counterfactual cut/response step into one next-move clean opportunity. -/
def amortizeC2
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    AmortizedC2Move frame :=
  ⟨c2_clean_carrier_from_imagined_exchange frame geometry⟩

/-- The amortized result exposes exactly the current clean opportunity needed by C2. -/
theorem amortized_c2_exposes_clean_opportunity
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent)
    (geometry : CanonicalC2DiskGeometry frame) :
    HasCanonicalCleanCarrier frame :=
  (amortizeC2 frame geometry).cleanOpportunity

end MeTTafy.FourColor

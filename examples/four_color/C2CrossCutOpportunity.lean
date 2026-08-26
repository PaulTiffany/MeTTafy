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
imagined responding to that cut.  A legal imagined response is incompatible
with b and d remaining one untouched B/C component.  That incompatibility is
enough for C2; no physical A/D--B/C carrier intersection is required.
-/

namespace MeTTafy.FourColor

/-- The two terminal-avoiding imagined A/D cross-cut probes in canonical A B A C D. -/
inductive CanonicalCrossCutChoice where
  | ac
  | ce
  deriving DecidableEq, Repr

/--
The opposite B/C state may answer the imagined cut from either exposed boundary
side.  These are counterfactual response roles, not realized successor states.
-/
inductive CanonicalOppositeResponse where
  | fromB
  | fromD
  deriving DecidableEq, Repr

/--
The exact planar-disk counterfactual interface needed by C2.

`cutAvailable` records which cross-cut probes the current inspected geometry
permits us to imagine. `responseAvailable cut response` records which opposite
responses can be imagined against that cut.

The response is *conditioned on* the imagined cut for deliberation, but there is
no `before -> after` state transition in this structure.  The cut and response
are evaluated together as one simultaneous imagined exchange.

The three ground disk laws are:

1. if a,c,e lie in one A/D carrier, inspection exposes a terminal-avoiding
   a--c or c--e imagined cross-cut;
2. every exposed imagined cross-cut admits at least one opposite B/C response;
3. any legal cut-response bundle is incompatible with b,d remaining one
   untouched B/C component.

These are the paper-map cross-cut mechanics of the declared planar-disk domain.
They are not supplied by an observer, a future route, or a realized intermediate
state.
-/
structure CanonicalC2DiskGeometry
    {ADComponent BCComponent : Type}
    (frame : CanonicalC2Incidence ADComponent BCComponent) where
  cutAvailable : CanonicalCrossCutChoice → Prop
  responseAvailable : CanonicalCrossCutChoice → CanonicalOppositeResponse → Prop
  spanning_ad_offers_crosscut :
    frame.adA = frame.adC →
    frame.adC = frame.adE →
    ∃ cut, cutAvailable cut
  crosscut_offers_response :
    ∀ cut, cutAvailable cut →
      ∃ response, responseAvailable cut response
  imagined_exchange_rejects_bc_lock :
    ∀ cut response,
      cutAvailable cut →
      responseAvailable cut response →
      frame.bcB ≠ frame.bcD

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
  response : CanonicalOppositeResponse
  response_imagined : geometry.responseAvailable cut response

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
  rcases geometry.crosscut_offers_response cut cutAvailable with
    ⟨response, responseAvailable⟩
  exact ⟨⟨cut, cutAvailable, response, responseAvailable⟩, trivial⟩

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
  geometry.imagined_exchange_rejects_bc_lock
    exchange.cut exchange.response exchange.cut_imagined exchange.response_imagined

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
response would reject that lock.  Hence at least one clean carrier opportunity
already exists in the current realized map.
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

/--
Amortize every C2 counterfactual cut/response step into one next-move clean
opportunity.
-/
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

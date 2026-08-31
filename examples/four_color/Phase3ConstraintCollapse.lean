import examples.four_color.ProofFrontierReduction

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Phase-3 constraint collapse for the independent Four Color research lane.

NOVELTY / SCOPE
---------------
This file does not add another search procedure or another completeness target.
It records the local imagination algebra already implicit in the existing V4,
forced-third, and construction-authority witnesses.

Fix one current/reference state. With no further restriction, phase 3 has exactly
three nonidentity imaginary shifts. Realized colored neighbors can only remove
possibilities from that surface:

  3 -> 2 -> 1 -> 0

One realized color places an admissible candidate on the three-direction surface.
A second distinct realized color removes one direction, leaving only a two-state
residue. Three distinct realized colors force the fourth state. If all four palette
states already occur around the void, direct instantiation is impossible and any
further work must remain imaginary/counter-play rather than inventing a fourth
phase-3 direction.

The key point is interface closure: two distinct imaginary phase shifts relative
to one reference determine the unique third by V4 addition. Real information can
collapse imagination; it cannot expand it beyond the three nonidentity directions.
-/

namespace MeTTafy.FourColor

universe u

/-! ## 1. The unconstrained anchored surface has exactly three phase shifts -/

/--
Fixing one current/reference state leaves exactly the three other palette states
as imaginary phase shifts. This is the `total colors - 1` lower and upper surface
for unconstrained phase-3 comparison relative to that reference.
-/
theorem anchored_step3_has_exactly_three_phase_shifts
    (reference : V4) :
    (imaginaryAlternatives reference).length = 3 ∧
      ∀ state : V4,
        state ∈ imaginaryAlternatives reference ↔ UpwardFrom reference state := by
  constructor
  · exact imaginaryAlternatives_length reference
  · intro state
    simpa [UpwardFrom] using
      (mem_imaginaryAlternatives_iff reference state)

/--
Every surviving non-reference state is still represented by one of the same three
nonidentity directions. Adding realized constraints never creates a fourth phase
shift.
-/
theorem surviving_candidate_stays_on_three_direction_surface
    (reference state : V4)
    (stateUp : UpwardFrom reference state) :
    ∃ direction : ImaginaryDirection,
      direction ∈ ImaginaryDirection.all ∧
      state = imaginedColor reference direction := by
  rcases distinct_imagined_color_has_unique_direction reference state stateUp with
    ⟨direction, equal, _unique⟩
  exact ⟨direction, ImaginaryDirection.mem_all direction, equal⟩

/-! ## 2. Constraint collapse inside the three-direction surface -/

/--
After one additional upward state is excluded, any remaining upward candidate is
one of only two states: a chosen surviving state or the forced third state.
-/
theorem one_additional_constraint_leaves_two_state_residue
    (reference excluded survivor state : V4)
    (excludedUp : UpwardFrom reference excluded)
    (survivorUp : UpwardFrom reference survivor)
    (different : excluded ≠ survivor)
    (stateUp : UpwardFrom reference state)
    (state_ne_excluded : state ≠ excluded) :
    state = survivor ∨
      state = forcedThirdFrom reference excluded survivor := by
  rcases upward_states_exhausted_by_pair_and_forcedThird
      reference excluded survivor state
      excludedUp survivorUp different stateUp with
    equalExcluded | equalSurvivor | equalThird
  · exact False.elim (state_ne_excluded equalExcluded)
  · exact Or.inl equalSurvivor
  · exact Or.inr equalThird

/--
After two additional distinct upward states are excluded, the only surviving
candidate is their unique forced third.
-/
theorem two_additional_constraints_force_unique_remaining_state
    (reference left right state : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right)
    (stateUp : UpwardFrom reference state)
    (state_ne_left : state ≠ left)
    (state_ne_right : state ≠ right) :
    state = forcedThirdFrom reference left right :=
  forcedThird_unique reference left right state
    leftUp rightUp different stateUp state_ne_left state_ne_right

/--
After the reference, two distinct upward states, and their forced third are all
excluded, no phase-3 candidate remains.
-/
theorem three_additional_constraints_exhaust_step3_surface
    (reference left right state : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right)
    (stateUp : UpwardFrom reference state)
    (state_ne_left : state ≠ left)
    (state_ne_right : state ≠ right)
    (state_ne_third : state ≠ forcedThirdFrom reference left right) :
    False := by
  have forced := two_additional_constraints_force_unique_remaining_state
    reference left right state leftUp rightUp different
    stateUp state_ne_left state_ne_right
  exact state_ne_third forced

/--
Two distinct imaginary phase shifts interface algebraically by determining the
unique third nonidentity phase shift. Their interface closes rather than expands
the phase-3 surface.
-/
theorem two_phase_shifts_interface_to_unique_third
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    UpwardFrom reference (forcedThirdFrom reference left right) ∧
    forcedThirdFrom reference left right ≠ left ∧
    forcedThirdFrom reference left right ≠ right ∧
    ∀ candidate : V4,
      UpwardFrom reference candidate →
      candidate ≠ left →
      candidate ≠ right →
      candidate = forcedThirdFrom reference left right := by
  exact ⟨
    forcedThird_ne_reference reference left right leftUp rightUp different,
    forcedThird_ne_left reference left right leftUp rightUp different,
    forcedThird_ne_right reference left right leftUp rightUp different,
    fun candidate candidateUp candidate_ne_left candidate_ne_right =>
      forcedThird_unique reference left right candidate
        leftUp rightUp different candidateUp candidate_ne_left candidate_ne_right
  ⟩

/-! ## 3. Realized colored neighbors instantiate those algebraic constraints -/

/--
One realized colored neighbor removes that color from any admissible candidate.
Thus the candidate lies on the three-direction surface relative to that neighbor
color.
-/
theorem one_realized_neighbor_places_candidate_on_step3_surface
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    {candidate : V4}
    (admissible : AdmissibleAt map focus candidate)
    (neighbor : Vertex)
    (neighborColor : V4)
    (touches :
      map.adjacent focus.vertex neighbor ∨
        map.adjacent neighbor focus.vertex)
    (realized : map.state neighbor = .colored neighborColor) :
    ∃ direction : ImaginaryDirection,
      direction ∈ ImaginaryDirection.all ∧
      candidate = imaginedColor neighborColor direction := by
  have different : candidate ≠ neighborColor :=
    admissible.differs_from_realized_neighbors
      neighbor neighborColor touches realized
  exact surviving_candidate_stays_on_three_direction_surface
    neighborColor candidate different

/--
Two distinct realized neighbor colors collapse direct imagination to a two-state
residue. `survivor` names either one of the two still-available colors; the other
is then forced algebraically.
-/
theorem two_realized_neighbor_colors_leave_two_state_residue
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    {candidate : V4}
    (admissible : AdmissibleAt map focus candidate)
    (referenceNeighbor excludedNeighbor : Vertex)
    (reference excluded survivor : V4)
    (referenceTouches :
      map.adjacent focus.vertex referenceNeighbor ∨
        map.adjacent referenceNeighbor focus.vertex)
    (excludedTouches :
      map.adjacent focus.vertex excludedNeighbor ∨
        map.adjacent excludedNeighbor focus.vertex)
    (referenceRealized : map.state referenceNeighbor = .colored reference)
    (excludedRealized : map.state excludedNeighbor = .colored excluded)
    (excludedUp : UpwardFrom reference excluded)
    (survivorUp : UpwardFrom reference survivor)
    (different : excluded ≠ survivor) :
    candidate = survivor ∨
      candidate = forcedThirdFrom reference excluded survivor := by
  have candidateUp : UpwardFrom reference candidate :=
    admissible.differs_from_realized_neighbors
      referenceNeighbor reference referenceTouches referenceRealized
  have candidate_ne_excluded : candidate ≠ excluded :=
    admissible.differs_from_realized_neighbors
      excludedNeighbor excluded excludedTouches excludedRealized
  exact one_additional_constraint_leaves_two_state_residue
    reference excluded survivor candidate
    excludedUp survivorUp different candidateUp candidate_ne_excluded

/--
Three distinct realized neighbor colors force the only remaining palette state.
This is the direct realized-map form of the phase-3 `3 -> 2 -> 1` collapse.
-/
theorem three_realized_neighbor_colors_force_fourth
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    {candidate : V4}
    (admissible : AdmissibleAt map focus candidate)
    (referenceNeighbor leftNeighbor rightNeighbor : Vertex)
    (reference left right : V4)
    (referenceTouches :
      map.adjacent focus.vertex referenceNeighbor ∨
        map.adjacent referenceNeighbor focus.vertex)
    (leftTouches :
      map.adjacent focus.vertex leftNeighbor ∨
        map.adjacent leftNeighbor focus.vertex)
    (rightTouches :
      map.adjacent focus.vertex rightNeighbor ∨
        map.adjacent rightNeighbor focus.vertex)
    (referenceRealized : map.state referenceNeighbor = .colored reference)
    (leftRealized : map.state leftNeighbor = .colored left)
    (rightRealized : map.state rightNeighbor = .colored right)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    candidate = forcedThirdFrom reference left right := by
  have candidateUp : UpwardFrom reference candidate :=
    admissible.differs_from_realized_neighbors
      referenceNeighbor reference referenceTouches referenceRealized
  have candidate_ne_left : candidate ≠ left :=
    admissible.differs_from_realized_neighbors
      leftNeighbor left leftTouches leftRealized
  have candidate_ne_right : candidate ≠ right :=
    admissible.differs_from_realized_neighbors
      rightNeighbor right rightTouches rightRealized
  exact two_additional_constraints_force_unique_remaining_state
    reference left right candidate leftUp rightUp different
    candidateUp candidate_ne_left candidate_ne_right

/--
If the fourth palette state is realized at another neighbor too, direct placement
is impossible. Phase 3 has collapsed to zero local candidates; any continuation
must be counter-play on surrounding relations, still inside the same three V4
phase shifts.
-/
theorem four_realized_neighbor_colors_block_direct_instantiation
    {Vertex : Type u}
    {map : RealizedMap Vertex}
    {focus : Focus Vertex}
    {candidate : V4}
    (admissible : AdmissibleAt map focus candidate)
    (referenceNeighbor leftNeighbor rightNeighbor thirdNeighbor : Vertex)
    (reference left right : V4)
    (referenceTouches :
      map.adjacent focus.vertex referenceNeighbor ∨
        map.adjacent referenceNeighbor focus.vertex)
    (leftTouches :
      map.adjacent focus.vertex leftNeighbor ∨
        map.adjacent leftNeighbor focus.vertex)
    (rightTouches :
      map.adjacent focus.vertex rightNeighbor ∨
        map.adjacent rightNeighbor focus.vertex)
    (thirdTouches :
      map.adjacent focus.vertex thirdNeighbor ∨
        map.adjacent thirdNeighbor focus.vertex)
    (referenceRealized : map.state referenceNeighbor = .colored reference)
    (leftRealized : map.state leftNeighbor = .colored left)
    (rightRealized : map.state rightNeighbor = .colored right)
    (thirdRealized :
      map.state thirdNeighbor =
        .colored (forcedThirdFrom reference left right))
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    False := by
  have forced : candidate = forcedThirdFrom reference left right :=
    three_realized_neighbor_colors_force_fourth
      admissible
      referenceNeighbor leftNeighbor rightNeighbor
      reference left right
      referenceTouches leftTouches rightTouches
      referenceRealized leftRealized rightRealized
      leftUp rightUp different
  have blocked : candidate ≠ forcedThirdFrom reference left right :=
    admissible.differs_from_realized_neighbors
      thirdNeighbor (forcedThirdFrom reference left right)
      thirdTouches thirdRealized
  exact blocked forced

/-! ## 4. One readable collapse spine -/

/--
The phase-3 imagination algebra in one theorem:

* a fixed reference exposes exactly three nonidentity phase shifts;
* one additional constraint leaves a two-state residue;
* two additional constraints force the unique third;
* three additional constraints exhaust the surface;
* two distinct phase shifts interface by forcing that unique third.

This is a reduction of possibility space, not a bound on how long imaginary
traversal may run.
-/
theorem phase3_constraint_collapse_spine
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    (imaginaryAlternatives reference).length = 3 ∧
    (∀ state : V4,
      UpwardFrom reference state →
      state ≠ left →
        state = right ∨
          state = forcedThirdFrom reference left right) ∧
    (∀ state : V4,
      UpwardFrom reference state →
      state ≠ left →
      state ≠ right →
        state = forcedThirdFrom reference left right) ∧
    (∀ state : V4,
      UpwardFrom reference state →
      state ≠ left →
      state ≠ right →
      state ≠ forcedThirdFrom reference left right →
        False) := by
  refine ⟨imaginaryAlternatives_length reference, ?_, ?_, ?_⟩
  · intro state stateUp state_ne_left
    exact one_additional_constraint_leaves_two_state_residue
      reference left right state leftUp rightUp different
      stateUp state_ne_left
  · intro state stateUp state_ne_left state_ne_right
    exact two_additional_constraints_force_unique_remaining_state
      reference left right state leftUp rightUp different
      stateUp state_ne_left state_ne_right
  · intro state stateUp state_ne_left state_ne_right state_ne_third
    exact three_additional_constraints_exhaust_step3_surface
      reference left right state leftUp rightUp different
      stateUp state_ne_left state_ne_right state_ne_third

end MeTTafy.FourColor

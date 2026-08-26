import examples.four_color.RedTeamComposition

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A game-theoretic construct grammar for the Four Color research lane.

FRAME CONTRACT
--------------
This file does not enumerate pictures and call the enumeration complete.
Instead, any local construct may enter the grammar if it exposes only the
operational facts needed by the game:

* which upward states have already acted;
* which upward states remain available;
* acted and available states are genuinely non-reference states;
* void prevents an already-acted state from being available again on the same
  local action surface.

Meta-constructs are finite recursive compositions of such local constructs.
Composition unions acted obligations and intersects remaining opportunities.
That is a game-semantic composition, not a claim that arbitrary sequential
Kempe turns commute geometrically.

A basic stripe is one simple generator.  The familiar three-upward red-team
surface is then exhibited as a composition of three stripes rather than made
into privileged ontology.  Other constructions may be added as ordinary local
constructs and composed through the same interface.

An empty meta-construct is a fresh local start: no upward state has acted and
all upward states are available.  When a composed surface has no available
upward state, the local game is stopped.  Choosing another void is a fresh
start outside that exhausted surface; this file does not choose the restart.
-/

namespace MeTTafy.FourColor

/--
The minimal operational interface for one local game construct.

Geometry may justify a construct elsewhere.  This structure records only the
facts required to compose its game behavior without promoting any particular
geometric picture to universal status.
-/
structure LocalConstruct (reference : V4) where
  acted : V4 → Prop
  available : V4 → Prop
  actedUpward : ∀ state, acted state → UpwardFrom reference state
  availableUpward : ∀ state, available state → UpwardFrom reference state
  voidBlocks : VoidBlocksActed acted available

/--
A finite grammar of game-theoretic meta-constructs.

`atom` accepts any local construct.  `compose` therefore scales by interface,
not by extending a closed enum of named patterns.
-/
inductive MetaConstruct (reference : V4) where
  | empty
  | atom (local : LocalConstruct reference)
  | compose (left right : MetaConstruct reference)

namespace MetaConstruct

/-- A composed surface has acted wherever either child has acted. -/
def acted {reference : V4} : MetaConstruct reference → V4 → Prop
  | .empty, _ => False
  | .atom local, state => local.acted state
  | .compose left right, state => acted left state ∨ acted right state

/--
An action remains available through a composition only when every composed
constraint still permits it.  The empty/fresh-start surface permits every
non-reference state.
-/
def available {reference : V4} : MetaConstruct reference → V4 → Prop
  | .empty, state => UpwardFrom reference state
  | .atom local, state => local.available state
  | .compose left right, state => available left state ∧ available right state

/-- Every acted state in a meta-construct is genuinely upward/non-reference. -/
theorem acted_upward
    {reference : V4}
    (construct : MetaConstruct reference)
    (state : V4) :
    acted construct state → UpwardFrom reference state := by
  induction construct with
  | empty =>
      intro impossible
      exact False.elim impossible
  | atom local =>
      exact local.actedUpward state
  | compose left right leftIH rightIH =>
      intro actedHere
      rcases actedHere with actedLeft | actedRight
      · exact leftIH actedLeft
      · exact rightIH actedRight

/-- Every available state in a meta-construct is genuinely upward/non-reference. -/
theorem available_upward
    {reference : V4}
    (construct : MetaConstruct reference)
    (state : V4) :
    available construct state → UpwardFrom reference state := by
  induction construct with
  | empty =>
      intro upward
      exact upward
  | atom local =>
      exact local.availableUpward state
  | compose left right leftIH rightIH =>
      intro availableHere
      exact leftIH availableHere.1

/--
Void-blocking is preserved by arbitrary finite construct composition.

This is the central closure fact for the grammar: a composed meta-construct
cannot make an already-consumed local action available again merely by adding
another compatible game constraint.
-/
theorem void_blocks_acted
    {reference : V4}
    (construct : MetaConstruct reference) :
    VoidBlocksActed (acted construct) (available construct) := by
  induction construct with
  | empty =>
      intro state impossible
      exact False.elim impossible
  | atom local =>
      exact local.voidBlocks
  | compose left right leftIH rightIH =>
      intro state actedHere availableHere
      rcases actedHere with actedLeft | actedRight
      · exact leftIH state actedLeft availableHere.1
      · exact rightIH state actedRight availableHere.2

/-- The complete game-coherence contract inherited by every meta-construct. -/
def GameCoherent
    {reference : V4}
    (construct : MetaConstruct reference) : Prop :=
  (∀ state, acted construct state → UpwardFrom reference state) ∧
  (∀ state, available construct state → UpwardFrom reference state) ∧
  VoidBlocksActed (acted construct) (available construct)

/-- Every recursively composed construct satisfies the declared game contract. -/
theorem game_coherent
    {reference : V4}
    (construct : MetaConstruct reference) :
    GameCoherent construct := by
  exact ⟨acted_upward construct, available_upward construct, void_blocks_acted construct⟩

/-- No upward action remains on this local composed surface. -/
def Stopped
    {reference : V4}
    (construct : MetaConstruct reference) : Prop :=
  UpwardGameStopped reference (available construct)

/-- At least one upward action remains on this local composed surface. -/
def HasAction
    {reference : V4}
    (construct : MetaConstruct reference) : Prop :=
  ∃ state, UpwardFrom reference state ∧ available construct state

/-- Stop is exactly absence of a remaining upward action. -/
theorem stopped_iff_no_action
    {reference : V4}
    (construct : MetaConstruct reference) :
    Stopped construct ↔ ¬ HasAction construct := by
  constructor
  · intro stopped hasAction
    rcases hasAction with ⟨state, upward, availableHere⟩
    exact stopped state upward availableHere
  · intro noAction state upward availableHere
    exact noAction ⟨state, upward, availableHere⟩

/--
A fresh local start has no acted state and exposes every upward state.
This is the local semantic target of a restart at another void; restart
selection itself remains external to the exhausted surface.
-/
theorem empty_is_fresh_start
    (reference state : V4) :
    (¬ acted (MetaConstruct.empty : MetaConstruct reference) state) ∧
    (available (MetaConstruct.empty : MetaConstruct reference) state ↔
      UpwardFrom reference state) := by
  constructor
  · intro impossible
    exact impossible
  · constructor <;> intro upward <;> exact upward

end MetaConstruct

/-! ## Basic stripe generator -/

/--
The simplest action construct: one upward state has acted, while every other
upward state remains available.

"Stripe" names this minimal repeated-contact/game pattern; no Euclidean stripe
geometry is asserted by this definition.
-/
def basicStripe
    (reference state : V4)
    (stateUp : UpwardFrom reference state) :
    LocalConstruct reference where
  acted := fun candidate => candidate = state
  available := fun candidate => UpwardFrom reference candidate ∧ candidate ≠ state
  actedUpward := by
    intro candidate equal
    subst candidate
    exact stateUp
  availableUpward := by
    intro candidate availableHere
    exact availableHere.1
  voidBlocks := by
    intro candidate actedHere availableHere
    exact availableHere.2 actedHere

/-- Promote one basic stripe into the generic meta-construct grammar. -/
def stripeMeta
    (reference state : V4)
    (stateUp : UpwardFrom reference state) :
    MetaConstruct reference :=
  .atom (basicStripe reference state stateUp)

/-- A stripe records its generating state as acted. -/
theorem stripe_acts_generator
    (reference state : V4)
    (stateUp : UpwardFrom reference state) :
    MetaConstruct.acted (stripeMeta reference state stateUp) state := by
  rfl

/-- A stripe leaves every different upward state available. -/
theorem stripe_leaves_other_upward_available
    (reference stripeState candidate : V4)
    (stripeUp : UpwardFrom reference stripeState)
    (candidateUp : UpwardFrom reference candidate)
    (different : candidate ≠ stripeState) :
    MetaConstruct.available (stripeMeta reference stripeState stripeUp) candidate := by
  exact ⟨candidateUp, different⟩

/-! ## The red-team surface as an ordinary composition -/

/--
Compose the two interacting upward states and their V4-forced third from three
ordinary stripes.  The red-team example is therefore generated by the same
construct grammar available to simpler and future patterns.
-/
def threeUpwardMeta
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    MetaConstruct reference :=
  .compose
    (stripeMeta reference left leftUp)
    (.compose
      (stripeMeta reference right rightUp)
      (stripeMeta
        reference
        (forcedThirdFrom reference left right)
        (forcedThird_ne_reference reference left right leftUp rightUp different)))

/-- The first generating upward state has acted in the three-stripe composite. -/
theorem threeUpwardMeta_left_acted
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    MetaConstruct.acted
      (threeUpwardMeta reference left right leftUp rightUp different)
      left := by
  exact Or.inl rfl

/-- The second generating upward state has acted in the three-stripe composite. -/
theorem threeUpwardMeta_right_acted
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    MetaConstruct.acted
      (threeUpwardMeta reference left right leftUp rightUp different)
      right := by
  exact Or.inr (Or.inl rfl)

/-- The V4-forced third upward state has acted in the three-stripe composite. -/
theorem threeUpwardMeta_forcedThird_acted
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    MetaConstruct.acted
      (threeUpwardMeta reference left right leftUp rightUp different)
      (forcedThirdFrom reference left right) := by
  exact Or.inr (Or.inr rfl)

/--
Three composed stripe generators exhaust the complete upward V4 action surface.
The generic composition law supplies void-blocking; no separate termination
ranking or red-team-specific stop mechanism is needed.
-/
theorem threeUpwardMeta_stops
    (reference left right : V4)
    (leftUp : UpwardFrom reference left)
    (rightUp : UpwardFrom reference right)
    (different : left ≠ right) :
    MetaConstruct.Stopped
      (threeUpwardMeta reference left right leftUp rightUp different) := by
  apply all_three_upward_acted_and_void_blocked_stop_game
    reference left right leftUp rightUp different
    (MetaConstruct.acted
      (threeUpwardMeta reference left right leftUp rightUp different))
    (MetaConstruct.available
      (threeUpwardMeta reference left right leftUp rightUp different))
  · exact threeUpwardMeta_left_acted reference left right leftUp rightUp different
  · exact threeUpwardMeta_right_acted reference left right leftUp rightUp different
  · exact threeUpwardMeta_forcedThird_acted reference left right leftUp rightUp different
  · exact MetaConstruct.void_blocks_acted
      (threeUpwardMeta reference left right leftUp rightUp different)

/-- Canonical A=0, B=a, C=b, D=c instance of the generic three-stripe stop. -/
theorem canonical_BCD_meta_stops :
    MetaConstruct.Stopped
      (threeUpwardMeta V4.zero V4.a V4.b
        (by simp [UpwardFrom])
        (by simp [UpwardFrom])
        (by simp)) := by
  exact threeUpwardMeta_stops
    V4.zero V4.a V4.b
    (by simp [UpwardFrom])
    (by simp [UpwardFrom])
    (by simp)

end MeTTafy.FourColor

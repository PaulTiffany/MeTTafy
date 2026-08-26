/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

A deliberately small Lean kernel for the Four Color research game.

FRAME CONTRACT
--------------
This module reasons from the formal global view of a finite Four Color state.
The checker may inspect the entire retained coloring needed by a theorem.
That God's-eye proof frame is a modeling choice for this combinatorial program;
it is not a claim that an embedded physical observer has the same information.

Time is construction order only.  This file introduces no asynchronous update,
delay, Markov-blanket, subjective-phase, future-route, or observer-dynamics
coordinate.  Those questions belong outside the Four Color theorem kernel unless
a later proof obligation mechanically requires them.
-/

namespace MeTTafy.FourColor

/-- The Klein four palette, identified with Z2 x Z2. -/
inductive V4 where
  | zero
  | a
  | b
  | c
  deriving DecidableEq, Repr

/-- Klein-four addition. Every element is its own inverse. -/
def add : V4 → V4 → V4
  | .zero, x => x
  | x, .zero => x
  | .a, .a => .zero
  | .a, .b => .c
  | .a, .c => .b
  | .b, .a => .c
  | .b, .b => .zero
  | .b, .c => .a
  | .c, .a => .b
  | .c, .b => .a
  | .c, .c => .zero

/-- In characteristic two, color difference is addition. -/
def difference (left right : V4) : V4 := add left right

theorem add_zero (x : V4) : add x .zero = x := by
  cases x <;> rfl

theorem zero_add (x : V4) : add .zero x = x := by
  rfl

theorem add_self (x : V4) : add x x = .zero := by
  cases x <;> rfl

theorem add_comm (x y : V4) : add x y = add y x := by
  cases x <;> cases y <;> rfl

theorem add_assoc (x y z : V4) : add (add x y) z = add x (add y z) := by
  cases x <;> cases y <;> cases z <;> rfl

theorem difference_zero_iff_eq (left right : V4) :
    difference left right = .zero ↔ left = right := by
  cases left <;> cases right <;> simp [difference, add]

theorem difference_nonzero_iff_ne (left right : V4) :
    difference left right ≠ .zero ↔ left ≠ right := by
  cases left <;> cases right <;> simp [difference, add]

/-- A cyclic five-region frontier. -/
structure Boundary5 where
  c0 : V4
  c1 : V4
  c2 : V4
  c3 : V4
  c4 : V4
  deriving Repr

/-- Consecutive frontier regions are pairwise different, including the closing edge. -/
def ProperPentagon (boundary : Boundary5) : Prop :=
  boundary.c0 ≠ boundary.c1 ∧
  boundary.c1 ≠ boundary.c2 ∧
  boundary.c2 ≠ boundary.c3 ∧
  boundary.c3 ≠ boundary.c4 ∧
  boundary.c4 ≠ boundary.c0

/-- Every frontier region differs from one fixed central region. -/
def SaturatedAround (center : V4) (boundary : Boundary5) : Prop :=
  center ≠ boundary.c0 ∧
  center ≠ boundary.c1 ∧
  center ≠ boundary.c2 ∧
  center ≠ boundary.c3 ∧
  center ≠ boundary.c4

/-- The five tangential V4 differences around the cyclic frontier. -/
def edgeMode0 (boundary : Boundary5) : V4 := difference boundary.c0 boundary.c1
def edgeMode1 (boundary : Boundary5) : V4 := difference boundary.c1 boundary.c2
def edgeMode2 (boundary : Boundary5) : V4 := difference boundary.c2 boundary.c3
def edgeMode3 (boundary : Boundary5) : V4 := difference boundary.c3 boundary.c4
def edgeMode4 (boundary : Boundary5) : V4 := difference boundary.c4 boundary.c0

/-- Cyclic sum of the five frontier differences. -/
def frontierClosure (boundary : Boundary5) : V4 :=
  add (edgeMode0 boundary)
    (add (edgeMode1 boundary)
      (add (edgeMode2 boundary)
        (add (edgeMode3 boundary) (edgeMode4 boundary))))

/-- The closed frontier telescopes to zero in V4. -/
theorem frontierClosure_zero (boundary : Boundary5) :
    frontierClosure boundary = .zero := by
  rcases boundary with ⟨c0, c1, c2, c3, c4⟩
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> cases c4 <;> rfl

/-- Count one nonzero mode on the five frontier edges. -/
def countMode (mode : V4) (boundary : Boundary5) : Nat :=
  (if edgeMode0 boundary = mode then 1 else 0) +
  (if edgeMode1 boundary = mode then 1 else 0) +
  (if edgeMode2 boundary = mode then 1 else 0) +
  (if edgeMode3 boundary = mode then 1 else 0) +
  (if edgeMode4 boundary = mode then 1 else 0)

/-- The three nonzero V4 mode counts have equal parity on every closed five-frontier. -/
def SameModeParity (boundary : Boundary5) : Prop :=
  countMode .a boundary % 2 = countMode .b boundary % 2 ∧
  countMode .b boundary % 2 = countMode .c boundary % 2

theorem frontier_mode_counts_same_parity (boundary : Boundary5) :
    SameModeParity boundary := by
  rcases boundary with ⟨c0, c1, c2, c3, c4⟩
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> cases c4 <;>
    simp [SameModeParity, countMode, edgeMode0, edgeMode1, edgeMode2, edgeMode3,
      edgeMode4, difference, add]

/--
The degree-five 3-1-1 law, stated without choosing which nonzero V4 mode is the
repeated one.
-/
def DegreeFive311 (boundary : Boundary5) : Prop :=
  (countMode .a boundary = 3 ∧ countMode .b boundary = 1 ∧ countMode .c boundary = 1) ∨
  (countMode .a boundary = 1 ∧ countMode .b boundary = 3 ∧ countMode .c boundary = 1) ∨
  (countMode .a boundary = 1 ∧ countMode .b boundary = 1 ∧ countMode .c boundary = 3)

/--
A proper pentagonal frontier saturated around one fixed region has tangential
V4 mode multiplicities 3,1,1.  This is the finite algebraic core currently
mirrored by `src/mettafy/plane_parameterization.py`.
-/
theorem saturated_proper_pentagon_has_311
    (center : V4)
    (boundary : Boundary5)
    (proper : ProperPentagon boundary)
    (saturated : SaturatedAround center boundary) :
    DegreeFive311 boundary := by
  rcases boundary with ⟨c0, c1, c2, c3, c4⟩
  cases center <;>
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> cases c4 <;>
    simp [ProperPentagon, SaturatedAround, DegreeFive311, countMode, edgeMode0,
      edgeMode1, edgeMode2, edgeMode3, edgeMode4, difference, add] at *

end MeTTafy.FourColor

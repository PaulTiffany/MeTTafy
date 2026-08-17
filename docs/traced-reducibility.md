# Traced reducibility contract

MeTTafy may promote a candidate transformation as a certified `Reduction` only when three independent mechanical obligations hold:

1. **Boundary preservation** — the source and reduced states have the same observable boundary signature.
2. **Strict descent** — an explicit nonnegative obstruction measure strictly decreases.
3. **Verified lift** — a mechanical witness establishes that a solution or witness on the reduced state extends back to the source obligation.

Formally, for a source state `x` and reduced state `y`, certification requires

\[
B(x)=B(y),\qquad \mu(y)<\mu(x),\qquad L(y\Rightarrow x)=\mathrm{verified}.
\]

These obligations are intentionally independent. A smaller object with a changed boundary is a different problem. A boundary-preserving object without strict descent does not support well-founded reduction. A smaller boundary-preserving object whose witness does not lift may solve only the reduced problem.

A successful certificate may authorize a `Reduction` Strategy IR node through the sibling provenance graph. The public Strategy serialization contract is unchanged.

`WIT-TRACED-REDUCIBILITY` includes one positive case and three fail-closed counterexamples: boundary drift, no strict descent, and failed lift.

## Four Color claim boundary

This contract is a reusable reducibility interface, not a proof of the Four Color Theorem. The pinned Rocq proof exposes `StructuralReduction`, `MinimalCounterexample`, `Unavoidability`, and `Reducibility` as held-out strategy labels for the high-level combinatorial theorem, but those labels remain outside recognition. The next obligation is to map mechanical artifacts from the pinned proof into the boundary, descent, and lift fields without using the held-out labels as classifier inputs.

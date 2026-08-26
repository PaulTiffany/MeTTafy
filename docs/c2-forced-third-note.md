# C2 forced-third bridge

This note records one bounded algebraic step in the independent Track-B Four Color research program.

Fix one palette state as the lower/reference state. Relative to that reference, the other three `V4` states are the only nontrivial upward states. If two distinct upward states interact, the remaining upward state is not a chooser output: it is forced by the Klein-four law.

For reference `r` and distinct upward states `x` and `y`, define

```text
z = r + x + y.
```

Then `z` is distinct from `r`, `x`, and `y`, and it is the unique palette state with that property. In the canonical gauge used by the C2 sketch,

```text
A = 0, B = a, C = b, D = c,
```

so

```text
B + C = D.
```

The Lean witness is [`examples/four_color/C2ForcedThird.lean`](../examples/four_color/C2ForcedThird.lean).

## What this does not prove

This result does **not** prove that the planar geometry forces two continuations to cross. It does not discharge `crosscut_meets_opposite`, the remaining planar/Jordan-style obligation isolated in [`C2ContactVoid.lean`](../examples/four_color/C2ContactVoid.lean).

The intended decomposition is therefore:

```text
planar boundary / void geometry
    -> forces the relevant interaction
V4 contact algebra
    -> fixes the unique third state at that interaction
```

The first arrow remains open. The second is now Lean-checkable.

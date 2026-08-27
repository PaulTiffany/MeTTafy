# Four Color Strategy-to-Color Projection

This note records the one-way transducer between the boundary-labelled Strategy IR and the color-level Reidemeister algebra.

The projection is deliberately weaker than equivalence.

```text
StrategyTangle
  -> grounded V4 color-word projection
  -> (stutter | ColorUncrossingStep)
  -> preserved color phase
```

## Grounded emissions

The four Strategy roles are identified with the existing Klein-four palette coordinates:

```text
A = 0, B = 1, C = 2, D = 3.
```

Only two primitive operations emit color content:

- `IntroduceRole(r)` emits the nonzero difference between the fixed anchor role and `r`;
- `Cross(left, right, sign)` emits the nonzero difference `left xor right`.

Every emitted direction carries provenance back to the exact Strategy operation that produced it. A projection is invalid if any emission cannot be replayed from that operation.

Crossing sign is intentionally forgotten at the color-algebra layer. Sign remains geometric information in Strategy space.

## Explicit stuttering

The following operations are color-silent at this layer:

- `Extend`;
- `Return`;
- `Probe`;
- `Periodic`.

They may change the Strategy presentation or bounded observer state without changing the projected color word. This is the formal stuttering channel.

Stuttering is not deletion of the source event. The projection receipt records which source operation was intentionally erased.

## Trivial crossing correspondence

For distinct roles `x != y`, both crossing orientations project to the same nonzero color direction

```text
d = x xor y.
```

Therefore an opposite-sign geometric crossing pair

```text
Cross(x,y,+), Cross(x,y,-)
```

projects to

```text
[d,d].
```

The color-level Lean witness already proves

```text
[d,d] -> []
```

by a local phase-preserving uncrossing. The new bridge proves the corresponding one-way statement:

```text
trivial geometric Strategy crossing
  -> repeated projected color direction
  -> local color uncrossing
  -> unchanged retained V4 phase.
```

This is the first mechanically checked StrategyTangle/color Reidemeister correspondence.

## Authority boundary

`StrategyColorProjection`, `ColorReidemeisterUncrossing`, and `StrategyColorSimulation` are all INFERENCE-only.

None may directly premise `StrategySafeContinuation`, `CertifiedInstantiation`, or realized construction. The existing completeness + inference-soundness bridge remains mandatory.

## Non-claims

This tranche does **not** prove:

- every geometric Strategy move has a color projection beyond the explicitly typed cases;
- every color uncrossing lifts to a geometric Strategy move;
- equality of geometric and color Reidemeister complexity;
- Strategy-IR completeness;
- the Four Color Theorem.

The next mathematical question is whether the one-way simulation yields a useful complexity bound, for example whether projected color uncrossing complexity is bounded above by the supported geometric staging complexity.

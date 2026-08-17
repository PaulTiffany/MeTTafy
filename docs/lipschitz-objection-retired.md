# Lipschitz Objection — Retired

**Status:** not a Four Color proof obligation.

## The objection

The discarded objection was:

> If chromatic refinement, browning-out, or terminal color commitment changes representation, then the underlying trajectory must make a discontinuous/non-Lipschitz jump. Therefore the proposed proof violates the Lipschitz contract.

That inference is false.

## What a Lipschitz contract actually controls

For a realization/evolution map `T`, a Lipschitz condition has the form

\[
d(Tx,Ty)\le L\,d(x,y).
\]

It bounds amplification of perturbations. It does **not** bound the cardinality of a later quotient, forbid multiple basins of attraction, or require an observer's discrete label map to be continuous.

The Principia differential substrate is itself compatible with local regularity: the symbolic Fokker--Planck evolution

\[
\partial_s\rho=-\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho
\]

is a continuous drift--diffusion evolution under the declared regularity hypotheses. The diffusion term is smoothing.

A discrete terminal chromatic observation may be represented separately by a quotient/decoder

\[
Q_O:\rho\mapsto q_i.
\]

A basin boundary can make `Q_O` discontinuous as a **label map** while the underlying density trajectory remains continuous and regular. No rupture of the differential dynamics follows.

## Browning-out does not require rupture

Browning-out is coarse-graining/amortization of microscopic chromatic provenance under the smooth dynamics and observer quotient. It may reduce terminal discriminability without erasing the underlying trajectory or indexed edge obligations.

Thus

```text
smooth drift--diffusion
  -> contraction / relaxation
  -> observer quotient
  -> brown or terminal label
```

is entirely compatible with a bounded realization map.

## Relation to the Cost-of-Cacophony pivot result

The earlier Cost-of-Cacophony 'pivot regime' used a different Lipschitz contract: bounded per-step movement in an embedding trajectory. A pivot was an empirical failure of that one-shot smooth-trajectory assumption. That result does not imply that every representation change in Principia is a pivot, nor that Four Color refinement requires a contract violation.

Amortized/staged dynamics can change the effective state and observer while each declared transformation remains bounded in its own state space.

## What remains load-bearing

The Four Color proof does **not** owe a `LipschitzViolation` lemma.

The real unresolved theorem is algebraic/topological:

\[
\text{planar chromatic constraints}
\Longrightarrow
\text{at most four independently terminal chromatic classes}.
\]

Equivalently, in the differential formulation, one must prove that the planar-admissible chromatic dynamics cannot support a fifth independent terminal mode/basin satisfying all indexed adjacency obligations.

Lipschitz regularity may be retained throughout that derivation. It neither proves nor obstructs the four-class bound.

## Dependency rule for MeTTa

The proof graph must treat the following as invalid blockers:

```text
representation change -> non-Lipschitz
terminal quotient -> non-Lipschitz
browning-out -> non-Lipschitz
SRMF route change -> non-Lipschitz
```

A claimed Lipschitz failure is relevant only if an explicit realization map `T` and metric are supplied and the inequality is actually violated.

Therefore the generic **Lipschitz violation strawman is retired** from Track B.
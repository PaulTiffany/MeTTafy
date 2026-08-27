# Four Color Strategy IR: ugly adversarial corpus

This tranche pressures the Strategy-IR quotient with cases that are deliberately
less tidy than the first pairwise corpus.

The goal is still not to guess a global number of strategy classes. The goal is
to discover which pieces of a long same-turn imagination trace are actually
proof-relevant to the bounded MapMaker.

## Stable normalizer versus experimental pressure

The merged staging normalizer remains unchanged.

The ugly corpus adds a separate experimental preprocessor with two explicit
hypotheses:

1. **Disjoint non-observational commutation**: same-frame imaginary work may be
   reordered only when the operations have disjoint role support and neither
   operation is a probe or a role introduction.
2. **Response-complete suffix cut**: a caller may name a probe after which later
   imaginary work is quotient-irrelevant.

Neither hypothesis is inferred from appearance. Each must be supplied in the
normalization policy for the challenge that uses it.

The response-complete cut happens before rebuilding the role ledger. A color role
introduced only after the cut therefore cannot silently consume independent role
freedom.

## Ugly motifs

The corpus includes:

- a 20-extension alternating recurrence stress inspired by the historical Errera
  recurrence phenomenon;
- inverse crossings separated by independent work;
- Extend/Return excursions wrapped around independent crossings;
- long re-entry tails after a response-complete probe;
- a role introduced only after the declared stopping observation;
- a pre-probe observation that must survive suffix garbage collection;
- a surviving crossing obstruction inspired by the Heawood/Kempe failure mode;
- an incomplete red-team recurrence prefix;
- mirror plus periodic re-entry composition.

The historical names identify stress motifs only. The fixtures are not exact
reconstructions of the Errera graph, Heawood's counterexample, or a historical
Kempe exchange sequence.

## Two-sided falsification

Every new compression mechanism is attacked from both directions.

Examples:

- inverse crossings separated by disjoint work should collapse **only** when
  disjoint commutation is explicitly authorized;
- a long suffix after `safe-option` should disappear **only** when that probe is
  explicitly declared response-complete;
- the same cut must not erase an observation that occurred before the probe;
- an incomplete recurrence must not be silently promoted to `Periodic`;
- periodic folding alone must not authorize mirror equivalence.

A failure therefore has an interpretation:

- **under-compression**: known projection noise survived;
- **over-compression**: a proof-relevant distinction disappeared;
- **missing observable**: the current Strategy IR cannot state why two cases
  should differ.

## Authority boundary

Everything in this corpus is INFERENCE.

A passing ugly audit is not:

- `FiniteResponseCompleteNormalForms`;
- `StrategyIRCompleteness`;
- `InferenceSoundness`;
- `StrategySafeContinuation`;
- `CertifiedInstantiation`;
- a proof of the Four Color Theorem.

The extra policies alter only how an imaginary trace is compared with another
imaginary trace. They do not recolor the realized map and they do not authorize
`⊥ -> c`.

## Operational checksum

> Stop counting how long imagination ran. Test which observations still change
> the decision after the tangle is unknotted.

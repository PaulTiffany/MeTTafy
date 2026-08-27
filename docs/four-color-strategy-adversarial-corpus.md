# Four Color Strategy Adversarial Corpus

Status: **inference experiment, not a Four Color proof**.

This tranche tests the working hypothesis that MapMaker imagination is a projected strategy tangle whose proof-relevant complexity is much smaller than its serialized chain-of-thought length.

## The object under test

The quotient is not over maps and not over raw recoloring histories. It is over same-turn strategy presentations after Unweave and Reidemeister-like staging:

```text
roleplay
  -> raw typed operations
  -> boundary-labelled strategy tangle
  -> staging / uncrossing
  -> strategy normal form
```

Construction time does not advance anywhere in that pipeline.

## Two-sided falsification

A useful quotient can fail in two opposite ways.

### Under-compression

Projection noise survives as fake strategy complexity. Examples in the corpus include:

- longer `BCBC...` recurrence;
- an `Extend/Return` excursion;
- opposed crossing pairs;
- disjoint reasoning/inspection operations presented in a different order;
- color-name permutations;
- mirror presentations when mirror equivalence is explicitly authorized.

These pairs are expected to **collapse**.

### Over-compression

A proof-relevant distinction is erased. Examples include:

- mirror presentations when reflection has not been authorized;
- a different available first-move option;
- a different response class;
- a different number of remaining independent color roles;
- operation order on shared role support;
- asking a different proof-relevant question;
- introducing the last unused role after a periodic recurrence.

These pairs are expected to **split**.

Every challenge names the observable that justifies its local claim. A failure therefore identifies a missing or excess distinction in the Strategy IR instead of merely adding another concrete map case.

## What is measured

`strategy_quotient_audit.py` reports:

- number of collapse challenges;
- number of split challenges;
- challenge failures;
- raw presentations;
- the **discovered** number of normal forms;
- empirical compression ratio.

No target such as 9 or 10 classes is encoded.

Run:

```bash
python scripts/report_four_color_strategy_adversaries.py
```

## Epistemic boundary

Passing this corpus is evidence that the proposed quotient survived these attacks. It is not `NormalFormCompleteness`, `StrategyIRCompleteness`, `InferenceSoundness`, or a certificate for realized construction.

The authority lane remains:

```text
finite / response-complete normal-form theorem       OPEN
  -> StrategyIRCompleteness                          OPEN
  + InferenceSoundness
  -> StrategySafeContinuation
  -> CertifiedInstantiation
  -> one realized void instantiation
```

The corpus is deliberately off that authority path.

## Research loop

When a challenge fails:

```text
counterexample
  -> identify the exact missing/excess observable
  -> minimally split or merge the Strategy IR
  -> rerun the whole corpus
```

The goal is not to protect a preferred class count. The goal is to discover the smallest response-complete vocabulary that survives adversarial roleplay.

**Checksum:** do not enumerate the imaginary maze; falsify what counts as the same decision.

from __future__ import annotations

from dataclasses import dataclass, field

from mettafy.strategy_staging import (
    Cross,
    Extend,
    IntroduceRole,
    NormalizationPolicy,
    Periodic,
    PrimitiveOp,
    Probe,
    RawStrategyTrace,
    Return,
    StagedOperation,
    StagingMetrics,
    StrategyNormalForm,
    StrategyTangle,
    normalize_strategy_tangle,
)


@dataclass(frozen=True)
class UglyNormalizationPolicy:
    """INFERENCE: explicit extra quotient assumptions for adversarial pressure.

    These assumptions are intentionally outside the stable normalizer. They are
    hypotheses to falsify on ugly fixtures, not construction rules.
    """

    base: NormalizationPolicy = field(default_factory=NormalizationPolicy)
    commute_disjoint_nonobservational: bool = False
    cut_after_probe_labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class UglyStagingMetrics:
    """INFERENCE: preprocessing pressure plus the stable staging metrics."""

    disjoint_commutations: int
    suffix_operations_dropped: int
    base: StagingMetrics


def _roles(op: PrimitiveOp) -> tuple[str, ...]:
    if isinstance(op, (IntroduceRole, Extend, Return)):
        return (op.role,)
    if isinstance(op, Cross):
        return (op.left, op.right)
    if isinstance(op, Probe):
        return op.roles
    return op.cycle


def _op_key(operation: StagedOperation) -> tuple[str, ...]:
    op = operation.op
    if isinstance(op, Cross):
        return ("0-cross", op.left, op.right, str(op.sign))
    if isinstance(op, Extend):
        return ("1-extend", op.role)
    if isinstance(op, Return):
        return ("2-return", op.role)
    if isinstance(op, Periodic):
        return ("3-periodic", *op.cycle)
    if isinstance(op, IntroduceRole):
        return ("4-introduce", op.role)
    return ("5-probe", op.label, *op.roles)


def _can_commute(left: StagedOperation, right: StagedOperation) -> bool:
    """Only same-frame, non-observational work on disjoint support may commute."""

    if left.frame != right.frame:
        return False
    if isinstance(left.op, (IntroduceRole, Probe)):
        return False
    if isinstance(right.op, (IntroduceRole, Probe)):
        return False
    return not bool(set(_roles(left.op)) & set(_roles(right.op)))


def _commute_disjoint_nonobservational(
    trace: RawStrategyTrace,
) -> tuple[RawStrategyTrace, int]:
    """Canonicalize explicitly independent same-frame imaginary work."""

    operations = list(trace.operations)
    count = 0
    changed = True
    while changed:
        changed = False
        for index in range(len(operations) - 1):
            left = operations[index]
            right = operations[index + 1]
            if not _can_commute(left, right):
                continue
            if _op_key(left) <= _op_key(right):
                continue
            operations[index], operations[index + 1] = right, left
            count += 1
            changed = True
    return RawStrategyTrace(trace.anchor, tuple(operations)), count


def _cut_after_probe(
    trace: RawStrategyTrace,
    labels: tuple[str, ...],
) -> tuple[RawStrategyTrace, int]:
    """Discard only a suffix explicitly declared irrelevant after one probe.

    The cut happens before the role ledger is rebuilt. A role introduced only in
    the discarded suffix therefore cannot silently consume independent freedom.
    """

    if not labels:
        return trace, 0
    allowed = set(labels)
    for index, operation in enumerate(trace.operations):
        op = operation.op
        if isinstance(op, Probe) and op.label in allowed:
            kept = trace.operations[: index + 1]
            return RawStrategyTrace(trace.anchor, kept), len(trace.operations) - len(kept)
    return trace, 0


def preprocess_ugly_tangle(
    tangle: StrategyTangle,
    policy: UglyNormalizationPolicy,
) -> tuple[StrategyTangle, int, int]:
    """INFERENCE: apply only the extra quotient assumptions named by the caller."""

    trace, dropped = _cut_after_probe(tangle.raw, policy.cut_after_probe_labels)
    commutations = 0
    if policy.commute_disjoint_nonobservational:
        trace, commutations = _commute_disjoint_nonobservational(trace)
    return (
        StrategyTangle(raw=trace, boundary=tangle.boundary, signature=tangle.signature),
        commutations,
        dropped,
    )


def normalize_ugly_strategy_tangle(
    tangle: StrategyTangle,
    policy: UglyNormalizationPolicy = UglyNormalizationPolicy(),
) -> tuple[StrategyNormalForm, UglyStagingMetrics]:
    """INFERENCE: pressure-test extra quotient hypotheses, then use stable staging."""

    prepared, commutations, dropped = preprocess_ugly_tangle(tangle, policy)
    normal, base_metrics = normalize_strategy_tangle(prepared, policy.base)
    return normal, UglyStagingMetrics(
        disjoint_commutations=commutations,
        suffix_operations_dropped=dropped,
        base=base_metrics,
    )

from __future__ import annotations

from mettafy.strategy_ir import StrategySignature
from mettafy.strategy_staging import (
    ColorRole,
    Cross,
    Extend,
    IntroduceRole,
    NormalizationPolicy,
    PrimitiveOp,
    Probe,
    RawStrategyTrace,
    Return,
    StagedOperation,
    StageFrame,
    StrategyTangle,
)
from mettafy.strategy_ugly_quotient_audit import UglyQuotientChallenge
from mettafy.strategy_ugly_staging import UglyNormalizationPolicy


def _stage(frame: StageFrame, op: PrimitiveOp) -> StagedOperation:
    return StagedOperation(frame, op)


def _tangle(
    operations: tuple[StagedOperation, ...],
    boundary: tuple[ColorRole, ...],
    *,
    response_classes: tuple[str, ...] = ("stable",),
    options: tuple[str, ...] = ("first-move-A",),
) -> StrategyTangle:
    return StrategyTangle(
        raw=RawStrategyTrace("A", operations),
        boundary=boundary,
        signature=StrategySignature(
            response_classes=response_classes,
            options=options,
        ),
    )


def _periodic(repetitions: int) -> StrategyTangle:
    repeated = tuple(
        _stage("analysis", Extend(role))
        for _ in range(repetitions)
        for role in ("B", "C")
    )
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            *repeated,
            _stage("inspection", Probe("recurrence-response", ("B", "C"))),
        ),
        ("A", "B", "C", "A"),
        response_classes=("periodic", "reenters"),
        options=("continue-A",),
    )


def _cross_bridge(*, noisy: bool) -> StrategyTangle:
    middle: tuple[StagedOperation, ...]
    if noisy:
        middle = (
            _stage("analysis", Cross("B", "C", 1)),
            _stage("analysis", Extend("D")),
            _stage("analysis", Cross("B", "C", -1)),
        )
    else:
        middle = (_stage("analysis", Extend("D")),)
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("D")),
            *middle,
            _stage("inspection", Probe("after-cross", ("B", "C", "D"))),
        ),
        ("A", "B", "C", "D"),
        response_classes=("crossing-cleared",),
    )


def _r1_bridge(*, noisy: bool) -> StrategyTangle:
    middle: tuple[StagedOperation, ...]
    if noisy:
        middle = (
            _stage("analysis", Extend("B")),
            _stage("analysis", Cross("C", "D", 1)),
            _stage("analysis", Return("B")),
        )
    else:
        middle = (_stage("analysis", Cross("C", "D", 1)),)
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("D")),
            *middle,
            _stage("inspection", Probe("after-loop", ("B", "C", "D"))),
        ),
        ("A", "B", "C", "D"),
        response_classes=("loop-cleared",),
    )


def _safe_probe() -> StrategyTangle:
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("safe-option", ("B", "C"))),
        ),
        ("A", "B", "C"),
        response_classes=("opens",),
        options=("safe-A",),
    )


def _safe_probe_with_reentry_tail() -> StrategyTangle:
    tail = tuple(
        _stage("analysis", Extend(role))
        for _ in range(6)
        for role in ("B", "C")
    )
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("safe-option", ("B", "C"))),
            *tail,
            _stage("analysis", Cross("B", "C", 1)),
            _stage("analysis", Cross("B", "C", -1)),
        ),
        ("A", "B", "C"),
        response_classes=("opens",),
        options=("safe-A",),
    )


def _safe_probe_with_post_role() -> StrategyTangle:
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("safe-option", ("B", "C"))),
            _stage("reasoning", IntroduceRole("D")),
            _stage("analysis", Extend("D")),
        ),
        ("A", "B", "C"),
        response_classes=("opens",),
        options=("safe-A",),
    )


def _safe_probe_with_pre_observation() -> StrategyTangle:
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("analysis", Extend("B")),
            _stage("inspection", Probe("safe-option", ("B", "C"))),
        ),
        ("A", "B", "C"),
        response_classes=("opens",),
        options=("safe-A",),
    )


def _crossing_obstruction(*, crossed: bool) -> StrategyTangle:
    crossing = (
        (_stage("analysis", Cross("B", "C", 1)),) if crossed else ()
    )
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            *crossing,
            _stage("inspection", Probe("kempe-contact", ("B", "C"))),
        ),
        ("A", "B", "C", "A"),
        response_classes=("blocked",),
        options=("inspect-again",),
    )


def _incomplete_recurrence(*, complete: bool) -> StrategyTangle:
    repeated: tuple[StagedOperation, ...]
    if complete:
        repeated = (
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
        )
    else:
        repeated = (
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
            _stage("analysis", Extend("B")),
        )
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            *repeated,
            _stage("inspection", Probe("recurrence-response", ("B", "C"))),
        ),
        ("A", "B", "C", "A"),
        response_classes=("reenters",),
        options=("inspect-again",),
    )


def _mirrored_reentry(sign: int) -> StrategyTangle:
    cross_sign = 1 if sign > 0 else -1
    boundary: tuple[ColorRole, ...]
    if sign > 0:
        boundary = ("A", "B", "C", "D")
    else:
        boundary = ("D", "C", "B", "A")
    repeated = tuple(
        _stage("analysis", Extend(role))
        for _ in range(5)
        for role in ("B", "C")
    )
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("D")),
            *repeated,
            _stage("analysis", Cross("B", "C", cross_sign)),
            _stage("inspection", Probe("reentry-crossing", ("B", "C"))),
        ),
        boundary,
        response_classes=("periodic", "crossing"),
        options=("inspect-again",),
    )


def ugly_strategy_challenges() -> tuple[UglyQuotientChallenge, ...]:
    """INFERENCE: ugly pressure beyond the first synthetic quotient corpus.

    Historical names identify stress motifs only. These fixtures are not exact
    reconstructions of the historical maps or exchange sequences.
    """

    periodic_base = NormalizationPolicy(periodic_cycles=(("B", "C"),))
    periodic = UglyNormalizationPolicy(base=periodic_base)
    commute = UglyNormalizationPolicy(commute_disjoint_nonobservational=True)
    cut = UglyNormalizationPolicy(cut_after_probe_labels=("safe-option",))
    mirror_periodic = UglyNormalizationPolicy(
        base=NormalizationPolicy(
            mirror_equivalent=True,
            periodic_cycles=(("B", "C"),),
        )
    )

    return (
        UglyQuotientChallenge(
            "errera-inspired-20-step-recurrence-is-not-strategy-depth",
            _periodic(2),
            _periodic(10),
            periodic,
            "collapse",
            "twenty serialized alternating extensions add no new response class",
            "Errera-inspired recurrence stress; not an Errera graph reconstruction",
        ),
        UglyQuotientChallenge(
            "inverse-crossings-cancel-across-disjoint-work-when-authorized",
            _cross_bridge(noisy=False),
            _cross_bridge(noisy=True),
            commute,
            "collapse",
            "disjoint D work may commute past a BC inverse crossing pair",
            "nested projection noise",
        ),
        UglyQuotientChallenge(
            "inverse-crossings-stay-distinct-without-commutation-authority",
            _cross_bridge(noisy=False),
            _cross_bridge(noisy=True),
            UglyNormalizationPolicy(),
            "split",
            "the same visual cancellation is not inferred across staging without policy",
            "authority guard for nested projection noise",
        ),
        UglyQuotientChallenge(
            "extend-return-cancels-across-disjoint-crossing-when-authorized",
            _r1_bridge(noisy=False),
            _r1_bridge(noisy=True),
            commute,
            "collapse",
            "a B excursion is removable around independent CD work",
            "nested loop noise",
        ),
        UglyQuotientChallenge(
            "response-complete-probe-garbage-collects-reentry-tail",
            _safe_probe(),
            _safe_probe_with_reentry_tail(),
            cut,
            "collapse",
            "imaginary work after the declared response-complete probe is suffix noise",
            "bounded MapMaker stops before a full red-team exemplar",
        ),
        UglyQuotientChallenge(
            "reentry-tail-survives-without-response-complete-cut",
            _safe_probe(),
            _safe_probe_with_reentry_tail(),
            UglyNormalizationPolicy(),
            "split",
            "the audit may not invent a stopping point",
            "authority guard for bounded stopping",
        ),
        UglyQuotientChallenge(
            "post-probe-role-introduction-cannot-consume-freedom-after-cut",
            _safe_probe(),
            _safe_probe_with_post_role(),
            cut,
            "collapse",
            "a role introduced only in a discarded suffix cannot change the role ledger",
            "garbage collection before role accounting",
        ),
        UglyQuotientChallenge(
            "pre-probe-observation-survives-the-cut",
            _safe_probe(),
            _safe_probe_with_pre_observation(),
            cut,
            "split",
            "response-complete suffix collection must not erase earlier imagination",
            "bounded-observer arrow-of-time guard",
        ),
        UglyQuotientChallenge(
            "heawood-style-crossing-obstruction-survives-normalization",
            _crossing_obstruction(crossed=False),
            _crossing_obstruction(crossed=True),
            UglyNormalizationPolicy(),
            "split",
            "a surviving BC crossing is proof-relevant obstruction structure",
            "Heawood/Kempe crossing-obstruction motif; not an exact map reconstruction",
        ),
        UglyQuotientChallenge(
            "incomplete-red-team-recurrence-is-not-a-complete-cycle",
            _incomplete_recurrence(complete=True),
            _incomplete_recurrence(complete=False),
            periodic,
            "split",
            "a partial BC prefix cannot be promoted to Periodic without completing the cycle",
            "incomplete red-team exemplar",
        ),
        UglyQuotientChallenge(
            "mirror-plus-reentry-collapses-only-under-composed-policy",
            _mirrored_reentry(1),
            _mirrored_reentry(-1),
            mirror_periodic,
            "collapse",
            "authorized reflection and periodic folding compose without adding a class",
            "mirrored re-entry composition",
        ),
        UglyQuotientChallenge(
            "mirror-plus-reentry-remains-split-without-reflection-authority",
            _mirrored_reentry(1),
            _mirrored_reentry(-1),
            periodic,
            "split",
            "periodicity alone does not authorize reflection",
            "authority guard for mirrored re-entry composition",
        ),
    )

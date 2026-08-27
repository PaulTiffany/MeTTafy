from __future__ import annotations

from mettafy.strategy_ir import StrategySignature
from mettafy.strategy_quotient_audit import QuotientChallenge
from mettafy.strategy_staging import (
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


def _stage(frame: StageFrame, op: PrimitiveOp) -> StagedOperation:
    return StagedOperation(frame, op)


def _tangle(
    operations: tuple[StagedOperation, ...],
    boundary: tuple[str, ...],
    *,
    anchor: str = "A",
    response_classes: tuple[str, ...] = ("stable",),
    options: tuple[str, ...] = ("first-move-A",),
) -> StrategyTangle:
    # The fixtures below use only literal V4 role names. Keeping this small helper
    # local makes each adversarial claim readable as a MapMaker transcript.
    return StrategyTangle(
        raw=RawStrategyTrace(anchor, operations),  # type: ignore[arg-type]
        boundary=boundary,  # type: ignore[arg-type]
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
        response_classes=("periodic", "opens", "reenters"),
    )


def _base_probe(*, option: str = "first-move-A", response: str = "stable") -> StrategyTangle:
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("inspection", Probe("inspect-B", ("B",))),
        ),
        ("A", "B"),
        response_classes=(response,),
        options=(option,),
    )


def _mirror(sign: int) -> StrategyTangle:
    boundary = ("A", "B", "C", "D") if sign > 0 else ("D", "C", "B", "A")
    cross_sign = 1 if sign > 0 else -1
    return _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("D")),
            _stage("analysis", Cross("B", "C", cross_sign)),
            _stage("inspection", Probe("crossing-response", ("B", "C"))),
        ),
        boundary,
        response_classes=("crossing",),
    )


def adversarial_strategy_challenges() -> tuple[QuotientChallenge, ...]:
    """INFERENCE: attacks on both under-compression and over-compression.

    No global normal-form count is encoded. Every pair states only one local
    quotient claim and the observable that would falsify that claim.
    """

    periodic_policy = NormalizationPolicy(periodic_cycles=(("B", "C"),))
    mirror_policy = NormalizationPolicy(mirror_equivalent=True)

    r1_clean = _base_probe()
    r1_noisy = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("analysis", Extend("B")),
            _stage("analysis", Return("B")),
            _stage("inspection", Probe("inspect-B", ("B",))),
        ),
        ("A", "B"),
    )

    r2_clean = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("inspect-BC", ("B", "C"))),
        ),
        ("A", "B", "C"),
    )
    r2_noisy = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("analysis", Cross("B", "C", 1)),
            _stage("analysis", Cross("B", "C", -1)),
            _stage("inspection", Probe("inspect-BC", ("B", "C"))),
        ),
        ("A", "B", "C"),
    )

    staged_left = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("analysis", Extend("C")),
            _stage("inspection", Probe("inspect-B", ("B",))),
        ),
        ("A", "B", "C"),
    )
    staged_right = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("inspect-B", ("B",))),
            _stage("analysis", Extend("C")),
        ),
        ("A", "B", "C"),
    )

    shared_support_left = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("analysis", Extend("B")),
            _stage("inspection", Probe("inspect-B", ("B",))),
        ),
        ("A", "B"),
    )
    shared_support_right = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("inspection", Probe("inspect-B", ("B",))),
            _stage("analysis", Extend("B")),
        ),
        ("A", "B"),
    )

    color_rename_left = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
        ),
        ("A", "B", "C", "A"),
    )
    color_rename_right = _tangle(
        (
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("B")),
            _stage("analysis", Extend("C")),
            _stage("analysis", Extend("B")),
        ),
        ("D", "C", "B", "D"),
        anchor="D",
    )

    two_roles = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("inspection", Probe("remaining-role", ("B", "C"))),
        ),
        ("A", "B", "C"),
    )
    three_roles = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("reasoning", IntroduceRole("D")),
            _stage("inspection", Probe("remaining-role", ("B", "C"))),
        ),
        ("A", "B", "C"),
    )

    probe_x = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("inspection", Probe("connects-left", ("B",))),
        ),
        ("A", "B"),
    )
    probe_y = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("inspection", Probe("connects-right", ("B",))),
        ),
        ("A", "B"),
    )

    periodic_tail = _tangle(
        (
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
            _stage("analysis", Extend("B")),
            _stage("analysis", Extend("C")),
            _stage("reasoning", IntroduceRole("D")),
            _stage("analysis", Extend("D")),
            _stage("inspection", Probe("recurrence-response", ("B", "C"))),
        ),
        ("A", "B", "C", "A"),
        response_classes=("periodic", "opens", "reenters"),
    )

    return (
        QuotientChallenge(
            "periodic-depth-is-not-strategy-depth",
            _periodic(2),
            _periodic(9),
            periodic_policy,
            "collapse",
            "extra BC repetitions must not change response classes or options",
        ),
        QuotientChallenge(
            "r1-excursion-is-projection-noise",
            r1_clean,
            r1_noisy,
            NormalizationPolicy(),
            "collapse",
            "Extend/Return on one known role contributes no new interface fact",
        ),
        QuotientChallenge(
            "r2-opposed-crossings-cancel",
            r2_clean,
            r2_noisy,
            NormalizationPolicy(),
            "collapse",
            "opposed crossings contribute no surviving relation",
        ),
        QuotientChallenge(
            "r3-disjoint-frame-order-is-staging-noise",
            staged_left,
            staged_right,
            NormalizationPolicy(),
            "collapse",
            "operations on disjoint role support may be batched by frame",
        ),
        QuotientChallenge(
            "mirror-is-one-class-when-explicitly-authorized",
            _mirror(1),
            _mirror(-1),
            mirror_policy,
            "collapse",
            "orientation is declared irrelevant for this challenge",
        ),
        QuotientChallenge(
            "mirror-remains-distinct-without-authority",
            _mirror(1),
            _mirror(-1),
            NormalizationPolicy(),
            "split",
            "reflection cannot be inferred from appearance alone",
        ),
        QuotientChallenge(
            "color-name-permutation-is-not-a-new-strategy",
            color_rename_left,
            color_rename_right,
            NormalizationPolicy(),
            "collapse",
            "only relative role introduction order is proof-relevant",
        ),
        QuotientChallenge(
            "safe-first-option-must-survive-quotient",
            _base_probe(option="first-move-A"),
            _base_probe(option="first-move-B"),
            NormalizationPolicy(),
            "split",
            "available certified first-move option differs",
        ),
        QuotientChallenge(
            "response-class-must-survive-quotient",
            _base_probe(response="opens"),
            _base_probe(response="reenters"),
            NormalizationPolicy(),
            "split",
            "MapMaker response class differs",
        ),
        QuotientChallenge(
            "remaining-independent-role-must-survive-quotient",
            two_roles,
            three_roles,
            NormalizationPolicy(),
            "split",
            "one presentation has one unused role and the other has none",
        ),
        QuotientChallenge(
            "shared-support-order-cannot-r3-commute",
            shared_support_left,
            shared_support_right,
            NormalizationPolicy(),
            "split",
            "analysis and inspection touch the same role and may not commute",
        ),
        QuotientChallenge(
            "probe-observable-must-survive-quotient",
            probe_x,
            probe_y,
            NormalizationPolicy(),
            "split",
            "the bounded MapMaker asked a different proof-relevant question",
        ),
        QuotientChallenge(
            "periodic-tail-is-new-until-proved-irrelevant",
            _periodic(2),
            periodic_tail,
            periodic_policy,
            "split",
            "introducing the last independent role after recurrence changes freedom",
        ),
    )

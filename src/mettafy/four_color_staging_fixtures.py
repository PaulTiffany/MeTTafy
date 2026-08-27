from __future__ import annotations

from mettafy.strategy_ir import StrategySignature
from mettafy.strategy_staging import (
    Cross,
    Extend,
    IntroduceRole,
    PrimitiveOp,
    Probe,
    RawStrategyTrace,
    Return,
    StageFrame,
    StagedOperation,
    StrategyTangle,
)


def _stage(frame: StageFrame, op: PrimitiveOp) -> StagedOperation:
    return StagedOperation(frame, op)


def _family_a(repetitions: int) -> StrategyTangle:
    """One realized bottom/lengthwise anchor; B/C form an imagined recurrence."""

    alternating: list[StagedOperation] = []
    for _ in range(repetitions):
        alternating.extend(
            (
                _stage("analysis", Extend("B")),
                _stage("analysis", Extend("C")),
            )
        )
    trace = RawStrategyTrace(
        anchor="A",
        operations=(
            _stage("reasoning", IntroduceRole("B")),
            _stage("reasoning", IntroduceRole("C")),
            *alternating,
            _stage("inspection", Probe("does recurrence change response?", ("B", "C"))),
        ),
    )
    return StrategyTangle(
        raw=trace,
        boundary=("A", "B", "C", "A"),
        signature=StrategySignature(
            response_classes=("periodic", "opens", "reenters"),
            options=("first-move-A",),
        ),
    )


def _family_a_mirror(sign: int) -> StrategyTangle:
    crossing = Cross("B", "C", 1 if sign > 0 else -1)
    boundary = ("A", "B", "C", "D") if sign > 0 else ("D", "C", "B", "A")
    return StrategyTangle(
        raw=RawStrategyTrace(
            anchor="A",
            operations=(
                _stage("reasoning", IntroduceRole("B")),
                _stage("reasoning", IntroduceRole("C")),
                _stage("reasoning", IntroduceRole("D")),
                _stage("analysis", crossing),
                _stage("inspection", Probe("crossing response", ("B", "C"))),
            ),
        ),
        boundary=boundary,
        signature=StrategySignature(
            response_classes=("crossing",),
            options=("first-move-A",),
        ),
    )


def _family_b() -> StrategyTangle:
    """Two running roles with transverse work that cancels/re-enters under staging."""

    return StrategyTangle(
        raw=RawStrategyTrace(
            anchor="A",
            operations=(
                _stage("reasoning", IntroduceRole("B")),
                _stage("reasoning", IntroduceRole("C")),
                _stage("reasoning", IntroduceRole("D")),
                _stage("inspection", Probe("D-side", ("D",))),
                _stage("analysis", Extend("B")),
                _stage("analysis", Return("B")),
                _stage("analysis", Cross("C", "D", 1)),
                _stage("analysis", Cross("C", "D", -1)),
                _stage("inspection", Probe("transverse response", ("C", "D"))),
            ),
        ),
        boundary=("A", "B", "C", "D"),
        signature=StrategySignature(
            response_classes=("alternating-transverse", "reenters"),
            options=("first-move-A",),
        ),
    )


def red_team_staging_fixtures() -> tuple[StrategyTangle, ...]:
    """INFERENCE: concrete stress fixtures; their normal-form count is discovered."""

    return (
        _family_a(2),
        _family_a(6),
        _family_a_mirror(1),
        _family_a_mirror(-1),
        _family_b(),
    )

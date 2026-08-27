from __future__ import annotations

import pytest

from mettafy.strategy_color_projection import (
    replace_stuttering_operation,
    uncross_trivial_crossing,
)
from mettafy.strategy_forcing_phase import (
    StrategyResponseQuotient,
    witness_strategy_forcing,
)
from mettafy.strategy_ir import StrategySignature
from mettafy.strategy_staging import (
    Cross,
    Extend,
    IntroduceRole,
    Probe,
    RawStrategyTrace,
    Return,
    StagedOperation,
    StrategyTangle,
)


def stuttering_tangle() -> StrategyTangle:
    return StrategyTangle(
        raw=RawStrategyTrace(
            "A",
            (
                StagedOperation("reasoning", IntroduceRole("B")),
                StagedOperation("inspection", Probe("live-responses", ("A", "B"))),
            ),
        ),
        boundary=("A", "B"),
        signature=StrategySignature(
            response_classes=("left", "right"),
            options=("forcing-line",),
        ),
    )


def crossing_tangle() -> StrategyTangle:
    return StrategyTangle(
        raw=RawStrategyTrace(
            "A",
            (
                StagedOperation("reasoning", IntroduceRole("B")),
                StagedOperation("reasoning", IntroduceRole("C")),
                StagedOperation("analysis", Cross("B", "C", 1)),
                StagedOperation("analysis", Cross("B", "C", -1)),
            ),
        ),
        boundary=("A", "B", "C"),
        signature=StrategySignature(
            response_classes=("alpha", "beta", "gamma"),
            options=("uncross",),
        ),
    )


def test_response_quotient_counts_classes_not_duplicate_presentations() -> None:
    quotient = StrategyResponseQuotient(("block", "counter", "pass"))

    assert quotient.rank == 3
    assert not quotient.forced
    assert not quotient.checkmate

    with pytest.raises(ValueError, match="must be unique"):
        StrategyResponseQuotient(("block", "block"))


def test_rank_one_is_forced_and_rank_zero_is_checkmate() -> None:
    forced = StrategyResponseQuotient(("only-live-response",))
    mate = StrategyResponseQuotient(())

    assert forced.forced
    assert not forced.checkmate
    assert mate.checkmate
    assert not mate.forced


def test_stuttering_can_reduce_strategy_phase_without_color_phase_change() -> None:
    move = replace_stuttering_operation(
        stuttering_tangle(),
        1,
        StagedOperation("inspection", Extend("B")),
    )
    witness = witness_strategy_forcing(
        move,
        ("left", "right", "pass"),
        ("forced-response",),
    )

    assert witness.valid
    assert witness.rank_drop == 2
    assert witness.color_phase_preserved
    assert witness.before.responses.rank == 3
    assert witness.after.responses.rank == 1
    assert witness.after.responses.forced


def test_phase_preserving_uncrossing_can_also_be_a_forcing_move() -> None:
    move = uncross_trivial_crossing(crossing_tangle(), 2)
    witness = witness_strategy_forcing(
        move,
        ("left", "right", "counter"),
        ("forced-response",),
    )

    assert witness.valid
    assert witness.rank_drop == 2
    assert witness.color_phase_preserved
    assert witness.after.responses.forced


def test_forced_response_plus_further_forcing_is_checkmate() -> None:
    move = replace_stuttering_operation(
        stuttering_tangle(),
        1,
        StagedOperation("inspection", Return("B")),
    )
    witness = witness_strategy_forcing(
        move,
        ("only-live-response",),
        (),
    )

    assert witness.valid
    assert witness.reaches_checkmate_from_forced
    assert witness.after.responses.checkmate


def test_nonreducing_transition_is_not_forcing() -> None:
    move = replace_stuttering_operation(
        stuttering_tangle(),
        1,
        StagedOperation("inspection", Extend("B")),
    )

    with pytest.raises(ValueError, match="strictly reduce"):
        witness_strategy_forcing(move, ("left", "right"), ("alpha", "beta"))


def test_checkmate_cannot_have_a_further_forcing_step() -> None:
    move = replace_stuttering_operation(
        stuttering_tangle(),
        1,
        StagedOperation("inspection", Extend("B")),
    )

    with pytest.raises(ValueError, match="strictly reduce"):
        witness_strategy_forcing(move, (), ())

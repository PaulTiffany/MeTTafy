from __future__ import annotations

import pytest

from mettafy.strategy_color_projection import (
    color_phase,
    direction_between,
    project_strategy_tangle,
    replace_stuttering_operation,
    uncross_trivial_crossing,
)
from mettafy.strategy_ir import StrategySignature
from mettafy.strategy_staging import (
    Cross,
    CrossSign,
    Extend,
    IntroduceRole,
    Probe,
    RawStrategyTrace,
    StagedOperation,
    StrategyTangle,
)


def shared_crossing_tangle(*, opposite: bool = True) -> StrategyTangle:
    second_sign: CrossSign = -1 if opposite else 1
    operations = (
        StagedOperation("reasoning", IntroduceRole("B")),
        StagedOperation("reasoning", IntroduceRole("C")),
        StagedOperation("analysis", Cross("B", "C", 1)),
        StagedOperation("analysis", Cross("B", "C", second_sign)),
        StagedOperation("inspection", Probe("response-complete", ("A", "B", "C"))),
    )
    return StrategyTangle(
        raw=RawStrategyTrace("A", operations),
        boundary=("A", "B", "C"),
        signature=StrategySignature(
            response_classes=("same-turn",),
            options=("first-move",),
        ),
    )


def test_v4_pair_projection_has_exactly_three_nonzero_directions() -> None:
    assert direction_between("A", "A") is None
    directions = tuple(direction_between("A", role) for role in ("B", "C", "D"))
    assert all(direction is not None for direction in directions)
    values = {direction.value for direction in directions if direction is not None}
    assert values == {1, 2, 3}


def test_strategy_tangle_projection_is_grounded_and_records_stutters() -> None:
    projection = project_strategy_tangle(shared_crossing_tangle())

    assert projection.grounded
    assert tuple(direction.value for direction in projection.word) == (1, 2, 3, 3)
    assert tuple(item.source for item in projection.emissions) == (
        "introduce",
        "introduce",
        "cross",
        "cross",
    )
    assert tuple(item.kind for item in projection.stutters) == ("probe",)


def test_crossing_orientation_is_forgotten_but_role_difference_is_preserved() -> None:
    projection = project_strategy_tangle(shared_crossing_tangle())
    first_cross = projection.emissions[2]
    second_cross = projection.emissions[3]

    assert first_cross.left == second_cross.left == "B"
    assert first_cross.right == second_cross.right == "C"
    assert first_cross.direction == second_cross.direction
    assert first_cross.direction.value == 3


def test_trivial_geometric_crossing_simulates_color_r2_without_phase_change() -> None:
    move = uncross_trivial_crossing(shared_crossing_tangle(), 2)

    assert move.valid
    assert move.color_cancel.valid
    assert move.color_cancel.prefix_length == 2
    assert tuple(direction.value for direction in move.color_cancel.before) == (1, 2, 3, 3)
    assert tuple(direction.value for direction in move.color_cancel.after) == (1, 2)
    assert color_phase(move.color_cancel.before) == color_phase(move.color_cancel.after)


def test_stuttering_rewrite_changes_presentation_not_color_word() -> None:
    tangle = shared_crossing_tangle()
    move = replace_stuttering_operation(
        tangle,
        4,
        StagedOperation("inspection", Extend("B")),
    )

    assert move.valid
    assert move.before != move.after
    assert move.before_projection.word == move.after_projection.word


def test_same_sign_crossings_are_not_a_trivial_uncrossing() -> None:
    with pytest.raises(ValueError, match="opposite signs"):
        uncross_trivial_crossing(shared_crossing_tangle(opposite=False), 2)


def test_emitting_operation_cannot_be_declared_a_stutter() -> None:
    with pytest.raises(ValueError, match="replacement operation is not color-stuttering"):
        replace_stuttering_operation(
            shared_crossing_tangle(),
            4,
            StagedOperation("reasoning", IntroduceRole("D")),
        )

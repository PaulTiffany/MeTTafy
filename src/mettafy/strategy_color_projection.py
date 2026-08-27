from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.strategy_staging import (
    ColorRole,
    Cross,
    Extend,
    IntroduceRole,
    Periodic,
    Probe,
    RawStrategyTrace,
    Return,
    StagedOperation,
    StrategyTangle,
    build_role_ledger,
)

ROLE_CODE: dict[ColorRole, int] = {"A": 0, "B": 1, "C": 2, "D": 3}
ProjectionSource = Literal["introduce", "cross"]
StutterKind = Literal["extend", "return", "probe", "periodic"]


@dataclass(frozen=True)
class ColorDirection:
    """INFERENCE: one non-identity V4 difference, encoded as 1, 2, or 3."""

    value: int

    def __post_init__(self) -> None:
        if self.value not in (1, 2, 3):
            raise ValueError("color direction must be a nonzero V4 difference")


def direction_between(left: ColorRole, right: ColorRole) -> ColorDirection | None:
    """Project a pair of color roles to their relative Klein-four direction.

    Equal roles have identity difference and therefore stutter. Distinct roles
    produce one of exactly three nonzero directions.
    """

    value = ROLE_CODE[left] ^ ROLE_CODE[right]
    return None if value == 0 else ColorDirection(value)


@dataclass(frozen=True)
class ProjectedDirection:
    """INFERENCE: provenance for one emitted color-word direction."""

    operation_index: int
    source: ProjectionSource
    left: ColorRole
    right: ColorRole
    direction: ColorDirection


@dataclass(frozen=True)
class ProjectionStutter:
    """INFERENCE: a geometric/observer operation intentionally erased by projection."""

    operation_index: int
    kind: StutterKind


@dataclass(frozen=True)
class StrategyColorProjection:
    """INFERENCE: one-way StrategyTangle -> color-word transduction receipt."""

    tangle: StrategyTangle
    word: tuple[ColorDirection, ...]
    emissions: tuple[ProjectedDirection, ...]
    stutters: tuple[ProjectionStutter, ...]

    @property
    def grounded(self) -> bool:
        operations = self.tangle.raw.operations
        if len(self.emissions) + len(self.stutters) != len(operations):
            return False

        seen: set[int] = set()
        emitted_word: list[ColorDirection] = []
        for emission in self.emissions:
            index = emission.operation_index
            if index in seen or index < 0 or index >= len(operations):
                return False
            seen.add(index)
            op = operations[index].op
            expected: ColorDirection | None
            if emission.source == "introduce":
                if not isinstance(op, IntroduceRole):
                    return False
                if emission.left != self.tangle.raw.anchor or emission.right != op.role:
                    return False
                expected = direction_between(self.tangle.raw.anchor, op.role)
            else:
                if not isinstance(op, Cross):
                    return False
                if emission.left != op.left or emission.right != op.right:
                    return False
                expected = direction_between(op.left, op.right)
            if expected is None or expected != emission.direction:
                return False
            emitted_word.append(emission.direction)

        for stutter in self.stutters:
            index = stutter.operation_index
            if index in seen or index < 0 or index >= len(operations):
                return False
            seen.add(index)
            if _stutter_kind(operations[index]) != stutter.kind:
                return False

        return seen == set(range(len(operations))) and tuple(emitted_word) == self.word


ColorWord: TypeAlias = tuple[ColorDirection, ...]


def _stutter_kind(operation: StagedOperation) -> StutterKind | None:
    op = operation.op
    if isinstance(op, Extend):
        return "extend"
    if isinstance(op, Return):
        return "return"
    if isinstance(op, Probe):
        return "probe"
    if isinstance(op, Periodic):
        return "periodic"
    return None


def project_strategy_tangle(tangle: StrategyTangle) -> StrategyColorProjection:
    """INFERENCE: project only grounded role differences and record every stutter.

    `IntroduceRole(r)` emits the difference between the fixed anchor and `r`.
    `Cross(l,r,sign)` emits `l xor r`; crossing sign is deliberately forgotten.
    Extend/Return/Probe/Periodic operations stutter at this color-algebra layer.
    """

    # Validate the same bounded role discipline used by Strategy IR before
    # emitting any algebraic content.
    build_role_ledger(tangle.raw)

    emissions: list[ProjectedDirection] = []
    stutters: list[ProjectionStutter] = []
    for index, operation in enumerate(tangle.raw.operations):
        op = operation.op
        if isinstance(op, IntroduceRole):
            direction = direction_between(tangle.raw.anchor, op.role)
            if direction is None:
                raise AssertionError("a newly introduced role cannot equal the anchor")
            emissions.append(
                ProjectedDirection(
                    operation_index=index,
                    source="introduce",
                    left=tangle.raw.anchor,
                    right=op.role,
                    direction=direction,
                )
            )
            continue
        if isinstance(op, Cross):
            direction = direction_between(op.left, op.right)
            if direction is None:
                raise AssertionError("Cross already requires two distinct roles")
            emissions.append(
                ProjectedDirection(
                    operation_index=index,
                    source="cross",
                    left=op.left,
                    right=op.right,
                    direction=direction,
                )
            )
            continue
        kind = _stutter_kind(operation)
        if kind is None:
            raise AssertionError(f"unclassified projection operation: {type(op).__name__}")
        stutters.append(ProjectionStutter(index, kind))

    projection = StrategyColorProjection(
        tangle=tangle,
        word=tuple(item.direction for item in emissions),
        emissions=tuple(emissions),
        stutters=tuple(stutters),
    )
    if not projection.grounded:
        raise AssertionError("StrategyTangle color projection lost provenance")
    return projection


def color_phase(word: ColorWord) -> int:
    """INFERENCE: retained V4 phase after forgetting serialized presentation."""

    phase = 0
    for direction in word:
        phase ^= direction.value
    return phase


@dataclass(frozen=True)
class ColorCancelWitness:
    """INFERENCE: one local `[d,d] -> []` phase-preserving color uncrossing."""

    before: ColorWord
    after: ColorWord
    prefix_length: int
    direction: ColorDirection

    @property
    def valid(self) -> bool:
        if self.prefix_length < 0 or self.prefix_length + 2 > len(self.before):
            return False
        prefix = self.before[: self.prefix_length]
        pair = self.before[self.prefix_length : self.prefix_length + 2]
        suffix = self.before[self.prefix_length + 2 :]
        return (
            pair == (self.direction, self.direction)
            and self.after == prefix + suffix
            and color_phase(self.before) == color_phase(self.after)
        )


@dataclass(frozen=True)
class TrivialCrossingMove:
    """INFERENCE: geometric opposite-sign crossing pair projected to color R2."""

    before: StrategyTangle
    after: StrategyTangle
    operation_index: int
    before_projection: StrategyColorProjection
    after_projection: StrategyColorProjection
    color_cancel: ColorCancelWitness

    @property
    def valid(self) -> bool:
        operations = self.before.raw.operations
        index = self.operation_index
        if index < 0 or index + 1 >= len(operations):
            return False
        first = operations[index].op
        second = operations[index + 1].op
        if not isinstance(first, Cross) or not isinstance(second, Cross):
            return False
        if (
            first.left != second.left
            or first.right != second.right
            or first.sign != -second.sign
        ):
            return False
        expected_after = StrategyTangle(
            raw=RawStrategyTrace(
                self.before.raw.anchor,
                operations[:index] + operations[index + 2 :],
            ),
            boundary=self.before.boundary,
            signature=self.before.signature,
        )
        return (
            self.after == expected_after
            and self.before_projection == project_strategy_tangle(self.before)
            and self.after_projection == project_strategy_tangle(self.after)
            and self.color_cancel.valid
            and self.color_cancel.before == self.before_projection.word
            and self.color_cancel.after == self.after_projection.word
        )


def uncross_trivial_crossing(tangle: StrategyTangle, operation_index: int) -> TrivialCrossingMove:
    """INFERENCE: remove one explicit geometric R2 pair and witness its color projection."""

    before_projection = project_strategy_tangle(tangle)
    operations = tangle.raw.operations
    if operation_index < 0 or operation_index + 1 >= len(operations):
        raise ValueError("trivial crossing index must name an adjacent operation pair")
    first = operations[operation_index].op
    second = operations[operation_index + 1].op
    if not isinstance(first, Cross) or not isinstance(second, Cross):
        raise ValueError("trivial crossing requires two adjacent Cross operations")
    if (
        first.left != second.left
        or first.right != second.right
        or first.sign != -second.sign
    ):
        raise ValueError("crossing pair must use the same roles with opposite signs")

    direction = direction_between(first.left, first.right)
    if direction is None:
        raise AssertionError("Cross already requires distinct roles")
    after = StrategyTangle(
        raw=RawStrategyTrace(
            tangle.raw.anchor,
            operations[:operation_index] + operations[operation_index + 2 :],
        ),
        boundary=tangle.boundary,
        signature=tangle.signature,
    )
    after_projection = project_strategy_tangle(after)
    prefix_length = sum(
        1
        for emission in before_projection.emissions
        if emission.operation_index < operation_index
    )
    cancel = ColorCancelWitness(
        before=before_projection.word,
        after=after_projection.word,
        prefix_length=prefix_length,
        direction=direction,
    )
    move = TrivialCrossingMove(
        before=tangle,
        after=after,
        operation_index=operation_index,
        before_projection=before_projection,
        after_projection=after_projection,
        color_cancel=cancel,
    )
    if not move.valid:
        raise AssertionError("geometric trivial crossing did not simulate color uncrossing")
    return move


@dataclass(frozen=True)
class StutteringMove:
    """INFERENCE: a changed StrategyTangle presentation with identical color word."""

    before: StrategyTangle
    after: StrategyTangle
    operation_index: int
    before_projection: StrategyColorProjection
    after_projection: StrategyColorProjection

    @property
    def valid(self) -> bool:
        return (
            self.before_projection == project_strategy_tangle(self.before)
            and self.after_projection == project_strategy_tangle(self.after)
            and self.before_projection.word == self.after_projection.word
        )


def replace_stuttering_operation(
    tangle: StrategyTangle,
    operation_index: int,
    replacement: StagedOperation,
) -> StutteringMove:
    """INFERENCE: rewrite one explicitly color-silent operation and verify stutter."""

    operations = tangle.raw.operations
    if operation_index < 0 or operation_index >= len(operations):
        raise ValueError("stutter replacement index is outside the trace")
    if _stutter_kind(operations[operation_index]) is None:
        raise ValueError("source operation is not color-stuttering")
    if _stutter_kind(replacement) is None:
        raise ValueError("replacement operation is not color-stuttering")

    updated = operations[:operation_index] + (replacement,) + operations[operation_index + 1 :]
    after = StrategyTangle(
        raw=RawStrategyTrace(tangle.raw.anchor, updated),
        boundary=tangle.boundary,
        signature=tangle.signature,
    )
    before_projection = project_strategy_tangle(tangle)
    after_projection = project_strategy_tangle(after)
    move = StutteringMove(
        before=tangle,
        after=after,
        operation_index=operation_index,
        before_projection=before_projection,
        after_projection=after_projection,
    )
    if not move.valid:
        raise AssertionError("declared stuttering move changed the projected color word")
    return move

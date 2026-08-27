from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias

from mettafy.strategy_ir import RoleplayEpisode, StrategySignature

ColorRole = Literal["A", "B", "C", "D"]
StageFrame = Literal["reasoning", "analysis", "inspection"]
CrossSign = Literal[-1, 1]

ALL_ROLES: tuple[ColorRole, ...] = ("A", "B", "C", "D")
FRAME_ORDER: dict[StageFrame, int] = {
    "reasoning": 0,
    "analysis": 1,
    "inspection": 2,
}


@dataclass(frozen=True)
class IntroduceRole:
    """INFERENCE: introduce one independent imaginary color-role."""

    role: ColorRole


@dataclass(frozen=True)
class Extend:
    """INFERENCE: continue an already-known strand/role."""

    role: ColorRole


@dataclass(frozen=True)
class Return:
    """INFERENCE: return along an already-known role."""

    role: ColorRole


@dataclass(frozen=True)
class Cross:
    """INFERENCE: one projected crossing relation between known roles."""

    left: ColorRole
    right: ColorRole
    sign: CrossSign

    def __post_init__(self) -> None:
        if self.left == self.right:
            raise ValueError("a crossing requires two distinct roles")


@dataclass(frozen=True)
class Probe:
    """INFERENCE: inspect a proof-relevant relation on explicit role support."""

    label: str
    roles: tuple[ColorRole, ...]


@dataclass(frozen=True)
class Periodic:
    """INFERENCE: one recognized periodic continuation class."""

    cycle: tuple[ColorRole, ...]

    def __post_init__(self) -> None:
        if not self.cycle:
            raise ValueError("periodic cycle must be non-empty")


PrimitiveOp: TypeAlias = IntroduceRole | Extend | Return | Cross | Probe | Periodic


@dataclass(frozen=True)
class StagedOperation:
    """INFERENCE: one unweaved operation plus the reasoning frame it belongs to."""

    frame: StageFrame
    op: PrimitiveOp


@dataclass(frozen=True)
class RawStrategyTrace:
    """INFERENCE: typed serialization of a same-turn MapMaker roleplay trace."""

    anchor: ColorRole
    operations: tuple[StagedOperation, ...]


@dataclass(frozen=True)
class RoleplayBinding:
    """UNWEAVE: bind one roleplay event to one lowest-level staging operation."""

    event_index: int
    operation: StagedOperation


@dataclass(frozen=True)
class RoleLedger:
    """INFERENCE: independent role commitments, distinct from CoT depth."""

    anchor: ColorRole
    introduced: tuple[ColorRole, ...]
    unused: tuple[ColorRole, ...]
    recurrence: tuple[tuple[ColorRole, ...], ...] = ()

    @property
    def remaining_degrees(self) -> int:
        return len(self.unused)


@dataclass(frozen=True)
class StrategyTangle:
    """INFERENCE: boundary-labelled tangle projected from one roleplay trace."""

    raw: RawStrategyTrace
    boundary: tuple[ColorRole, ...]
    signature: StrategySignature = field(default_factory=StrategySignature)

    @property
    def ledger(self) -> RoleLedger:
        return build_role_ledger(self.raw)


@dataclass(frozen=True)
class NormalizationPolicy:
    """INFERENCE: explicit quotient assumptions permitted during staging.

    Mirror and periodic equivalence are never inferred from appearance alone.
    They must be supplied as part of the strategy hypothesis being tested.
    """

    mirror_equivalent: bool = False
    periodic_cycles: tuple[tuple[ColorRole, ...], ...] = ()


@dataclass(frozen=True)
class StagingMetrics:
    """INFERENCE: measured simplifications performed by the staging pass."""

    r1_loops: int = 0
    r2_cancellations: int = 0
    r3_reorders: int = 0
    periodic_folds: int = 0
    raw_operations: int = 0
    normal_operations: int = 0


@dataclass(frozen=True)
class StrategyNormalForm:
    """INFERENCE: deterministic strategy-class representative."""

    anchor: ColorRole
    boundary: tuple[ColorRole, ...]
    operations: tuple[StagedOperation, ...]
    remaining_roles: tuple[ColorRole, ...]
    response_classes: tuple[str, ...]
    options: tuple[str, ...]


@dataclass(frozen=True)
class StagedStrategySignature:
    """INFERENCE: structured Strategy IR extracted from a normal form."""

    anchor_form: ColorRole
    role_partition: tuple[ColorRole, ...]
    boundary_form: tuple[ColorRole, ...]
    recurrence_form: tuple[tuple[ColorRole, ...], ...]
    remaining_degrees: int


@dataclass(frozen=True)
class StrategyInterface:
    """INFERENCE: proof-relevant interface that staging is allowed to preserve."""

    remaining_roles: tuple[ColorRole, ...]
    boundary: tuple[ColorRole, ...]
    periodic_cycles: tuple[tuple[ColorRole, ...], ...]
    response_classes: tuple[str, ...]
    options: tuple[str, ...]


@dataclass(frozen=True)
class StagedStrategyClass:
    """INFERENCE: one discovered normal form plus concrete fixture members."""

    normal: StrategyNormalForm
    members: tuple[int, ...]


@dataclass(frozen=True)
class StagingReport:
    """INFERENCE: empirical compression summary; class count is discovered."""

    raw_traces: int
    raw_operations: int
    normal_forms: int
    max_remaining_degrees: int
    max_normalized_operations: int


def _op_roles(op: PrimitiveOp) -> tuple[ColorRole, ...]:
    if isinstance(op, (IntroduceRole, Extend, Return)):
        return (op.role,)
    if isinstance(op, Cross):
        return (op.left, op.right)
    if isinstance(op, Probe):
        return op.roles
    return op.cycle


def _op_key(operation: StagedOperation) -> tuple[str, ...]:
    op = operation.op
    if isinstance(op, IntroduceRole):
        payload = ("introduce", op.role)
    elif isinstance(op, Extend):
        payload = ("extend", op.role)
    elif isinstance(op, Return):
        payload = ("return", op.role)
    elif isinstance(op, Cross):
        payload = ("cross", op.left, op.right, str(op.sign))
    elif isinstance(op, Probe):
        payload = ("probe", op.label, *op.roles)
    else:
        payload = ("periodic", *op.cycle)
    return (operation.frame, *payload)


def unweave_roleplay(
    episode: RoleplayEpisode,
    anchor: ColorRole,
    bindings: tuple[RoleplayBinding, ...],
) -> RawStrategyTrace:
    """UNWEAVE: type only the roleplay events selected as strategy operations."""

    seen: set[int] = set()
    ordered: list[RoleplayBinding] = []
    for binding in sorted(bindings, key=lambda item: item.event_index):
        if binding.event_index < 0 or binding.event_index >= len(episode.events):
            raise ValueError("roleplay binding points outside the episode")
        if binding.event_index in seen:
            raise ValueError("one roleplay event cannot supply two staging operations")
        seen.add(binding.event_index)
        ordered.append(binding)
    return RawStrategyTrace(anchor, tuple(item.operation for item in ordered))


def build_role_ledger(trace: RawStrategyTrace) -> RoleLedger:
    """INFERENCE: count independent roles, not serialized imagination steps."""

    known: set[ColorRole] = {trace.anchor}
    introduced: list[ColorRole] = []
    recurrence: list[tuple[ColorRole, ...]] = []
    for operation in trace.operations:
        op = operation.op
        if isinstance(op, IntroduceRole):
            if op.role in known:
                raise ValueError("imaginary role was introduced more than once")
            known.add(op.role)
            introduced.append(op.role)
            continue
        missing = set(_op_roles(op)) - known
        if missing:
            raise ValueError(f"operation uses unintroduced roles: {sorted(missing)}")
        if isinstance(op, Periodic) and op.cycle not in recurrence:
            recurrence.append(op.cycle)
    unused = tuple(role for role in ALL_ROLES if role not in known)
    return RoleLedger(trace.anchor, tuple(introduced), unused, tuple(recurrence))


def _canonical_mapping(trace: RawStrategyTrace) -> dict[ColorRole, ColorRole]:
    ledger = build_role_ledger(trace)
    ordered = (ledger.anchor, *ledger.introduced)
    targets = ALL_ROLES[: len(ordered)]
    return dict(zip(ordered, targets, strict=True))


def _map_role(role: ColorRole, mapping: dict[ColorRole, ColorRole]) -> ColorRole:
    return mapping.get(role, role)


def _map_op(op: PrimitiveOp, mapping: dict[ColorRole, ColorRole]) -> PrimitiveOp:
    if isinstance(op, IntroduceRole):
        return IntroduceRole(_map_role(op.role, mapping))
    if isinstance(op, Extend):
        return Extend(_map_role(op.role, mapping))
    if isinstance(op, Return):
        return Return(_map_role(op.role, mapping))
    if isinstance(op, Cross):
        return Cross(
            _map_role(op.left, mapping),
            _map_role(op.right, mapping),
            op.sign,
        )
    if isinstance(op, Probe):
        return Probe(op.label, tuple(_map_role(role, mapping) for role in op.roles))
    return Periodic(tuple(_map_role(role, mapping) for role in op.cycle))


def _canonicalize_tangle(
    tangle: StrategyTangle,
    policy: NormalizationPolicy,
) -> tuple[RawStrategyTrace, tuple[ColorRole, ...], NormalizationPolicy]:
    mapping = _canonical_mapping(tangle.raw)
    operations = tuple(
        StagedOperation(item.frame, _map_op(item.op, mapping))
        for item in tangle.raw.operations
    )
    trace = RawStrategyTrace("A", operations)
    boundary = tuple(_map_role(role, mapping) for role in tangle.boundary)
    cycles = tuple(
        tuple(_map_role(role, mapping) for role in cycle)
        for cycle in policy.periodic_cycles
    )
    return trace, boundary, NormalizationPolicy(policy.mirror_equivalent, cycles)


def _cancel_r1(
    operations: tuple[StagedOperation, ...],
) -> tuple[tuple[StagedOperation, ...], int]:
    result: list[StagedOperation] = []
    count = 0
    index = 0
    while index < len(operations):
        if index + 1 < len(operations):
            first = operations[index].op
            second = operations[index + 1].op
            if (
                isinstance(first, Extend)
                and isinstance(second, Return)
                and first.role == second.role
            ):
                count += 1
                index += 2
                continue
        result.append(operations[index])
        index += 1
    return tuple(result), count


def _cancel_r2(
    operations: tuple[StagedOperation, ...],
) -> tuple[tuple[StagedOperation, ...], int]:
    result: list[StagedOperation] = []
    count = 0
    index = 0
    while index < len(operations):
        if index + 1 < len(operations):
            first = operations[index].op
            second = operations[index + 1].op
            if (
                isinstance(first, Cross)
                and isinstance(second, Cross)
                and first.left == second.left
                and first.right == second.right
                and first.sign == -second.sign
            ):
                count += 1
                index += 2
                continue
        result.append(operations[index])
        index += 1
    return tuple(result), count


def _periodic_fold(
    operations: tuple[StagedOperation, ...],
    cycles: tuple[tuple[ColorRole, ...], ...],
) -> tuple[tuple[StagedOperation, ...], int]:
    if not cycles:
        return operations, 0
    result: list[StagedOperation] = []
    folds = 0
    index = 0
    while index < len(operations):
        folded = False
        for cycle in sorted(cycles, key=len, reverse=True):
            if not cycle:
                continue
            width = len(cycle)
            if index + 2 * width > len(operations):
                continue
            frame = operations[index].frame
            repeats = 0
            cursor = index
            while cursor + width <= len(operations):
                window = operations[cursor : cursor + width]
                if any(item.frame != frame for item in window):
                    break
                roles: list[ColorRole] = []
                for item in window:
                    if not isinstance(item.op, Extend):
                        break
                    roles.append(item.op.role)
                if tuple(roles) != cycle:
                    break
                repeats += 1
                cursor += width
            if repeats >= 2:
                result.append(StagedOperation(frame, Periodic(cycle)))
                folds += 1
                index = cursor
                folded = True
                break
        if not folded:
            result.append(operations[index])
            index += 1
    return tuple(result), folds


def _support(operation: StagedOperation) -> frozenset[ColorRole]:
    return frozenset(_op_roles(operation.op))


def _can_r3_swap(left: StagedOperation, right: StagedOperation) -> bool:
    if isinstance(left.op, IntroduceRole) or isinstance(right.op, IntroduceRole):
        return False
    return not bool(_support(left) & _support(right))


def _r3_stage(
    operations: tuple[StagedOperation, ...],
) -> tuple[tuple[StagedOperation, ...], int]:
    items = list(operations)
    count = 0
    changed = True
    while changed:
        changed = False
        for index in range(len(items) - 1):
            left = items[index]
            right = items[index + 1]
            if FRAME_ORDER[left.frame] <= FRAME_ORDER[right.frame]:
                continue
            if not _can_r3_swap(left, right):
                continue
            items[index], items[index + 1] = right, left
            count += 1
            changed = True
    return tuple(items), count


def _mirror_op(operation: StagedOperation) -> StagedOperation:
    op = operation.op
    if isinstance(op, Cross):
        mirrored: PrimitiveOp = Cross(op.left, op.right, -op.sign)
    else:
        mirrored = op
    return StagedOperation(operation.frame, mirrored)


def _representation_key(
    boundary: tuple[ColorRole, ...],
    operations: tuple[StagedOperation, ...],
) -> tuple[str, ...]:
    return (*boundary, *("/".join(_op_key(item)) for item in operations))


def _choose_mirror(
    boundary: tuple[ColorRole, ...],
    operations: tuple[StagedOperation, ...],
    enabled: bool,
) -> tuple[tuple[ColorRole, ...], tuple[StagedOperation, ...]]:
    if not enabled:
        return boundary, operations
    mirrored_boundary = tuple(reversed(boundary))
    mirrored_operations = tuple(_mirror_op(item) for item in operations)
    if _representation_key(mirrored_boundary, mirrored_operations) < _representation_key(
        boundary, operations
    ):
        return mirrored_boundary, mirrored_operations
    return boundary, operations


def normalize_strategy_tangle(
    tangle: StrategyTangle,
    policy: NormalizationPolicy = NormalizationPolicy(),
) -> tuple[StrategyNormalForm, StagingMetrics]:
    """INFERENCE: deterministically stage/uncross one same-turn strategy tangle."""

    trace, boundary, canonical_policy = _canonicalize_tangle(tangle, policy)
    operations = trace.operations
    raw_count = len(operations)
    r1_total = 0
    r2_total = 0
    r3_total = 0
    periodic_total = 0

    while True:
        before = operations
        operations, r1 = _cancel_r1(operations)
        operations, r2 = _cancel_r2(operations)
        operations, periodic = _periodic_fold(
            operations, canonical_policy.periodic_cycles
        )
        operations, r3 = _r3_stage(operations)
        r1_total += r1
        r2_total += r2
        r3_total += r3
        periodic_total += periodic
        if operations == before:
            break

    boundary, operations = _choose_mirror(
        boundary, operations, canonical_policy.mirror_equivalent
    )
    normal_trace = RawStrategyTrace("A", operations)
    ledger = build_role_ledger(normal_trace)
    normal = StrategyNormalForm(
        anchor="A",
        boundary=boundary,
        operations=operations,
        remaining_roles=ledger.unused,
        response_classes=tangle.signature.response_classes,
        options=tangle.signature.options,
    )
    metrics = StagingMetrics(
        r1_loops=r1_total,
        r2_cancellations=r2_total,
        r3_reorders=r3_total,
        periodic_folds=periodic_total,
        raw_operations=raw_count,
        normal_operations=len(operations),
    )
    return normal, metrics


def staged_signature(normal: StrategyNormalForm) -> StagedStrategySignature:
    recurrence = tuple(
        item.op.cycle for item in normal.operations if isinstance(item.op, Periodic)
    )
    introduced = tuple(
        item.op.role
        for item in normal.operations
        if isinstance(item.op, IntroduceRole)
    )
    return StagedStrategySignature(
        anchor_form=normal.anchor,
        role_partition=introduced,
        boundary_form=normal.boundary,
        recurrence_form=recurrence,
        remaining_degrees=len(normal.remaining_roles),
    )


def strategy_interface(normal: StrategyNormalForm) -> StrategyInterface:
    cycles = tuple(
        item.op.cycle for item in normal.operations if isinstance(item.op, Periodic)
    )
    return StrategyInterface(
        remaining_roles=normal.remaining_roles,
        boundary=normal.boundary,
        periodic_cycles=cycles,
        response_classes=normal.response_classes,
        options=normal.options,
    )


def classify_normal_forms(
    tangles: tuple[StrategyTangle, ...],
    policy: NormalizationPolicy = NormalizationPolicy(),
) -> tuple[StagedStrategyClass, ...]:
    """INFERENCE: discover normal-form classes without encoding their count."""

    order: list[StrategyNormalForm] = []
    members: dict[StrategyNormalForm, list[int]] = {}
    for index, tangle in enumerate(tangles):
        normal, _ = normalize_strategy_tangle(tangle, policy)
        if normal not in members:
            order.append(normal)
            members[normal] = []
        members[normal].append(index)
    return tuple(
        StagedStrategyClass(normal, tuple(members[normal])) for normal in order
    )


def build_staging_report(
    tangles: tuple[StrategyTangle, ...],
    policy: NormalizationPolicy = NormalizationPolicy(),
) -> StagingReport:
    normals: list[StrategyNormalForm] = []
    raw_operations = 0
    max_degrees = 0
    max_normal_size = 0
    for tangle in tangles:
        normal, metrics = normalize_strategy_tangle(tangle, policy)
        normals.append(normal)
        raw_operations += metrics.raw_operations
        max_degrees = max(max_degrees, len(normal.remaining_roles))
        max_normal_size = max(max_normal_size, metrics.normal_operations)
    return StagingReport(
        raw_traces=len(tangles),
        raw_operations=raw_operations,
        normal_forms=len(set(normals)),
        max_remaining_degrees=max_degrees,
        max_normalized_operations=max_normal_size,
    )

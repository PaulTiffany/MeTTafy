from __future__ import annotations

from mettafy.color_construction import ConstructionState
from mettafy.four_color_staging_fixtures import red_team_staging_fixtures
from mettafy.strategy_ir import (
    Ask,
    RoleplayEpisode,
    See,
    StrategySignature,
    StrategySnapshot,
    begin_hypothetical,
)
from mettafy.strategy_staging import (
    Cross,
    Extend,
    IntroduceRole,
    NormalizationPolicy,
    PrimitiveOp,
    Probe,
    RawStrategyTrace,
    Return,
    RoleplayBinding,
    StageFrame,
    StagedOperation,
    StrategyTangle,
    build_role_ledger,
    build_staging_report,
    classify_normal_forms,
    normalize_strategy_tangle,
    staged_signature,
    strategy_interface,
    unweave_roleplay,
)


def stage(frame: StageFrame, op: PrimitiveOp) -> StagedOperation:
    return StagedOperation(frame, op)


def test_independent_role_freedom_is_not_chain_of_thought_depth() -> None:
    """INFERENCE: repeated known roles do not consume new color-role freedom."""

    repeated = tuple(
        stage("analysis", Extend(role))
        for _ in range(20)
        for role in ("B", "C")
    )
    trace = RawStrategyTrace(
        "A",
        (
            stage("reasoning", IntroduceRole("B")),
            stage("reasoning", IntroduceRole("C")),
            *repeated,
        ),
    )
    ledger = build_role_ledger(trace)

    assert len(trace.operations) == 42
    assert ledger.introduced == ("B", "C")
    assert ledger.unused == ("D",)
    assert ledger.remaining_degrees == 1


def test_periodic_extension_collapses_long_and_short_imagination_to_one_class() -> None:
    """INFERENCE: BCBC... length is not automatically a new strategy class."""

    short, long, *_ = red_team_staging_fixtures()
    policy = NormalizationPolicy(periodic_cycles=(("B", "C"),))
    short_normal, short_metrics = normalize_strategy_tangle(short, policy)
    long_normal, long_metrics = normalize_strategy_tangle(long, policy)

    assert short_normal == long_normal
    assert short_metrics.periodic_folds == 1
    assert long_metrics.periodic_folds == 1
    assert long_metrics.raw_operations > short_metrics.raw_operations
    assert long_metrics.normal_operations == short_metrics.normal_operations
    assert staged_signature(long_normal).remaining_degrees == 1


def test_mirror_equivalence_is_explicit_and_collapses_only_when_enabled() -> None:
    """INFERENCE: reflection is a caller-supplied quotient hypothesis."""

    _, _, left, right, _ = red_team_staging_fixtures()
    left_raw, _ = normalize_strategy_tangle(left)
    right_raw, _ = normalize_strategy_tangle(right)
    assert left_raw != right_raw

    policy = NormalizationPolicy(mirror_equivalent=True)
    left_normal, _ = normalize_strategy_tangle(left, policy)
    right_normal, _ = normalize_strategy_tangle(right, policy)
    assert left_normal == right_normal


def test_r1_and_r2_like_uncrossing_remove_projection_noise() -> None:
    """INFERENCE: loop and opposed-pair cancellation preserve the strategy interface."""

    *_, family_b = red_team_staging_fixtures()
    normal, metrics = normalize_strategy_tangle(family_b)

    assert metrics.r1_loops == 1
    assert metrics.r2_cancellations == 1
    assert not any(isinstance(item.op, Return) for item in normal.operations)
    assert not any(isinstance(item.op, Cross) for item in normal.operations)
    assert strategy_interface(normal).response_classes == (
        "alternating-transverse",
        "reenters",
    )


def test_r3_like_staging_batches_independent_frames_without_crossing_support() -> None:
    """INFERENCE: independent work may stage together; shared support may not commute."""

    tangle = StrategyTangle(
        raw=RawStrategyTrace(
            "A",
            (
                stage("reasoning", IntroduceRole("B")),
                stage("reasoning", IntroduceRole("C")),
                stage("inspection", Probe("inspect-B", ("B",))),
                stage("analysis", Extend("C")),
            ),
        ),
        boundary=("A", "B", "C"),
    )
    normal, metrics = normalize_strategy_tangle(tangle)

    assert metrics.r3_reorders == 1
    assert normal.operations[-2].frame == "analysis"
    assert normal.operations[-1].frame == "inspection"

    blocked = StrategyTangle(
        raw=RawStrategyTrace(
            "A",
            (
                stage("reasoning", IntroduceRole("B")),
                stage("inspection", Probe("inspect-B", ("B",))),
                stage("analysis", Extend("B")),
            ),
        ),
        boundary=("A", "B"),
    )
    blocked_normal, blocked_metrics = normalize_strategy_tangle(blocked)
    assert blocked_metrics.r3_reorders == 0
    assert blocked_normal.operations[-2].frame == "inspection"


def test_normalization_is_idempotent() -> None:
    """INFERENCE: a normal form is a fixed point of the staging pass."""

    _, long, *_ = red_team_staging_fixtures()
    policy = NormalizationPolicy(periodic_cycles=(("B", "C"),))
    normal, _ = normalize_strategy_tangle(long, policy)
    replay = StrategyTangle(
        raw=RawStrategyTrace(normal.anchor, normal.operations),
        boundary=normal.boundary,
        signature=StrategySignature(
            response_classes=normal.response_classes,
            options=normal.options,
        ),
    )
    renormalized, metrics = normalize_strategy_tangle(replay, policy)

    assert renormalized == normal
    assert metrics.r1_loops == 0
    assert metrics.r2_cancellations == 0
    assert metrics.r3_reorders == 0
    assert metrics.periodic_folds == 0


def test_unweave_binds_sequential_roleplay_to_typed_operations_only() -> None:
    """UNWEAVE: roleplay order is serialized observation, not construction history."""

    realized = ConstructionState({"a": ("b",), "b": ("a",)}, {"a": 0})
    root = begin_hypothetical(realized)
    snapshot = StrategySnapshot(root, StrategySignature())
    episode = RoleplayEpisode(
        realized,
        (
            See(snapshot),
            Ask(snapshot, "inspect-b"),
        ),
    )
    trace = unweave_roleplay(
        episode,
        "A",
        (
            RoleplayBinding(0, stage("reasoning", IntroduceRole("B"))),
            RoleplayBinding(1, stage("inspection", Probe("inspect-b", ("B",)))),
        ),
    )

    assert trace.anchor == "A"
    assert len(trace.operations) == 2
    assert build_role_ledger(trace).remaining_degrees == 2
    assert dict(realized.coloring) == {"a": 0}


def test_class_count_is_discovered_not_encoded() -> None:
    """INFERENCE: fixture compression reports whatever normal forms actually remain."""

    fixtures = red_team_staging_fixtures()
    policy = NormalizationPolicy(
        mirror_equivalent=True,
        periodic_cycles=(("B", "C"),),
    )
    classes = classify_normal_forms(fixtures, policy)
    report = build_staging_report(fixtures, policy)

    assert report.raw_traces == len(fixtures)
    assert report.normal_forms == len(classes)
    assert report.normal_forms < report.raw_traces
    assert report.raw_operations > report.max_normalized_operations

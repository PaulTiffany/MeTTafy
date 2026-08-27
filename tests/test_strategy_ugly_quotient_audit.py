from __future__ import annotations

from mettafy.four_color_strategy_ugly_adversaries import ugly_strategy_challenges
from mettafy.strategy_ugly_quotient_audit import (
    audit_ugly_quotient_challenges,
    evaluate_ugly_quotient_challenge,
)
from mettafy.strategy_ugly_staging import normalize_ugly_strategy_tangle


def _by_name() -> dict[str, object]:
    return {challenge.name: challenge for challenge in ugly_strategy_challenges()}


def test_ugly_corpus_pressures_collapse_and_split_without_target_class_count() -> None:
    """INFERENCE: every local claim passes; global class count remains discovered."""

    challenges = ugly_strategy_challenges()
    results, report = audit_ugly_quotient_challenges(challenges)

    assert len(challenges) == 12
    assert report.collapse_challenges == 6
    assert report.split_challenges == 6
    assert report.passed == len(challenges)
    assert report.failures == ()
    assert report.discovered_normal_forms <= report.raw_presentations
    assert all(result.passed for result in results)


def test_disjoint_commutation_is_explicit_not_visual_guessing() -> None:
    """INFERENCE: the same nested crossing pair collapses only with authority."""

    challenges = {item.name: item for item in ugly_strategy_challenges()}
    authorized = evaluate_ugly_quotient_challenge(
        challenges[
            "inverse-crossings-cancel-across-disjoint-work-when-authorized"
        ]
    )
    guarded = evaluate_ugly_quotient_challenge(
        challenges[
            "inverse-crossings-stay-distinct-without-commutation-authority"
        ]
    )

    assert authorized.same_normal_form
    assert not guarded.same_normal_form


def test_response_complete_cut_happens_before_role_accounting() -> None:
    """INFERENCE: suffix-only role introduction cannot consume independent freedom."""

    challenges = {item.name: item for item in ugly_strategy_challenges()}
    challenge = challenges[
        "post-probe-role-introduction-cannot-consume-freedom-after-cut"
    ]
    left, left_metrics = normalize_ugly_strategy_tangle(
        challenge.left, challenge.policy
    )
    right, right_metrics = normalize_ugly_strategy_tangle(
        challenge.right, challenge.policy
    )

    assert left == right
    assert left.remaining_roles == ("D",)
    assert left_metrics.suffix_operations_dropped == 0
    assert right_metrics.suffix_operations_dropped == 2


def test_response_complete_cut_does_not_erase_pre_probe_observation() -> None:
    """INFERENCE: bounded stopping discards only the suffix, never observer history."""

    challenges = {item.name: item for item in ugly_strategy_challenges()}
    result = evaluate_ugly_quotient_challenge(
        challenges["pre-probe-observation-survives-the-cut"]
    )

    assert not result.same_normal_form
    assert result.same_interface


def test_incomplete_recurrence_cannot_be_promoted_to_periodic() -> None:
    """INFERENCE: a partial red-team exemplar remains distinguishable."""

    challenges = {item.name: item for item in ugly_strategy_challenges()}
    result = evaluate_ugly_quotient_challenge(
        challenges["incomplete-red-team-recurrence-is-not-a-complete-cycle"]
    )

    assert not result.same_normal_form


def test_ugly_normalization_does_not_mutate_source_trace() -> None:
    """INFERENCE: staging consumes a projection copy, not the realized antecedent."""

    challenge = ugly_strategy_challenges()[4]
    before = challenge.right.raw.operations
    normalize_ugly_strategy_tangle(challenge.right, challenge.policy)

    assert challenge.right.raw.operations == before

from __future__ import annotations

from dataclasses import dataclass

from mettafy.strategy_quotient_audit import (
    QuotientAuditReport,
    QuotientChallengeResult,
    QuotientExpectation,
)
from mettafy.strategy_staging import StrategyTangle, strategy_interface
from mettafy.strategy_ugly_staging import (
    UglyNormalizationPolicy,
    normalize_ugly_strategy_tangle,
)


@dataclass(frozen=True)
class UglyQuotientChallenge:
    """INFERENCE: one deliberately ugly local claim about the strategy quotient."""

    name: str
    left: StrategyTangle
    right: StrategyTangle
    policy: UglyNormalizationPolicy
    expectation: QuotientExpectation
    observable: str
    motif: str


def evaluate_ugly_quotient_challenge(
    challenge: UglyQuotientChallenge,
) -> QuotientChallengeResult:
    """Normalize both ugly presentations without granting construction authority."""

    left_normal, _ = normalize_ugly_strategy_tangle(challenge.left, challenge.policy)
    right_normal, _ = normalize_ugly_strategy_tangle(challenge.right, challenge.policy)
    left_interface = strategy_interface(left_normal)
    right_interface = strategy_interface(right_normal)
    same_normal = left_normal == right_normal
    same_interface = left_interface == right_interface
    expected_same = challenge.expectation == "collapse"
    return QuotientChallengeResult(
        name=challenge.name,
        expectation=challenge.expectation,
        observable=challenge.observable,
        same_normal_form=same_normal,
        same_interface=same_interface,
        passed=same_normal == expected_same,
        left_normal=left_normal,
        right_normal=right_normal,
        left_interface=left_interface,
        right_interface=right_interface,
    )


def audit_ugly_quotient_challenges(
    challenges: tuple[UglyQuotientChallenge, ...],
) -> tuple[tuple[QuotientChallengeResult, ...], QuotientAuditReport]:
    """Run ugly pressure while discovering, rather than prescribing, class count."""

    results = tuple(evaluate_ugly_quotient_challenge(item) for item in challenges)
    normals = tuple(
        normal
        for result in results
        for normal in (result.left_normal, result.right_normal)
    )
    failures = tuple(result.name for result in results if not result.passed)
    report = QuotientAuditReport(
        challenges=len(results),
        collapse_challenges=sum(result.expectation == "collapse" for result in results),
        split_challenges=sum(result.expectation == "split" for result in results),
        passed=sum(result.passed for result in results),
        failures=failures,
        raw_presentations=2 * len(results),
        discovered_normal_forms=len(set(normals)),
    )
    return results, report

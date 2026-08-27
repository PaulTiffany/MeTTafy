from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.strategy_staging import (
    NormalizationPolicy,
    StrategyInterface,
    StrategyNormalForm,
    StrategyTangle,
    normalize_strategy_tangle,
    strategy_interface,
)

QuotientExpectation: TypeAlias = Literal["collapse", "split"]


@dataclass(frozen=True)
class QuotientChallenge:
    """INFERENCE: one falsifiable claim about the Strategy-IR quotient.

    `observable` names the proof-relevant distinction whose presence or absence
    justifies the expected relation. The challenge never grants construction
    authority; it only attacks the proposed normal-form equivalence.
    """

    name: str
    left: StrategyTangle
    right: StrategyTangle
    policy: NormalizationPolicy
    expectation: QuotientExpectation
    observable: str


@dataclass(frozen=True)
class QuotientChallengeResult:
    """INFERENCE: measured outcome of one quotient challenge."""

    name: str
    expectation: QuotientExpectation
    observable: str
    same_normal_form: bool
    same_interface: bool
    passed: bool
    left_normal: StrategyNormalForm
    right_normal: StrategyNormalForm
    left_interface: StrategyInterface
    right_interface: StrategyInterface


@dataclass(frozen=True)
class QuotientAuditReport:
    """INFERENCE: corpus-level pressure against under- and over-compression."""

    challenges: int
    collapse_challenges: int
    split_challenges: int
    passed: int
    failures: tuple[str, ...]
    raw_presentations: int
    discovered_normal_forms: int

    @property
    def compression_ratio(self) -> float:
        if self.raw_presentations == 0:
            return 1.0
        return self.discovered_normal_forms / self.raw_presentations


def evaluate_quotient_challenge(challenge: QuotientChallenge) -> QuotientChallengeResult:
    """Normalize both presentations and test the caller's explicit quotient claim."""

    left_normal, _ = normalize_strategy_tangle(challenge.left, challenge.policy)
    right_normal, _ = normalize_strategy_tangle(challenge.right, challenge.policy)
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


def audit_quotient_challenges(
    challenges: tuple[QuotientChallenge, ...],
) -> tuple[tuple[QuotientChallengeResult, ...], QuotientAuditReport]:
    """Run the adversarial quotient corpus without encoding a target class count."""

    results = tuple(evaluate_quotient_challenge(item) for item in challenges)
    normals: list[StrategyNormalForm] = []
    for result in results:
        normals.extend((result.left_normal, result.right_normal))
    failures = tuple(result.name for result in results if not result.passed)
    report = QuotientAuditReport(
        challenges=len(results),
        collapse_challenges=sum(
            result.expectation == "collapse" for result in results
        ),
        split_challenges=sum(result.expectation == "split" for result in results),
        passed=sum(result.passed for result in results),
        failures=failures,
        raw_presentations=2 * len(results),
        discovered_normal_forms=len(set(normals)),
    )
    return results, report

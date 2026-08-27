from __future__ import annotations

import json

from mettafy.four_color_strategy_ugly_adversaries import ugly_strategy_challenges
from mettafy.strategy_ugly_quotient_audit import audit_ugly_quotient_challenges
from mettafy.strategy_ugly_staging import normalize_ugly_strategy_tangle


def main() -> None:
    challenges = ugly_strategy_challenges()
    results, report = audit_ugly_quotient_challenges(challenges)
    by_name = {challenge.name: challenge for challenge in challenges}

    commutations = 0
    suffix_drops = 0
    outcomes: list[dict[str, object]] = []
    for result in results:
        challenge = by_name[result.name]
        _, left_metrics = normalize_ugly_strategy_tangle(
            challenge.left, challenge.policy
        )
        _, right_metrics = normalize_ugly_strategy_tangle(
            challenge.right, challenge.policy
        )
        commutations += (
            left_metrics.disjoint_commutations + right_metrics.disjoint_commutations
        )
        suffix_drops += (
            left_metrics.suffix_operations_dropped
            + right_metrics.suffix_operations_dropped
        )
        outcomes.append(
            {
                "name": result.name,
                "motif": challenge.motif,
                "expectation": result.expectation,
                "observable": result.observable,
                "same_normal_form": result.same_normal_form,
                "same_interface": result.same_interface,
                "passed": result.passed,
            }
        )

    payload = {
        "challenges": report.challenges,
        "collapse_challenges": report.collapse_challenges,
        "split_challenges": report.split_challenges,
        "passed": report.passed,
        "failures": list(report.failures),
        "raw_presentations": report.raw_presentations,
        "discovered_normal_forms": report.discovered_normal_forms,
        "compression_ratio": report.compression_ratio,
        "disjoint_commutations": commutations,
        "suffix_operations_dropped": suffix_drops,
        "outcomes": outcomes,
        "non_claim": (
            "Ugly fixture success is evidence about explicit quotient hypotheses, "
            "not StrategyIRCompleteness, InferenceSoundness, a CertifiedInstantiation, "
            "or the Four Color Theorem."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json

from mettafy.four_color_strategy_adversaries import adversarial_strategy_challenges
from mettafy.strategy_quotient_audit import audit_quotient_challenges


def main() -> None:
    results, report = audit_quotient_challenges(adversarial_strategy_challenges())
    payload = {
        "challenges": report.challenges,
        "collapse_challenges": report.collapse_challenges,
        "split_challenges": report.split_challenges,
        "passed": report.passed,
        "failures": report.failures,
        "raw_presentations": report.raw_presentations,
        "discovered_normal_forms": report.discovered_normal_forms,
        "compression_ratio": report.compression_ratio,
        "outcomes": [
            {
                "name": result.name,
                "expectation": result.expectation,
                "same_normal_form": result.same_normal_form,
                "same_interface": result.same_interface,
                "observable": result.observable,
            }
            for result in results
        ],
        "non_claim": (
            "Finite fixture success is evidence about the proposed quotient, "
            "not a proof of StrategyIRCompleteness or the Four Color Theorem."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

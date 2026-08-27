from __future__ import annotations

from mettafy.four_color_strategy_adversaries import adversarial_strategy_challenges
from mettafy.strategy_quotient_audit import audit_quotient_challenges


def test_adversarial_corpus_attacks_under_and_over_compression() -> None:
    challenges = adversarial_strategy_challenges()
    results, report = audit_quotient_challenges(challenges)

    assert report.collapse_challenges > 0
    assert report.split_challenges > 0
    assert report.passed == report.challenges, report.failures
    assert report.failures == ()
    assert report.discovered_normal_forms < report.raw_presentations
    assert any(result.same_normal_form for result in results)
    assert any(not result.same_normal_form for result in results)


def test_periodic_depth_collapses_but_periodic_tail_does_not() -> None:
    results, _ = audit_quotient_challenges(adversarial_strategy_challenges())
    by_name = {result.name: result for result in results}

    depth = by_name["periodic-depth-is-not-strategy-depth"]
    tail = by_name["periodic-tail-is-new-until-proved-irrelevant"]
    assert depth.same_normal_form
    assert depth.same_interface
    assert not tail.same_normal_form
    assert not tail.same_interface


def test_explicit_mirror_authority_changes_only_the_quotient_claim() -> None:
    results, _ = audit_quotient_challenges(adversarial_strategy_challenges())
    by_name = {result.name: result for result in results}

    enabled = by_name["mirror-is-one-class-when-explicitly-authorized"]
    disabled = by_name["mirror-remains-distinct-without-authority"]
    assert enabled.same_normal_form
    assert not disabled.same_normal_form


def test_proof_relevant_interface_differences_are_not_normalized_away() -> None:
    results, _ = audit_quotient_challenges(adversarial_strategy_challenges())
    by_name = {result.name: result for result in results}

    for name in (
        "safe-first-option-must-survive-quotient",
        "response-class-must-survive-quotient",
        "remaining-independent-role-must-survive-quotient",
    ):
        result = by_name[name]
        assert not result.same_normal_form
        assert not result.same_interface


def test_shared_support_order_and_probe_identity_resist_overcompression() -> None:
    results, _ = audit_quotient_challenges(adversarial_strategy_challenges())
    by_name = {result.name: result for result in results}

    shared = by_name["shared-support-order-cannot-r3-commute"]
    probe = by_name["probe-observable-must-survive-quotient"]
    assert not shared.same_normal_form
    assert not probe.same_normal_form

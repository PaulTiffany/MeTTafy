"""Tests for blind-only structural recognition and unit-local evaluation."""

from __future__ import annotations

import pytest

from mettafy.ir import StrategyKind
from mettafy.recognition import evaluate_against_held_out, recognize_from_structural
from mettafy.structural import (
    blind_audit_map,
    blind_structural_view,
    extract_structural_evidence,
)

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.

Theorem induction_only n : target n.
Proof.
elim: n => // n IHn.
exact IHn.
Qed.

Theorem decision_only x : target x.
Proof.
have H := decide_colorable x.
exact x.
Qed.

Theorem plain x : target x.
Proof. exact x. Qed.
'''


def _raw():
    return extract_structural_evidence(
        {"proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="test"
    )


def test_recognizer_rejects_raw_structural_evidence_by_type_boundary():
    with pytest.raises(TypeError, match="BlindStructuralEvidence"):
        recognize_from_structural(_raw())  # type: ignore[arg-type]


def test_compound_dataflow_can_promote_to_generic_reduction():
    blind = blind_structural_view(_raw())
    result = recognize_from_structural(blind)
    reductions = [
        strategy for strategy in result.strategies if strategy.kind == StrategyKind.REDUCTION
    ]
    assert len(reductions) == 1
    assert reductions[0].evidence[0].kind == "structural-dataflow-composition"
    assert reductions[0].evidence[0].span.filename.startswith("source:")


def test_single_induction_and_decision_observations_abstain_instead_of_overclaiming():
    raw = _raw()
    blind = blind_structural_view(raw)
    audit = blind_audit_map(raw)
    result = recognize_from_structural(blind)

    name_by_blind_id = {unit_id: info["original_name"] for unit_id, info in audit.items()}
    abstained_names = {
        name_by_blind_id[item["local_id"]]
        for item in result.abstentions
    }
    assert "induction_only" in abstained_names
    assert "decision_only" in abstained_names
    assert all(strategy.kind != StrategyKind.CERTIFICATE_CHECK for strategy in result.strategies)


def test_near_miss_multiple_applications_without_dataflow_does_not_become_reduction():
    source = r'''Theorem near_miss x : target x.
Proof. apply helper. exact x. Qed.
'''
    raw = extract_structural_evidence({"n.v": source}, upstream_sha=UPSTREAM_SHA)
    result = recognize_from_structural(blind_structural_view(raw))
    assert not result.strategies
    assert result.abstentions


def test_recognition_output_contains_no_held_out_labels_or_audit_names():
    raw = _raw()
    result = recognize_from_structural(blind_structural_view(raw))
    dumped = str(result.to_dict()).lower()
    for token in (
        "composed",
        "induction_only",
        "decision_only",
        "finitereduction",
        "discretization",
        "unavoidability",
        "reducibility",
    ):
        assert token not in dumped


def test_evaluation_is_unit_local_and_cannot_credit_an_unrelated_layer():
    raw = _raw()
    blind = blind_structural_view(raw)
    audit = blind_audit_map(raw)
    result = recognize_from_structural(blind)
    composed_id = next(
        unit_id for unit_id, info in audit.items() if info["original_name"] == "composed"
    )
    induction_id = next(
        unit_id
        for unit_id, info in audit.items()
        if info["original_name"] == "induction_only"
    )

    report = evaluate_against_held_out(
        result,
        {
            composed_id: ["FiniteReduction"],
            induction_id: ["StructuralReduction"],
        },
    )
    assert report["evaluation_only"] is True
    assert report["unit_local"] is True
    assert any(item["unit"] == composed_id for item in report["matches"])
    assert induction_id in report["unpredicted_units"]
    assert not any(item["unit"] == induction_id for item in report["matches"])

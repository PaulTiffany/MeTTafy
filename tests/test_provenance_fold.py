from __future__ import annotations

from mettafy.emit import emit_strategy_metta
from mettafy.recognition import RECOGNITION_RULES, recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
'''


def test_provenance_survives_recognition_ir_and_metta_emission() -> None:
    raw = extract_structural_evidence(
        {"proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="test"
    )
    result = recognize_from_structural(blind_structural_view(raw))

    assert len(result.strategies) == 1
    assert len(result.rule_traces) == len(RECOGNITION_RULES)
    assert len(result.provenance_edges) == 1
    strategy = result.strategies[0]
    trace = next(item for item in result.rule_traces if item.decision == "promote")
    edge = result.provenance_edges[0]

    assert edge.relation == "authorized_by"
    assert edge.source_id == trace.trace_id
    assert edge.target_id == strategy.id
    assert "provenance" not in strategy.to_dict()

    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    expected = f'(Provenance "authorized_by" "{trace.trace_id}" "{strategy.id}")'
    assert expected in emitted


def test_emitted_provenance_remains_inside_blind_capability_boundary() -> None:
    raw = extract_structural_evidence(
        {"secret-fourcolor-proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="test"
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    ).lower()

    for forbidden in (
        "secret-fourcolor-proof",
        "four_color",
        "discretization",
        "unavoidability",
        "reducibility",
        UPSTREAM_SHA.lower(),
    ):
        assert forbidden not in emitted

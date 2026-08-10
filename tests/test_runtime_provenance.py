from __future__ import annotations

from mettafy.emit import emit_strategy_metta
from mettafy.recognition import recognize_from_structural
from mettafy.runtime_trace import check_emitted_provenance
from mettafy.structural import blind_structural_view, extract_structural_evidence

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
'''


def _result():
    raw = extract_structural_evidence(
        {"proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="runtime-test"
    )
    return recognize_from_structural(blind_structural_view(raw))


def test_runtime_checker_closes_fold_from_emitted_artifact_to_witness() -> None:
    result = _result()
    emitted = emit_strategy_metta(
        result.strategies, provenance_edges=result.provenance_edges
    )
    trace, witness, links = check_emitted_provenance(
        emitted, provenance_edges=result.provenance_edges
    )

    assert trace.decision == "pass"
    assert trace.expected_edges == trace.verified_edges == 1
    assert witness.decision == "pass"
    assert witness.runtime_trace_id == trace.trace_id
    assert witness.artifact_sha256 == trace.artifact_sha256
    assert [(edge.relation, edge.source_id, edge.target_id) for edge in links] == [
        ("checked_as", trace.artifact_id, trace.trace_id),
        ("certified_by", trace.trace_id, witness.witness_id),
    ]


def test_runtime_checker_fails_closed_when_provenance_atom_is_missing() -> None:
    result = _result()
    emitted = emit_strategy_metta(result.strategies)
    trace, witness, _ = check_emitted_provenance(
        emitted, provenance_edges=result.provenance_edges
    )
    assert trace.decision == "fail"
    assert trace.verified_edges == 0
    assert witness.decision == "fail"


def test_public_strategy_contract_remains_unchanged() -> None:
    strategy = _result().strategies[0]
    assert set(strategy.to_dict()) == {"id", "kind", "confidence", "evidence", "children"}

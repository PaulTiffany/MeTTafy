from __future__ import annotations

import pytest

from mettafy.derived_probe import (
    derive_authorized_by_liveness_program,
    derived_probe_links,
)
from mettafy.emit import emit_strategy_metta
from mettafy.hyperon_witness import trace_from_record
from mettafy.recognition import recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
SOURCE = r"""
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
"""


def _result():
    raw = extract_structural_evidence(
        {"proof.v": SOURCE},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="derived-probe-test",
    )
    return recognize_from_structural(blind_structural_view(raw))


def test_probe_is_justified_by_promoted_recovered_dependency() -> None:
    result = _result()
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    program = derive_authorized_by_liveness_program(emitted, result)
    assert program is not None

    edge = program.justification.dependency
    assert edge.relation == "authorized_by"
    assert edge in result.provenance_edges
    assert program.justification.rule_trace_id == edge.source_id
    assert program.justification.strategy_id == edge.target_id
    assert program.justification.observed_required_features == ("composition",)
    assert program.probe.dependency_id == program.justification.dependency_id


def test_probe_is_instrumented_derivative_not_canonical_artifact() -> None:
    result = _result()
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    program = derive_authorized_by_liveness_program(emitted, result)
    assert program is not None

    assert program.instrumented_metta.startswith(emitted)
    assert program.instrumented_metta != emitted
    assert program.instrumented_artifact_sha256 != program.canonical_artifact_sha256
    assert program.instrumented_artifact_id != program.canonical_artifact_id
    assert "!(remove-atom &self (Provenance " in program.instrumented_metta
    assert "!(add-atom &self (Provenance " in program.instrumented_metta


def test_probe_indices_account_for_existing_queries_and_forms() -> None:
    result = _result()
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    with_existing_query = emitted + "!(existing-query)\n"
    program = derive_authorized_by_liveness_program(with_existing_query, result)
    assert program is not None

    assert program.probe.baseline_query_index == 1
    assert program.probe.perturbed_query_index == 3
    assert program.probe.restored_query_index == 5

    existing_forms = sum(
        1
        for line in with_existing_query.splitlines()
        if line.strip() and not line.lstrip().startswith(";")
    )
    assert program.probe.mutation_step_index == existing_forms + 1
    assert program.probe.restoration_step_index == existing_forms + 3


def test_probe_abstains_when_recognition_has_no_promoted_dependency() -> None:
    raw = extract_structural_evidence(
        {"proof.v": "Theorem inert x : target x.\nProof.\nexact x.\nQed.\n"},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="derived-probe-test",
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    assert derive_authorized_by_liveness_program(emitted, result) is None


def test_probe_fails_closed_if_recovered_edge_was_not_emitted() -> None:
    result = _result()
    emitted_without_provenance = emit_strategy_metta(result.strategies)
    with pytest.raises(ValueError, match="dependency is absent"):
        derive_authorized_by_liveness_program(emitted_without_provenance, result)


def test_derived_links_require_trace_identity_and_digest_match() -> None:
    result = _result()
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    program = derive_authorized_by_liveness_program(emitted, result)
    assert program is not None

    good_record = {
        "ok": True,
        "engine": "hyperon",
        "engine_version": "test",
        "results": [],
        "atoms": [],
        "steps": [],
        "error": "",
    }
    trace = trace_from_record(
        program.instrumented_metta,
        good_record,
        artifact_id=program.instrumented_artifact_id,
    )
    assert [edge.relation for edge in derived_probe_links(program, trace)] == [
        "instrumented_as",
        "executed_as",
    ]

    wrong_trace = trace_from_record(
        program.instrumented_metta + "; changed\n",
        good_record,
        artifact_id=program.instrumented_artifact_id,
    )
    assert [edge.relation for edge in derived_probe_links(program, wrong_trace)] == [
        "instrumented_as"
    ]

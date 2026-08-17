from __future__ import annotations

from mettafy.derived_probe import derive_authorized_by_liveness_program
from mettafy.distinction_witness import (
    DistinctionDecision,
    assess_distinction_preservation,
    instrument_dependency_observation,
)
from mettafy.emit import emit_strategy_metta
from mettafy.hyperon_witness import trace_from_record
from mettafy.recognition import recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
BASELINE = r"""
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
"""
PERTURBED = r"""
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (finish x).
Qed.
"""


def _compile(source: str, label: str):
    raw = extract_structural_evidence(
        {"proof.v": source},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha=label,
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    return result, emitted


def _record(results: list[list[str]], *, ok: bool = True):
    return {
        "ok": ok,
        "engine": "hyperon",
        "engine_version": "test",
        "results": results,
        "atoms": [],
        "steps": [],
        "error": "" if ok else "boom",
    }


def _programs():
    baseline_result, baseline_emitted = _compile(BASELINE, "baseline")
    perturbed_result, perturbed_emitted = _compile(PERTURBED, "perturbed")
    restored_result, restored_emitted = _compile(BASELINE, "baseline")

    derived = derive_authorized_by_liveness_program(
        baseline_emitted,
        baseline_result,
    )
    assert derived is not None
    justification = derived.justification

    baseline_program = instrument_dependency_observation(
        baseline_emitted,
        justification,
        canonical_artifact_id="artifact:baseline",
    )
    perturbed_program = instrument_dependency_observation(
        perturbed_emitted,
        justification,
        canonical_artifact_id="artifact:perturbed",
    )
    restored_program = instrument_dependency_observation(
        restored_emitted,
        justification,
        canonical_artifact_id="artifact:restored",
    )
    return (
        baseline_result,
        perturbed_result,
        restored_result,
        baseline_emitted,
        perturbed_emitted,
        restored_emitted,
        baseline_program,
        perturbed_program,
        restored_program,
    )


def test_source_composition_distinction_changes_recovered_dependency() -> None:
    (
        baseline_result,
        perturbed_result,
        restored_result,
        baseline_emitted,
        perturbed_emitted,
        restored_emitted,
        *_,
    ) = _programs()

    assert baseline_result.strategies
    assert baseline_result.provenance_edges
    assert perturbed_result.strategies == []
    assert perturbed_result.provenance_edges == []
    assert restored_result.strategies
    assert baseline_emitted != perturbed_emitted
    assert baseline_emitted == restored_emitted


def test_observation_program_is_read_only_and_variant_specific() -> None:
    *_, baseline_program, perturbed_program, restored_program = _programs()

    assert "!(match &self (Provenance " in baseline_program.instrumented_metta
    assert "remove-atom" not in baseline_program.instrumented_metta
    assert "add-atom" not in baseline_program.instrumented_metta
    assert baseline_program.canonical_artifact_sha256 != (
        perturbed_program.canonical_artifact_sha256
    )
    assert baseline_program.canonical_artifact_sha256 == (
        restored_program.canonical_artifact_sha256
    )
    assert baseline_program.dependency_id == perturbed_program.dependency_id
    assert baseline_program.dependency_id == restored_program.dependency_id


def test_preserved_when_target_observation_tracks_source_perturbation() -> None:
    *_, baseline_program, perturbed_program, restored_program = _programs()
    baseline_trace = trace_from_record(
        baseline_program.instrumented_metta,
        _record([["Present"]]),
        artifact_id=baseline_program.instrumented_artifact_id,
    )
    perturbed_trace = trace_from_record(
        perturbed_program.instrumented_metta,
        _record([[]]),
        artifact_id=perturbed_program.instrumented_artifact_id,
    )
    restored_trace = trace_from_record(
        restored_program.instrumented_metta,
        _record([["Present"]]),
        artifact_id=restored_program.instrumented_artifact_id,
    )
    assessment = assess_distinction_preservation(
        baseline_trace,
        baseline_program,
        perturbed_trace,
        perturbed_program,
        restored_trace,
        restored_program,
    )
    assert assessment.decision is DistinctionDecision.PRESERVED
    assert assessment.baseline == ("Present",)
    assert assessment.perturbed == ()
    assert assessment.restored == ("Present",)


def test_collapsed_when_source_perturbation_does_not_change_target_observation() -> None:
    *_, baseline_program, perturbed_program, restored_program = _programs()
    traces = [
        trace_from_record(
            program.instrumented_metta,
            _record([["Present"]]),
            artifact_id=program.instrumented_artifact_id,
        )
        for program in (baseline_program, perturbed_program, restored_program)
    ]
    assessment = assess_distinction_preservation(
        traces[0],
        baseline_program,
        traces[1],
        perturbed_program,
        traces[2],
        restored_program,
    )
    assert assessment.decision is DistinctionDecision.COLLAPSED


def test_inconsistent_when_restoration_does_not_recover_baseline() -> None:
    *_, baseline_program, perturbed_program, restored_program = _programs()
    baseline_trace = trace_from_record(
        baseline_program.instrumented_metta,
        _record([["Present"]]),
        artifact_id=baseline_program.instrumented_artifact_id,
    )
    perturbed_trace = trace_from_record(
        perturbed_program.instrumented_metta,
        _record([[]]),
        artifact_id=perturbed_program.instrumented_artifact_id,
    )
    restored_trace = trace_from_record(
        restored_program.instrumented_metta,
        _record([[]]),
        artifact_id=restored_program.instrumented_artifact_id,
    )
    assessment = assess_distinction_preservation(
        baseline_trace,
        baseline_program,
        perturbed_trace,
        perturbed_program,
        restored_trace,
        restored_program,
    )
    assert assessment.decision is DistinctionDecision.INCONSISTENT

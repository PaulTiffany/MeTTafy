from __future__ import annotations

import json
from pathlib import Path

from mettafy.derived_probe import derive_authorized_by_liveness_program
from mettafy.distinction_witness import (
    DistinctionDecision,
    assess_distinction_preservation,
    instrument_dependency_observation,
)
from mettafy.emit import emit_strategy_metta
from mettafy.hyperon_witness import run_hyperon_witness
from mettafy.recognition import recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "source-distinction-correspondence.json"
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
    blind = blind_structural_view(raw)
    result = recognize_from_structural(blind)
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    return blind, result, emitted


def main() -> int:
    baseline_blind, baseline_result, baseline_emitted = _compile(
        BASELINE,
        "source-distinction-baseline",
    )
    perturbed_blind, perturbed_result, perturbed_emitted = _compile(
        PERTURBED,
        "source-distinction-perturbed",
    )
    restored_blind, restored_result, restored_emitted = _compile(
        BASELINE,
        "source-distinction-baseline",
    )

    derived = derive_authorized_by_liveness_program(
        baseline_emitted,
        baseline_result,
    )
    if derived is None:
        raise SystemExit("baseline recognizer produced no dependency to observe")
    justification = derived.justification

    baseline_program = instrument_dependency_observation(
        baseline_emitted,
        justification,
        canonical_artifact_id="artifact:semantic-metta",
    )
    perturbed_program = instrument_dependency_observation(
        perturbed_emitted,
        justification,
        canonical_artifact_id="artifact:semantic-metta:perturbed",
    )
    restored_program = instrument_dependency_observation(
        restored_emitted,
        justification,
        canonical_artifact_id="artifact:semantic-metta",
    )

    baseline_trace = run_hyperon_witness(
        baseline_program.instrumented_metta,
        artifact_id=baseline_program.instrumented_artifact_id,
    )
    perturbed_trace = run_hyperon_witness(
        perturbed_program.instrumented_metta,
        artifact_id=perturbed_program.instrumented_artifact_id,
    )
    restored_trace = run_hyperon_witness(
        restored_program.instrumented_metta,
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

    baseline_features = {
        feature.value
        for unit in baseline_blind.units
        for feature in unit.features
    }
    perturbed_features = {
        feature.value
        for unit in perturbed_blind.units
        for feature in unit.features
    }
    restored_features = {
        feature.value
        for unit in restored_blind.units
        for feature in unit.features
    }

    failures: list[str] = []
    if "composition" not in baseline_features:
        failures.append("baseline source did not expose the composition premise")
    if "composition" in perturbed_features:
        failures.append("source perturbation did not remove the composition premise")
    if restored_features != baseline_features:
        failures.append("source restoration did not recover baseline structural features")
    if not baseline_result.provenance_edges:
        failures.append("baseline recognition produced no promoted provenance dependency")
    if perturbed_result.provenance_edges:
        failures.append("perturbed recognition retained a dependency that should disappear")
    if baseline_emitted == perturbed_emitted:
        failures.append("source perturbation collapsed to the same emitted artifact")
    if baseline_emitted != restored_emitted:
        failures.append("source restoration did not recover the byte-identical emitted artifact")
    if assessment.decision is not DistinctionDecision.PRESERVED:
        failures.append(
            f"runtime distinction was not preserved: {assessment.decision.value}"
        )

    payload = {
        "witness": "WIT-SOURCE-DISTINCTION-CORRESPONDENCE",
        "result": "pass" if not failures else "fail",
        "claim": (
            "For the bounded dataflow-composition distinction used by MeTTafy's current "
            "Reduction recognizer, removing the source-side mechanical premise removes "
            "the recovered dependency from the emitted target and from the exact Hyperon "
            "observation; restoring the source recovers the byte-identical target artifact "
            "and runtime observation."
        ),
        "non_claims": [
            "general source-to-target semantic faithfulness",
            "Rocq theorem validity of the synthetic perturbation fixture",
            "equivalence of all source programs sharing the same structural features",
            "causal completeness of the current recognizer",
        ],
        "source_distinction": {
            "feature": "composition",
            "baseline_features": sorted(baseline_features),
            "perturbed_features": sorted(perturbed_features),
            "restored_features": sorted(restored_features),
            "baseline_corpus_hash": baseline_blind.provenance.corpus_hash,
            "perturbed_corpus_hash": perturbed_blind.provenance.corpus_hash,
            "restored_corpus_hash": restored_blind.provenance.corpus_hash,
        },
        "recovered_dependency": {
            "dependency_id": justification.dependency_id,
            "relation": justification.dependency.relation,
            "source_id": justification.dependency.source_id,
            "target_id": justification.dependency.target_id,
            "rule_id": justification.rule_id,
            "observed_required_features": list(justification.observed_required_features),
        },
        "canonical_artifacts": {
            "baseline_sha256": baseline_program.canonical_artifact_sha256,
            "perturbed_sha256": perturbed_program.canonical_artifact_sha256,
            "restored_sha256": restored_program.canonical_artifact_sha256,
            "baseline_equals_restored": baseline_emitted == restored_emitted,
        },
        "runtime_observations": {
            "baseline": list(assessment.baseline),
            "perturbed": list(assessment.perturbed),
            "restored": list(assessment.restored),
            "baseline_trace_id": baseline_trace.trace_id,
            "perturbed_trace_id": perturbed_trace.trace_id,
            "restored_trace_id": restored_trace.trace_id,
            "engine_version": baseline_trace.engine_version,
        },
        "assessment": {
            "decision": assessment.decision.value,
            "reason": assessment.reason,
        },
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print(
        "Source-distinction correspondence witness passed: "
        "composition -> Present, perturb -> absent, restore -> Present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

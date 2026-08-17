from __future__ import annotations

import json
from pathlib import Path

from mettafy.derived_probe import (
    derive_authorized_by_liveness_program,
    derived_probe_links,
)
from mettafy.emit import emit_strategy_metta
from mettafy.hyperon_witness import (
    LivenessDecision,
    assess_state_liveness,
    run_hyperon_witness,
)
from mettafy.recognition import recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "derived-hyperon-liveness.json"
UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
SOURCE = r"""
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
"""


def main() -> int:
    raw = extract_structural_evidence(
        {"proof.v": SOURCE},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="derived-hyperon-witness",
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )
    program = derive_authorized_by_liveness_program(emitted, result)
    if program is None:
        raise SystemExit("recognizer produced no eligible dependency for a derived liveness probe")

    trace = run_hyperon_witness(
        program.instrumented_metta,
        artifact_id=program.instrumented_artifact_id,
    )
    assessment = assess_state_liveness(trace, program.probe)
    links = derived_probe_links(program, trace)

    failures: list[str] = []
    if not trace.ok:
        failures.append(f"Hyperon execution failed: {trace.error}")
    if assessment.decision is not LivenessDecision.LIVE:
        failures.append(
            f"derived dependency was not demonstrated live: {assessment.decision.value}"
        )
    if [edge.relation for edge in links] != ["instrumented_as", "executed_as"]:
        failures.append("instrumented artifact provenance linkage drifted")

    payload = {
        "witness": "WIT-DERIVED-HYPERON-LIVENESS",
        "result": "pass" if not failures else "fail",
        "claim": (
            "A provenance dependency mechanically promoted by MeTTafy's blind recognizer "
            "survived emission and was observably coupled to target MeTTa runtime state: "
            "removing that exact dependency changed its query result and restoring it "
            "returned the result to baseline."
        ),
        "non_claims": [
            "source-to-target semantic faithfulness",
            "that every recovered strategy dependency is operationally live",
            "that failure of a future perturbation would prove dead semantics",
            "arbitrary causal interpretability of Hyperon internals",
        ],
        "canonical_artifact": {
            "artifact_id": program.canonical_artifact_id,
            "sha256": program.canonical_artifact_sha256,
        },
        "instrumented_artifact": {
            "artifact_id": program.instrumented_artifact_id,
            "sha256": program.instrumented_artifact_sha256,
        },
        "justification": {
            "dependency_id": program.justification.dependency_id,
            "dependency": {
                "relation": program.justification.dependency.relation,
                "source_id": program.justification.dependency.source_id,
                "target_id": program.justification.dependency.target_id,
            },
            "rule_trace_id": program.justification.rule_trace_id,
            "rule_id": program.justification.rule_id,
            "unit_id": program.justification.unit_id,
            "strategy_id": program.justification.strategy_id,
            "observed_required_features": list(
                program.justification.observed_required_features
            ),
        },
        "probe": {
            "baseline_query_index": program.probe.baseline_query_index,
            "perturbed_query_index": program.probe.perturbed_query_index,
            "restored_query_index": program.probe.restored_query_index,
            "mutation_step_index": program.probe.mutation_step_index,
            "restoration_step_index": program.probe.restoration_step_index,
        },
        "execution": {
            "trace_id": trace.trace_id,
            "engine": trace.engine,
            "engine_version": trace.engine_version,
            "ok": trace.ok,
            "results": [list(items) for items in trace.results],
            "steps": [
                {
                    "form": step.form,
                    "results": list(step.results),
                    "added": list(step.added),
                    "removed": list(step.removed),
                }
                for step in trace.steps[-5:]
            ],
        },
        "assessment": {
            "decision": assessment.decision.value,
            "reason": assessment.reason,
        },
        "links": [
            {
                "relation": edge.relation,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
            }
            for edge in links
        ],
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print(
        "Derived Hyperon liveness witness passed: recovered dependency "
        "-> emitted atom -> reversible runtime effect."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

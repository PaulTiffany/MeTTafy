from __future__ import annotations

import json
from pathlib import Path

from mettafy.hyperon_witness import (
    LivenessDecision,
    StateLivenessProbe,
    assess_state_liveness,
    execution_links,
    run_hyperon_witness,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "hyperon-state-liveness.json"

SOURCE = """
(likes Sam pizza)
!(match &self (likes Sam $f) $f)
!(add-atom &self (likes Sam sushi))
!(match &self (likes Sam $f) $f)
!(remove-atom &self (likes Sam sushi))
!(match &self (likes Sam $f) $f)
""".strip() + "\n"

PROBE = StateLivenessProbe(
    dependency_id="fixture:likes-sushi",
    baseline_query_index=0,
    perturbed_query_index=2,
    restored_query_index=4,
    mutation_step_index=2,
    restoration_step_index=4,
)


def main() -> int:
    trace = run_hyperon_witness(SOURCE, artifact_id="artifact:liveness-fixture")
    assessment = assess_state_liveness(trace, PROBE)
    links = execution_links(trace)

    failures = []
    if not trace.ok:
        failures.append(f"Hyperon execution failed: {trace.error}")
    if assessment.decision is not LivenessDecision.LIVE:
        failures.append(f"state liveness was not demonstrated: {assessment.decision.value}")
    if [edge.relation for edge in links] != ["executed_as"]:
        failures.append("successful Hyperon execution did not produce the typed executed_as relation")

    payload = {
        "witness": "WIT-HYPERON-STATE-LIVENESS",
        "result": "pass" if not failures else "fail",
        "claim": (
            "A query result changed under a witnessed MeTTa-resident state perturbation "
            "and returned to baseline after witnessed restoration."
        ),
        "non_claims": [
            "source-to-target semantic faithfulness",
            "proof of the Four Color Theorem",
            "failure of an arbitrary perturbation proves dead semantics",
            "python -I is a hostile-code security sandbox",
        ],
        "execution": {
            "trace_id": trace.trace_id,
            "artifact_sha256": trace.artifact_sha256,
            "engine": trace.engine,
            "engine_version": trace.engine_version,
            "ok": trace.ok,
            "results": [list(result) for result in trace.results],
            "steps": [
                {
                    "form": step.form,
                    "results": list(step.results),
                    "added": list(step.added),
                    "removed": list(step.removed),
                }
                for step in trace.steps
            ],
            "error": trace.error,
        },
        "liveness": {
            "dependency_id": assessment.dependency_id,
            "decision": assessment.decision.value,
            "reason": assessment.reason,
        },
        "runtime_links": [
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
    print("Hyperon state-liveness witness passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

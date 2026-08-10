from __future__ import annotations

import json
from pathlib import Path

from mettafy.emit import emit_strategy_metta
from mettafy.recognition import recognize_from_structural
from mettafy.runtime_trace import check_emitted_provenance
from mettafy.structural import blind_structural_view, extract_structural_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "runtime-provenance-fold.json"
UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
'''


def main() -> int:
    raw = extract_structural_evidence(
        {"proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="runtime-witness"
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies, provenance_edges=result.provenance_edges
    )
    trace, witness, runtime_links = check_emitted_provenance(
        emitted, provenance_edges=result.provenance_edges
    )

    failures: list[str] = []
    if trace.decision != "pass":
        failures.append("artifact provenance checker did not pass")
    if witness.decision != "pass":
        failures.append("witness record did not certify the checked artifact")
    if trace.expected_edges != trace.verified_edges:
        failures.append("not all expected provenance edges survived emission")
    if [edge.relation for edge in runtime_links] != ["checked_as", "certified_by"]:
        failures.append("runtime provenance relations drifted")

    payload = {
        "witness": "WIT-RUNTIME-PROVENANCE-FOLD",
        "result": "pass" if not failures else "fail",
        "claim": (
            "The emitted semantic MeTTa artifact is deterministically checked for its expected "
            "provenance edges and linked through a typed runtime trace to a certification witness."
        ),
        "non_claims": [
            "the MeTTa artifact has been evaluated by a MeTTa execution engine",
            "semantic correctness beyond the checked provenance relation",
            "arbitrary runtime causal interpretability",
        ],
        "runtime_trace": {
            "trace_id": trace.trace_id,
            "artifact_id": trace.artifact_id,
            "artifact_sha256": trace.artifact_sha256,
            "checker": trace.checker,
            "expected_edges": trace.expected_edges,
            "verified_edges": trace.verified_edges,
            "decision": trace.decision,
        },
        "witness_record": {
            "witness_id": witness.witness_id,
            "runtime_trace_id": witness.runtime_trace_id,
            "decision": witness.decision,
            "artifact_sha256": witness.artifact_sha256,
        },
        "runtime_links": [
            {
                "relation": edge.relation,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
            }
            for edge in runtime_links
        ],
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print("Runtime provenance witness passed: artifact -> runtime trace -> witness linkage intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

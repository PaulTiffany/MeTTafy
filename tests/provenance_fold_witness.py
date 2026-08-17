from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mettafy.emit import emit_strategy_metta
from mettafy.recognition import recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "provenance-fold-collapse.json"
UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.
'''


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    raw = extract_structural_evidence(
        {"proof.v": SOURCE}, upstream_sha=UPSTREAM_SHA, mettafy_sha="witness"
    )
    result = recognize_from_structural(blind_structural_view(raw))
    emitted = emit_strategy_metta(
        result.strategies,
        provenance_edges=result.provenance_edges,
    )

    failures: list[str] = []
    chains: list[dict[str, str]] = []
    traces = {trace.trace_id: trace for trace in result.rule_traces}

    for strategy in result.strategies:
        parents = [
            edge
            for edge in result.provenance_edges
            if edge.relation == "authorized_by" and edge.target_id == strategy.id
        ]
        if len(parents) != 1:
            failures.append(f"{strategy.id}: expected exactly one authorized_by parent")
            continue
        edge = parents[0]
        trace = traces.get(edge.source_id)
        if trace is None or trace.decision != "promote":
            failures.append(f"{strategy.id}: invalid authorization parent")
            continue
        expected = f'(Provenance "authorized_by" "{edge.source_id}" "{edge.target_id}")'
        if expected not in emitted:
            failures.append(f"{strategy.id}: emitted MeTTa lost authorization edge")
        chains.append(
            {
                "trace_id": trace.trace_id,
                "rule_id": trace.rule_id,
                "strategy_id": strategy.id,
                "relation": edge.relation,
            }
        )

    canonical = json.dumps(chains, sort_keys=True, separators=(",", ":"))
    payload = {
        "witness": "WIT-PROVENANCE-FOLD-COLLAPSE",
        "result": "pass" if not failures else "fail",
        "claim": "Sibling RuleTrace authorization survives Strategy construction and MeTTa emission.",
        "chains": chains,
        "chain_sha256": sha256(canonical),
        "emitted_metta_sha256": sha256(emitted),
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("; ".join(failures))
    print("Provenance fold witness passed with stable Strategy contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

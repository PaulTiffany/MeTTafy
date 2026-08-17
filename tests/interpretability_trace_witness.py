from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mettafy.recognition import RECOGNITION_RULES, recognize_from_structural
from mettafy.structural import blind_structural_view, extract_structural_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "mechanistic-interpretability-trace.json"
UPSTREAM_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

SOURCE = r'''
Theorem composed x : target x.
Proof.
pose proof (prepare x) as [w transport].
exact (transport (finish w)).
Qed.

Theorem near_miss x : target x.
Proof. apply helper. exact x. Qed.
'''


def canonical_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def run(min_confidence: float = 0.55) -> dict[str, object]:
    raw = extract_structural_evidence(
        {"proof.v": SOURCE},
        upstream_sha=UPSTREAM_SHA,
        mettafy_sha="interpretability-witness",
    )
    blind = blind_structural_view(raw)
    result = recognize_from_structural(blind, min_confidence=min_confidence)
    return result.to_dict()


def main() -> int:
    failures: list[str] = []
    baseline = run()
    replay = run()
    strict = run(min_confidence=0.80)

    baseline_hash = canonical_hash(baseline)
    replay_hash = canonical_hash(replay)
    if baseline_hash != replay_hash:
        failures.append("mechanistic trace replay is not deterministic")

    strategies = baseline["strategies"]
    traces = baseline["rule_traces"]
    abstentions = baseline["abstentions"]
    if not isinstance(strategies, list) or len(strategies) != 1:
        failures.append("baseline must promote exactly one strategy")
    expected_trace_count = 2 * len(RECOGNITION_RULES)
    if not isinstance(traces, list) or len(traces) != expected_trace_count:
        failures.append("baseline must emit one rule trace per rule per blind unit")
    if not isinstance(abstentions, list) or len(abstentions) != 1:
        failures.append("baseline must abstain on the near-miss unit")

    promote_traces = [item for item in traces if item.get("decision") == "promote"]
    miss_traces = [item for item in traces if item.get("decision") == "not_applicable"]
    if len(promote_traces) != 1:
        failures.append("expected exactly one promoting trace")
    if len(miss_traces) != expected_trace_count - 1:
        failures.append("all non-promoting baseline rule evaluations must be visible")
    if not any(
        item.get("rule_id") == "recognition.reduction.dataflow-composition.v1"
        and item.get("missing_required_features") == ["composition"]
        for item in miss_traces
    ):
        failures.append("near-miss composition trace must identify the exact missing premise")

    strict_strategies = strict["strategies"]
    strict_traces = strict["rule_traces"]
    if not isinstance(strict_strategies, list) or strict_strategies:
        failures.append("strict confidence threshold must suppress promotion")
    if not any(item.get("decision") == "below_threshold" for item in strict_traces):
        failures.append("strict run must expose below-threshold decision")

    dumped = json.dumps(baseline, sort_keys=True).lower()
    forbidden = (
        "composed",
        "near_miss",
        "proof.v",
        "four_color",
        "discretization",
        "unavoidability",
        "reducibility",
        UPSTREAM_SHA.lower(),
    )
    leaked = [token for token in forbidden if token in dumped]
    if leaked:
        failures.append("trace leaked source/audit/held-out tokens: " + ", ".join(leaked))

    payload = {
        "witness": "WIT-MECHANISTIC-INTERPRETABILITY-TRACE",
        "strength": "bounded",
        "result": "pass" if not failures else "fail",
        "claim": (
            "For the bounded bootstrap recognizer, every configured semantic rule emits a "
            "source-neutral deterministic trace exposing premises, missing premises, guards, "
            "confidence threshold, decision, and abstention counterfactuals without changing "
            "the recognizer's semantic authority boundary."
        ),
        "non_claims": [
            "the trace explains arbitrary neural-model internals",
            "the current rule vocabulary is semantically complete",
            "held-out Four Color labels are available to the recognizer",
            "natural-language explanations are causal evidence",
            "the bounded witness proves general mechanistic interpretability",
        ],
        "rule_count": len(RECOGNITION_RULES),
        "baseline_sha256": baseline_hash,
        "replay_sha256": replay_hash,
        "baseline": baseline,
        "strict_threshold": strict,
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("; ".join(failures))
    print(
        "Mechanistic interpretability witness passed: deterministic source-neutral rule traces, "
        "exact missing-premise counterfactuals, and visible confidence gating verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

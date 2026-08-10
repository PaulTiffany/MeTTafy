"""Source-neutral semantic recognition with mechanistic rule traces.

Recognizers accept only BlindStructuralEvidence. Raw source text, names,
references, paths, comments, and held-out annotations are outside the
recognizer's object capability, not merely ignored by convention.

The trace layer records which bounded rule was considered, which premises were
observed, which guards failed, and why. Provenance is carried in a sibling graph
so the stable public Strategy serialization contract remains unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ir import Evidence, ProvenanceEdge, SourceSpan, Strategy, StrategyKind
from .structural import BlindStructuralEvidence, BlindStructuralUnit, ObservableFeature


@dataclass(frozen=True)
class RuleTrace:
    rule_id: str
    local_id: str
    target: str
    required_features: tuple[str, ...]
    observed_required_features: tuple[str, ...]
    missing_required_features: tuple[str, ...]
    forbidden_features: tuple[str, ...]
    observed_forbidden_features: tuple[str, ...]
    confidence: float
    min_confidence: float
    decision: str
    reason: str

    @property
    def trace_id(self) -> str:
        return f"trace:{self.local_id}:{self.rule_id}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "rule_id": self.rule_id,
            "local_id": self.local_id,
            "target": self.target,
            "required_features": list(self.required_features),
            "observed_required_features": list(self.observed_required_features),
            "missing_required_features": list(self.missing_required_features),
            "forbidden_features": list(self.forbidden_features),
            "observed_forbidden_features": list(self.observed_forbidden_features),
            "confidence": self.confidence,
            "min_confidence": self.min_confidence,
            "decision": self.decision,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class RecognitionRule:
    rule_id: str
    target: StrategyKind
    required: frozenset[ObservableFeature]
    forbidden: frozenset[ObservableFeature]
    confidence: float
    evidence_kind: str
    evidence_detail: str


REDUCTION_COMPOSITION_RULE = RecognitionRule(
    rule_id="recognition.reduction.dataflow-composition.v1",
    target=StrategyKind.REDUCTION,
    required=frozenset({ObservableFeature.COMPOSITION}),
    forbidden=frozenset(),
    confidence=0.78,
    evidence_kind="structural-dataflow-composition",
    evidence_detail=(
        "A result bound by one proof application is consumed by a later "
        "application in the same structural unit"
    ),
)

COUNTEREXAMPLE_DISCHARGE_RULE = RecognitionRule(
    rule_id="recognition.reduction.counterexample-discharge.v1",
    target=StrategyKind.REDUCTION,
    required=frozenset(
        {
            ObservableFeature.INDUCTION,
            ObservableFeature.CASE_SPLIT,
            ObservableFeature.DECISION_CALL,
            ObservableFeature.APPLICATION,
        }
    ),
    forbidden=frozenset(),
    confidence=0.74,
    evidence_kind="structural-counterexample-discharge",
    evidence_detail=(
        "An inductive descent is combined with an explicit decision branch and "
        "subsequent proof application, mechanically indicating a candidate "
        "counterexample-discharge reduction"
    ),
)

RECOGNITION_RULES: tuple[RecognitionRule, ...] = (
    REDUCTION_COMPOSITION_RULE,
    COUNTEREXAMPLE_DISCHARGE_RULE,
)
UNSUPPORTED_SEMANTIC_FEATURES = frozenset(
    {
        ObservableFeature.INDUCTION,
        ObservableFeature.CASE_SPLIT,
        ObservableFeature.REWRITE_TRANSPORT,
        ObservableFeature.DECISION_CALL,
        ObservableFeature.APPLICATION,
        ObservableFeature.RECURSION,
        ObservableFeature.EXTERNAL_BOUNDARY,
    }
)


@dataclass(frozen=True)
class RecognitionResult:
    strategies: list[Strategy]
    abstentions: list[dict[str, Any]] = field(default_factory=list)
    predictions_by_unit: dict[str, list[str]] = field(default_factory=dict)
    rule_traces: list[RuleTrace] = field(default_factory=list)
    provenance_edges: list[ProvenanceEdge] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategies": [strategy.to_dict() for strategy in self.strategies],
            "abstentions": list(self.abstentions),
            "predictions_by_unit": dict(self.predictions_by_unit),
            "rule_traces": [trace.to_dict() for trace in self.rule_traces],
            "provenance_edges": [
                {
                    "relation": edge.relation,
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                }
                for edge in self.provenance_edges
            ],
        }


def _span_from_blind(unit: BlindStructuralUnit) -> SourceSpan:
    return SourceSpan(
        filename=unit.source_token or "<blind>",
        start_line=unit.start_line,
        end_line=unit.end_line,
    )


def _feature_names(
    features: set[ObservableFeature] | frozenset[ObservableFeature],
) -> tuple[str, ...]:
    return tuple(sorted(feature.value for feature in features))


def _evaluate_rule(
    rule: RecognitionRule,
    unit: BlindStructuralUnit,
    *,
    min_confidence: float,
) -> RuleTrace:
    features = set(unit.features)
    observed_required = rule.required & features
    missing_required = rule.required - features
    observed_forbidden = rule.forbidden & features
    if missing_required:
        decision, reason = (
            "not_applicable",
            "required mechanical premise(s) were not observed",
        )
    elif observed_forbidden:
        decision, reason = "blocked", "a forbidden mechanical feature was observed"
    elif rule.confidence < min_confidence:
        decision, reason = (
            "below_threshold",
            "rule confidence is below the configured promotion threshold",
        )
    else:
        decision, reason = (
            "promote",
            "all mechanical premises hold and no guard blocks promotion",
        )
    return RuleTrace(
        rule_id=rule.rule_id,
        local_id=unit.local_id,
        target=rule.target.value,
        required_features=_feature_names(rule.required),
        observed_required_features=_feature_names(observed_required),
        missing_required_features=_feature_names(missing_required),
        forbidden_features=_feature_names(rule.forbidden),
        observed_forbidden_features=_feature_names(observed_forbidden),
        confidence=rule.confidence,
        min_confidence=min_confidence,
        decision=decision,
        reason=reason,
    )


def recognize_from_structural(
    blind: BlindStructuralEvidence,
    *,
    min_confidence: float = 0.55,
) -> RecognitionResult:
    if not isinstance(blind, BlindStructuralEvidence):
        raise TypeError(
            "recognize_from_structural accepts only BlindStructuralEvidence; "
            "raw StructuralEvidence must first pass through blind_structural_view()"
        )
    if not 0.0 <= min_confidence <= 1.0:
        raise ValueError("min_confidence must be between 0 and 1")

    strategies: list[Strategy] = []
    abstentions: list[dict[str, Any]] = []
    predictions_by_unit: dict[str, list[str]] = {}
    rule_traces: list[RuleTrace] = []
    provenance_edges: list[ProvenanceEdge] = []

    for unit in blind.units:
        features = set(unit.features)
        span = _span_from_blind(unit)
        unit_predictions: list[str] = []
        unit_traces: list[RuleTrace] = []
        for rule in RECOGNITION_RULES:
            trace = _evaluate_rule(rule, unit, min_confidence=min_confidence)
            rule_traces.append(trace)
            unit_traces.append(trace)
            if trace.decision != "promote":
                continue
            strategy_id = f"pred:{unit.local_id}:{rule.target.value.lower()}"
            strategy = Strategy(
                id=strategy_id,
                kind=rule.target,
                confidence=rule.confidence,
                evidence=[
                    Evidence(
                        kind=rule.evidence_kind,
                        detail=rule.evidence_detail,
                        span=span,
                    )
                ],
            )
            strategies.append(strategy)
            provenance_edges.append(
                ProvenanceEdge(
                    relation="authorized_by",
                    source_id=trace.trace_id,
                    target_id=strategy_id,
                )
            )
            unit_predictions.append(strategy.kind.value)

        unsupported = sorted(
            feature.value
            for feature in features
            if feature in UNSUPPORTED_SEMANTIC_FEATURES
        )
        if not unit_predictions:
            if unsupported:
                reason = (
                    "mechanical features are present, but no configured semantic rule "
                    "is justified by the blind evidence"
                )
            elif not features:
                reason = "no high-precision structural features observed"
            else:
                reason = "observed features do not satisfy any configured promotion rule"
            abstentions.append(
                {
                    "local_id": unit.local_id,
                    "observed_features": sorted(feature.value for feature in features),
                    "unsupported_semantic_features": unsupported,
                    "considered_rules": [trace.rule_id for trace in unit_traces],
                    "why_not": [
                        {
                            "rule_id": trace.rule_id,
                            "target": trace.target,
                            "decision": trace.decision,
                            "missing_required_features": list(
                                trace.missing_required_features
                            ),
                            "observed_forbidden_features": list(
                                trace.observed_forbidden_features
                            ),
                            "reason": trace.reason,
                        }
                        for trace in unit_traces
                        if trace.decision != "promote"
                    ],
                    "reason": reason,
                    "status": "abstain",
                }
            )
        if unit_predictions:
            predictions_by_unit[unit.local_id] = unit_predictions

    return RecognitionResult(
        strategies=strategies,
        abstentions=abstentions,
        predictions_by_unit=predictions_by_unit,
        rule_traces=rule_traces,
        provenance_edges=provenance_edges,
    )


def evaluate_against_held_out(
    result: RecognitionResult,
    held_out_by_unit: dict[str, list[str]],
) -> dict[str, Any]:
    alignment = {
        "Reduction": {"FiniteReduction", "StructuralReduction", "Reducibility"},
        "CertificateCheck": {"DecisionProcedure", "CertificateCheck"},
    }
    matches: list[dict[str, Any]] = []
    misses: list[dict[str, Any]] = []
    unpredicted_units: list[str] = []
    unevaluated_prediction_units: list[str] = []
    for unit_id, targets in held_out_by_unit.items():
        target_set = set(targets)
        predictions = result.predictions_by_unit.get(unit_id, [])
        if not predictions:
            unpredicted_units.append(unit_id)
            continue
        for prediction in predictions:
            related = alignment.get(prediction, set())
            hit = target_set & related
            if hit:
                matches.append(
                    {
                        "unit": unit_id,
                        "predicted": prediction,
                        "held_out_hit": sorted(hit),
                    }
                )
            else:
                misses.append(
                    {
                        "unit": unit_id,
                        "predicted": prediction,
                        "held_out": sorted(target_set),
                        "note": "no documented alignment for this unit",
                    }
                )
    for unit_id in result.predictions_by_unit:
        if unit_id not in held_out_by_unit:
            unevaluated_prediction_units.append(unit_id)
    return {
        "matches": matches,
        "misses": misses,
        "unpredicted_units": sorted(unpredicted_units),
        "unevaluated_prediction_units": sorted(unevaluated_prediction_units),
        "abstention_count": len(result.abstentions),
        "evaluation_only": True,
        "unit_local": True,
        "note": (
            "Comparison is unit-local and post-hoc. Held-out annotations are "
            "outside the recognizer input boundary."
        ),
    }

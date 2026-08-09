"""Source-neutral semantic recognition seam for Issue #32.

Recognizers accept only BlindStructuralEvidence. Raw source text, names,
references, paths, comments, and held-out annotations are therefore outside the
recognizer's object capability, not merely ignored by convention.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ir import Evidence, SourceSpan, Strategy, StrategyKind
from .structural import (
    BlindStructuralEvidence,
    BlindStructuralUnit,
    ObservableFeature,
)


@dataclass(frozen=True)
class RecognitionResult:
    strategies: list[Strategy]
    abstentions: list[dict[str, Any]] = field(default_factory=list)
    predictions_by_unit: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategies": [strategy.to_dict() for strategy in self.strategies],
            "abstentions": list(self.abstentions),
            "predictions_by_unit": dict(self.predictions_by_unit),
        }


def _span_from_blind(unit: BlindStructuralUnit) -> SourceSpan:
    return SourceSpan(
        filename=unit.source_token or "<blind>",
        start_line=unit.start_line,
        end_line=unit.end_line,
    )


def recognize_from_structural(
    blind: BlindStructuralEvidence,
    *,
    min_confidence: float = 0.55,
) -> RecognitionResult:
    """Promote only compound structural evidence to semantic StrategyKind.

    Single lower-level observations such as induction, rewrite, case split, or
    a decision-procedure-shaped call remain structural facts. They are reported
    as abstentions when the current StrategyKind vocabulary would require a
    stronger semantic claim than the evidence warrants.
    """
    if not isinstance(blind, BlindStructuralEvidence):
        raise TypeError(
            "recognize_from_structural accepts only BlindStructuralEvidence; "
            "raw StructuralEvidence must first pass through blind_structural_view()"
        )

    strategies: list[Strategy] = []
    abstentions: list[dict[str, Any]] = []
    predictions_by_unit: dict[str, list[str]] = {}

    for unit in blind.units:
        features = set(unit.features)
        span = _span_from_blind(unit)
        unit_predictions: list[str] = []

        # A dataflow composition is stronger than the mere occurrence of two
        # tactic words: one applied result is mechanically observed feeding a
        # later application. The existing bootstrap vocabulary can honestly
        # represent that as a generic Reduction, but not as a more specific
        # Four Color strategy such as Discretization or ProofByTransport.
        if ObservableFeature.COMPOSITION in features:
            strategy = Strategy(
                id=f"pred:{unit.local_id}:reduction",
                kind=StrategyKind.REDUCTION,
                confidence=0.78,
                evidence=[
                    Evidence(
                        kind="structural-dataflow-composition",
                        detail=(
                            "A result bound by one proof application is consumed "
                            "by a later application in the same structural unit"
                        ),
                        span=span,
                    )
                ],
            )
            if strategy.confidence >= min_confidence:
                strategies.append(strategy)
                unit_predictions.append(strategy.kind.value)

        unsupported = sorted(
            feature.value
            for feature in features
            if feature
            in {
                ObservableFeature.INDUCTION,
                ObservableFeature.CASE_SPLIT,
                ObservableFeature.REWRITE_TRANSPORT,
                ObservableFeature.DECISION_CALL,
                ObservableFeature.APPLICATION,
                ObservableFeature.RECURSION,
                ObservableFeature.EXTERNAL_BOUNDARY,
            }
        )
        if unsupported and not unit_predictions:
            abstentions.append(
                {
                    "local_id": unit.local_id,
                    "observed_features": unsupported,
                    "reason": (
                        "mechanical features are present, but the current "
                        "StrategyKind vocabulary would overstate their semantics"
                    ),
                    "status": "abstain",
                }
            )
        elif not features:
            abstentions.append(
                {
                    "local_id": unit.local_id,
                    "observed_features": [],
                    "reason": "no high-precision structural features observed",
                    "status": "abstain",
                }
            )

        if unit_predictions:
            predictions_by_unit[unit.local_id] = unit_predictions

    return RecognitionResult(
        strategies=strategies,
        abstentions=abstentions,
        predictions_by_unit=predictions_by_unit,
    )


def evaluate_against_held_out(
    result: RecognitionResult,
    held_out_by_unit: dict[str, list[str]],
) -> dict[str, Any]:
    """Perform unit-local post-hoc evaluation; never classifier feedback."""
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

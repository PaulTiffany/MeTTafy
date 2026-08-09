"""Source-neutral semantic recognition seam (Issue #32).

The recognizer is typed to accept only BlindStructuralEvidence.
It therefore cannot access body_form, original names, raw references,
or path strings. Held-out annotations are consulted only in the
evaluation helper, never as classifier input.
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
    # local_id → list of predicted StrategyKind values (for unit-local eval)
    predictions_by_unit: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategies": [s.to_dict() for s in self.strategies],
            "abstentions": list(self.abstentions),
            "predictions_by_unit": dict(self.predictions_by_unit),
        }


def _span_from_blind(unit: BlindStructuralUnit) -> SourceSpan:
    # Filename is the opaque span token only — no recoverable path.
    return SourceSpan(
        filename=unit.span_token or "<blind>",
        start_line=unit.start_line,
        end_line=unit.end_line,
    )


def recognize_from_structural(
    blind: BlindStructuralEvidence,
    *,
    min_confidence: float = 0.55,
) -> RecognitionResult:
    """Map blind structural observations to Strategy candidates or abstain.

    Parameters
    ----------
    blind:
        Must be BlindStructuralEvidence. Passing raw StructuralEvidence is a
        type error and is the mechanical enforcement of the authority boundary.
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
        feats = set(unit.features)
        span = _span_from_blind(unit)
        local = unit.local_id
        unit_preds: list[str] = []

        if ObservableFeature.COMPOSITION in feats or (
            ObservableFeature.APPLICATION in feats
            and ObservableFeature.REWRITE_TRANSPORT in feats
        ):
            strategies.append(
                Strategy(
                    id=f"pred:{local}:reduction",
                    kind=StrategyKind.REDUCTION,
                    confidence=0.78,
                    evidence=[
                        Evidence(
                            kind="structural-composition",
                            detail=(
                                "Unit exhibits multiple applications / "
                                "composition of previously established results"
                            ),
                            span=span,
                        )
                    ],
                )
            )
            unit_preds.append(StrategyKind.REDUCTION.value)

        if ObservableFeature.INDUCTION in feats:
            strategies.append(
                Strategy(
                    id=f"pred:{local}:induction",
                    kind=StrategyKind.REDUCTION,
                    confidence=0.72,
                    evidence=[
                        Evidence(
                            kind="structural-induction",
                            detail="Inductive argument on a size measure is present",
                            span=span,
                        )
                    ],
                )
            )
            unit_preds.append(StrategyKind.REDUCTION.value)

        if ObservableFeature.DECISION_CALL in feats:
            strategies.append(
                Strategy(
                    id=f"pred:{local}:decision",
                    kind=StrategyKind.CERTIFICATE_CHECK,
                    confidence=0.70,
                    evidence=[
                        Evidence(
                            kind="structural-decision",
                            detail="Explicit decision-procedure call observed",
                            span=span,
                        )
                    ],
                )
            )
            unit_preds.append(StrategyKind.CERTIFICATE_CHECK.value)

        if not feats:
            abstentions.append(
                {
                    "local_id": local,
                    "reason": "no high-precision structural features observed",
                    "status": "abstain",
                }
            )

        if unit_preds:
            predictions_by_unit[local] = unit_preds

    strategies = [s for s in strategies if s.confidence >= min_confidence]
    return RecognitionResult(
        strategies=strategies,
        abstentions=abstentions,
        predictions_by_unit=predictions_by_unit,
    )


def evaluate_against_held_out(
    result: RecognitionResult,
    held_out_by_unit: dict[str, list[str]],
) -> dict[str, Any]:
    """Unit-local post-hoc comparison. Never used as classifier input.

    Parameters
    ----------
    result:
        Output of recognize_from_structural.
    held_out_by_unit:
        Mapping from blind local_id (or a stable unit key) to held-out
        strategy label strings. Only predictions for the same unit are
        compared; there is no global credit across layers.
    """
    alignment = {
        "Reduction": {"FiniteReduction", "StructuralReduction", "Reducibility"},
        "CertificateCheck": {"DecisionProcedure", "CertificateCheck"},
    }

    matches: list[dict[str, Any]] = []
    misses: list[dict[str, Any]] = []
    unmatched_units: list[str] = []

    for unit_id, targets in held_out_by_unit.items():
        target_set = set(targets)
        preds = result.predictions_by_unit.get(unit_id, [])
        if not preds:
            unmatched_units.append(unit_id)
            continue
        for pred in preds:
            related = alignment.get(pred, set())
            hit = target_set & related
            if hit:
                matches.append(
                    {
                        "unit": unit_id,
                        "predicted": pred,
                        "held_out_hit": sorted(hit),
                    }
                )
            else:
                misses.append(
                    {
                        "unit": unit_id,
                        "predicted": pred,
                        "held_out": sorted(target_set),
                        "note": "no documented alignment for this unit",
                    }
                )

    return {
        "matches": matches,
        "misses": misses,
        "unmatched_units": unmatched_units,
        "abstention_count": len(result.abstentions),
        "evaluation_only": True,
        "unit_local": True,
        "note": (
            "Comparison is unit-local and post-hoc. "
            "It must never be fed back into the recognizer."
        ),
    }

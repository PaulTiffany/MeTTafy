"""Source-neutral semantic recognition seam (Issue #32).

Consumes StructuralEvidence (or its blind projection) and produces
evidence-backed Strategy candidates. The recognizer is deliberately
conservative: it may return Unknown / abstain rather than invent labels.

Authority boundary
------------------
- Structural features are observed facts.
- Strategy labels are predictions with explicit evidence and confidence.
- Rocq remains the sole theorem-validity authority.
- Held-out annotations are consulted only in the evaluation helper,
  never as classifier input.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .ir import Evidence, SourceSpan, Strategy, StrategyKind
from .structural import ObservableFeature, StructuralEvidence, StructuralUnit


@dataclass(frozen=True)
class RecognitionResult:
    strategies: list[Strategy]
    abstentions: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategies": [s.to_dict() for s in self.strategies],
            "abstentions": list(self.abstentions),
        }


def _span_from_unit(unit: StructuralUnit) -> SourceSpan:
    if unit.span is None:
        return SourceSpan(filename="<unknown>", start_line=1, end_line=1)
    return SourceSpan(
        filename=unit.span.path,
        start_line=unit.span.start_line,
        end_line=unit.span.end_line,
    )


def _feature_set(unit: StructuralUnit) -> set[ObservableFeature]:
    return set(unit.features)


def recognize_from_structural(
    evidence: StructuralEvidence,
    *,
    min_confidence: float = 0.55,
) -> RecognitionResult:
    """Map structural observations to Strategy candidates or abstain.

    The mapping is intentionally narrow and high-precision. It uses only
    the mechanical features already present in the StructuralEvidence IR.
    No theorem names, path roles, or held-out labels are consulted.
    """
    strategies: list[Strategy] = []
    abstentions: list[dict[str, Any]] = []

    for unit in evidence.units:
        feats = _feature_set(unit)
        span = _span_from_unit(unit)
        local = unit.local_id

        # Composition of applications on a short theorem body is a strong
        # structural signal for a reduction / transport pipeline.
        if (
            ObservableFeature.COMPOSITION in feats
            or (
                ObservableFeature.APPLICATION in feats
                and ObservableFeature.REWRITE_TRANSPORT in feats
            )
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
                                "Unit body exhibits multiple applications / "
                                "composition of previously established results"
                            ),
                            span=span,
                        )
                    ],
                )
            )

        # Induction + decision procedure is a classic minimal-counterexample
        # / structural-reduction shape; we surface it as REDUCTION with
        # supporting evidence rather than inventing a new StrategyKind.
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

        if ObservableFeature.DECISION_CALL in feats:
            strategies.append(
                Strategy(
                    id=f"pred:{local}:decision",
                    kind=StrategyKind.CERTIFICATE_CHECK,
                    confidence=0.70,
                    evidence=[
                        Evidence(
                            kind="structural-decision",
                            detail="Explicit colorability / decision procedure call observed",
                            span=span,
                        )
                    ],
                )
            )

        # If a unit carries no recognised high-precision features, abstain.
        if not feats:
            abstentions.append(
                {
                    "local_id": local,
                    "reason": "no high-precision structural features observed",
                    "status": "abstain",
                }
            )

    # Filter by minimum confidence
    strategies = [s for s in strategies if s.confidence >= min_confidence]
    return RecognitionResult(strategies=strategies, abstentions=abstentions)


def evaluate_against_held_out(
    result: RecognitionResult,
    held_out: dict[str, list[str]],
) -> dict[str, Any]:
    """Post-hoc comparison only. Never used as classifier input.

    Parameters
    ----------
    result:
        Output of recognize_from_structural.
    held_out:
        Mapping from proof-layer id to list of strategy label strings,
        typically produced by exemplar_strategy_targets(manifest).
    """
    predicted_kinds = {s.kind.value for s in result.strategies}
    # The held-out vocabulary uses different surface names; we perform a
    # deliberately coarse, documented alignment for evaluation only.
    alignment = {
        "Reduction": {"FiniteReduction", "StructuralReduction", "Reducibility"},
        "CertificateCheck": {"DecisionProcedure", "CertificateCheck"},
        # Further alignments can be added as the recognizer grows.
    }

    matches: list[dict[str, Any]] = []
    misses: list[dict[str, Any]] = []

    for layer_id, targets in held_out.items():
        target_set = set(targets)
        for pred in predicted_kinds:
            related = alignment.get(pred, set())
            hit = target_set & related
            if hit:
                matches.append(
                    {
                        "layer": layer_id,
                        "predicted": pred,
                        "held_out_hit": sorted(hit),
                    }
                )
            else:
                misses.append(
                    {
                        "layer": layer_id,
                        "predicted": pred,
                        "held_out": sorted(target_set),
                        "note": "no documented alignment",
                    }
                )

    return {
        "predicted_kinds": sorted(predicted_kinds),
        "matches": matches,
        "misses": misses,
        "abstention_count": len(result.abstentions),
        "evaluation_only": True,
        "note": (
            "This comparison is performed after recognition and must never "
            "be fed back into the recognizer as input."
        ),
    }

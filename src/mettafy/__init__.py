"""MeTTafy: semantic decompilation into executable MeTTa."""

from .analysis import analyze_source
from .emit import emit_strategy_metta
from .ir import Evidence, SourceSpan, Strategy, StrategyKind
from .recognition import (
    RecognitionResult,
    recognize_from_structural,
    evaluate_against_held_out,
)
from .structural import (
    StructuralEvidence,
    StructuralUnit,
    BlindStructuralEvidence,
    BlindStructuralUnit,
    extract_structural_evidence,
    blind_structural_view,
    PRIMARY_PROOF_LAYERS,
    EXTRACTOR_VERSION,
)

__all__ = [
    "Evidence",
    "SourceSpan",
    "Strategy",
    "StrategyKind",
    "analyze_source",
    "emit_strategy_metta",
    "StructuralEvidence",
    "StructuralUnit",
    "BlindStructuralEvidence",
    "BlindStructuralUnit",
    "extract_structural_evidence",
    "blind_structural_view",
    "PRIMARY_PROOF_LAYERS",
    "EXTRACTOR_VERSION",
    "RecognitionResult",
    "recognize_from_structural",
    "evaluate_against_held_out",
]

__version__ = "0.0.1"

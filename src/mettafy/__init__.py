"""MeTTafy: semantic decompilation into executable MeTTa."""

from .analysis import analyze_source
from .emit import emit_strategy_metta
from .ir import Evidence, SourceSpan, Strategy, StrategyKind
from .recognition import (
    RecognitionResult,
    evaluate_against_held_out,
    recognize_from_structural,
)
from .structural import (
    EXTRACTOR_VERSION,
    HIGH_LEVEL_PROOF_LAYERS,
    PRIMARY_PROOF_LAYERS,
    BlindProvenance,
    BlindStructuralEvidence,
    BlindStructuralUnit,
    StructuralEvidence,
    StructuralUnit,
    blind_audit_map,
    blind_structural_view,
    extract_structural_evidence,
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
    "BlindProvenance",
    "BlindStructuralEvidence",
    "BlindStructuralUnit",
    "extract_structural_evidence",
    "blind_structural_view",
    "blind_audit_map",
    "PRIMARY_PROOF_LAYERS",
    "HIGH_LEVEL_PROOF_LAYERS",
    "EXTRACTOR_VERSION",
    "RecognitionResult",
    "recognize_from_structural",
    "evaluate_against_held_out",
]

__version__ = "0.0.1"

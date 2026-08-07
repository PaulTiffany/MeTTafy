"""MeTTafy: semantic decompilation into executable MeTTa."""

from .analysis import analyze_source
from .emit import emit_strategy_metta
from .ir import Evidence, SourceSpan, Strategy, StrategyKind

__all__ = [
    "Evidence",
    "SourceSpan",
    "Strategy",
    "StrategyKind",
    "analyze_source",
    "emit_strategy_metta",
]

__version__ = "0.0.1"

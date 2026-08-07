from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class StrategyKind(str, Enum):
    BACKTRACKING_SEARCH = "BacktrackingSearch"
    CONSTRAINT_PROPAGATION = "ConstraintPropagation"
    BRANCH_AND_BOUND = "BranchAndBound"
    GRAPH_TRAVERSAL = "GraphTraversal"
    MEMOIZATION = "Memoization"
    DYNAMIC_PROGRAMMING = "DynamicProgramming"
    REWRITE = "Rewrite"
    REDUCTION = "Reduction"
    SYMMETRY_BREAKING = "SymmetryBreaking"
    HEURISTIC_SELECTION = "HeuristicSelection"
    FIXPOINT_ITERATION = "FixpointIteration"
    CERTIFICATE_CHECK = "CertificateCheck"
    EXTERNAL_SOLVER_CALL = "ExternalSolverCall"
    UNKNOWN = "UnknownStrategy"


@dataclass(frozen=True)
class SourceSpan:
    filename: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class Evidence:
    kind: str
    detail: str
    span: SourceSpan


@dataclass
class Strategy:
    id: str
    kind: StrategyKind
    confidence: float
    evidence: list[Evidence] = field(default_factory=list)
    children: list["Strategy"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "confidence": self.confidence,
            "evidence": [
                {
                    "kind": item.kind,
                    "detail": item.detail,
                    "span": {
                        "filename": item.span.filename,
                        "start_line": item.span.start_line,
                        "end_line": item.span.end_line,
                    },
                }
                for item in self.evidence
            ],
            "children": [child.to_dict() for child in self.children],
        }

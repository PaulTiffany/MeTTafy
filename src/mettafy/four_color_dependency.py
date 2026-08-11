from __future__ import annotations

from dataclasses import dataclass

FORBIDDEN_UPSTREAM = {
    "FourColorTheorem",
    "HeldOutRocqAuthority",
    "SRMFFourCharts",
    "NoStableFifthClass",
}


@dataclass(frozen=True)
class ProofEdge:
    premise: str
    conclusion: str


def ancestors(target: str, edges: tuple[ProofEdge, ...]) -> frozenset[str]:
    reverse: dict[str, set[str]] = {}
    for edge in edges:
        reverse.setdefault(edge.conclusion, set()).add(edge.premise)

    seen: set[str] = set()
    frontier = list(reverse.get(target, set()))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(reverse.get(node, set()))
    return frozenset(seen)


def closure_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """Contract Expansion Closure must not be proved by a downstream authority."""
    upstream = ancestors("ContractExpansionClosure", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def theorem_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """The final theorem must pass through the declared local closure interface."""
    upstream = ancestors("FourColorTheorem", edges)
    return "ContractExpansionClosure" in upstream

from __future__ import annotations

from dataclasses import dataclass

FORBIDDEN_UPSTREAM = {
    "FourColorTheorem",
    "HeldOutRocqAuthority",
    "SRMFFourCharts",
    "NoStableFifthClass",
    "ExhaustiveBoundaryEnumeration",
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
    """Contract Expansion Closure must not be proved by downstream authority."""
    upstream = ancestors("ContractExpansionClosure", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def nilpotent_desaturation_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """Legal desaturation cannot be inferred from forbidden theorem authority.

    The index-four nilpotent algebra and exact boundary kernel may be premises,
    but neither finite enumeration nor the Four Color conclusion may certify
    the graph-level desaturation step.
    """
    upstream = ancestors("NilpotentDesaturationClosure", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def theorem_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """The final theorem must pass through the explicit graph-level gate."""
    upstream = ancestors("FourColorTheorem", edges)
    return {
        "ContractExpansionClosure",
        "NilpotentDesaturationClosure",
    } <= upstream

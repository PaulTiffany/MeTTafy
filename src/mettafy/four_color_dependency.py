from __future__ import annotations

from dataclasses import dataclass

FORBIDDEN_UPSTREAM = {
    "FourColorTheorem",
    "HeldOutRocqAuthority",
    "SRMFFourCharts",
    "NoStableFifthClass",
    "ExhaustiveBoundaryEnumeration",
    "BrownObserverProjection",
    "TerminalCompletedMap",
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
    """Construction closure must not be proved by downstream authority."""
    upstream = ancestors("ContractExpansionClosure", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def traversal_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """Traversal law is upstream of both observer projection and final decode."""
    upstream = ancestors("TraversalConstructionLaw", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def nilpotent_desaturation_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """Legal desaturation cannot be inferred from observer or theorem authority.

    The index-four nilpotent algebra, exact admissible-color complement, and
    graph edge ledger may be premises. Brown observation, completed-map facts,
    exhaustive enumeration, and the Four Color conclusion may not certify the
    construction rewrite.
    """
    upstream = ancestors("NilpotentDesaturationClosure", edges)
    return not bool(upstream & FORBIDDEN_UPSTREAM)


def theorem_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """The final theorem must pass through construction and graph-level gates."""
    upstream = ancestors("FourColorTheorem", edges)
    return {
        "TraversalConstructionLaw",
        "ContractExpansionClosure",
        "NilpotentDesaturationClosure",
        "TerminalDecodeSoundness",
    } <= upstream

from __future__ import annotations

from dataclasses import dataclass

DOWNSTREAM_OR_EXTERNAL_AUTHORITY = {
    "FourColorTheorem",
    "HeldOutRocqAuthority",
    "SRMFFourCharts",
    "NoStableFifthClass",
    "ExhaustiveBoundaryEnumeration",
    "BrownObserverProjection",
    "TerminalCompletedMap",
}

INFERENCE_ONLY_NODES = {
    "ImaginedState",
    "CounterfactualTraversalLaw",
    "ContractExpansionInference",
    "NilpotentDesaturationInference",
    "FocusSlackPath",
    "PredictedResponse",
}


@dataclass(frozen=True)
class ProofEdge:
    premise: str
    conclusion: str


def direct_premises(target: str, edges: tuple[ProofEdge, ...]) -> frozenset[str]:
    return frozenset(edge.premise for edge in edges if edge.conclusion == target)


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


def inference_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """INFERENCE: blocked-focus resolution cannot be supplied by downstream authority."""

    upstream = ancestors("EveryBlockedFocusResolvable", edges)
    return not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def authority_bridge_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """BRIDGE: imagined data cannot directly become construction authority.

    A sound certified-instantiation theorem must have both the resolution and
    soundness obligations upstream. Counterfactual states, paths, and predicted
    responses may feed those inference theorems, but may not be direct premises
    of construction authority.
    """

    target = "CertifiedInstantiationSoundness"
    upstream = ancestors(target, edges)
    direct = direct_premises(target, edges)
    required = {"EveryBlockedFocusResolvable", "InferenceSoundness"}
    return (
        required <= upstream
        and not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)
        and not bool(direct & INFERENCE_ONLY_NODES)
    )


def construction_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """REALIZED: completion must pass through certification and the void clock."""

    upstream = ancestors("CompletedConstruction", edges)
    required = {
        "CertifiedInstantiationSoundness",
        "VoidCountMonotone",
        "InstantiationPreservesProperness",
        "FiniteRealizedMap",
    }
    return required <= upstream and not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def terminal_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """TERMINAL: final decode is downstream of a completed proper construction."""

    upstream = ancestors("TerminalDecodeSoundness", edges)
    return {"CompletedConstruction", "ExactEdgeLedger"} <= upstream


def theorem_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """The final theorem must cross inference, bridge, construction, then terminal gates."""

    upstream = ancestors("FourColorTheorem", edges)
    direct = direct_premises("FourColorTheorem", edges)
    required = {
        "FinitePlanarMap",
        "EveryBlockedFocusResolvable",
        "InferenceSoundness",
        "CertifiedInstantiationSoundness",
        "VoidCountMonotone",
        "InstantiationPreservesProperness",
        "CompletedConstruction",
        "TerminalDecodeSoundness",
    }
    return required <= upstream and not bool(direct & INFERENCE_ONLY_NODES)


# Compatibility guards for archived dependency witnesses. These lanes are now
# explicitly inference-only; passing them never authorizes realized construction.
def closure_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    upstream = ancestors("ContractExpansionInference", edges)
    return not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def traversal_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    upstream = ancestors("CounterfactualTraversalLaw", edges)
    return not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def nilpotent_desaturation_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    upstream = ancestors("NilpotentDesaturationInference", edges)
    return not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)

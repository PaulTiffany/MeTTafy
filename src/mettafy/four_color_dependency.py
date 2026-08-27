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
    "HypotheticalMap",
    "CounterfactualTraversalLaw",
    "ContractExpansionInference",
    "NilpotentDesaturationInference",
    "FocusSlackPath",
    "PredictedResponse",
    "RoleplayTranscript",
    "StrategySignature",
    "RawStrategyTrace",
    "StrategyTangle",
    "StrategyColorProjection",
    "ColorReidemeisterUncrossing",
    "StrategyColorSimulation",
    "ReidemeisterStaging",
    "StrategyNormalForm",
    "NormalFormCompleteness",
    "StagingMetrics",
    "AdversarialStrategyCorpus",
    "QuotientChallenge",
    "QuotientAudit",
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


def staging_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """INFERENCE: normal-form completeness must arise through the staging lane."""

    upstream = ancestors("NormalFormCompleteness", edges)
    required = {
        "RawStrategyTrace",
        "StrategyTangle",
        "ReidemeisterStaging",
        "StrategyNormalForm",
    }
    return required <= upstream and not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def quotient_audit_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """INFERENCE: empirical quotient pressure is evidence, never authority."""

    upstream = ancestors("QuotientAudit", edges)
    required = {"AdversarialStrategyCorpus", "StrategyNormalForm", "QuotientChallenge"}
    return required <= upstream and not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def inference_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """INFERENCE: strategy completeness cannot be supplied by downstream authority."""

    upstream = ancestors("StrategyIRCompleteness", edges)
    return not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)


def authority_bridge_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """BRIDGE: strategy data cannot directly become construction authority.

    A safe-continuation theorem must have both strategy completeness and
    inference soundness upstream. Counterfactual states, roleplay transcripts,
    staged tangles, color projections/simulations, normal forms, and adversarial
    audits may feed inference work, but may not be direct premises of construction
    authority.
    """

    target = "StrategySafeContinuation"
    upstream = ancestors(target, edges)
    direct = direct_premises(target, edges)
    required = {"StrategyIRCompleteness", "InferenceSoundness"}
    return (
        required <= upstream
        and not bool(upstream & DOWNSTREAM_OR_EXTERNAL_AUTHORITY)
        and not bool(direct & INFERENCE_ONLY_NODES)
    )


def construction_dependency_clean(edges: tuple[ProofEdge, ...]) -> bool:
    """REALIZED: completion must preserve strategy safety and consume voids."""

    upstream = ancestors("CompletedConstruction", edges)
    required = {
        "StrategySafeInitialState",
        "StrategySafeContinuation",
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
    """The final theorem must cross strategy, bridge, construction, then terminal gates."""

    upstream = ancestors("FourColorTheorem", edges)
    direct = direct_premises("FourColorTheorem", edges)
    required = {
        "FinitePlanarMap",
        "StrategyIRCompleteness",
        "InferenceSoundness",
        "StrategySafeInitialState",
        "StrategySafeContinuation",
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

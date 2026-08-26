from __future__ import annotations

from mettafy.four_color_dependency import (
    ProofEdge,
    authority_bridge_clean,
    construction_dependency_clean,
    inference_dependency_clean,
    theorem_dependency_clean,
    terminal_dependency_clean,
)


def clean_authority_graph() -> tuple[ProofEdge, ...]:
    return (
        # INFERENCE: counterfactual machinery may support the open resolution theorem.
        ProofEdge("CounterfactualTraversalLaw", "DerivedInferenceGeometry"),
        ProofEdge("ContractExpansionInference", "DerivedInferenceGeometry"),
        ProofEdge("NilpotentDesaturationInference", "DerivedInferenceGeometry"),
        ProofEdge("DerivedInferenceGeometry", "EveryBlockedFocusResolvable"),
        ProofEdge("RealizedMapInspection", "InferenceSoundness"),
        # BRIDGE: resolution and soundness are both required before authority exists.
        ProofEdge("EveryBlockedFocusResolvable", "CertifiedInstantiationSoundness"),
        ProofEdge("InferenceSoundness", "CertifiedInstantiationSoundness"),
        # REALIZED: only certified instantiation plus the construction monotones complete.
        ProofEdge("CertifiedInstantiationSoundness", "CompletedConstruction"),
        ProofEdge("VoidCountMonotone", "CompletedConstruction"),
        ProofEdge("InstantiationPreservesProperness", "CompletedConstruction"),
        ProofEdge("FiniteRealizedMap", "CompletedConstruction"),
        # TERMINAL: final decoding starts only after completion.
        ProofEdge("CompletedConstruction", "TerminalDecodeSoundness"),
        ProofEdge("ExactEdgeLedger", "TerminalDecodeSoundness"),
        ProofEdge("FinitePlanarMap", "FourColorTheorem"),
        ProofEdge("CompletedConstruction", "FourColorTheorem"),
        ProofEdge("TerminalDecodeSoundness", "FourColorTheorem"),
    )


def test_clean_world_model_dependency_graph() -> None:
    edges = clean_authority_graph()
    assert inference_dependency_clean(edges)
    assert authority_bridge_clean(edges)
    assert construction_dependency_clean(edges)
    assert terminal_dependency_clean(edges)
    assert theorem_dependency_clean(edges)


def test_imagined_state_cannot_directly_authorize_instantiation() -> None:
    """NEGATIVE: imagined data requires an explicit inference/soundness bridge."""

    edges = clean_authority_graph() + (
        ProofEdge("ImaginedState", "CertifiedInstantiationSoundness"),
    )
    assert not authority_bridge_clean(edges)


def test_counterfactual_data_may_feed_inference_before_the_bridge() -> None:
    """INFERENCE/BRIDGE: imagination is lawful upstream of an explicit theorem."""

    edges = (
        ProofEdge("ImaginedState", "EveryBlockedFocusResolvable"),
        ProofEdge("EveryBlockedFocusResolvable", "CertifiedInstantiationSoundness"),
        ProofEdge("InferenceSoundness", "CertifiedInstantiationSoundness"),
    )
    assert inference_dependency_clean(edges)
    assert authority_bridge_clean(edges)


def test_predicted_response_cannot_be_the_certificate_payload() -> None:
    edges = (
        ProofEdge("EveryBlockedFocusResolvable", "CertifiedInstantiationSoundness"),
        ProofEdge("InferenceSoundness", "CertifiedInstantiationSoundness"),
        ProofEdge("PredictedResponse", "CertifiedInstantiationSoundness"),
    )
    assert not authority_bridge_clean(edges)


def test_realized_completion_requires_void_monotone_and_properness() -> None:
    edges = (
        ProofEdge("CertifiedInstantiationSoundness", "CompletedConstruction"),
        ProofEdge("InstantiationPreservesProperness", "CompletedConstruction"),
        ProofEdge("FiniteRealizedMap", "CompletedConstruction"),
    )
    assert not construction_dependency_clean(edges)


def test_terminal_decode_cannot_start_from_partial_map() -> None:
    edges = (
        ProofEdge("RealizedPartialMap", "TerminalDecodeSoundness"),
        ProofEdge("ExactEdgeLedger", "TerminalDecodeSoundness"),
    )
    assert not terminal_dependency_clean(edges)


def test_counterfactual_traversal_cannot_jump_directly_to_four_color_theorem() -> None:
    edges = clean_authority_graph() + (
        ProofEdge("CounterfactualTraversalLaw", "FourColorTheorem"),
    )
    assert not theorem_dependency_clean(edges)


def test_held_out_authority_cannot_supply_blocked_focus_resolution() -> None:
    edges = (
        ProofEdge("HeldOutRocqAuthority", "EveryBlockedFocusResolvable"),
    )
    assert not inference_dependency_clean(edges)


def test_theorem_requires_the_open_inference_obligation() -> None:
    edges = tuple(
        edge
        for edge in clean_authority_graph()
        if edge.premise != "EveryBlockedFocusResolvable"
        and edge.conclusion != "EveryBlockedFocusResolvable"
    )
    assert not theorem_dependency_clean(edges)

from __future__ import annotations

from mettafy.four_color_dependency import (
    ProofEdge,
    authority_bridge_clean,
    construction_dependency_clean,
    inference_dependency_clean,
    staging_dependency_clean,
    terminal_dependency_clean,
    theorem_dependency_clean,
)


def clean_authority_graph() -> tuple[ProofEdge, ...]:
    return (
        # INFERENCE: roleplay is unweaved, staged, then quotiented before completeness.
        ProofEdge("RoleplayTranscript", "RawStrategyTrace"),
        ProofEdge("RawStrategyTrace", "StrategyTangle"),
        ProofEdge("StrategySignature", "StrategyTangle"),
        ProofEdge("StrategyTangle", "ReidemeisterStaging"),
        ProofEdge("ReidemeisterStaging", "StrategyNormalForm"),
        ProofEdge("StrategyNormalForm", "NormalFormCompleteness"),
        ProofEdge("CounterfactualTraversalLaw", "DerivedStrategyGeometry"),
        ProofEdge("ContractExpansionInference", "DerivedStrategyGeometry"),
        ProofEdge("NilpotentDesaturationInference", "DerivedStrategyGeometry"),
        ProofEdge("DerivedStrategyGeometry", "NormalFormCompleteness"),
        ProofEdge("NormalFormCompleteness", "StrategyIRCompleteness"),
        ProofEdge("RealizedMapInspection", "InferenceSoundness"),
        # BRIDGE: complete strategy + sound inference yields one safe realized turn.
        ProofEdge("StrategyIRCompleteness", "StrategySafeContinuation"),
        ProofEdge("InferenceSoundness", "StrategySafeContinuation"),
        # REALIZED: induction begins safe and consumes one void per safe continuation.
        ProofEdge("StrategySafeInitialState", "CompletedConstruction"),
        ProofEdge("StrategySafeContinuation", "CompletedConstruction"),
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
    assert staging_dependency_clean(edges)
    assert inference_dependency_clean(edges)
    assert authority_bridge_clean(edges)
    assert construction_dependency_clean(edges)
    assert terminal_dependency_clean(edges)
    assert theorem_dependency_clean(edges)


def test_staging_lane_requires_unweave_tangle_and_normal_form() -> None:
    edges = (
        ProofEdge("StrategyTangle", "ReidemeisterStaging"),
        ProofEdge("ReidemeisterStaging", "StrategyNormalForm"),
        ProofEdge("StrategyNormalForm", "NormalFormCompleteness"),
    )
    assert not staging_dependency_clean(edges)


def test_imagined_state_cannot_directly_authorize_safe_continuation() -> None:
    """NEGATIVE: imagined data requires an explicit inference/soundness bridge."""

    edges = clean_authority_graph() + (
        ProofEdge("ImaginedState", "StrategySafeContinuation"),
    )
    assert not authority_bridge_clean(edges)


def test_strategy_normal_form_cannot_directly_authorize_safe_continuation() -> None:
    """NEGATIVE: normalization is inference data, never construction authority."""

    edges = clean_authority_graph() + (
        ProofEdge("StrategyNormalForm", "StrategySafeContinuation"),
    )
    assert not authority_bridge_clean(edges)


def test_counterfactual_data_may_feed_strategy_completeness_before_bridge() -> None:
    """INFERENCE/BRIDGE: imagination is lawful upstream of an explicit theorem."""

    edges = (
        ProofEdge("HypotheticalMap", "StrategyIRCompleteness"),
        ProofEdge("StrategyIRCompleteness", "StrategySafeContinuation"),
        ProofEdge("InferenceSoundness", "StrategySafeContinuation"),
    )
    assert inference_dependency_clean(edges)
    assert authority_bridge_clean(edges)


def test_predicted_response_cannot_be_safe_continuation_payload() -> None:
    edges = (
        ProofEdge("StrategyIRCompleteness", "StrategySafeContinuation"),
        ProofEdge("InferenceSoundness", "StrategySafeContinuation"),
        ProofEdge("PredictedResponse", "StrategySafeContinuation"),
    )
    assert not authority_bridge_clean(edges)


def test_roleplay_transcript_cannot_directly_become_realized_authority() -> None:
    edges = (
        ProofEdge("StrategyIRCompleteness", "StrategySafeContinuation"),
        ProofEdge("InferenceSoundness", "StrategySafeContinuation"),
        ProofEdge("RoleplayTranscript", "StrategySafeContinuation"),
    )
    assert not authority_bridge_clean(edges)


def test_realized_completion_requires_initial_safety_void_monotone_and_properness() -> None:
    edges = (
        ProofEdge("StrategySafeContinuation", "CompletedConstruction"),
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


def test_held_out_authority_cannot_supply_strategy_completeness() -> None:
    edges = (
        ProofEdge("HeldOutRocqAuthority", "StrategyIRCompleteness"),
    )
    assert not inference_dependency_clean(edges)


def test_theorem_requires_strategy_completeness() -> None:
    edges = tuple(
        edge
        for edge in clean_authority_graph()
        if edge.premise != "StrategyIRCompleteness"
        and edge.conclusion != "StrategyIRCompleteness"
    )
    assert not theorem_dependency_clean(edges)

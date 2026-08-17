from __future__ import annotations

from mettafy.four_color_dependency import (
    ProofEdge,
    closure_dependency_clean,
    nilpotent_desaturation_dependency_clean,
    theorem_dependency_clean,
    traversal_dependency_clean,
)


def test_clean_contract_expansion_dependency_graph() -> None:
    edges = (
        ProofEdge("NilpotencyIndexFour", "TraversalConstructionLaw"),
        ProofEdge("AdmissibleColorComplement", "TraversalConstructionLaw"),
        ProofEdge("ExactEdgeLedger", "TraversalConstructionLaw"),
        ProofEdge("TraversalConstructionLaw", "ContractExpansionClosure"),
        ProofEdge("PlanarGeneratorCalculus", "ContractExpansionClosure"),
        ProofEdge("TraversalConstructionLaw", "NilpotentDesaturationClosure"),
        ProofEdge("SaturatedBoundaryKernel", "NilpotentDesaturationClosure"),
        ProofEdge("ExactEdgeLedger", "NilpotentDesaturationClosure"),
        ProofEdge("CompletedConstruction", "TerminalDecodeSoundness"),
        ProofEdge("ExactEdgeLedger", "TerminalDecodeSoundness"),
        ProofEdge("TraversalConstructionLaw", "FourColorTheorem"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
        ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
        ProofEdge("TerminalDecodeSoundness", "FourColorTheorem"),
    )
    assert traversal_dependency_clean(edges)
    assert closure_dependency_clean(edges)
    assert nilpotent_desaturation_dependency_clean(edges)
    assert theorem_dependency_clean(edges)


def test_observer_projection_cannot_authorize_traversal() -> None:
    edges = (
        ProofEdge("BrownObserverProjection", "TraversalConstructionLaw"),
        ProofEdge("TraversalConstructionLaw", "FourColorTheorem"),
    )
    assert not traversal_dependency_clean(edges)


def test_completed_map_cannot_define_traversal_upstream() -> None:
    edges = (
        ProofEdge("TerminalCompletedMap", "TraversalConstructionLaw"),
        ProofEdge("TraversalConstructionLaw", "FourColorTheorem"),
    )
    assert not traversal_dependency_clean(edges)


def test_held_out_authority_cannot_prove_local_closure() -> None:
    edges = (
        ProofEdge("HeldOutRocqAuthority", "ContractExpansionClosure"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
    )
    assert not closure_dependency_clean(edges)


def test_srmf_cardinality_cannot_be_source_of_fourness() -> None:
    edges = (
        ProofEdge("SRMFFourCharts", "ContractExpansionClosure"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
    )
    assert not closure_dependency_clean(edges)


def test_no_stable_fifth_class_cannot_be_used_circularly() -> None:
    edges = (
        ProofEdge("NoStableFifthClass", "ContractExpansionClosure"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
    )
    assert not closure_dependency_clean(edges)


def test_observer_and_terminal_views_cannot_prove_desaturation() -> None:
    for forbidden in (
        "HeldOutRocqAuthority",
        "FourColorTheorem",
        "ExhaustiveBoundaryEnumeration",
        "BrownObserverProjection",
        "TerminalCompletedMap",
    ):
        edges = (
            ProofEdge(forbidden, "NilpotentDesaturationClosure"),
            ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
        )
        assert not nilpotent_desaturation_dependency_clean(edges)


def test_theorem_requires_all_declared_species_gates() -> None:
    missing_decode = (
        ProofEdge("TraversalConstructionLaw", "FourColorTheorem"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
        ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
    )
    complete = missing_decode + (
        ProofEdge("TerminalDecodeSoundness", "FourColorTheorem"),
    )
    assert not theorem_dependency_clean(missing_decode)
    assert theorem_dependency_clean(complete)


def test_theorem_cannot_jump_directly_from_planarity() -> None:
    edges = (ProofEdge("Planarity", "FourColorTheorem"),)
    assert not theorem_dependency_clean(edges)

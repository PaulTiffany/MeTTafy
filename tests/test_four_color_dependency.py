from __future__ import annotations

from mettafy.four_color_dependency import (
    ProofEdge,
    closure_dependency_clean,
    theorem_dependency_clean,
)


def test_clean_contract_expansion_dependency_graph() -> None:
    edges = (
        ProofEdge("PrincipiaFokkerPlanck", "DifferentialRealization"),
        ProofEdge("PlanarGeneratorCalculus", "ContractExpansionClosure"),
        ProofEdge("LocalExpansionWitnesses", "ContractExpansionClosure"),
        ProofEdge("DifferentialRealization", "LocalExpansionWitnesses"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
    )
    assert closure_dependency_clean(edges)
    assert theorem_dependency_clean(edges)


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


def test_theorem_must_pass_through_local_contract_closure() -> None:
    edges = (ProofEdge("Planarity", "FourColorTheorem"),)
    assert not theorem_dependency_clean(edges)

from __future__ import annotations

from mettafy.four_color_dependency import (
    ProofEdge,
    closure_dependency_clean,
    nilpotent_desaturation_dependency_clean,
    theorem_dependency_clean,
)


def test_clean_contract_expansion_dependency_graph() -> None:
    edges = (
        ProofEdge("PrincipiaFokkerPlanck", "DifferentialRealization"),
        ProofEdge("PlanarGeneratorCalculus", "ContractExpansionClosure"),
        ProofEdge("LocalExpansionWitnesses", "ContractExpansionClosure"),
        ProofEdge("DifferentialRealization", "LocalExpansionWitnesses"),
        ProofEdge("NilpotencyIndexFour", "NilpotentDesaturationClosure"),
        ProofEdge("SaturatedBoundaryKernel", "NilpotentDesaturationClosure"),
        ProofEdge("ExactEdgeLedger", "NilpotentDesaturationClosure"),
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
        ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
    )
    assert closure_dependency_clean(edges)
    assert nilpotent_desaturation_dependency_clean(edges)
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


def test_forbidden_authority_cannot_prove_nilpotent_desaturation() -> None:
    for forbidden in (
        "HeldOutRocqAuthority",
        "FourColorTheorem",
        "ExhaustiveBoundaryEnumeration",
    ):
        edges = (
            ProofEdge(forbidden, "NilpotentDesaturationClosure"),
            ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
        )
        assert not nilpotent_desaturation_dependency_clean(edges)


def test_theorem_requires_both_global_gates() -> None:
    only_contract = (
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
    )
    only_desaturation = (
        ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
    )
    both = (
        ProofEdge("ContractExpansionClosure", "FourColorTheorem"),
        ProofEdge("NilpotentDesaturationClosure", "FourColorTheorem"),
    )
    assert not theorem_dependency_clean(only_contract)
    assert not theorem_dependency_clean(only_desaturation)
    assert theorem_dependency_clean(both)


def test_theorem_cannot_jump_directly_from_planarity() -> None:
    edges = (ProofEdge("Planarity", "FourColorTheorem"),)
    assert not theorem_dependency_clean(edges)

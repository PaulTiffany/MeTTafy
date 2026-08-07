from pathlib import Path

from mettafy import StrategyKind, analyze_source, emit_strategy_metta

EXAMPLE = Path("examples/four_color/solver.py")


def test_recovers_backtracking_and_constraint_strategy():
    source = EXAMPLE.read_text(encoding="utf-8")
    strategies = analyze_source(source, filename=str(EXAMPLE))
    kinds = {strategy.kind for strategy in strategies}

    assert StrategyKind.BACKTRACKING_SEARCH in kinds
    assert StrategyKind.CONSTRAINT_PROPAGATION in kinds


def test_all_classifications_have_source_evidence():
    source = EXAMPLE.read_text(encoding="utf-8")
    strategies = analyze_source(source, filename=str(EXAMPLE))

    assert strategies
    assert all(strategy.evidence for strategy in strategies)
    assert all(
        evidence.span.start_line >= 1
        for strategy in strategies
        for evidence in strategy.evidence
    )


def test_metta_output_contains_strategy_and_provenance_atoms():
    source = EXAMPLE.read_text(encoding="utf-8")
    strategies = analyze_source(source, filename=str(EXAMPLE))
    output = emit_strategy_metta(strategies)

    assert "BacktrackingSearch" in output
    assert "ConstraintPropagation" in output
    assert "SourceSpan" in output
    assert "Supports" in output

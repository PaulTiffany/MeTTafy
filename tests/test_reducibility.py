from __future__ import annotations

import hashlib

import pytest

from mettafy.ir import StrategyKind
from mettafy.reducibility import (
    ReductionState,
    evaluate_reducibility,
    strategy_from_certificate,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def state(state_id: str, boundary: str, obstruction: int) -> ReductionState:
    return ReductionState(
        state_id=state_id,
        boundary_sha256=digest(boundary),
        obstruction_measure=obstruction,
    )


def test_certifies_only_boundary_preserving_strict_descent() -> None:
    before = state("before", "same-boundary", 7)
    after = state("after", "same-boundary", 4)

    trace, certificate, provenance = evaluate_reducibility(before, after)

    assert trace.decision == "certify"
    assert trace.boundary_preserved is True
    assert trace.obstruction_decreased is True
    assert certificate is not None
    assert certificate.boundary_sha256 == before.boundary_sha256
    assert certificate.obstruction_before == 7
    assert certificate.obstruction_after == 4
    assert [edge.relation for edge in provenance] == ["reduced_to", "justified_by"]

    strategy, authorization = strategy_from_certificate(certificate)
    assert strategy.kind is StrategyKind.REDUCTION
    assert strategy.confidence == 1.0
    assert authorization.relation == "authorized_by"
    assert authorization.source_id == certificate.certificate_id
    assert authorization.target_id == strategy.id


def test_rejects_when_observable_boundary_changes() -> None:
    trace, certificate, provenance = evaluate_reducibility(
        state("before", "boundary-a", 7),
        state("after", "boundary-b", 4),
    )
    assert trace.decision == "reject"
    assert trace.reason == "observable boundary changed"
    assert certificate is None
    assert provenance == []


def test_rejects_when_obstruction_does_not_strictly_decrease() -> None:
    for after_measure in (7, 8):
        trace, certificate, provenance = evaluate_reducibility(
            state("before", "same-boundary", 7),
            state("after", "same-boundary", after_measure),
        )
        assert trace.decision == "reject"
        assert trace.reason == "obstruction measure did not strictly decrease"
        assert certificate is None
        assert provenance == []


def test_invalid_reduction_state_fails_closed() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        ReductionState("bad", digest("boundary"), -1)
    with pytest.raises(ValueError, match="SHA-256"):
        ReductionState("bad", "abcd", 1)
    with pytest.raises(ValueError, match="hexadecimal"):
        ReductionState("bad", "z" * 64, 1)

from __future__ import annotations

from mettafy.reducibility import ReducibilityCertificate, certify_reducibility


def cert(
    *,
    before_boundary: tuple[str, ...] = ("a", "b", "c"),
    after_boundary: tuple[str, ...] = ("a", "b", "c"),
    before: int = 9,
    after: int = 7,
) -> ReducibilityCertificate:
    return ReducibilityCertificate(
        certificate_id="certificate:unit:reducibility",
        local_id="unit:00001",
        boundary_before=before_boundary,
        boundary_after=after_boundary,
        obstruction_before=before,
        obstruction_after=after,
    )


def test_valid_certificate_requires_boundary_preservation_and_strict_descent() -> None:
    certificate = cert()
    assert certificate.boundary_preserved
    assert certificate.strict_descent
    assert certificate.valid

    strategy, provenance = certify_reducibility(certificate)
    assert strategy is not None
    assert strategy.confidence == 1.0
    assert [edge.relation for edge in provenance] == [
        "authorized_by",
        "preserves_boundary",
        "strictly_decreases",
    ]


def test_boundary_drift_fails_closed() -> None:
    strategy, provenance = certify_reducibility(
        cert(after_boundary=("a", "b", "d"))
    )
    assert strategy is None
    assert provenance == []


def test_non_descent_fails_closed() -> None:
    for after in (9, 10):
        strategy, provenance = certify_reducibility(cert(after=after))
        assert strategy is None
        assert provenance == []


def test_negative_obstruction_measure_rejected() -> None:
    certificate = cert(before=-1, after=0)
    try:
        certify_reducibility(certificate)
    except ValueError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("negative obstruction measure was accepted")

from __future__ import annotations

from fractions import Fraction

import pytest

from mettafy.observer_critical import (
    ImaginationDetectorState,
    SymmetricConstraintGeometry,
    route_reason,
    route_required,
)


def geometry(rho: Fraction, *, budget: int = 4) -> SymmetricConstraintGeometry:
    return SymmetricConstraintGeometry(
        k=4,
        rho=rho,
        tau=Fraction(1),
        m=Fraction(1),
        observer_budget=Fraction(budget),
    )


def detector(real: Fraction, imag: Fraction) -> ImaginationDetectorState:
    return ImaginationDetectorState(
        real_mismatch=real,
        imaginary_residue=imag,
        real_tolerance=Fraction(1),
        phase_tolerance=Fraction(1),
    )


def test_observer_threshold_occurs_before_mathematical_singularity() -> None:
    state = geometry(Fraction(1, 5))
    assert state.critical_rho == Fraction(1, 3)
    assert state.observer_soft_floor == Fraction(1, 4)
    assert state.observer_rho == Fraction(1, 4)
    assert state.observer_rho < state.critical_rho


def test_cost_and_soft_mode_collapse_conditions_are_exactly_equivalent() -> None:
    for k in range(2, 9):
        denominator = 12 * (k - 1)
        for step in range(12):
            rho = Fraction(step, denominator)
            for tau in (1, 2):
                for m in (1, 3):
                    for budget in (1, 2, 4, 8):
                        state = SymmetricConstraintGeometry(
                            k=k,
                            rho=rho,
                            tau=Fraction(tau),
                            m=Fraction(m),
                            observer_budget=Fraction(budget),
                        )
                        assert state.collapse_equivalence


def test_response_cost_softens_monotonically_toward_the_cliff() -> None:
    rhos = [Fraction(i, 30) for i in range(10)]  # all below rho_c = 1/3 for k=4
    costs = [geometry(rho).minimum_cost_squared for rho in rhos]
    assert all(left < right for left, right in zip(costs, costs[1:], strict=True))


def test_observer_routes_before_singularity_when_budget_is_exhausted() -> None:
    below = geometry(Fraction(1, 5))
    at = geometry(Fraction(1, 4))
    above = geometry(Fraction(3, 10))
    assert below.collapse_by_cost is False
    assert at.collapse_by_cost is True
    assert above.collapse_by_cost is True
    assert above.rho < above.critical_rho


def test_imagination_detector_requires_real_closeness_and_phase_crossing() -> None:
    assert detector(Fraction(1, 2), Fraction(1)).latent_phase_crossing is True
    assert detector(Fraction(1), Fraction(2)).latent_phase_crossing is False
    assert detector(Fraction(1, 2), Fraction(1, 2)).latent_phase_crossing is False


def test_route_composes_critical_geometry_and_latent_phase_without_conflating_them() -> None:
    subcritical = geometry(Fraction(1, 5))
    critical = geometry(Fraction(3, 10))
    ordinary = detector(Fraction(1, 2), Fraction(1, 2))
    imagined = detector(Fraction(1, 2), Fraction(2))

    assert route_required(subcritical, ordinary) is False
    assert route_reason(subcritical, ordinary) == "continue"
    assert route_reason(subcritical, imagined) == "latent_phase"
    assert route_reason(critical, ordinary) == "critical_geometry"
    assert route_reason(critical, imagined) == "critical_and_imaginary"


def test_invalid_parameter_domains_fail_closed() -> None:
    with pytest.raises(ValueError, match="critical point"):
        geometry(Fraction(1, 3))
    with pytest.raises(ValueError, match="real_tolerance"):
        ImaginationDetectorState(
            real_mismatch=Fraction(0),
            imaginary_residue=Fraction(0),
            real_tolerance=Fraction(0),
            phase_tolerance=Fraction(1),
        )

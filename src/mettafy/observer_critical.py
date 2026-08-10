"""Exact observer-critical collapse and imagination-detector primitives.

This module encodes a narrow, mechanically checkable fragment of the
Cost-of-Cacophony / Hypothesis-Surface / Principia-Symbolica correspondence.
It does not claim the Four Color Theorem or quantum measurement dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class SymmetricConstraintGeometry:
    """Symmetric k-constraint geometry with an observer resource budget.

    The smallest Gram eigenvalue is

        M = 1 - rho (k - 1)

    and the squared lower bound on diagonal response cost is

        delta_min^2 = k tau^2 / (m^2 M).

    The observer must route/change representation once this minimum required
    cost reaches or exceeds ``observer_budget``.
    """

    k: int
    rho: Fraction
    tau: Fraction
    m: Fraction
    observer_budget: Fraction

    def __post_init__(self) -> None:
        if self.k < 2:
            raise ValueError("k must be at least 2")
        if self.tau <= 0:
            raise ValueError("tau must be positive")
        if self.m <= 0:
            raise ValueError("m must be positive")
        if self.observer_budget <= 0:
            raise ValueError("observer_budget must be positive")
        if self.rho < 0:
            raise ValueError("rho must be non-negative in this symmetric witness")
        if self.rho >= self.critical_rho:
            raise ValueError("rho must remain below the positive-definite critical point")

    @property
    def critical_rho(self) -> Fraction:
        """Mathematical soft-mode singularity rho_c = 1/(k-1)."""
        return Fraction(1, self.k - 1)

    @property
    def soft_mode(self) -> Fraction:
        """Smallest symmetric Gram eigenvalue / phase order parameter."""
        return Fraction(1) - self.rho * (self.k - 1)

    @property
    def observer_soft_floor(self) -> Fraction:
        """Soft-mode value at which the minimum response exhausts the budget."""
        numerator = self.k * self.tau * self.tau
        denominator = self.m * self.m * self.observer_budget * self.observer_budget
        return numerator / denominator

    @property
    def observer_rho(self) -> Fraction:
        """Observer-specific precritical threshold rho_O.

        rho_O may be negative when the observer budget is already insufficient
        at rho = 0. In that case collapse/routing is required throughout the
        admissible non-negative rho domain.
        """
        return (Fraction(1) - self.observer_soft_floor) / (self.k - 1)

    @property
    def minimum_cost_squared(self) -> Fraction:
        """Exact squared lower bound, avoiding irrational square roots."""
        numerator = self.k * self.tau * self.tau
        denominator = self.m * self.m * self.soft_mode
        return numerator / denominator

    @property
    def collapse_by_cost(self) -> bool:
        """Whether the required response cost reaches/exceeds observer budget."""
        return self.minimum_cost_squared >= self.observer_budget * self.observer_budget

    @property
    def collapse_by_soft_mode(self) -> bool:
        """Equivalent observer-floor condition expressed only through M."""
        return self.soft_mode <= self.observer_soft_floor

    @property
    def collapse_equivalence(self) -> bool:
        """Exact algebraic equivalence of cost and soft-mode collapse tests."""
        return self.collapse_by_cost == self.collapse_by_soft_mode


@dataclass(frozen=True)
class ImaginationDetectorState:
    """Observer-relative real/imaginary displacement at one comparison point."""

    real_mismatch: Fraction
    imaginary_residue: Fraction
    real_tolerance: Fraction
    phase_tolerance: Fraction

    def __post_init__(self) -> None:
        for name, value in (
            ("real_mismatch", self.real_mismatch),
            ("imaginary_residue", self.imaginary_residue),
        ):
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.real_tolerance <= 0:
            raise ValueError("real_tolerance must be positive")
        if self.phase_tolerance <= 0:
            raise ValueError("phase_tolerance must be positive")

    @property
    def real_endpoint_is_close(self) -> bool:
        return self.real_mismatch < self.real_tolerance

    @property
    def latent_phase_crossing(self) -> bool:
        """Same-looking endpoint with phase/orientation beyond reintegration."""
        return self.real_endpoint_is_close and self.imaginary_residue >= self.phase_tolerance


def route_required(
    geometry: SymmetricConstraintGeometry,
    detector: ImaginationDetectorState,
) -> bool:
    """Route when real geometry is insolvent or latent phase crossed tolerance."""
    return geometry.collapse_by_soft_mode or detector.latent_phase_crossing


def route_reason(
    geometry: SymmetricConstraintGeometry,
    detector: ImaginationDetectorState,
) -> str:
    """Return a bounded diagnostic class, not a physical ontology claim."""
    critical = geometry.collapse_by_soft_mode
    imaginary = detector.latent_phase_crossing
    if critical and imaginary:
        return "critical_and_imaginary"
    if critical:
        return "critical_geometry"
    if imaginary:
        return "latent_phase"
    return "continue"

"""Exact conditional separation between four- and five-channel observer stability.

This module proves only a resource-geometric statement. It does not prove that
planarity induces the required conflict parameter, nor does it prove the Four
Color Theorem. Those remain independent bridge obligations.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ChannelStabilityWindow:
    """Symmetric soft-mode model shared across channel counts.

    For k simultaneous mutually conflicting channels,

        M_k = 1 - rho (k - 1).

    A channel count remains observer-stable exactly while M_k > M_O. Crossing
    M_k <= M_O means the finite observer budget forces a route/change of
    representation under the observer-critical witness convention.
    """

    rho: Fraction
    observer_soft_floor: Fraction

    def __post_init__(self) -> None:
        if self.rho < 0:
            raise ValueError("rho must be non-negative")
        if not Fraction(0) < self.observer_soft_floor < Fraction(1):
            raise ValueError("observer_soft_floor must lie strictly between 0 and 1")

    def soft_mode(self, channels: int) -> Fraction:
        if channels < 2:
            raise ValueError("channels must be at least 2")
        return Fraction(1) - self.rho * (channels - 1)

    def stable(self, channels: int) -> bool:
        return self.soft_mode(channels) > self.observer_soft_floor

    def routes(self, channels: int) -> bool:
        return not self.stable(channels)

    @property
    def four_five_window_lower(self) -> Fraction:
        """Inclusive lower rho bound where the fifth channel must route."""
        return (Fraction(1) - self.observer_soft_floor) / 4

    @property
    def four_five_window_upper(self) -> Fraction:
        """Exclusive upper rho bound where four channels still remain stable."""
        return (Fraction(1) - self.observer_soft_floor) / 3

    @property
    def in_four_stable_five_routes_window(self) -> bool:
        return self.four_five_window_lower <= self.rho < self.four_five_window_upper

    @property
    def four_stable_five_routes(self) -> bool:
        """Mechanical theorem predicate for the exact separation window."""
        return self.stable(4) and self.routes(5)

    @property
    def separation_equivalence(self) -> bool:
        """Exact equivalence between interval membership and stability behavior."""
        return self.in_four_stable_five_routes_window == self.four_stable_five_routes


def window_nonempty(observer_soft_floor: Fraction) -> bool:
    """For 0 < M_O < 1, [(1-M_O)/4, (1-M_O)/3) is nonempty."""
    if not Fraction(0) < observer_soft_floor < Fraction(1):
        raise ValueError("observer_soft_floor must lie strictly between 0 and 1")
    lower = (Fraction(1) - observer_soft_floor) / 4
    upper = (Fraction(1) - observer_soft_floor) / 3
    return lower < upper

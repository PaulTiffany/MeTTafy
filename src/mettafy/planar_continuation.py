from __future__ import annotations

from dataclasses import dataclass

Endpoint = int
Pair = tuple[Endpoint, Endpoint]


def _normalize_pair(pair: Pair, boundary_size: int) -> Pair:
    left, right = pair
    if boundary_size < 4:
        raise ValueError("boundary must have at least four marked positions")
    if left == right:
        raise ValueError("continuation endpoints must be distinct")
    if left not in range(boundary_size) or right not in range(boundary_size):
        raise ValueError("endpoint lies outside cyclic boundary")
    return (left, right)


def _strictly_between(start: int, end: int, point: int, modulus: int) -> bool:
    distance_to_end = (end - start) % modulus
    distance_to_point = (point - start) % modulus
    return 0 < distance_to_point < distance_to_end


def endpoints_alternate(
    first: Pair,
    second: Pair,
    boundary_size: int,
) -> bool:
    """Whether two endpoint pairs alternate in cyclic order.

    For simple arcs inside a disk with disjoint endpoints, alternation is the
    exact topological obstruction: alternating endpoints force an intersection.
    Non-alternation does not assert that a particular embedding exists; it only
    says cyclic order alone does not force the two continuations to cross.
    """

    a, b = _normalize_pair(first, boundary_size)
    c, d = _normalize_pair(second, boundary_size)
    if len({a, b, c, d}) != 4:
        raise ValueError("continuation pairs must have disjoint endpoints")
    c_inside = _strictly_between(a, b, c, boundary_size)
    d_inside = _strictly_between(a, b, d, boundary_size)
    return c_inside != d_inside


@dataclass(frozen=True)
class ContinuationPair:
    """Two proposed state continuations relative to one cyclic frontier."""

    boundary_size: int
    first: Pair
    second: Pair

    @property
    def forced_intersection(self) -> bool:
        return endpoints_alternate(self.first, self.second, self.boundary_size)

    @property
    def bounded_planar_coexistence_not_refuted(self) -> bool:
        """True when cyclic order does not itself force a crossing."""

        return not self.forced_intersection

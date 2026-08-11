from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

Color = int
V4 = tuple[int, int]
BoundaryWord = tuple[Color, ...]

COLOR_TO_V4: dict[Color, V4] = {
    0: (0, 0),
    1: (1, 0),
    2: (0, 1),
    3: (1, 1),
}
ZERO: V4 = (0, 0)
NONZERO_MODES: tuple[V4, V4, V4] = ((1, 0), (0, 1), (1, 1))


def v4_add(left: V4, right: V4) -> V4:
    return (left[0] ^ right[0], left[1] ^ right[1])


def color_difference(left: Color, right: Color) -> V4:
    try:
        return v4_add(COLOR_TO_V4[left], COLOR_TO_V4[right])
    except KeyError as exc:
        raise ValueError("color lies outside Q4") from exc


def proper_cycle(boundary: BoundaryWord) -> bool:
    if len(boundary) < 3:
        return False
    return all(
        boundary[index] in COLOR_TO_V4
        and boundary[index] != boundary[(index + 1) % len(boundary)]
        for index in range(len(boundary))
    )


def frontier_modes(boundary: BoundaryWord) -> tuple[V4, ...]:
    """Differences along the cyclic frontier between successive neighbors."""

    if not proper_cycle(boundary):
        raise ValueError("boundary must be a proper color cycle")
    return tuple(
        color_difference(boundary[index], boundary[(index + 1) % len(boundary)])
        for index in range(len(boundary))
    )


def frontier_closure(boundary: BoundaryWord) -> V4:
    """Telescoping V4 sum of the cyclic frontier differences."""

    total = ZERO
    for mode in frontier_modes(boundary):
        total = v4_add(total, mode)
    return total


def frontier_mode_counts(boundary: BoundaryWord) -> dict[V4, int]:
    counts = Counter(frontier_modes(boundary))
    return {mode: counts[mode] for mode in NONZERO_MODES}


def same_parity_mode_counts(boundary: BoundaryWord) -> bool:
    """Closed-frontier parity law for the three nonzero V4 modes.

    If n10, n01 and n11 count the three nonzero frontier modes, V4 closure
    yields n10+n11 = 0 mod 2 and n01+n11 = 0 mod 2.  Hence all three counts
    have the same parity.
    """

    counts = frontier_mode_counts(boundary)
    parities = {counts[mode] % 2 for mode in NONZERO_MODES}
    return len(parities) == 1 and frontier_closure(boundary) == ZERO


@dataclass(frozen=True)
class FixedRegionFrontier:
    """A region-relative parameterization of a triangulated local frontier.

    ``center_color`` is a gauge/reference choice for one already colored
    region.  Every boundary color must differ from it.  Consecutive boundary
    regions are assumed adjacent, so the boundary itself is a proper cycle.
    Relative to the fixed region, the four absolute colors reduce to the three
    nonzero V4 radial states; along the frontier, operational differences are
    again the three nonzero V4 modes.
    """

    center_color: Color
    boundary: BoundaryWord

    def __post_init__(self) -> None:
        if self.center_color not in COLOR_TO_V4:
            raise ValueError("center color lies outside Q4")
        if not proper_cycle(self.boundary):
            raise ValueError("boundary must be a proper cycle")
        if any(color == self.center_color for color in self.boundary):
            raise ValueError("boundary color collides with fixed region")

    @property
    def radial_modes(self) -> tuple[V4, ...]:
        return tuple(
            color_difference(self.center_color, color) for color in self.boundary
        )

    @property
    def tangential_modes(self) -> tuple[V4, ...]:
        return frontier_modes(self.boundary)

    @property
    def mode_counts(self) -> dict[V4, int]:
        return frontier_mode_counts(self.boundary)

    @property
    def parity_closed(self) -> bool:
        return same_parity_mode_counts(self.boundary)

    @property
    def degree_five_signature(self) -> tuple[int, int, int]:
        if len(self.boundary) != 5:
            raise ValueError("signature is specific to a degree-five frontier")
        counts = sorted(self.mode_counts.values(), reverse=True)
        return (counts[0], counts[1], counts[2])

    @property
    def degree_five_singleton_edges(self) -> tuple[int, int]:
        """The two exceptional frontier edges in the degree-five 3-1-1 law."""

        if self.degree_five_signature != (3, 1, 1):
            raise ValueError("degree-five frontier does not have the 3-1-1 signature")
        counts = self.mode_counts
        singletons = tuple(
            index
            for index, mode in enumerate(self.tangential_modes)
            if counts[mode] == 1
        )
        if len(singletons) != 2:
            raise AssertionError("3-1-1 frontier must have exactly two singleton edges")
        return (singletons[0], singletons[1])

    @property
    def degree_five_singletons_are_adjacent(self) -> bool:
        left, right = self.degree_five_singleton_edges
        return (left - right) % 5 in (1, 4)

    @property
    def degree_five_exceptional_vertex(self) -> int:
        """Unique boundary vertex where the two singleton edges meet."""

        left, right = self.degree_five_singleton_edges
        if (left + 1) % 5 == right:
            return right
        if (right + 1) % 5 == left:
            return left
        raise ValueError("singleton edges are not adjacent")

    @property
    def degree_five_dominant_run_edges(self) -> tuple[int, int, int]:
        """The complementary three-edge run carrying one repeated frontier mode."""

        singleton_set = set(self.degree_five_singleton_edges)
        dominant = tuple(index for index in range(5) if index not in singleton_set)
        if len(dominant) != 3:
            raise AssertionError("degree-five frontier must have three dominant edges")
        return (dominant[0], dominant[1], dominant[2])

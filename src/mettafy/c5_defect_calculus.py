from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import mettafy.plane_parameterization as plane

Boundary5 = tuple[int, int, int, int, int]
V4 = plane.V4


@dataclass(frozen=True)
class SaturatedC5Roles:
    """Canonical roles in a proper four-color C5 word A-B-A-C-D.

    The repeated color A occurs at two nonadjacent positions.  We orient the
    cycle so that the repeated positions are two edges apart; B is the unique
    boundary vertex on that short arc, and C,D are the remaining singleton
    colors on the complementary arc.
    """

    repeated_color: int
    repeated_indices: tuple[int, int]
    pivot_index: int
    flank_indices: tuple[int, int]
    pivot_color: int
    flank_colors: tuple[int, int]


@dataclass(frozen=True)
class C5DefectState:
    """The V4 discrete derivative of the actual five-neighbor boundary.

    This object does not introduce a colored center.  It acts directly on the
    proper C5 boundary that remains after deleting a degree-five focus vertex.
    """

    boundary: Boundary5

    def __post_init__(self) -> None:
        if not plane.proper_cycle(self.boundary):
            raise ValueError("boundary must be a proper C5 coloring")

    @property
    def modes(self) -> tuple[V4, V4, V4, V4, V4]:
        modes = plane.frontier_modes(self.boundary)
        return (modes[0], modes[1], modes[2], modes[3], modes[4])

    @property
    def mode_counts(self) -> dict[V4, int]:
        counts = Counter(self.modes)
        return {mode: counts[mode] for mode in plane.NONZERO_MODES}

    @property
    def signature(self) -> tuple[int, int, int]:
        counts = sorted(self.mode_counts.values(), reverse=True)
        return (counts[0], counts[1], counts[2])

    @property
    def singleton_edges(self) -> tuple[int, int]:
        counts = self.mode_counts
        singleton = tuple(
            index for index, mode in enumerate(self.modes) if counts[mode] == 1
        )
        if len(singleton) != 2:
            raise AssertionError("proper C5 closure must have exactly two singleton modes")
        return (singleton[0], singleton[1])

    @property
    def singleton_edges_adjacent(self) -> bool:
        left, right = self.singleton_edges
        return (left - right) % 5 in (1, 4)

    @property
    def color_count(self) -> int:
        return len(set(self.boundary))

    @property
    def is_open_three_color_boundary(self) -> bool:
        return self.color_count == 3

    @property
    def is_saturated_four_color_boundary(self) -> bool:
        return self.color_count == 4

    @property
    def adjacency_class_matches_color_count(self) -> bool:
        """Exact C5 classification: adjacent defects iff three colors are used."""

        return self.singleton_edges_adjacent == self.is_open_three_color_boundary

    @property
    def saturated_roles(self) -> SaturatedC5Roles:
        if not self.is_saturated_four_color_boundary:
            raise ValueError("roles require a saturated four-color C5 boundary")

        positions: dict[int, list[int]] = {}
        for index, color in enumerate(self.boundary):
            positions.setdefault(color, []).append(index)
        repeated = [
            (color, indexes) for color, indexes in positions.items() if len(indexes) == 2
        ]
        if len(repeated) != 1:
            raise AssertionError("saturated proper C5 must have one repeated color")

        repeated_color, indexes = repeated[0]
        first, second = indexes
        if (second - first) % 5 == 2:
            left, right = first, second
        elif (first - second) % 5 == 2:
            left, right = second, first
        else:
            raise AssertionError("repeated C5 color must be separated by one vertex")

        pivot = (left + 1) % 5
        flank_a = (right + 1) % 5
        flank_b = (right + 2) % 5
        return SaturatedC5Roles(
            repeated_color=repeated_color,
            repeated_indices=(left, right),
            pivot_index=pivot,
            flank_indices=(flank_a, flank_b),
            pivot_color=self.boundary[pivot],
            flank_colors=(self.boundary[flank_a], self.boundary[flank_b]),
        )

    @property
    def candidate_opening_color_pairs(self) -> tuple[frozenset[int], frozenset[int]]:
        """The two color-pair separations that can open a saturated C5 in one swap.

        This is boundary algebra only.  Whether either separation is available
        depends on the retained exterior connectivity witness.
        """

        roles = self.saturated_roles
        first, second = roles.flank_colors
        return (
            frozenset({roles.pivot_color, first}),
            frozenset({roles.pivot_color, second}),
        )

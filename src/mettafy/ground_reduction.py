from __future__ import annotations

from collections.abc import Sequence
from typing import cast

from mettafy.color_construction import PALETTE4

BoundaryPattern = tuple[int, int, int, int, int]
SATURATED_BOUNDARY_NORMAL_FORM: BoundaryPattern = (0, 1, 0, 2, 3)


def immediate_restoration_color(neighbor_colors: Sequence[int]) -> int:
    """Return a missing Q4 color for the genuinely immediate low-degree case.

    With at most three neighbors, four colors guarantee a missing color.
    Degree four is deliberately excluded: four differently colored neighbors
    are a counterexample to the stronger "missing color" shortcut.
    """

    colors = tuple(neighbor_colors)
    if any(color not in PALETTE4 for color in colors):
        raise ValueError("neighbor color lies outside Q4")
    if len(colors) > 3:
        raise ValueError(
            "immediate missing-color restoration is certified only for degree <= 3"
        )

    available = PALETTE4 - frozenset(colors)
    if not available:
        raise AssertionError("degree <= 3 unexpectedly exhausted Q4")
    return min(available)


def proper_five_cycle(colors: Sequence[int]) -> bool:
    """Whether five Q4 colors form a proper cyclic boundary."""

    values = tuple(colors)
    if len(values) != 5 or any(color not in PALETTE4 for color in values):
        return False
    return all(values[index] != values[(index + 1) % 5] for index in range(5))


def saturated_five_cycle(colors: Sequence[int]) -> bool:
    """Whether a proper five-cycle uses all four terminal colors."""

    values = tuple(colors)
    return proper_five_cycle(values) and frozenset(values) == PALETTE4


def _normalize_labels(colors: Sequence[int]) -> BoundaryPattern:
    labels: dict[int, int] = {}
    normalized: list[int] = []
    for color in colors:
        if color not in labels:
            labels[color] = len(labels)
        normalized.append(labels[color])
    if len(normalized) != 5:
        raise ValueError("boundary normalization requires five positions")
    return cast(BoundaryPattern, tuple(normalized))


def _dihedral_images(colors: BoundaryPattern) -> tuple[BoundaryPattern, ...]:
    images: list[BoundaryPattern] = []
    for orientation in (colors, tuple(reversed(colors))):
        for offset in range(5):
            rotated = orientation[offset:] + orientation[:offset]
            images.append(cast(BoundaryPattern, rotated))
    return tuple(images)


def saturated_boundary_normal_form(colors: Sequence[int]) -> BoundaryPattern:
    """Canonicalize the unique proper saturated Q4 coloring species of C5.

    Quotient by dihedral symmetry of the five-cycle and by color-name
    permutation. The sole orbit is represented by 0,1,0,2,3.
    """

    values = tuple(colors)
    if not saturated_five_cycle(values):
        raise ValueError("boundary must be a proper saturated Q4 five-cycle")

    typed = cast(BoundaryPattern, values)
    canonical = min(_normalize_labels(image) for image in _dihedral_images(typed))
    if canonical != SATURATED_BOUNDARY_NORMAL_FORM:
        raise AssertionError(f"unexpected saturated boundary species: {canonical}")
    return canonical

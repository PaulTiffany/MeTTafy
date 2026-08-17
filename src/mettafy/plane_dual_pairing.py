from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from mettafy.c5_defect_calculus import C5DefectState
from mettafy.plane_parameterization import (
    NONZERO_MODES,
    V4,
    color_difference,
    v4_add,
)

Boundary5 = tuple[int, int, int, int, int]
ModeWord5 = tuple[V4, V4, V4, V4, V4]
Pair = tuple[int, int]
Pairing = tuple[Pair, Pair]


def triangle_modes(colors: tuple[int, int, int]) -> tuple[V4, V4, V4]:
    """Edge-difference modes of one properly colored triangular face."""

    if len(set(colors)) != 3:
        raise ValueError("triangle vertices must carry three distinct colors")
    first = color_difference(colors[0], colors[1])
    second = color_difference(colors[1], colors[2])
    third = color_difference(colors[2], colors[0])
    modes = (first, second, third)
    if set(modes) != set(NONZERO_MODES):
        raise AssertionError("proper V4 triangle must realize all three nonzero modes")
    return modes


def selected_two_mode_degree(
    colors: tuple[int, int, int],
    excluded_mode: V4,
) -> int:
    """Dual degree contributed by the two modes other than ``excluded_mode``."""

    if excluded_mode not in NONZERO_MODES:
        raise ValueError("excluded mode must be nonzero in V4")
    return sum(mode != excluded_mode for mode in triangle_modes(colors))


def noncrossing_pairings_four(
    terminals: tuple[int, int, int, int],
) -> tuple[Pairing, Pairing]:
    """The two noncrossing perfect matchings of four cyclic C5 terminals."""

    if len(set(terminals)) != 4:
        raise ValueError("four distinct boundary terminals are required")
    if any(index not in range(5) for index in terminals):
        raise ValueError("terminal edge lies outside the degree-five boundary")
    first, second, third, fourth = sorted(terminals)
    return (
        ((first, second), (third, fourth)),
        ((first, fourth), (second, third)),
    )


def toggle_cut_endpoints(
    modes: ModeWord5,
    translation_mode: V4,
    pair: Pair,
) -> ModeWord5:
    """Boundary effect of translating one side of an admissible planar cut.

    A V4 translation by ``translation_mode`` leaves internal edge differences
    unchanged. At a cut edge it adds the translation mode to the old edge
    mode. Properness therefore requires every crossed edge mode to differ from
    the translation mode.
    """

    if translation_mode not in NONZERO_MODES:
        raise ValueError("translation mode must be nonzero in V4")
    left, right = pair
    if left == right or left not in range(5) or right not in range(5):
        raise ValueError("cut endpoints must be two distinct C5 edges")

    updated = list(modes)
    for index in pair:
        if updated[index] == translation_mode:
            raise ValueError("cut crosses the forbidden translation mode")
        updated[index] = v4_add(updated[index], translation_mode)
        if updated[index] == (0, 0):
            raise AssertionError("admissible cut translation cannot create zero mode")

    result = tuple(updated)
    return (result[0], result[1], result[2], result[3], result[4])


def singleton_edges_adjacent(modes: ModeWord5) -> bool:
    counts = Counter(modes)
    if sorted(counts.values(), reverse=True) != [3, 1, 1]:
        raise ValueError("mode word must have the degree-five 3-1-1 signature")
    singleton = tuple(index for index, mode in enumerate(modes) if counts[mode] == 1)
    if len(singleton) != 2:
        raise AssertionError("3-1-1 mode word must have two singleton edges")
    return (singleton[0] - singleton[1]) % 5 in (1, 4)


@dataclass(frozen=True)
class DegreeFiveDualPairing:
    """Boundary calculus forced by two-mode continuation in a triangulated disk.

    In a proper colored triangle the three edge differences are exactly the
    three nonzero V4 modes. Selecting two modes therefore gives degree two at
    every interior dual triangle. Boundary occurrences of those modes are
    terminals of disjoint dual paths, and planarity restricts four terminals
    to the two noncrossing pairings returned here.

    This object certifies only the boundary consequences. It does not invent
    or assert an interior dual path without an embedding witness.
    """

    boundary: Boundary5
    translation_mode: V4

    def __post_init__(self) -> None:
        defects = C5DefectState(self.boundary)
        if not defects.is_saturated_four_color_boundary:
            raise ValueError("dual pairing calculus requires a saturated C5")
        counts = Counter(defects.modes)
        if self.translation_mode not in NONZERO_MODES:
            raise ValueError("translation mode must be nonzero in V4")
        if counts[self.translation_mode] != 1:
            raise ValueError("translation mode must be one of the singleton modes")

    @property
    def modes(self) -> ModeWord5:
        modes = C5DefectState(self.boundary).modes
        return (modes[0], modes[1], modes[2], modes[3], modes[4])

    @property
    def terminal_edges(self) -> tuple[int, int, int, int]:
        terminals = tuple(
            index
            for index, mode in enumerate(self.modes)
            if mode != self.translation_mode
        )
        if len(terminals) != 4:
            raise AssertionError("singleton translation must leave exactly four terminals")
        return (terminals[0], terminals[1], terminals[2], terminals[3])

    @property
    def pairing_options(self) -> tuple[Pairing, Pairing]:
        return noncrossing_pairings_four(self.terminal_edges)

    def pair_opens(self, pair: Pair) -> bool:
        if pair not in self.pairing_options[0] + self.pairing_options[1]:
            raise ValueError("pair is not a planar pairing option for this boundary")
        return singleton_edges_adjacent(
            toggle_cut_endpoints(self.modes, self.translation_mode, pair)
        )

    @property
    def opening_pairing(self) -> Pairing:
        opening = tuple(
            pairing
            for pairing in self.pairing_options
            if all(self.pair_opens(pair) for pair in pairing)
        )
        if len(opening) != 1:
            raise AssertionError("saturated C5 must have one opening pairing type")
        return opening[0]

    @property
    def locked_pairing(self) -> Pairing:
        locked = tuple(
            pairing
            for pairing in self.pairing_options
            if not any(self.pair_opens(pair) for pair in pairing)
        )
        if len(locked) != 1:
            raise AssertionError("saturated C5 must have one locked pairing type")
        return locked[0]

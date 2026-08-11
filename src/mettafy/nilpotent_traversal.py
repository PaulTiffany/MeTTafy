from __future__ import annotations

from dataclasses import dataclass

Vector4 = tuple[int, int, int, int]
ColorWord = tuple[int, int, int, int, int]
TerminalColor = int

PALETTE4: tuple[TerminalColor, ...] = (0, 1, 2, 3)
ZERO4: Vector4 = (0, 0, 0, 0)
BASIS4: tuple[Vector4, ...] = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)


def nilpotent_step(vector: Vector4) -> Vector4:
    """The cyclic shift N with nilpotency index exactly four.

    N e0 = e1, N e1 = e2, N e2 = e3, N e3 = 0.
    Thus N^3 e0 != 0 while N^4 e0 = 0.  Once N^4 is zero, every
    higher power is zero as well; 'index four' means four is the first
    vanishing power, not that N^5 somehow becomes nonzero again.
    """

    a, b, c, _d = vector
    return (0, a, b, c)


def nilpotent_power(vector: Vector4, exponent: int) -> Vector4:
    if exponent < 0:
        raise ValueError("nilpotent traversal has no negative powers")
    result = vector
    for _ in range(exponent):
        result = nilpotent_step(result)
    return result


def cyclic_terminal_states() -> tuple[Vector4, ...]:
    """The four nonzero states generated from e0 before annihilation."""

    seed = BASIS4[0]
    return tuple(nilpotent_power(seed, exponent) for exponent in range(4))


def admissible_colors(used_neighbor_colors: frozenset[int]) -> frozenset[int]:
    """Exact Four-Color complement Q4 minus S."""

    if not used_neighbor_colors <= frozenset(PALETTE4):
        raise ValueError("neighbor color lies outside Q4")
    return frozenset(PALETTE4) - used_neighbor_colors


def proper_c5(word: ColorWord) -> bool:
    return all(
        word[index] in PALETTE4
        and word[index] != word[(index + 1) % 5]
        for index in range(5)
    )


@dataclass(frozen=True)
class SaturatedBoundaryDependency:
    """The exact one-dimensional dependency in a saturated C5 boundary.

    A proper C5 word using all four terminal colors has multiplicity pattern
    2+1+1+1.  The repeated color occurs at two nonadjacent boundary positions.
    The free module on the five indexed edge obligations therefore has a
    kernel relation e_left - e_right under the map sending each position to
    its terminal color basis state.
    """

    word: ColorWord
    repeated_color: int
    left_index: int
    right_index: int

    @property
    def kernel_vector(self) -> tuple[int, int, int, int, int]:
        out = [0, 0, 0, 0, 0]
        out[self.left_index] = 1
        out[self.right_index] = -1
        return tuple(out)  # type: ignore[return-value]

    @property
    def repeated_positions_are_nonadjacent(self) -> bool:
        delta = (self.left_index - self.right_index) % 5
        return delta not in (1, 4)


def saturated_boundary_dependency(word: ColorWord) -> SaturatedBoundaryDependency:
    if not proper_c5(word):
        raise ValueError("boundary is not a proper C5 coloring")
    if len(set(word)) != 4:
        raise ValueError("boundary is not saturated")

    positions_by_color: dict[int, list[int]] = {}
    for index, color in enumerate(word):
        positions_by_color.setdefault(color, []).append(index)
    repeated = [
        (color, positions)
        for color, positions in positions_by_color.items()
        if len(positions) == 2
    ]
    if len(repeated) != 1:
        raise AssertionError("saturated proper C5 must have one repeated color")
    color, positions = repeated[0]
    dependency = SaturatedBoundaryDependency(
        word=word,
        repeated_color=color,
        left_index=positions[0],
        right_index=positions[1],
    )
    if not dependency.repeated_positions_are_nonadjacent:
        raise AssertionError("proper C5 cannot repeat a color on adjacent vertices")
    return dependency


@dataclass(frozen=True)
class ExternalEdgeConstraint:
    boundary_index: int
    exterior_color: int

    def __post_init__(self) -> None:
        if self.boundary_index not in range(5):
            raise ValueError("boundary index must lie in 0..4")
        if self.exterior_color not in PALETTE4:
            raise ValueError("exterior color lies outside Q4")


@dataclass(frozen=True)
class DesaturationCertificate:
    """Exact witness required to turn nilpotent dependency into graph progress.

    Nilpotency and the boundary kernel do *not* establish this certificate.
    A successful proof must construct an ``after`` boundary with at most three
    distinct terminal colors while preserving the C5 edges and every declared
    external edge constraint.
    """

    before: ColorWord
    after: ColorWord
    external_edges: tuple[ExternalEdgeConstraint, ...] = ()

    @property
    def source_is_saturated(self) -> bool:
        return proper_c5(self.before) and len(set(self.before)) == 4

    @property
    def target_is_desaturated(self) -> bool:
        return proper_c5(self.after) and len(set(self.after)) <= 3

    @property
    def source_external_edges_valid(self) -> bool:
        return all(
            self.before[edge.boundary_index] != edge.exterior_color
            for edge in self.external_edges
        )

    @property
    def target_external_edges_valid(self) -> bool:
        return all(
            self.after[edge.boundary_index] != edge.exterior_color
            for edge in self.external_edges
        )

    @property
    def valid(self) -> bool:
        return (
            self.source_is_saturated
            and self.target_is_desaturated
            and self.source_external_edges_valid
            and self.target_external_edges_valid
        )


def direct_extension_count(boundary: ColorWord) -> int:
    """Number of terminal colors immediately available to the center."""

    if not proper_c5(boundary):
        raise ValueError("boundary is not a proper C5 coloring")
    return len(admissible_colors(frozenset(boundary)))

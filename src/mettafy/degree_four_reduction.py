from __future__ import annotations

from dataclasses import dataclass

from mettafy.color_construction import PALETTE4, ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    apply_kempe_move,
    two_color_component,
)


def _validate_degree_four_frontier(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, str, str, str],
) -> None:
    if focus in state.coloring:
        raise ValueError("degree-four reduction requires an uncommitted focus")
    if tuple(state.graph[focus]) != boundary:
        raise ValueError("boundary must be the ordered degree-four focus neighborhood")
    if any(vertex not in state.coloring for vertex in boundary):
        raise ValueError("degree-four boundary must already be colored")
    for index, vertex in enumerate(boundary):
        neighbor = boundary[(index + 1) % 4]
        if neighbor not in state.graph[vertex]:
            raise ValueError("degree-four triangulated frontier must be a four-cycle")


def degree_four_opening_move(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, str, str, str],
) -> KempeMove | None:
    """Derive the standard degree-four Kempe opening from the current coloring.

    A nonempty admissible color means no Kempe change is needed. In the
    saturated four-color case, try one pair of opposite boundary colors. If
    those terminals are connected, planarity of the triangulated frontier
    requires the complementary opposite pair to be disconnected; the second
    branch verifies that exact component fact rather than assuming it.
    """

    _validate_degree_four_frontier(state, focus, boundary)

    if state.admissible_colors(focus):
        return None

    colors = tuple(state.coloring[vertex] for vertex in boundary)
    if frozenset(colors) != PALETTE4:
        raise AssertionError("zero degree-four slack must use all four Q4 colors")

    a, b, c, d = boundary
    color_c = state.coloring[c]
    component_ac = two_color_component(state, a, color_c)
    if c not in component_ac:
        return KempeMove(seed=a, other_color=color_c)

    color_d = state.coloring[d]
    component_bd = two_color_component(state, b, color_d)
    if d not in component_bd:
        return KempeMove(seed=b, other_color=color_d)

    raise ValueError(
        "both opposite Kempe pairs are connected; planar crosscut premise is violated"
    )


@dataclass(frozen=True)
class DegreeFourReductionCertificate:
    """Exact executable interface for the standard degree-four reduction."""

    before: ConstructionState
    focus: str
    boundary: tuple[str, str, str, str]
    move: KempeMove

    @property
    def valid(self) -> bool:
        try:
            expected = degree_four_opening_move(
                self.before,
                self.focus,
                self.boundary,
            )
        except ValueError:
            return False
        if expected is None or expected != self.move:
            return False

        after = apply_kempe_move(self.before, self.move)
        return (
            self.before.committed_edges_valid
            and after.committed_edges_valid
            and bool(after.admissible_colors(self.focus))
        )


def certify_degree_four_reduction(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, str, str, str],
) -> DegreeFourReductionCertificate | None:
    move = degree_four_opening_move(state, focus, boundary)
    if move is None:
        return None
    return DegreeFourReductionCertificate(
        before=state,
        focus=focus,
        boundary=boundary,
        move=move,
    )

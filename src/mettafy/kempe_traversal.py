from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from mettafy.color_construction import (
    PALETTE4,
    ConstructionState,
    CounterfactualTraversalWitness,
)


@dataclass(frozen=True)
class KempeMove:
    """INFERENCE: one exact two-color component intervention.

    ``seed`` selects the connected component in the subgraph induced by the
    seed color and ``other_color``. Swapping those two labels on the entire
    component preserves every committed edge obligation in the imagined
    coloring carrier.

    This object has no authority to recolor the realized construction.
    """

    seed: str
    other_color: int


def two_color_component(
    state: ConstructionState, seed: str, other_color: int
) -> frozenset[str]:
    if seed not in state.coloring:
        raise ValueError("Kempe seed must already be committed")
    seed_color = state.coloring[seed]
    if other_color not in PALETTE4:
        raise ValueError("other color lies outside Q4")
    if other_color == seed_color:
        raise ValueError("Kempe traversal requires two distinct colors")

    allowed = frozenset({seed_color, other_color})
    seen: set[str] = {seed}
    frontier = [seed]
    while frontier:
        vertex = frontier.pop()
        for neighbor in state.graph[vertex]:
            if neighbor in seen or neighbor not in state.coloring:
                continue
            if state.coloring[neighbor] in allowed:
                seen.add(neighbor)
                frontier.append(neighbor)
    return frozenset(seen)


def apply_kempe_move(state: ConstructionState, move: KempeMove) -> ConstructionState:
    """INFERENCE: compute a proper counterfactual recoloring snapshot."""

    component = two_color_component(state, move.seed, move.other_color)
    seed_color = state.coloring[move.seed]
    updated = dict(state.coloring)
    for vertex in component:
        current = state.coloring[vertex]
        updated[vertex] = move.other_color if current == seed_color else seed_color
    return ConstructionState(state.graph, updated)


def all_component_moves(state: ConstructionState) -> tuple[KempeMove, ...]:
    """INFERENCE: enumerate graph-native Kempe thought experiments.

    This is a mechanical witness/falsifier helper, not proof authority.
    """

    moves: list[KempeMove] = []
    committed = set(state.coloring)
    for color_a, color_b in combinations(sorted(PALETTE4), 2):
        remaining = {
            vertex
            for vertex in committed
            if state.coloring[vertex] in (color_a, color_b)
        }
        while remaining:
            seed = min(remaining)
            other = color_b if state.coloring[seed] == color_a else color_a
            component = two_color_component(state, seed, other)
            moves.append(KempeMove(seed=seed, other_color=other))
            remaining.difference_update(component)
    return tuple(moves)


def opening_single_moves(
    state: ConstructionState, focus: str
) -> tuple[KempeMove, ...]:
    """INFERENCE: imagined one-move branches that expose apparent focus slack."""

    if state.admissible_colors(focus):
        return ()
    opening: list[KempeMove] = []
    for move in all_component_moves(state):
        after = apply_kempe_move(state, move)
        if after.admissible_colors(focus):
            opening.append(move)
    return tuple(opening)


def single_move_locked(state: ConstructionState, focus: str) -> bool:
    """INFERENCE/NEGATIVE: no one-step imagined Kempe branch opens the focus."""

    return not state.admissible_colors(focus) and not opening_single_moves(state, focus)


@dataclass(frozen=True)
class CounterfactualKempeTraversal:
    """INFERENCE: a finite composition of imagined exact component moves.

    The witness succeeds only when replaying the declared counterfactual moves
    produces a proper graph-level recoloring that exposes apparent focus slack.
    It does not authorize that recoloring as construction history. Any final
    color still has to cross the independent CertifiedInstantiation boundary on
    the unchanged realized map.
    """

    initial: ConstructionState
    focus: str
    moves: tuple[KempeMove, ...]

    def replay(self) -> tuple[ConstructionState, ...]:
        states = [self.initial]
        current = self.initial
        for move in self.moves:
            current = apply_kempe_move(current, move)
            states.append(current)
        return tuple(states)

    @property
    def final(self) -> ConstructionState:
        return self.replay()[-1]

    @property
    def valid(self) -> bool:
        if not self.moves:
            return False
        return CounterfactualTraversalWitness(
            before=self.initial,
            after=self.final,
            focus=self.focus,
        ).valid


# Historical public name retained for archived experiments. Semantics are
# inference-only.
KempeTraversalCertificate = CounterfactualKempeTraversal

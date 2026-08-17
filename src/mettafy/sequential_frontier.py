from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from mettafy.color_construction import PALETTE4, ConstructionState
from mettafy.kempe_traversal import KempeMove, apply_kempe_move, two_color_component


@dataclass(frozen=True)
class CleanFrontierTurn:
    """One complete bichromatic state turn at a degree-five frontier.

    The entire two-color component is derived before the turn is applied.  A
    turn is *clean* exactly when that component meets the focus frontier in one
    vertex, so the realized turn changes one frontier state and leaves every
    other indexed frontier obligation untouched.
    """

    before: ConstructionState
    focus: str
    boundary: tuple[str, ...]
    move: KempeMove
    component: frozenset[str]
    after: ConstructionState

    @property
    def boundary_hits(self) -> frozenset[str]:
        return frozenset(vertex for vertex in self.boundary if vertex in self.component)

    @property
    def changed_boundary_vertices(self) -> frozenset[str]:
        return frozenset(
            vertex
            for vertex in self.boundary
            if self.before.coloring[vertex] != self.after.coloring[vertex]
        )

    @property
    def valid(self) -> bool:
        if self.focus in self.before.coloring or self.focus in self.after.coloring:
            return False
        if set(self.boundary) != set(self.before.graph[self.focus]):
            return False
        if tuple(self.before.graph[self.focus]) != self.boundary:
            return False
        if self.move.seed not in self.boundary:
            return False
        if self.move.other_color not in PALETTE4:
            return False
        if self.move.other_color == self.before.coloring[self.move.seed]:
            return False
        expected_component = two_color_component(
            self.before,
            self.move.seed,
            self.move.other_color,
        )
        if self.component != expected_component:
            return False
        if self.boundary_hits != frozenset({self.move.seed}):
            return False
        expected_after = apply_kempe_move(self.before, self.move)
        if dict(self.after.coloring) != dict(expected_after.coloring):
            return False
        if dict(self.after.graph) != dict(self.before.graph):
            return False
        if self.changed_boundary_vertices != frozenset({self.move.seed}):
            return False
        return self.before.committed_edges_valid and self.after.committed_edges_valid


def clean_frontier_turns(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, ...],
) -> tuple[CleanFrontierTurn, ...]:
    """Derive all complete current turns that alter exactly one frontier state.

    This function derives permissions from the actual current construction.  It
    does not choose a future route.
    """

    if focus in state.coloring:
        raise ValueError("clean frontier turns require an uncommitted focus")
    if tuple(state.graph[focus]) != boundary:
        raise ValueError("boundary must be the ordered focus neighborhood")

    turns: list[CleanFrontierTurn] = []
    for seed in boundary:
        seed_color = state.coloring[seed]
        for other_color in sorted(PALETTE4 - {seed_color}):
            move = KempeMove(seed=seed, other_color=other_color)
            component = two_color_component(state, seed, other_color)
            if frozenset(vertex for vertex in boundary if vertex in component) != frozenset({seed}):
                continue
            after = apply_kempe_move(state, move)
            turn = CleanFrontierTurn(
                before=state,
                focus=focus,
                boundary=boundary,
                move=move,
                component=component,
                after=after,
            )
            if not turn.valid:
                raise AssertionError("derived clean frontier turn failed certification")
            turns.append(turn)
    return tuple(turns)


@dataclass(frozen=True)
class CleanFrontierAuditRoute:
    """Mechanical falsifier/audit route, never a construction-state oracle."""

    initial: ConstructionState
    focus: str
    boundary: tuple[str, ...]
    turns: tuple[CleanFrontierTurn, ...]

    @property
    def final(self) -> ConstructionState:
        return self.turns[-1].after if self.turns else self.initial

    @property
    def valid(self) -> bool:
        if not self.turns:
            return False
        current = self.initial
        for turn in self.turns:
            if not turn.valid or turn.before != current:
                return False
            current = turn.after
        return bool(current.admissible_colors(self.focus))


def shortest_clean_frontier_audit_route(
    state: ConstructionState,
    focus: str,
    boundary: tuple[str, ...],
    *,
    max_turns: int,
) -> CleanFrontierAuditRoute | None:
    """Exhaustively falsify a bounded clean-turn claim.

    Enumeration is deliberately confined to the audit layer.  A proof-relevant
    construction still takes one current turn, realizes it, and then derives
    the next turn from the actual successor.
    """

    if max_turns < 1:
        raise ValueError("max_turns must be positive")
    if state.admissible_colors(focus):
        return None

    queue: deque[tuple[ConstructionState, tuple[CleanFrontierTurn, ...]]] = deque(
        [(state, ())]
    )
    seen = {tuple(sorted(state.coloring.items()))}

    while queue:
        current, route = queue.popleft()
        if len(route) >= max_turns:
            continue
        for turn in clean_frontier_turns(current, focus, boundary):
            next_route = route + (turn,)
            if turn.after.admissible_colors(focus):
                certificate = CleanFrontierAuditRoute(
                    initial=state,
                    focus=focus,
                    boundary=boundary,
                    turns=next_route,
                )
                if not certificate.valid:
                    raise AssertionError("clean frontier audit route failed certification")
                return certificate
            key = tuple(sorted(turn.after.coloring.items()))
            if key in seen:
                continue
            seen.add(key)
            queue.append((turn.after, next_route))
    return None

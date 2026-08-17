from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import TypeAlias

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import ControlTransition, StateKey, state_key
from mettafy.kempe_traversal import KempeMove, all_component_moves, apply_kempe_move

ParentRecord: TypeAlias = tuple[StateKey, KempeMove]


@dataclass(frozen=True)
class FocusSlackPathCertificate:
    """Finite exact trajectory ending at positive focus palette slack.

    The path is reconstructed from controls actually available at each visited
    state. No future target is a coordinate of the construction state itself.
    """

    initial: ConstructionState
    focus: str
    moves: tuple[KempeMove, ...]

    def replay(self) -> tuple[ConstructionState, ...]:
        states = [self.initial]
        current = self.initial
        for move in self.moves:
            if move not in all_component_moves(current):
                raise AssertionError("declared move is not a current graph-derived control")
            current = apply_kempe_move(current, move)
            states.append(current)
        return tuple(states)

    @property
    def final(self) -> ConstructionState:
        return self.replay()[-1]

    @property
    def valid(self) -> bool:
        states = self.replay()
        return (
            all(dict(state.graph) == dict(self.initial.graph) for state in states)
            and all(state.surface_genus == self.initial.surface_genus == 0 for state in states)
            and all(state.committed_edges_valid for state in states)
            and bool(self.final.admissible_colors(self.focus))
        )


@dataclass(frozen=True)
class SlacklessControlComponentCertificate:
    """Exhaustive local-control component with zero focus palette slack.

    This is not a theorem-level stopping state. It is an exact certificate that
    the currently declared Kempe control family has been exhausted on one fixed
    carrier without producing positive A(focus), so the retained witness must be
    handed to the next admissible control layer.
    """

    initial: ConstructionState
    focus: str
    states: tuple[ConstructionState, ...]
    transitions: tuple[ControlTransition, ...]

    @property
    def state_keys(self) -> frozenset[StateKey]:
        return frozenset(state_key(state) for state in self.states)

    @property
    def valid(self) -> bool:
        keys = self.state_keys
        if state_key(self.initial) not in keys:
            return False
        if any(state.admissible_colors(self.focus) for state in self.states):
            return False
        if any(dict(state.graph) != dict(self.initial.graph) for state in self.states):
            return False
        if any(state.surface_genus != self.initial.surface_genus for state in self.states):
            return False
        if any(not state.committed_edges_valid for state in self.states):
            return False

        transitions = {
            (transition.source, transition.target)
            for transition in self.transitions
        }
        for state in self.states:
            source = state_key(state)
            for move in all_component_moves(state):
                after = apply_kempe_move(state, move)
                target = state_key(after)
                if target not in keys:
                    return False
                if (source, target) not in transitions:
                    return False
        return True


ControlAuditResult: TypeAlias = FocusSlackPathCertificate | SlacklessControlComponentCertificate


def audit_control_component(
    initial: ConstructionState, focus: str
) -> ControlAuditResult:
    """Exhaust the finite current-control component without a depth oracle.

    Because the carrier and committed vertex set are fixed and the palette is
    Q4, there are at most 4**n coloring states for n committed vertices. The
    breadth-first audit therefore terminates. It returns either a finite exact
    path to positive A(focus), or an exhaustive slackless component certificate
    for the current Kempe control family.
    """

    if focus not in initial.graph:
        raise ValueError(f"unknown focus vertex {focus!r}")
    if focus in initial.coloring:
        raise ValueError("focus must remain uncommitted during control audit")
    if initial.admissible_colors(focus):
        path_certificate = FocusSlackPathCertificate(initial, focus, ())
        if not path_certificate.valid:
            raise AssertionError("initial focus slack failed exact certification")
        return path_certificate

    initial_key = state_key(initial)
    states: dict[StateKey, ConstructionState] = {initial_key: initial}
    parent: dict[StateKey, ParentRecord] = {}
    queue: deque[StateKey] = deque([initial_key])
    transitions: list[ControlTransition] = []

    while queue:
        source_key = queue.popleft()
        source = states[source_key]
        for move in all_component_moves(source):
            after = apply_kempe_move(source, move)
            target_key = state_key(after)
            transitions.append(ControlTransition(source_key, move, target_key))

            if target_key not in states:
                states[target_key] = after
                parent[target_key] = (source_key, move)
                if after.admissible_colors(focus):
                    moves = _reconstruct_moves(initial_key, target_key, parent)
                    path_certificate = FocusSlackPathCertificate(initial, focus, moves)
                    if not path_certificate.valid:
                        raise AssertionError("reconstructed focus-slack path is invalid")
                    return path_certificate
                queue.append(target_key)

    component_certificate = SlacklessControlComponentCertificate(
        initial=initial,
        focus=focus,
        states=tuple(states.values()),
        transitions=tuple(transitions),
    )
    if not component_certificate.valid:
        raise AssertionError("exhaustive slackless control component is invalid")
    return component_certificate


def _reconstruct_moves(
    initial_key: StateKey,
    target_key: StateKey,
    parent: dict[StateKey, ParentRecord],
) -> tuple[KempeMove, ...]:
    moves: list[KempeMove] = []
    current = target_key
    while current != initial_key:
        previous, move = parent[current]
        moves.append(move)
        current = previous
    moves.reverse()
    return tuple(moves)

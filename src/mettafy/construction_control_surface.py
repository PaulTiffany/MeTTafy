from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from mettafy.color_construction import PALETTE4, ConstructionState
from mettafy.kempe_traversal import KempeMove, all_component_moves, apply_kempe_move

StateKey = tuple[tuple[str, int], ...]


# INFERENCE: this module explores counterfactual recoloring geometry only.
# It is intentionally not a realized-construction API.  The authority boundary
# for actual play is `mettafy.active_inference_boundary`: imagined recolorings
# may inform reasoning, but only a CertifiedInstantiation may commit one void.


def state_key(state: ConstructionState) -> StateKey:
    """INFERENCE: canonical key for one counterfactual coloring snapshot."""

    return tuple(sorted(state.coloring.items()))


@dataclass(frozen=True)
class CounterfactualTransition:
    """INFERENCE: one graph-derived recoloring edge in imagination space."""

    source: StateKey
    move: KempeMove
    target: StateKey


# Compatibility name for historical callers.  It does not denote construction
# history; all values produced by this module remain inference objects.
ControlTransition = CounterfactualTransition


@dataclass(frozen=True)
class CounterfactualControlWitness:
    """INFERENCE: one exact imagined Kempe-component transformation.

    ``before`` and ``after`` are computational coloring carriers used to inspect
    a hypothetical intervention.  Neither is promoted to the next realized map
    by this witness.  In particular, ``after`` may remain blocked, open, or later
    be abandoned without advancing construction time.
    """

    before: ConstructionState
    focus: str
    move: KempeMove
    after: ConstructionState

    @property
    def source_is_blocked(self) -> bool:
        return not self.before.admissible_colors(self.focus)

    # Historical property name retained for compatibility.  "requires control"
    # means only that the counterfactual exploration was requested at a blocked
    # focus; it does not authorize a realized recoloring.
    @property
    def source_requires_control(self) -> bool:
        return self.source_is_blocked

    @property
    def same_carrier(self) -> bool:
        return dict(self.before.graph) == dict(self.after.graph)

    @property
    def same_committed_vertices(self) -> bool:
        return set(self.before.coloring) == set(self.after.coloring)

    @property
    def state_changes(self) -> bool:
        return state_key(self.before) != state_key(self.after)

    @property
    def valid(self) -> bool:
        if not self.source_is_blocked:
            return False
        replayed = apply_kempe_move(self.before, self.move)
        return (
            self.same_carrier
            and self.same_committed_vertices
            and self.before.surface_genus == self.after.surface_genus == 0
            and self.before.committed_edges_valid
            and self.after.committed_edges_valid
            and self.state_changes
            and state_key(replayed) == state_key(self.after)
        )


# Historical name retained as an alias so old experiments keep replaying.  New
# code should use CounterfactualControlWitness or active_inference_boundary.
ImmediateControlCertificate = CounterfactualControlWitness


def counterfactual_control_access(
    state: ConstructionState, focus: str
) -> CounterfactualControlWitness | None:
    """INFERENCE: construct one exact current-state Kempe thought experiment.

    If the focus already has palette slack, no such diagnostic intervention is
    required and ``None`` is returned. Otherwise a graph-native Kempe component
    is selected and replayed in imagination space.

    The resulting ``after`` coloring is *not* a realized construction successor.
    It may be inspected, chained with more imagined moves, or discarded.  No
    future route and no construction authority are supplied by this function.
    """

    if focus not in state.graph:
        raise ValueError(f"unknown focus vertex {focus!r}")
    if focus in state.coloring:
        raise ValueError("focus must remain uncommitted during inference")
    if state.admissible_colors(focus):
        return None

    committed_neighbors = sorted(
        neighbor for neighbor in state.graph[focus] if neighbor in state.coloring
    )
    if not committed_neighbors:
        raise AssertionError("zero focus slack requires committed neighbors")

    seed = committed_neighbors[0]
    seed_color = state.coloring[seed]
    other_color = min(color for color in PALETTE4 if color != seed_color)
    move = KempeMove(seed=seed, other_color=other_color)
    after = apply_kempe_move(state, move)
    witness = CounterfactualControlWitness(state, focus, move, after)
    if not witness.valid:
        raise AssertionError("graph-derived counterfactual control failed its exact witness")
    return witness


def immediate_control_access(
    state: ConstructionState, focus: str
) -> CounterfactualControlWitness | None:
    """INFERENCE compatibility wrapper; no realized control is executed."""

    return counterfactual_control_access(state, focus)


@dataclass(frozen=True)
class CounterfactualColorationSurface:
    """INFERENCE: finite recoloring surface for audit and falsification.

    Each node is a proper ``ConstructionState`` used as a coloring carrier for
    hypothetical Kempe calculations on one fixed graph.  Nodes are not successive
    realized maps.  Breadth-first exploration, paths, commutation checks, and
    repeated ``step`` calls are therefore test-time imagination only.

    To affect construction, reasoning over this surface must be amortized through
    an independently checked ``CertifiedInstantiation`` against the unchanged
    realized map.
    """

    initial: ConstructionState
    focus: str

    def controls(self, state: ConstructionState) -> tuple[KempeMove, ...]:
        """INFERENCE: derive currently imaginable Kempe interventions."""

        self._require_same_carrier(state)
        return all_component_moves(state)

    def immediate_access(
        self, state: ConstructionState
    ) -> CounterfactualControlWitness | None:
        """INFERENCE: inspect one counterfactual current-state intervention."""

        self._require_same_carrier(state)
        return counterfactual_control_access(state, self.focus)

    def step(self, state: ConstructionState, move: KempeMove) -> ConstructionState:
        """INFERENCE: return one imagined recoloring successor.

        Despite the historical method name, this does not advance construction
        time and must not be passed directly to realized play as authority.
        """

        self._require_same_carrier(state)
        after = apply_kempe_move(state, move)
        self._require_same_carrier(after)
        return after

    def explore(
        self, max_depth: int
    ) -> tuple[dict[StateKey, ConstructionState], tuple[CounterfactualTransition, ...]]:
        """INFERENCE: enumerate the imagined recoloring surface for audit."""

        if max_depth < 0:
            raise ValueError("max_depth must be non-negative")

        initial_key = state_key(self.initial)
        states = {initial_key: self.initial}
        depth = {initial_key: 0}
        queue: deque[StateKey] = deque([initial_key])
        transitions: list[CounterfactualTransition] = []

        while queue:
            source_key = queue.popleft()
            source = states[source_key]
            source_depth = depth[source_key]
            if source_depth >= max_depth:
                continue

            for move in self.controls(source):
                target = self.step(source, move)
                target_key = state_key(target)
                transitions.append(CounterfactualTransition(source_key, move, target_key))
                if target_key not in states:
                    states[target_key] = target
                    depth[target_key] = source_depth + 1
                    queue.append(target_key)

        return states, tuple(transitions)

    def shortest_focus_slack_path(
        self, max_depth: int
    ) -> tuple[KempeMove, ...] | None:
        """INFERENCE: bounded diagnostic search, never a future construction route."""

        if max_depth < 0:
            raise ValueError("max_depth must be non-negative")
        if self.initial.admissible_colors(self.focus):
            return ()

        initial_key = state_key(self.initial)
        states = {initial_key: self.initial}
        paths: dict[StateKey, tuple[KempeMove, ...]] = {initial_key: ()}
        queue: deque[StateKey] = deque([initial_key])

        while queue:
            source_key = queue.popleft()
            source = states[source_key]
            path = paths[source_key]
            if len(path) >= max_depth:
                continue

            for move in self.controls(source):
                target = self.step(source, move)
                target_key = state_key(target)
                candidate = path + (move,)
                if target.admissible_colors(self.focus):
                    return candidate
                if target_key not in states:
                    states[target_key] = target
                    paths[target_key] = candidate
                    queue.append(target_key)

        return None

    def ordered_pair_endpoints(
        self, first: KempeMove, second: KempeMove
    ) -> tuple[ConstructionState, ConstructionState]:
        """INFERENCE: compare two imagined control orders on the same snapshot."""

        first_then_second = self.step(self.step(self.initial, first), second)
        second_then_first = self.step(self.step(self.initial, second), first)
        return first_then_second, second_then_first

    def pair_commutes(self, first: KempeMove, second: KempeMove) -> bool:
        """INFERENCE: whether two imagined control orders share an endpoint."""

        left, right = self.ordered_pair_endpoints(first, second)
        return state_key(left) == state_key(right)

    def _require_same_carrier(self, state: ConstructionState) -> None:
        if dict(state.graph) != dict(self.initial.graph):
            raise ValueError("counterfactual traversal changed the graph carrier")
        if state.surface_genus != self.initial.surface_genus:
            raise ValueError("counterfactual traversal changed the surface species")
        if set(state.coloring) != set(self.initial.coloring):
            raise ValueError("counterfactual traversal changed committed vertex identity")


# Historical public name retained as an explicit compatibility alias.  The
# semantics are now counterfactual only.
ColorationControlSurface = CounterfactualColorationSurface

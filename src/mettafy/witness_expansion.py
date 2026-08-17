from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.plane_parameterization import NONZERO_MODES, V4

StageId = str
WitnessAtom = str
StageStatus = Literal["continuable", "exhausted"]
Edge: TypeAlias = tuple[str, str]


@dataclass(frozen=True)
class WitnessExpansionState:
    """Finite retained-witness state for compelled staging.

    ``witness_atoms`` records facts that later stages are not allowed to forget.
    ``stage_universe`` is a caller-supplied finite universe of concrete stage
    certificates available on the fixed construction object.  This class does
    not prove that the universe is complete or that any particular stage exists.

    The only well-founded quantity certified here is the number of declared
    stages that have not yet been consumed.
    """

    witness_atoms: frozenset[WitnessAtom]
    stage_universe: frozenset[StageId]
    stage_history: tuple[StageId, ...] = ()

    def __post_init__(self) -> None:
        if any(not stage for stage in self.stage_universe):
            raise ValueError("stage identifiers must be nonempty")
        if len(set(self.stage_history)) != len(self.stage_history):
            raise ValueError("a compelled stage cannot be consumed twice")
        if not set(self.stage_history) <= self.stage_universe:
            raise ValueError("stage history contains an undeclared stage")

    @property
    def remaining_stages(self) -> frozenset[StageId]:
        return self.stage_universe - frozenset(self.stage_history)

    @property
    def stage_rank(self) -> int:
        """Well-founded finite rank for the declared stage universe."""

        return len(self.remaining_stages)

    @property
    def status(self) -> StageStatus:
        if self.remaining_stages:
            return "continuable"
        return "exhausted"


def apply_compelled_stage(
    state: WitnessExpansionState,
    stage_id: StageId,
    introduced_witnesses: frozenset[WitnessAtom],
) -> WitnessExpansionState:
    """Consume one fresh stage while strictly enlarging the retained witness.

    Replaying a consumed stage is rejected.  This makes the known reversible
    locked-boundary two-cycle unavailable as a *progress* step once the concrete
    cut/certificate that justified it has already been consumed.

    This function does not assert that a fresh admissible stage always exists,
    nor that exhausting the finite stage universe opens the original center.
    Those are theorem obligations outside this mechanical witness.
    """

    if stage_id not in state.stage_universe:
        raise ValueError("stage is outside the declared finite universe")
    if stage_id in state.stage_history:
        raise ValueError("stage has already been consumed")

    novel = introduced_witnesses - state.witness_atoms
    if not novel:
        raise ValueError("a compelled stage must strictly enlarge the retained witness")

    after = WitnessExpansionState(
        witness_atoms=state.witness_atoms | introduced_witnesses,
        stage_universe=state.stage_universe,
        stage_history=state.stage_history + (stage_id,),
    )
    if not state.witness_atoms < after.witness_atoms:
        raise AssertionError("compelled staging must strictly enlarge the witness")
    if after.stage_rank != state.stage_rank - 1:
        raise AssertionError("every compelled stage must consume exactly one finite stage")
    return after


def _canonical_edge(left: str, right: str) -> Edge:
    if left == right:
        raise ValueError("graph-native stage cannot contain a self-loop")
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True, order=True)
class GraphNativeStageId:
    """Content address for one physical dual-cut control.

    The identity is the V4 translation mode together with the unordered set of
    crossed physical primal edges.  Path orientation, traversal direction, and
    color-language relabeling are not part of the identity.  In V4 the inverse
    translation uses the same mode, so immediate reversal of the same physical
    cut receives the same stage identity.
    """

    translation_mode: V4
    crossed_edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        if self.translation_mode not in NONZERO_MODES:
            raise ValueError("graph-native stage requires a nonzero V4 mode")
        canonical = tuple(
            sorted({_canonical_edge(left, right) for left, right in self.crossed_edges})
        )
        if not canonical:
            raise ValueError("graph-native stage requires at least one physical cut edge")
        object.__setattr__(self, "crossed_edges", canonical)

    @property
    def token(self) -> str:
        mode = f"{self.translation_mode[0]}{self.translation_mode[1]}"
        edges = ",".join(f"{left}--{right}" for left, right in self.crossed_edges)
        return f"dual:{mode}:{edges}"


@dataclass(frozen=True)
class GraphNativeWitnessExpansionState:
    """Finite proof history derived from one fixed physical graph carrier.

    Unlike ``WitnessExpansionState``, this form has no caller-invented stage
    universe.  A stage is content-addressed from an actual V4 mode and actual
    crossed graph edges when the planar control is derived.

    The retained physical carrier and consumed control identities are separate:
    a new chromatic typing of an already retained cut does not masquerade as new
    geometry.  Finiteness follows from the fixed carrier itself.  With ``m``
    committed carrier edges, there are at most ``3 * (2**m - 1)`` nonempty
    mode/cut identities, an intentionally loose graph-derived upper bound.
    """

    carrier_edges: frozenset[Edge]
    retained_carrier_edges: frozenset[Edge] = frozenset()
    stage_history: tuple[GraphNativeStageId, ...] = ()

    def __post_init__(self) -> None:
        canonical_carrier = frozenset(
            _canonical_edge(left, right) for left, right in self.carrier_edges
        )
        canonical_retained = frozenset(
            _canonical_edge(left, right) for left, right in self.retained_carrier_edges
        )
        object.__setattr__(self, "carrier_edges", canonical_carrier)
        object.__setattr__(self, "retained_carrier_edges", canonical_retained)

        if not canonical_retained <= canonical_carrier:
            raise ValueError("retained witness edge lies outside the fixed carrier")
        if len(set(self.stage_history)) != len(self.stage_history):
            raise ValueError("a graph-native stage cannot be consumed twice")
        for stage in self.stage_history:
            if not set(stage.crossed_edges) <= canonical_carrier:
                raise ValueError("stage history contains an edge outside the fixed carrier")

    @property
    def stage_capacity_upper_bound(self) -> int:
        edge_count = len(self.carrier_edges)
        return len(NONZERO_MODES) * ((1 << edge_count) - 1)

    @property
    def remaining_stage_capacity(self) -> int:
        return self.stage_capacity_upper_bound - len(self.stage_history)


def apply_graph_native_stage(
    state: GraphNativeWitnessExpansionState,
    stage_id: GraphNativeStageId,
) -> GraphNativeWitnessExpansionState:
    """Consume one embedding-derived stage without denying its inverse symmetry.

    The recoloring operation itself may remain reversible.  This function only
    says the same content-addressed mode/cut certificate cannot be counted twice
    as proof progress.  Physical witness retention is monotone but need not grow
    strictly when a fresh control reuses already retained carrier edges.
    """

    if not set(stage_id.crossed_edges) <= state.carrier_edges:
        raise ValueError("graph-native stage lies outside the fixed carrier")
    if stage_id in state.stage_history:
        raise ValueError("graph-native stage has already been consumed as proof progress")

    after = GraphNativeWitnessExpansionState(
        carrier_edges=state.carrier_edges,
        retained_carrier_edges=(
            state.retained_carrier_edges | frozenset(stage_id.crossed_edges)
        ),
        stage_history=state.stage_history + (stage_id,),
    )
    if not state.retained_carrier_edges <= after.retained_carrier_edges:
        raise AssertionError("graph-native staging lost a retained physical witness")
    if after.remaining_stage_capacity != state.remaining_stage_capacity - 1:
        raise AssertionError("fresh graph-native stage must consume one finite identity")
    return after

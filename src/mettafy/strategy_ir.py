from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from mettafy.active_inference_boundary import (
    CertifiedInstantiation,
    InferenceEpisode,
    amortize,
    void_count,
)
from mettafy.color_construction import ConstructionState


def _same_state(left: ConstructionState, right: ConstructionState) -> bool:
    return dict(left.graph) == dict(right.graph) and dict(left.coloring) == dict(right.coloring)


@dataclass(frozen=True)
class HypotheticalMap:
    """INFERENCE: one legal future-construction branch rooted in the actual map.

    ``state`` may contain additional hypothetical ``void -> V4`` commitments,
    but every realized commitment in ``realized`` is preserved exactly. ``depth``
    is level-of-thinking depth, not construction time.
    """

    realized: ConstructionState
    state: ConstructionState
    depth: int = 0

    def __post_init__(self) -> None:
        if dict(self.realized.graph) != dict(self.state.graph):
            raise ValueError("hypothetical branch must preserve the realized graph")
        for vertex, color in self.realized.coloring.items():
            if self.state.coloring.get(vertex) != color:
                raise ValueError("hypothetical branch cannot rewrite a realized color")
        added = len(self.state.coloring) - len(self.realized.coloring)
        if added < 0 or self.depth != added:
            raise ValueError("hypothetical depth must equal added imaginary commitments")

    @property
    def realized_voids(self) -> int:
        """REALIZED clock frozen for the entire same-turn imagination episode."""

        return void_count(self.realized)

    @property
    def imagined_voids(self) -> int:
        """INFERENCE: unresolved vertices remaining inside this hypothetical line."""

        return void_count(self.state)


def begin_hypothetical(realized: ConstructionState) -> HypotheticalMap:
    """INFERENCE: open a level-of-thinking branch without advancing construction."""

    return HypotheticalMap(
        realized=realized,
        state=ConstructionState(realized.graph, realized.coloring),
        depth=0,
    )


@dataclass(frozen=True)
class ImaginedCommit:
    """INFERENCE: ``if I instantiate this, then ...`` -- never construction history."""

    before: HypotheticalMap
    focus: str
    color: int
    after: HypotheticalMap

    @property
    def valid(self) -> bool:
        try:
            replayed = self.before.state.commit(self.focus, self.color)
        except ValueError:
            return False
        return (
            self.after.realized is self.before.realized
            and self.after.depth == self.before.depth + 1
            and _same_state(replayed, self.after.state)
        )


def imagine_commit(before: HypotheticalMap, focus: str, color: int) -> ImaginedCommit:
    """INFERENCE: extend one hypothetical game line by one legal imagined commit."""

    after_state = before.state.commit(focus, color)
    after = HypotheticalMap(
        realized=before.realized,
        state=after_state,
        depth=before.depth + 1,
    )
    witness = ImaginedCommit(before=before, focus=focus, color=color, after=after)
    if not witness.valid:
        raise AssertionError("imagined commit failed exact replay")
    return witness


@dataclass(frozen=True)
class StrategySignature:
    """INFERENCE: proof-relevant MapMaker view used to quotient concrete states.

    The vocabulary is deliberately uncommitted. Roleplay supplies only the
    lowest-level distinctions it actually needs; counterexamples may force this
    signature to split later.
    """

    observables: tuple[tuple[str, str], ...] = ()
    available_probes: tuple[str, ...] = ()
    response_classes: tuple[str, ...] = ()
    options: tuple[str, ...] = ()


@dataclass(frozen=True)
class StrategySnapshot:
    """INFERENCE: a hypothetical position plus its current meta-strategy class."""

    state: HypotheticalMap
    signature: StrategySignature


@dataclass(frozen=True)
class See:
    """ROLEPLAY/SEE: record only observables available at this bounded position."""

    snapshot: StrategySnapshot


@dataclass(frozen=True)
class Ask:
    """ROLEPLAY/ASK: select one proof-relevant probe."""

    snapshot: StrategySnapshot
    probe: str


@dataclass(frozen=True)
class Answer:
    """ROLEPLAY/ANSWER: classify the map's imagined response to a probe."""

    snapshot: StrategySnapshot
    probe: str
    response_class: str


@dataclass(frozen=True)
class CommitOrNot:
    """ROLEPLAY/COMMIT-OR-NOT: inference verdict about one candidate first move."""

    snapshot: StrategySnapshot
    focus: str
    color: int
    decision: Literal["commit", "reject", "undecided"]


RoleplayEvent: TypeAlias = See | Ask | Answer | CommitOrNot


@dataclass(frozen=True)
class RoleplayEpisode:
    """INFERENCE: sequential human inspection of same-turn hypothetical structure."""

    realized: ConstructionState
    events: tuple[RoleplayEvent, ...]

    def __post_init__(self) -> None:
        for event in self.events:
            root = event.snapshot.state.realized
            if not _same_state(root, self.realized):
                raise ValueError("every roleplay event must share one realized antecedent")

    @property
    def construction_voids(self) -> int:
        return void_count(self.realized)

    @property
    def sequential_observations(self) -> int:
        return len(self.events)

    @property
    def max_level_of_thinking(self) -> int:
        return max((event.snapshot.state.depth for event in self.events), default=0)


@dataclass(frozen=True)
class StrategyClass:
    """INFERENCE: one quotient class and the trace positions that instantiate it."""

    signature: StrategySignature
    members: tuple[int, ...]


def quotient_strategy_trace(
    snapshots: tuple[StrategySnapshot, ...],
) -> tuple[StrategyClass, ...]:
    """INFERENCE: compress a concrete inspection transcript by strategy signature."""

    order: list[StrategySignature] = []
    members: dict[StrategySignature, list[int]] = {}
    for index, snapshot in enumerate(snapshots):
        signature = snapshot.signature
        if signature not in members:
            order.append(signature)
            members[signature] = []
        members[signature].append(index)
    return tuple(
        StrategyClass(signature=signature, members=tuple(members[signature]))
        for signature in order
    )


def first_repeated_strategy(
    snapshots: tuple[StrategySnapshot, ...],
) -> tuple[int, int] | None:
    """INFERENCE: return the first proof-relevant loop instead of unrolling it."""

    first_seen: dict[StrategySignature, int] = {}
    for index, snapshot in enumerate(snapshots):
        previous = first_seen.get(snapshot.signature)
        if previous is not None:
            return previous, index
        first_seen[snapshot.signature] = index
    return None


def amortize_first_move(
    episode: InferenceEpisode,
    candidate: ImaginedCommit,
) -> CertifiedInstantiation:
    """BRIDGE: only a depth-zero imagined move may be considered for reality.

    Deeper level-of-thinking commitments are discarded with the old imagination
    episode. The surviving first move still passes through ``amortize``, which
    rechecks it against the unchanged actual map.
    """

    if candidate.before.depth != 0:
        raise ValueError("only the first imagined move may cross the turn boundary")
    if not _same_state(candidate.before.realized, episode.realized):
        raise ValueError("candidate and inference episode do not share a realized root")
    if candidate.focus != episode.focus:
        raise ValueError("candidate focus does not match the actual inference focus")
    return amortize(episode, candidate.color)

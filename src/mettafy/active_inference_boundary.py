from __future__ import annotations

from dataclasses import dataclass

from mettafy.color_construction import PALETTE4, ConstructionState
from mettafy.kempe_traversal import KempeMove, apply_kempe_move


@dataclass(frozen=True)
class ImaginedState:
    """INFERENCE: one counterfactual coloring inspected at test time.

    The wrapped ``ConstructionState`` is a convenient proper-coloring carrier for
    graph-native calculations. It is *not* construction history and has no method
    that can commit itself as the next realized state.
    """

    coloring: ConstructionState


@dataclass(frozen=True)
class CounterfactualMove:
    """INFERENCE: one imagined Kempe intervention and its imagined result."""

    before: ImaginedState
    move: KempeMove
    after: ImaginedState

    @property
    def valid(self) -> bool:
        replayed = apply_kempe_move(self.before.coloring, self.move)
        return (
            dict(replayed.graph) == dict(self.after.coloring.graph)
            and dict(replayed.coloring) == dict(self.after.coloring.coloring)
            and replayed.committed_edges_valid
        )


def inspect(realized: ConstructionState) -> ImaginedState:
    """INFERENCE: copy the actual partial map into imagination space."""

    return ImaginedState(ConstructionState(realized.graph, realized.coloring))


def imagine_kempe(before: ImaginedState, move: KempeMove) -> CounterfactualMove:
    """INFERENCE: apply a Kempe move only to an imagined state."""

    after = ImaginedState(apply_kempe_move(before.coloring, move))
    witness = CounterfactualMove(before=before, move=move, after=after)
    if not witness.valid:
        raise AssertionError("counterfactual Kempe replay failed its exact witness")
    return witness


@dataclass(frozen=True)
class InferenceEpisode:
    """INFERENCE: arbitrary counterfactual work rooted in one actual map/focus.

    ``imagined`` may branch or repeat states. Its length is not construction time.
    No future construction route is stored here.
    """

    realized: ConstructionState
    focus: str
    imagined: tuple[ImaginedState, ...] = ()

    def __post_init__(self) -> None:
        if self.focus not in self.realized.graph:
            raise ValueError(f"unknown focus vertex {self.focus!r}")
        if self.focus in self.realized.coloring:
            raise ValueError("focus must be void/uncommitted in the realized map")


@dataclass(frozen=True)
class CertifiedInstantiation:
    """BRIDGE: the only object authorized to cross into realized construction.

    Validity is checked against ``realized`` itself. Counterfactual states and
    predicted responses are intentionally absent from this type.
    """

    realized: ConstructionState
    focus: str
    color: int

    @property
    def valid(self) -> bool:
        if self.focus not in self.realized.graph:
            return False
        if self.focus in self.realized.coloring:
            return False
        if self.color not in PALETTE4:
            return False
        try:
            candidate = self.realized.commit(self.focus, self.color)
        except ValueError:
            return False
        return candidate.committed_edges_valid


def amortize(episode: InferenceEpisode, color: int) -> CertifiedInstantiation:
    """BRIDGE: collapse arbitrary reasoning into one actual-map certificate.

    A successful imagined branch is not enough. The selected color must be
    admissible on the *unchanged realized map* at the current focus.
    """

    certificate = CertifiedInstantiation(
        realized=episode.realized,
        focus=episode.focus,
        color=color,
    )
    if not certificate.valid:
        raise ValueError(
            "inference did not certify an admissible state on the realized map"
        )
    return certificate


def instantiate(certificate: CertifiedInstantiation) -> ConstructionState:
    """REALIZED: perform exactly one ``void -> V4`` construction event."""

    if not certificate.valid:
        raise ValueError("invalid certified instantiation")
    return certificate.realized.commit(certificate.focus, certificate.color)


def void_count(state: ConstructionState) -> int:
    """REALIZED: number of currently uninstantiated vertices."""

    return len(state.graph) - len(state.coloring)

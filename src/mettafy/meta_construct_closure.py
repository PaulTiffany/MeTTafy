from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from mettafy.active_inference_boundary import (
    CertifiedInstantiation,
    ImaginedState,
    InferenceEpisode,
    instantiate,
    void_count,
)
from mettafy.color_construction import ConstructionState


class MetaConstructFamily(str, Enum):
    """The two current degree-five test-time meta-construct families.

    This enum is a research-language boundary, not an exhaustiveness theorem.
    Proving that every relevant planar continuation projects into one of these
    two constructors remains an explicit mathematical obligation.
    """

    RED_TEAM = "red_team"
    ALTERNATING_PAIR = "two_upward_alternating_horizontal"


ALL_META_CONSTRUCT_FAMILIES = frozenset(MetaConstructFamily)


@dataclass(frozen=True)
class MetaConstructPrefix:
    """INFERENCE: a finite observed prefix of one local meta-construct.

    A prefix may stop at any length. Stopping does not imply failure and does not
    imply construction progress: test time is not game time.
    """

    family: MetaConstructFamily
    states: tuple[ImaginedState, ...] = ()

    @property
    def may_stop(self) -> bool:
        """Every finite prefix is allowed to terminate the current test branch."""

        return True


@dataclass(frozen=True)
class ImaginationBox:
    """INFERENCE: open imaginary work bounded only by one authority target.

    The box deliberately carries no path, depth, step budget, or finite-state
    schema. An imaginary witness may be any caller-supplied Python object. The
    only fixed boundary is the realized map/focus that any projected answer must
    satisfy before it can acquire construction authority.

    This is not a claim that a concrete program can execute an infinite amount
    of work. It is an interface claim: theorem machinery does not impose a
    search-depth bound merely to make counterfactual reasoning proof relevant.
    """

    realized: ConstructionState
    focus: str

    def __post_init__(self) -> None:
        if self.focus not in self.realized.graph:
            raise ValueError(f"unknown focus vertex {self.focus!r}")
        if self.focus in self.realized.coloring:
            raise ValueError("imagination focus must remain void in the realized map")


@dataclass(frozen=True)
class ImaginaryProjection:
    """BRIDGE CANDIDATE: compress arbitrary imaginary structure to `V4 | None`.

    `project` may inspect any caller-defined witness structure. A result of
    `None` remains wholly imaginary. A proposed color is still powerless until
    it validates as a `CertifiedInstantiation` on the unchanged realized map.
    """

    box: ImaginationBox
    project: Callable[[object], int | None]

    def compress(self, witness: object) -> CertifiedInstantiation | None:
        color = self.project(witness)
        if color is None:
            return None
        certificate = CertifiedInstantiation(
            realized=self.box.realized,
            focus=self.box.focus,
            color=color,
        )
        if not certificate.valid:
            raise ValueError(
                "imaginary projection proposed a color that is not admissible "
                "on the realized authority target"
            )
        return certificate


@dataclass(frozen=True)
class DecisionReachability:
    """WITNESS: one finite admissible `if-this-then-this` decision chain.

    The chain is a transferable residue, not a search budget. There is no maximum
    length field and no claim that imagination considered only these states. A
    successful research episode may branch, restart, stutter, or change
    representation before leaving this finite auditable spine.

    `admissible_step(a, b)` is the caller-supplied refinement obligation between
    adjacent witness states. Only the final state is projected. Even a valid
    chain has zero construction authority until that endpoint survives the
    projection's actual-map admissibility check.
    """

    projection: ImaginaryProjection
    states: tuple[object, ...]
    admissible_step: Callable[[object, object], bool]

    def __post_init__(self) -> None:
        if not self.states:
            raise ValueError("Decision Reachability requires at least one witness state")

    @property
    def endpoint(self) -> object:
        return self.states[-1]

    @property
    def witnessed(self) -> bool:
        """Whether every adjacent implication/refinement step is admissible."""

        return all(
            self.admissible_step(before, after)
            for before, after in zip(self.states, self.states[1:], strict=False)
        )

    def compress(self) -> CertifiedInstantiation:
        """Collapse a witnessed deciding chain through the existing authority wall."""

        if not self.witnessed:
            raise ValueError("Decision Reachability chain contains a non-admissible step")
        certificate = self.projection.compress(self.endpoint)
        if certificate is None:
            raise ValueError("Decision Reachability chain does not end at a projected answer")
        return certificate


@dataclass(frozen=True)
class TwoFamilyCover:
    """INFERENCE: both named families considered for one realized obligation.

    ``exhaustive`` is deliberately supplied rather than inferred. The code can
    enumerate the research ontology; it cannot prove the planar classification
    theorem that connects that ontology to every admissible continuation.
    """

    episode: InferenceEpisode
    prefixes: tuple[MetaConstructPrefix, ...]
    exhaustive: bool = False

    def __post_init__(self) -> None:
        realized_graph = dict(self.episode.realized.graph)
        for prefix in self.prefixes:
            for state in prefix.states:
                if dict(state.coloring.graph) != realized_graph:
                    raise ValueError("meta-construct prefix belongs to a different graph")

    @property
    def observed_families(self) -> frozenset[MetaConstructFamily]:
        return frozenset(prefix.family for prefix in self.prefixes)

    @property
    def both_families_observed(self) -> bool:
        return self.observed_families == ALL_META_CONSTRUCT_FAMILIES

    @property
    def classification_closed(self) -> bool:
        return self.both_families_observed and self.exhaustive


@dataclass(frozen=True)
class Restart:
    """INFERENCE: abandon this branch and re-observe without changing the map."""

    episode: InferenceEpisode

    def realized_state(self) -> ConstructionState:
        return self.episode.realized


@dataclass(frozen=True)
class VoidEnd:
    """BRIDGE: the only local end state carrying construction authority.

    The payload is already a ``CertifiedInstantiation`` checked against the
    unchanged realized map. No imagined state or meta-construct prefix crosses
    the authority boundary.
    """

    certificate: CertifiedInstantiation

    def __post_init__(self) -> None:
        if not self.certificate.valid:
            raise ValueError("void/end requires a valid actual-map certificate")

    def realize(self) -> ConstructionState:
        return instantiate(self.certificate)


LocalEnd = Restart | VoidEnd


def end_as_restart(episode: InferenceEpisode) -> Restart:
    """INFERENCE: terminate any finite test-time prefix without a realized move."""

    return Restart(episode=episode)


def end_as_void(certificate: CertifiedInstantiation) -> VoidEnd:
    """BRIDGE: terminate locally only after actual-map admissibility is certified."""

    return VoidEnd(certificate=certificate)


def end_from_decision(reachability: DecisionReachability) -> VoidEnd:
    """BRIDGE: a witnessed deciding chain may end only through its checked projection."""

    return end_as_void(reachability.compress())


def realized_void_delta(end: LocalEnd) -> int:
    """Measure construction-time progress, ignoring arbitrary test-time length.

    Restart consumes zero voids. A valid ``VoidEnd`` consumes exactly one.
    """

    if isinstance(end, Restart):
        return 0
    before = void_count(end.certificate.realized)
    after = void_count(end.realize())
    return before - after


@dataclass(frozen=True)
class ClosureObligation:
    """Current independent Track-B closure boundary for one map and focus.

    Classification closure alone is not Four Color closure. A closed local proof
    obligation additionally needs a sound actual-map void/end for this same
    realized state and focus. Unrelated certificates cannot satisfy the ledger.
    """

    cover: TwoFamilyCover
    ends: tuple[LocalEnd, ...]

    def __post_init__(self) -> None:
        expected_map = self.cover.episode.realized
        expected_focus = self.cover.episode.focus
        for end in self.ends:
            if isinstance(end, Restart):
                same_map = end.episode.realized is expected_map
                same_focus = end.episode.focus == expected_focus
            else:
                same_map = end.certificate.realized is expected_map
                same_focus = end.certificate.focus == expected_focus
            if not same_map or not same_focus:
                raise ValueError("local end belongs to a different realized obligation")

    @property
    def has_certified_void_end(self) -> bool:
        return any(isinstance(end, VoidEnd) for end in self.ends)

    @property
    def closed(self) -> bool:
        return self.cover.classification_closed and self.has_certified_void_end

    @property
    def missing(self) -> tuple[str, ...]:
        missing: list[str] = []
        if not self.cover.both_families_observed:
            missing.append("two-family coverage")
        if not self.cover.exhaustive:
            missing.append("planar two-family exhaustiveness theorem")
        if not self.has_certified_void_end:
            missing.append("admissible Decision Reachability chain")
        return tuple(missing)

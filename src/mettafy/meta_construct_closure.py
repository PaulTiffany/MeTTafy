from __future__ import annotations

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
            missing.append("sound certified-instantiation reachability")
        return tuple(missing)

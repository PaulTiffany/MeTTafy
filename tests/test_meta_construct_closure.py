from __future__ import annotations

import pytest

from mettafy.active_inference_boundary import CertifiedInstantiation, InferenceEpisode, inspect
from mettafy.color_construction import ConstructionState
from mettafy.meta_construct_closure import (
    ClosureObligation,
    MetaConstructFamily,
    MetaConstructPrefix,
    TwoFamilyCover,
    end_as_restart,
    end_as_void,
    realized_void_delta,
)

BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary_colors: tuple[int, int, int, int, int]) -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(graph, dict(zip(BOUNDARY, boundary_colors, strict=True)))


def both_family_cover(realized: ConstructionState, *, exhaustive: bool) -> TwoFamilyCover:
    imagined = inspect(realized)
    episode = InferenceEpisode(realized=realized, focus="v", imagined=(imagined,))
    return TwoFamilyCover(
        episode=episode,
        prefixes=(
            MetaConstructPrefix(MetaConstructFamily.RED_TEAM, (imagined,)),
            MetaConstructPrefix(MetaConstructFamily.ALTERNATING_PAIR, (imagined,)),
        ),
        exhaustive=exhaustive,
    )


def test_red_team_prefix_may_end_without_becoming_construction_history() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    episode = InferenceEpisode(realized=realized, focus="v", imagined=(inspect(realized),))
    prefix = MetaConstructPrefix(MetaConstructFamily.RED_TEAM, episode.imagined)

    assert prefix.may_stop

    end = end_as_restart(episode)
    assert end.realized_state() is realized
    assert realized_void_delta(end) == 0
    assert "v" not in realized.coloring


def test_two_named_families_do_not_silently_assert_planar_exhaustiveness() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    cover = both_family_cover(realized, exhaustive=False)

    assert cover.both_families_observed
    assert not cover.classification_closed

    obligation = ClosureObligation(cover=cover, ends=())
    assert not obligation.closed
    assert "planar two-family exhaustiveness theorem" in obligation.missing


def test_classification_exhaustiveness_alone_does_not_create_authority() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    cover = both_family_cover(realized, exhaustive=True)
    restart = end_as_restart(cover.episode)

    obligation = ClosureObligation(cover=cover, ends=(restart,))

    assert cover.classification_closed
    assert not obligation.closed
    assert obligation.missing == ("sound certified-instantiation reachability",)


def test_blocked_abacd_focus_cannot_be_promoted_to_void_end() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    assert realized.admissible_colors("v") == frozenset()

    invalid = CertifiedInstantiation(realized=realized, focus="v", color=0)
    assert not invalid.valid

    with pytest.raises(ValueError, match="actual-map certificate"):
        end_as_void(invalid)


def test_certified_void_end_consumes_exactly_one_realized_void() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    assert realized.admissible_colors("v") == frozenset({3})

    certificate = CertifiedInstantiation(realized=realized, focus="v", color=3)
    end = end_as_void(certificate)

    assert realized_void_delta(end) == 1
    after = end.realize()
    assert after.coloring["v"] == 3
    assert "v" not in realized.coloring


def test_unrelated_certificate_cannot_close_another_obligation() -> None:
    blocked = wheel_state((0, 1, 0, 2, 3))
    cover = both_family_cover(blocked, exhaustive=True)

    unrelated = wheel_state((0, 1, 0, 1, 2))
    certificate = CertifiedInstantiation(realized=unrelated, focus="v", color=3)

    with pytest.raises(ValueError, match="different realized obligation"):
        ClosureObligation(cover=cover, ends=(end_as_void(certificate),))


def test_local_closure_requires_both_open_mathematical_obligations() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    cover = both_family_cover(realized, exhaustive=True)
    certificate = CertifiedInstantiation(realized=realized, focus="v", color=3)

    obligation = ClosureObligation(cover=cover, ends=(end_as_void(certificate),))

    assert obligation.closed
    assert obligation.missing == ()

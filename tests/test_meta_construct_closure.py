from __future__ import annotations

import pytest

from mettafy.active_inference_boundary import (
    CertifiedInstantiation,
    InferenceEpisode,
    inspect,
)
from mettafy.color_construction import ConstructionState
from mettafy.meta_construct_closure import (
    ClosureObligation,
    DecisionReachability,
    ImaginaryProjection,
    ImaginationBox,
    MetaConstructFamily,
    MetaConstructPrefix,
    TwoFamilyCover,
    end_as_restart,
    end_as_void,
    end_from_decision,
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


def test_imagination_box_bounds_authority_not_search_shape() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    box = ImaginationBox(realized=realized, focus="v")

    assert tuple(box.__dataclass_fields__) == ("realized", "focus")
    assert set(box.__dataclass_fields__).isdisjoint(
        {"path", "route", "depth", "max_depth", "steps", "max_steps", "states"}
    )


def test_arbitrary_imaginary_structure_compresses_to_certificate_only() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    box = ImaginationBox(realized=realized, focus="v")
    witness = {
        "red_team": ["branch", "reverse", "branch", "restart"],
        "alternating": {"horizontal": (0, 1, 0, 1), "nested": [{"again": True}]},
        "researcher_note": "the witness can have whatever internal shape is useful",
    }
    projection = ImaginaryProjection(
        box=box,
        project=lambda imagined: 3 if isinstance(imagined, dict) else None,
    )

    certificate = projection.compress(witness)

    assert certificate is not None
    assert certificate.valid
    assert certificate.realized is realized
    assert certificate.focus == "v"
    assert certificate.color == 3
    assert tuple(certificate.__dataclass_fields__) == ("realized", "focus", "color")


def test_imaginary_stuttering_does_not_become_construction_history() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda _witness: 3,
    )

    short = projection.compress(("red-team",))
    long = projection.compress(tuple("red-team" for _ in range(10_000)))

    assert short is not None
    assert long is not None
    assert short.realized is long.realized is realized
    assert short.focus == long.focus == "v"
    assert short.color == long.color == 3
    assert "v" not in realized.coloring


def test_decision_reachability_is_an_auditable_if_then_chain() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == "decide" else None,
    )
    allowed = {
        ("seed", "if-red-team"),
        ("if-red-team", "if-alternating"),
        ("if-alternating", "decide"),
    }
    reachability = DecisionReachability(
        projection=projection,
        states=("seed", "if-red-team", "if-alternating", "decide"),
        admissible_step=lambda before, after: (before, after) in allowed,
    )

    assert reachability.witnessed
    certificate = reachability.compress()
    assert certificate.valid
    assert certificate.color == 3
    assert certificate.realized is realized
    assert "v" not in realized.coloring


def test_decision_reachability_has_no_a_priori_chain_length_bound() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == 10_000 else None,
    )
    reachability = DecisionReachability(
        projection=projection,
        states=tuple(range(10_001)),
        admissible_step=lambda before, after: (
            isinstance(before, int) and isinstance(after, int) and after == before + 1
        ),
    )

    assert tuple(reachability.__dataclass_fields__) == (
        "projection",
        "states",
        "admissible_step",
    )
    assert set(reachability.__dataclass_fields__).isdisjoint(
        {"max_depth", "max_steps", "budget"}
    )
    assert reachability.witnessed
    assert reachability.compress().color == 3


def test_decision_reachability_fails_closed_on_broken_implication() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == "decide" else None,
    )
    reachability = DecisionReachability(
        projection=projection,
        states=("seed", "unsupported-jump", "decide"),
        admissible_step=lambda before, after: (before, after) == ("seed", "decide"),
    )

    assert not reachability.witnessed
    with pytest.raises(ValueError, match="non-admissible step"):
        reachability.compress()


def test_decision_reachability_requires_a_deciding_endpoint() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda _witness: None,
    )
    reachability = DecisionReachability(
        projection=projection,
        states=("seed", "still-thinking"),
        admissible_step=lambda _before, _after: True,
    )

    assert reachability.witnessed
    with pytest.raises(ValueError, match="does not end at a projected answer"):
        reachability.compress()


def test_no_projected_answer_remains_inside_imagination_box() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda _witness: None,
    )

    assert projection.compress({"cycle": [1, 2, 1, 2]}) is None
    assert "v" not in realized.coloring


def test_unsound_imaginary_answer_cannot_cross_authority_boundary() -> None:
    realized = wheel_state((0, 1, 0, 2, 3))
    assert realized.admissible_colors("v") == frozenset()
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda _witness: 0,
    )

    with pytest.raises(ValueError, match="not admissible on the realized authority target"):
        projection.compress({"imagined_opening": 0})

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
    assert obligation.missing == ("admissible Decision Reachability chain",)


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


def test_local_closure_uses_witnessed_decision_reachability() -> None:
    realized = wheel_state((0, 1, 0, 1, 2))
    cover = both_family_cover(realized, exhaustive=True)
    projection = ImaginaryProjection(
        box=ImaginationBox(realized=realized, focus="v"),
        project=lambda witness: 3 if witness == "answer" else None,
    )
    reachability = DecisionReachability(
        projection=projection,
        states=("observe", "if-this", "then-this", "answer"),
        admissible_step=lambda _before, _after: True,
    )

    obligation = ClosureObligation(cover=cover, ends=(end_from_decision(reachability),))

    assert obligation.closed
    assert obligation.missing == ()

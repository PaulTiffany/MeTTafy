from __future__ import annotations

import pytest

from mettafy.active_inference_boundary import (
    CertifiedInstantiation,
    InferenceEpisode,
    amortize,
    imagine_kempe,
    inspect,
    instantiate,
    void_count,
)
from mettafy.color_construction import ConstructionState, terminal_decode
from mettafy.kempe_traversal import KempeMove

BOUNDARY = ("a", "b", "c", "d", "e")


def locked_planar_c5_state() -> ConstructionState:
    """Retained saturated planar C5 used by the counterfactual witnesses."""

    graph = {
        "v": ("a", "b", "c", "d", "e"),
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "x", "p"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "y"),
        "e": ("v", "d", "a", "q"),
        "x": ("b", "y"),
        "y": ("x", "d"),
        "p": ("b", "q"),
        "q": ("p", "e"),
    }
    return ConstructionState(
        graph,
        {
            "a": 0,
            "b": 1,
            "c": 0,
            "d": 2,
            "e": 3,
            "x": 2,
            "y": 1,
            "p": 3,
            "q": 1,
        },
    )


def persistent_double_lock_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c", "d", "e"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e", "b"),
        "e": ("v", "d", "a", "b"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 2, "e": 3},
    )


def open_wheel_state() -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(
        graph,
        {"a": 0, "b": 1, "c": 0, "d": 1, "e": 2},
    )


def boundary_word(state: ConstructionState) -> tuple[int, int, int, int, int]:
    return tuple(state.coloring[name] for name in BOUNDARY)  # type: ignore[return-value]


def test_inference_hard_to_hard_does_not_advance_construction() -> None:
    """INFERENCE/NEGATIVE: a hard imagined successor is not construction history."""

    realized = locked_planar_c5_state()
    before_voids = void_count(realized)
    imagined = inspect(realized)

    branch = imagine_kempe(imagined, KempeMove(seed="a", other_color=1))

    assert branch.valid
    assert boundary_word(realized) == (0, 1, 0, 2, 3)
    assert realized.admissible_colors("v") == frozenset()
    assert boundary_word(branch.after.coloring) == (1, 0, 1, 2, 3)
    assert branch.after.coloring.admissible_colors("v") == frozenset()
    assert void_count(realized) == before_voids

    episode = InferenceEpisode(
        realized=realized,
        focus="v",
        imagined=(imagined, branch.after),
    )
    assert episode.realized is realized
    assert "v" not in episode.realized.coloring


def test_imagined_opening_cannot_silently_acquire_construction_authority() -> None:
    """NEGATIVE/BRIDGE: imagined slack is not admissibility on the actual map."""

    realized = persistent_double_lock_state()
    assert realized.admissible_colors("v") == frozenset()

    start = inspect(realized)
    first = imagine_kempe(start, KempeMove(seed="a", other_color=2))
    second = imagine_kempe(first.after, KempeMove(seed="c", other_color=3))

    assert second.after.coloring.admissible_colors("v") == frozenset({0})
    assert realized.admissible_colors("v") == frozenset()

    episode = InferenceEpisode(
        realized=realized,
        focus="v",
        imagined=(start, first.after, second.after),
    )

    with pytest.raises(
        ValueError,
        match="admissible state on the realized map",
    ):
        amortize(episode, 0)

    assert "v" not in realized.coloring
    assert boundary_word(realized) == (0, 1, 0, 2, 3)


def test_certified_instantiation_is_the_only_realization_payload() -> None:
    """BRIDGE: no imagined state, Kempe move, route, or predicted response crosses."""

    names = tuple(CertifiedInstantiation.__dataclass_fields__)
    assert names == ("realized", "focus", "color")
    assert set(names).isdisjoint(
        {"imagined", "move", "after", "path", "route", "response", "opening"}
    )


def test_amortize_then_instantiate_consumes_exactly_one_void() -> None:
    """BRIDGE/REALIZED/TERMINAL: imagine many, instantiate one, re-observe."""

    realized = open_wheel_state()
    assert realized.admissible_colors("v") == frozenset({3})
    assert not realized.complete

    episode = InferenceEpisode(
        realized=realized,
        focus="v",
        imagined=(inspect(realized), inspect(realized), inspect(realized)),
    )
    certificate = amortize(episode, 3)
    assert certificate.valid

    after = instantiate(certificate)

    assert void_count(after) == void_count(realized) - 1
    assert after.coloring["v"] == 3
    assert "v" not in realized.coloring
    assert dict(after.graph) == dict(realized.graph)
    for vertex, color in realized.coloring.items():
        assert after.coloring[vertex] == color

    with pytest.raises(ValueError, match="completed construction"):
        terminal_decode(realized)
    assert terminal_decode(after) == dict(after.coloring)

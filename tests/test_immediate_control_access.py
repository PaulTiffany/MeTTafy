from __future__ import annotations

from dataclasses import fields
from itertools import product

from mettafy.color_construction import ConstructionState
from mettafy.construction_control_surface import (
    ImmediateControlCertificate,
    immediate_control_access,
    state_key,
)
from mettafy.plane_parameterization import proper_cycle


BOUNDARY = ("a", "b", "c", "d", "e")


def wheel_state(boundary: tuple[int, int, int, int, int]) -> ConstructionState:
    graph = {
        "v": BOUNDARY,
        "a": ("v", "b", "e"),
        "b": ("v", "a", "c"),
        "c": ("v", "b", "d"),
        "d": ("v", "c", "e"),
        "e": ("v", "d", "a"),
    }
    return ConstructionState(graph, dict(zip(BOUNDARY, boundary)))


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


def saturated_boundaries() -> tuple[tuple[int, int, int, int, int], ...]:
    out: list[tuple[int, int, int, int, int]] = []
    for word in product(range(4), repeat=5):
        if proper_cycle(word) and len(set(word)) == 4:
            out.append((word[0], word[1], word[2], word[3], word[4]))
    return tuple(out)


def test_immediate_certificate_contains_no_future_path_coordinate() -> None:
    names = tuple(field.name for field in fields(ImmediateControlCertificate))
    assert names == ("before", "focus", "move", "after")
    assert set(names).isdisjoint({"target", "path", "route", "goal", "closure", "opening"})


def test_every_saturated_c5_has_a_current_exact_control_without_lookahead() -> None:
    boundaries = saturated_boundaries()
    assert len(boundaries) == 120

    for boundary in boundaries:
        state = wheel_state(boundary)
        assert state.admissible_colors("v") == frozenset()
        certificate = immediate_control_access(state, "v")
        assert certificate is not None
        assert certificate.valid
        assert certificate.source_requires_control
        assert certificate.state_changes
        assert dict(certificate.after.graph) == dict(state.graph)
        assert certificate.after.surface_genus == state.surface_genus == 0
        assert certificate.after.committed_edges_valid


def test_positive_focus_slack_requires_no_continuation_control() -> None:
    state = wheel_state((0, 1, 0, 1, 2))
    assert state.admissible_colors("v") == frozenset({3})
    assert immediate_control_access(state, "v") is None


def test_access_survives_the_persistent_exterior_carrier() -> None:
    state = persistent_double_lock_state()
    certificate = immediate_control_access(state, "v")
    assert certificate is not None
    assert certificate.valid
    assert state_key(certificate.after) != state_key(state)
    assert dict(certificate.after.graph) == dict(state.graph)
    assert certificate.after.committed_edges_valid


def test_next_control_is_recomputed_from_the_actual_next_state() -> None:
    state = persistent_double_lock_state()
    first = immediate_control_access(state, "v")
    assert first is not None and first.valid

    if first.after.admissible_colors("v"):
        assert immediate_control_access(first.after, "v") is None
        return

    second = immediate_control_access(first.after, "v")
    assert second is not None and second.valid
    assert second.before == first.after
    assert second.move.seed in first.after.coloring
    assert second.after.committed_edges_valid

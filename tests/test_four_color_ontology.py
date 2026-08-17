from __future__ import annotations

from dataclasses import dataclass, fields
from inspect import signature

import pytest

from mettafy.color_construction import ConstructionState, TraversalRewriteCertificate
from mettafy.four_color_ontology import (
    FOUR_COLOR_SURFACE_GENUS,
    FOUR_COLOR_SURFACE_NAME,
    assert_four_color_state_schema,
)


def test_construction_state_has_only_graph_and_coloring_coordinates() -> None:
    assert_four_color_state_schema(ConstructionState)
    assert tuple(field.name for field in fields(ConstructionState)) == ("graph", "coloring")
    assert tuple(signature(ConstructionState).parameters) == ("graph", "coloring")
    assert ConstructionState.surface_genus == FOUR_COLOR_SURFACE_GENUS == 0
    assert ConstructionState.surface_name == FOUR_COLOR_SURFACE_NAME == "sphere/plane"


def test_rewrite_certificate_has_no_open_or_closure_coordinate() -> None:
    names = {field.name.lower() for field in fields(TraversalRewriteCertificate)}
    assert names == {"before", "after", "focus"}
    assert names.isdisjoint({"open", "opened", "opening", "closed", "closure"})


def test_guard_rejects_evaluation_state_parameter() -> None:
    @dataclass(frozen=True)
    class BadState:
        graph: object
        coloring: object
        closure: bool

        surface_name = FOUR_COLOR_SURFACE_NAME
        surface_genus = FOUR_COLOR_SURFACE_GENUS

    with pytest.raises(AssertionError, match="forbidden theorem/species parameter"):
        assert_four_color_state_schema(BadState)


def test_guard_rejects_surface_topology_as_mutable_parameter() -> None:
    @dataclass(frozen=True)
    class ToroidalState:
        graph: object
        coloring: object
        surface_genus: int = 1

        surface_name = "torus"

    with pytest.raises(AssertionError, match="forbidden theorem/species parameter"):
        assert_four_color_state_schema(ToroidalState)

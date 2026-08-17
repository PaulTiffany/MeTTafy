from __future__ import annotations

from dataclasses import fields
from inspect import signature

from mettafy.color_construction import ConstructionState, TraversalRewriteCertificate
from mettafy.four_color_ontology import (
    FOUR_COLOR_SURFACE_GENUS,
    FOUR_COLOR_SURFACE_NAME,
    assert_four_color_state_schema,
)


def main() -> int:
    assert_four_color_state_schema(ConstructionState)

    state_fields = tuple(field.name for field in fields(ConstructionState))
    state_parameters = tuple(signature(ConstructionState).parameters)
    if state_fields != ("graph", "coloring"):
        raise SystemExit(f"unexpected Four Color state fields: {state_fields}")
    if state_parameters != ("graph", "coloring"):
        raise SystemExit(f"unexpected Four Color constructor parameters: {state_parameters}")

    rewrite_fields = {field.name.lower() for field in fields(TraversalRewriteCertificate)}
    forbidden = rewrite_fields & {"open", "opened", "opening", "closed", "closure"}
    if forbidden:
        raise SystemExit(
            "rewrite certificate contains forbidden evaluation coordinate(s): "
            + ", ".join(sorted(forbidden))
        )

    if ConstructionState.surface_genus != FOUR_COLOR_SURFACE_GENUS or FOUR_COLOR_SURFACE_GENUS != 0:
        raise SystemExit("Four Color species is no longer fixed to genus zero")
    if ConstructionState.surface_name != FOUR_COLOR_SURFACE_NAME:
        raise SystemExit("Four Color surface species tag drifted")

    print(
        "Four Color ontology boundary valid: state=(graph,coloring), "
        "surface species fixed at genus 0, no open/closed/closure state coordinate."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

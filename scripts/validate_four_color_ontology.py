from __future__ import annotations

from dataclasses import fields
from inspect import signature

from mettafy.active_inference_boundary import CertifiedInstantiation
from mettafy.color_construction import ConstructionState, CounterfactualTraversalWitness
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

    imagined_fields = {field.name.lower() for field in fields(CounterfactualTraversalWitness)}
    forbidden = imagined_fields & {"open", "opened", "opening", "closed", "closure"}
    if forbidden:
        raise SystemExit(
            "counterfactual witness contains forbidden evaluation coordinate(s): "
            + ", ".join(sorted(forbidden))
        )

    authority_fields = tuple(field.name for field in fields(CertifiedInstantiation))
    if authority_fields != ("realized", "focus", "color"):
        raise SystemExit(
            "CertifiedInstantiation must contain only actual map, focus, and color"
        )
    authority_forbidden = {
        "after",
        "imagined",
        "move",
        "opening",
        "path",
        "response",
        "route",
        "target",
    }
    if authority_forbidden.intersection(authority_fields):
        raise SystemExit("construction authority contains inference or future-route payload")

    if ConstructionState.surface_genus != FOUR_COLOR_SURFACE_GENUS or FOUR_COLOR_SURFACE_GENUS != 0:
        raise SystemExit("Four Color species is no longer fixed to genus zero")
    if ConstructionState.surface_name != FOUR_COLOR_SURFACE_NAME:
        raise SystemExit("Four Color surface species tag drifted")

    print(
        "Four Color ontology boundary valid: state=(graph,coloring), "
        "counterfactual traversal is inference-only, CertifiedInstantiation is the authority bridge."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

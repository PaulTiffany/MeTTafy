from __future__ import annotations

from dataclasses import fields
from inspect import getsource, signature

import mettafy.action_local_control as action_local_control
from mettafy.action_local_control import (
    ChangeDirectionAction,
    StopAction,
    realize_change_direction,
    realize_stop,
)
from mettafy.plane_parameterization import COLOR_TO_V4, NONZERO_MODES, v4_add
from mettafy.v4_action_lipschitz import (
    apply_palette_choice,
    changed_partner,
    complementary_palette_opportunity,
    edge_opportunity_modes,
    palette_choice_is_lipschitz_one,
)


def main() -> None:
    change_fields = tuple(field.name for field in fields(ChangeDirectionAction))
    stop_fields = tuple(field.name for field in fields(StopAction))

    if change_fields != ("parameter", "before_history", "stage"):
        raise SystemExit(
            "change-direction action must carry one chosen parameter and one realized stage"
        )
    if stop_fields != ("before", "focus", "color", "after"):
        raise SystemExit("stop action must carry one source and one realized successor")

    forbidden = {
        "alternatives",
        "candidates",
        "future",
        "outcomes",
        "route",
        "routes",
        "targets",
    }
    if forbidden.intersection(change_fields) or forbidden.intersection(stop_fields):
        raise SystemExit("proof-relevant action object contains counterfactual sibling state")

    if tuple(signature(realize_change_direction).parameters) != ("parameter", "history"):
        raise SystemExit("change-direction realization must consume exactly one chosen control")
    if tuple(signature(realize_stop).parameters) != ("before", "focus", "color"):
        raise SystemExit("stop realization must consume exactly one chosen focus color")

    source = getsource(action_local_control)
    forbidden_imports = ("cacophony_router", "staged_cacophony_search")
    if any(name in source for name in forbidden_imports):
        raise SystemExit("action-local proof surface may not import counterfactual routers")

    palette = set(COLOR_TO_V4)
    for mode in NONZERO_MODES:
        if not palette_choice_is_lipschitz_one(mode, 0):
            raise SystemExit("stay choice lost the exact L=1 palette bound")
        if not palette_choice_is_lipschitz_one(mode, 1):
            raise SystemExit("change-direction choice lost the exact L=1 palette bound")

        edge_opportunity = edge_opportunity_modes(mode)
        if len(edge_opportunity) != 2 or mode in edge_opportunity:
            raise SystemExit("one selected mode must leave exactly two opportunity modes")
        if v4_add(edge_opportunity[0], mode) != edge_opportunity[1]:
            raise SystemExit("opportunity modes are not exchanged by selected direction")

        for color in COLOR_TO_V4:
            partner = changed_partner(color, mode)
            if partner == color:
                raise SystemExit("nonzero direction must have one distinct palette partner")
            if apply_palette_choice(partner, mode, 1) != color:
                raise SystemExit("nonzero palette direction must remain involutive")

            opportunity = complementary_palette_opportunity(color, mode)
            if {color, partner}.intersection(opportunity):
                raise SystemExit("realized pair and opportunity pair must be disjoint")
            if {color, partner, *opportunity} != palette:
                raise SystemExit("one realized pair plus shared opportunity must exhaust Q4")
            if changed_partner(opportunity[0], mode) != opportunity[1]:
                raise SystemExit("the two other palette states must share one opportunity")

    print("Four Color action-local control boundary: PASS")


if __name__ == "__main__":
    main()

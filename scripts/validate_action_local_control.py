from __future__ import annotations

from dataclasses import fields
from inspect import getsource, signature

import mettafy.action_local_control as action_local_control
from mettafy.action_local_control import (
    CommitFocusAction,
    CounterfactualDirectionChange,
    imagine_change_direction,
    realize_focus_commit,
)
from mettafy.active_inference_boundary import CertifiedInstantiation
from mettafy.plane_parameterization import COLOR_TO_V4, NONZERO_MODES, v4_add
from mettafy.v4_action_lipschitz import (
    apply_palette_choice,
    changed_partner,
    complementary_palette_opportunity,
    edge_opportunity_modes,
    palette_choice_is_lipschitz_one,
)


def main() -> None:
    imagined_fields = tuple(field.name for field in fields(CounterfactualDirectionChange))
    commit_fields = tuple(field.name for field in fields(CommitFocusAction))
    authority_fields = tuple(field.name for field in fields(CertifiedInstantiation))

    if imagined_fields != ("parameter", "before_history", "stage"):
        raise SystemExit(
            "counterfactual direction change must carry one parameter and one imagined stage"
        )
    if authority_fields != ("realized", "focus", "color"):
        raise SystemExit(
            "construction authority must contain only actual map, focus, and certified color"
        )
    if commit_fields != ("certificate", "after"):
        raise SystemExit("realized focus commit must consume one certificate and one successor")

    forbidden = {
        "alternatives",
        "candidates",
        "future",
        "outcomes",
        "route",
        "routes",
        "targets",
    }
    if forbidden.intersection(imagined_fields) or forbidden.intersection(authority_fields):
        raise SystemExit("inference/authority object contains a stored future-route coordinate")

    if tuple(signature(imagine_change_direction).parameters) != ("parameter", "history"):
        raise SystemExit("counterfactual direction change must inspect one chosen current control")
    if tuple(signature(realize_focus_commit).parameters) != ("certificate",):
        raise SystemExit("realized focus commitment must consume CertifiedInstantiation only")

    source = getsource(action_local_control)
    forbidden_imports = ("cacophony_router", "staged_cacophony_search")
    if any(name in source for name in forbidden_imports):
        raise SystemExit("authority-facing Four Color control may not import counterfactual routers")
    if "StopAction" in source or "realize_stop" in source:
        raise SystemExit("Four Color focus admissibility may not be encoded as a stop action")

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

    print("Four Color authority boundary: PASS (imagine many, instantiate one)")


if __name__ == "__main__":
    main()

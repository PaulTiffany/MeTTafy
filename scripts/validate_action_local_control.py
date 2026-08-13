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

    print("Four Color action-local control boundary: PASS")


if __name__ == "__main__":
    main()

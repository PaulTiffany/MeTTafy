from __future__ import annotations

from dataclasses import fields, is_dataclass
from inspect import signature
from typing import Any

FOUR_COLOR_SURFACE_NAME = "sphere/plane"
FOUR_COLOR_SURFACE_GENUS = 0

# These are theorem/evaluation words, not coordinates of a Four Color state.
FORBIDDEN_STATE_PARAMETERS = frozenset(
    {
        "open",
        "opened",
        "opening",
        "closed",
        "closure",
        "genus",
        "surface",
        "surface_genus",
        "surface_name",
    }
)


def assert_four_color_state_schema(state_type: type[Any]) -> None:
    """Reject theorem/evaluation parameters from a Four Color state schema.

    The Four Color problem in this Track-B model has a fixed genus-zero carrier.
    Surface topology is therefore a species constant, not a mutable/constructor
    coordinate. Likewise, words such as open/closed/closure are downstream
    judgments and may not be smuggled into the construction state.
    """

    if not is_dataclass(state_type):
        raise TypeError("Four Color construction state must be a dataclass")

    dataclass_names = {field.name.lower() for field in fields(state_type)}
    constructor_names = {
        name.lower()
        for name in signature(state_type).parameters
        if name not in {"self", "cls"}
    }
    forbidden = (dataclass_names | constructor_names) & FORBIDDEN_STATE_PARAMETERS
    if forbidden:
        raise AssertionError(
            "Four Color state schema contains forbidden theorem/species parameter(s): "
            + ", ".join(sorted(forbidden))
        )

    if getattr(state_type, "surface_genus", None) != FOUR_COLOR_SURFACE_GENUS:
        raise AssertionError("Four Color construction species must remain genus zero")
    if getattr(state_type, "surface_name", None) != FOUR_COLOR_SURFACE_NAME:
        raise AssertionError("Four Color construction species surface tag changed")

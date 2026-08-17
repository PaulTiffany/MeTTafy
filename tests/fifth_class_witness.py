from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from mettafy.fifth_class import ChannelStabilityWindow, window_nonempty

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "four-stable-five-routes.json"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> int:
    failures: list[str] = []
    cases: list[dict[str, object]] = []

    floors = [Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(9, 10)]
    for floor in floors:
        if not window_nonempty(floor):
            failures.append(f"floor={q(floor)}: predicted separation window is empty")
            continue
        lower = (Fraction(1) - floor) / 4
        upper = (Fraction(1) - floor) / 3
        midpoint = (lower + upper) / 2
        for label, rho in (
            ("lower", lower),
            ("middle", midpoint),
            ("upper", upper),
        ):
            state = ChannelStabilityWindow(rho, floor)
            if not state.separation_equivalence:
                failures.append(
                    f"floor={q(floor)} rho={q(rho)}: interval/behavior equivalence failed"
                )
            expected = label != "upper"
            if state.four_stable_five_routes != expected:
                failures.append(
                    f"floor={q(floor)} rho={q(rho)}: expected separation={expected}"
                )
            cases.append(
                {
                    "observer_soft_floor": q(floor),
                    "rho": q(rho),
                    "position": label,
                    "window_lower": q(state.four_five_window_lower),
                    "window_upper": q(state.four_five_window_upper),
                    "M4": q(state.soft_mode(4)),
                    "M5": q(state.soft_mode(5)),
                    "four_stable": state.stable(4),
                    "five_routes": state.routes(5),
                    "separation": state.four_stable_five_routes,
                }
            )

    payload = {
        "witness": "WIT-FOUR-STABLE-FIVE-ROUTES",
        "strength": "bounded",
        "result": "pass" if not failures else "fail",
        "claim": (
            "In the symmetric Cacophony soft-mode model, for every observer floor "
            "0 < M_O < 1 there is a nonempty exact conflict interval "
            "[(1-M_O)/4, (1-M_O)/3) on which four channels remain observer-stable "
            "while a fifth channel crosses the observer routing floor."
        ),
        "non_claims": [
            "planarity forces rho into this interval",
            "every planar conflict graph is represented by one symmetric rho",
            "the Four Color Theorem follows from observer criticality",
            "NoStableFifthClass is proved without additional bridge assumptions",
            "five semantic operators are impossible in non-planar or differently coupled systems",
        ],
        "derivation": {
            "soft_mode": "M_k = 1 - rho(k - 1)",
            "four_stable": "1 - 3 rho > M_O",
            "five_routes": "1 - 4 rho <= M_O",
            "equivalent_window": "(1 - M_O)/4 <= rho < (1 - M_O)/3",
        },
        "cases": cases,
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("; ".join(failures))
    print("Four-stable/five-routes witness passed across exact boundary cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from mettafy.observer_critical import (
    ImaginationDetectorState,
    SymmetricConstraintGeometry,
    route_reason,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses" / "observer-critical-collapse.json"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def geometry(rho: Fraction) -> SymmetricConstraintGeometry:
    return SymmetricConstraintGeometry(
        k=4,
        rho=rho,
        tau=Fraction(1),
        m=Fraction(1),
        observer_budget=Fraction(4),
    )


def detector(real: Fraction, imaginary: Fraction) -> ImaginationDetectorState:
    return ImaginationDetectorState(
        real_mismatch=real,
        imaginary_residue=imaginary,
        real_tolerance=Fraction(1),
        phase_tolerance=Fraction(1),
    )


def main() -> int:
    failures: list[str] = []
    cases: list[dict[str, object]] = []

    ordinary = detector(Fraction(1, 2), Fraction(1, 2))
    imagined = detector(Fraction(1, 2), Fraction(2))
    samples = [
        ("precritical-continue", Fraction(1, 5), ordinary, "continue"),
        ("observer-floor", Fraction(1, 4), ordinary, "critical_geometry"),
        ("pre-singularity-route", Fraction(3, 10), ordinary, "critical_geometry"),
        ("latent-phase-route", Fraction(1, 5), imagined, "latent_phase"),
        ("combined-route", Fraction(3, 10), imagined, "critical_and_imaginary"),
    ]

    for case_id, rho, phase, expected_reason in samples:
        state = geometry(rho)
        reason = route_reason(state, phase)
        if not state.collapse_equivalence:
            failures.append(f"{case_id}: cost and soft-mode collapse predicates disagree")
        if reason != expected_reason:
            failures.append(
                f"{case_id}: expected route reason {expected_reason}, observed {reason}"
            )
        cases.append(
            {
                "id": case_id,
                "rho": q(state.rho),
                "critical_rho": q(state.critical_rho),
                "soft_mode": q(state.soft_mode),
                "observer_soft_floor": q(state.observer_soft_floor),
                "observer_rho": q(state.observer_rho),
                "minimum_cost_squared": q(state.minimum_cost_squared),
                "observer_budget_squared": q(
                    state.observer_budget * state.observer_budget
                ),
                "collapse_by_cost": state.collapse_by_cost,
                "collapse_by_soft_mode": state.collapse_by_soft_mode,
                "real_mismatch": q(phase.real_mismatch),
                "imaginary_residue": q(phase.imaginary_residue),
                "latent_phase_crossing": phase.latent_phase_crossing,
                "route_reason": reason,
            }
        )

    reference = geometry(Fraction(1, 5))
    if reference.observer_rho != Fraction(1, 4):
        failures.append("reference observer threshold must be rho_O = 1/4")
    if reference.critical_rho != Fraction(1, 3):
        failures.append("reference mathematical critical point must be rho_c = 1/3")
    if not reference.observer_rho < reference.critical_rho:
        failures.append("observer threshold must precede the mathematical singularity")

    payload = {
        "witness": "WIT-OBSERVER-CRITICAL",
        "strength": "bounded",
        "result": "pass" if not failures else "fail",
        "claim": (
            "Within the exact symmetric constraint model, exhausting a finite observer "
            "response budget is algebraically equivalent to crossing an observer-specific "
            "soft-mode floor; real-close/imaginary-far states are separately detected as "
            "latent phase crossings."
        ),
        "non_claims": [
            "the Four Color Theorem follows from SRMF",
            "NoStableFifthClass is proved",
            "the detector is a physical quantum measurement model",
            "Born-rule probabilities are derived",
            "the bounded sample corpus establishes empirical cognitive validity",
        ],
        "model": {
            "soft_mode": "M = 1 - rho(k - 1)",
            "minimum_cost_squared": "delta_min^2 = k tau^2 / (m^2 M)",
            "observer_soft_floor": "M_O = k tau^2 / (m^2 B_O^2)",
            "observer_threshold": "rho_O = (1 - M_O) / (k - 1)",
            "collapse_equivalence": "delta_min >= B_O iff M <= M_O",
            "imagination_event": "d_Re < epsilon_O and d_Im >= theta_O",
        },
        "reference_parameters": {
            "k": 4,
            "tau": "1/1",
            "m": "1/1",
            "observer_budget": "4/1",
            "observer_rho": q(reference.observer_rho),
            "critical_rho": q(reference.critical_rho),
        },
        "cases": cases,
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("; ".join(failures))
    print(
        "Observer-critical witness passed: exact budget/soft-mode equivalence, "
        "precritical threshold, and latent-phase detector cases verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

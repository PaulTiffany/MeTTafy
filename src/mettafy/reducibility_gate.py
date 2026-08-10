from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BlindDischargeEvidence:
    """Source-neutral evidence for a counterexample-discharge proof skeleton."""

    induction_descent: bool
    decision_branch: bool
    contradiction_elimination: bool
    proof_application: bool

    @property
    def complete(self) -> bool:
        return all(
            (
                self.induction_descent,
                self.decision_branch,
                self.contradiction_elimination,
                self.proof_application,
            )
        )

    def to_dict(self) -> dict[str, bool]:
        return {
            "induction_descent": self.induction_descent,
            "decision_branch": self.decision_branch,
            "contradiction_elimination": self.contradiction_elimination,
            "proof_application": self.proof_application,
            "complete": self.complete,
        }


@dataclass(frozen=True)
class TraversalCertificate:
    """Independent certificate for an admissible reduction traversal.

    The gate requires both an unchanged observable boundary and a strict decrease
    in a non-negative well-founded measure. The certificate does not establish
    that a particular Four Color configuration has these properties; a producer
    for the deeper reducibility layer must supply that evidence separately.
    """

    boundary_before_sha256: str
    boundary_after_sha256: str
    measure_before: int
    measure_after: int

    @classmethod
    def from_boundaries(
        cls,
        *,
        boundary_before: str,
        boundary_after: str,
        measure_before: int,
        measure_after: int,
    ) -> "TraversalCertificate":
        return cls(
            boundary_before_sha256=_sha256(boundary_before),
            boundary_after_sha256=_sha256(boundary_after),
            measure_before=measure_before,
            measure_after=measure_after,
        )

    @property
    def boundary_preserved(self) -> bool:
        return self.boundary_before_sha256 == self.boundary_after_sha256

    @property
    def strictly_decreases(self) -> bool:
        return (
            self.measure_before >= 0
            and self.measure_after >= 0
            and self.measure_after < self.measure_before
        )

    @property
    def valid(self) -> bool:
        return self.boundary_preserved and self.strictly_decreases

    def to_dict(self) -> dict[str, object]:
        return {
            "boundary_before_sha256": self.boundary_before_sha256,
            "boundary_after_sha256": self.boundary_after_sha256,
            "boundary_preserved": self.boundary_preserved,
            "measure_before": self.measure_before,
            "measure_after": self.measure_after,
            "strictly_decreases": self.strictly_decreases,
            "valid": self.valid,
        }


GateDecision = Literal[
    "not_candidate",
    "skeleton_incomplete",
    "certificate_required",
    "certificate_rejected",
    "admissible_traversal",
]


@dataclass(frozen=True)
class ReducibilityGateTrace:
    reduction_predicted: bool
    discharge_evidence: BlindDischargeEvidence
    certificate_present: bool
    certificate_valid: bool | None
    decision: GateDecision
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "reduction_predicted": self.reduction_predicted,
            "discharge_evidence": self.discharge_evidence.to_dict(),
            "certificate_present": self.certificate_present,
            "certificate_valid": self.certificate_valid,
            "decision": self.decision,
            "reason": self.reason,
        }


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_blind_discharge_evidence(source: str) -> BlindDischargeEvidence:
    """Project a Rocq proof surface into four bounded source-neutral booleans.

    The extractor intentionally does not emit theorem names, referenced identifiers,
    source paths, or semantic labels. It recognizes only a narrow syntax surface used
    by the pinned high-level Four Color fixture.
    """
    induction_descent = bool(re.search(r"\belim\s*:", source, re.IGNORECASE))
    decision_branch = bool(
        re.search(
            r"\bhave\b[^\n:=]*\[[^\]]*\|[^\]]*\]\s*:=\s*decide_",
            source,
            re.IGNORECASE,
        )
    )
    contradiction_elimination = bool(
        re.search(r"\b(?:by\s+)?have\s*\[\s*\]\s*:=", source, re.IGNORECASE)
    )
    proof_application = bool(
        re.search(r"\b(?:exact|apply\s*:|apply|have)\b", source, re.IGNORECASE)
    )
    return BlindDischargeEvidence(
        induction_descent=induction_descent,
        decision_branch=decision_branch,
        contradiction_elimination=contradiction_elimination,
        proof_application=proof_application,
    )


def assess_admissible_traversal(
    *,
    reduction_predicted: bool,
    discharge_evidence: BlindDischargeEvidence,
    certificate: TraversalCertificate | None = None,
) -> ReducibilityGateTrace:
    """Fail closed unless all independent reducibility obligations are present."""
    if not reduction_predicted:
        return ReducibilityGateTrace(
            reduction_predicted=False,
            discharge_evidence=discharge_evidence,
            certificate_present=certificate is not None,
            certificate_valid=certificate.valid if certificate is not None else None,
            decision="not_candidate",
            reason="no independently recognized Reduction candidate is present",
        )
    if not discharge_evidence.complete:
        return ReducibilityGateTrace(
            reduction_predicted=True,
            discharge_evidence=discharge_evidence,
            certificate_present=certificate is not None,
            certificate_valid=certificate.valid if certificate is not None else None,
            decision="skeleton_incomplete",
            reason="the bounded contradiction/discharge skeleton is incomplete",
        )
    if certificate is None:
        return ReducibilityGateTrace(
            reduction_predicted=True,
            discharge_evidence=discharge_evidence,
            certificate_present=False,
            certificate_valid=None,
            decision="certificate_required",
            reason=(
                "a traversal certificate proving boundary preservation and strict "
                "well-founded decrease is required before promotion"
            ),
        )
    if not certificate.valid:
        return ReducibilityGateTrace(
            reduction_predicted=True,
            discharge_evidence=discharge_evidence,
            certificate_present=True,
            certificate_valid=False,
            decision="certificate_rejected",
            reason="the supplied traversal certificate failed an admissibility obligation",
        )
    return ReducibilityGateTrace(
        reduction_predicted=True,
        discharge_evidence=discharge_evidence,
        certificate_present=True,
        certificate_valid=True,
        decision="admissible_traversal",
        reason=(
            "Reduction prediction, contradiction/discharge evidence, boundary preservation, "
            "and strict well-founded decrease are all mechanically certified"
        ),
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from mettafy.proof_surface import ProofSurface, four_color_ordered_surface

FindingStatus = Literal["supported", "falsified"]
CandidateStatus = Literal["planned", "mechanically-passed"]


@dataclass(frozen=True)
class ClaimFinding:
    """A result attached to one frozen hypothesis without rewriting it."""

    id: str
    hypothesis: str
    claim: str
    status: FindingStatus
    artifact: str
    note: str


@dataclass(frozen=True)
class SuccessorCandidate:
    """A proposed repair descended from a frozen hypothesis."""

    id: str
    parent_hypothesis: str
    target_claim: str
    artifact: str
    status: CandidateStatus


@dataclass(frozen=True)
class ProofGenealogy:
    name: str
    surface: ProofSurface
    frozen_hypothesis: str
    findings: tuple[ClaimFinding, ...]
    successors: tuple[SuccessorCandidate, ...]

    def reference_errors(self) -> tuple[str, ...]:
        errors: list[str] = []
        claim_ids = self.surface.claim_ids
        finding_ids: set[str] = set()
        successor_ids: set[str] = set()

        for finding in self.findings:
            if finding.id in finding_ids:
                errors.append(f"duplicate finding id: {finding.id}")
            finding_ids.add(finding.id)
            if finding.hypothesis != self.frozen_hypothesis:
                errors.append(f"finding is not attached to frozen hypothesis: {finding.id}")
            if finding.claim not in claim_ids:
                errors.append(f"unknown finding claim: {finding.id}->{finding.claim}")

        for successor in self.successors:
            if successor.id in successor_ids:
                errors.append(f"duplicate successor id: {successor.id}")
            successor_ids.add(successor.id)
            if successor.parent_hypothesis != self.frozen_hypothesis:
                errors.append(f"successor has unknown parent: {successor.id}")
            if successor.target_claim not in claim_ids:
                errors.append(f"unknown successor target: {successor.id}->{successor.target_claim}")

        return tuple(sorted(errors))

    def assert_structurally_sound(self) -> None:
        errors = self.reference_errors()
        if errors:
            raise AssertionError("; ".join(errors))

    def findings_with_status(
        self,
        status: FindingStatus,
        *,
        hypothesis: str | None = None,
    ) -> tuple[ClaimFinding, ...]:
        selected = (
            finding
            for finding in self.findings
            if finding.status == status
            and (hypothesis is None or finding.hypothesis == hypothesis)
        )
        return tuple(sorted(selected, key=lambda finding: finding.id))

    def falsified_claims(self, hypothesis: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                finding.claim
                for finding in self.findings_with_status("falsified", hypothesis=hypothesis)
            )
        )

    def supported_claims(self, hypothesis: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                finding.claim
                for finding in self.findings_with_status("supported", hypothesis=hypothesis)
            )
        )

    def unresolved_claims(self) -> tuple[str, ...]:
        """Keep falsified claims open even when a successor candidate is green."""

        mechanically_open = set(self.surface.unwitnessed_claims())
        supported = set(self.supported_claims(self.frozen_hypothesis))
        return tuple(sorted(mechanically_open - supported))

    def successor_candidates(self, claim: str) -> tuple[SuccessorCandidate, ...]:
        if claim not in self.surface.claim_ids:
            raise ValueError(f"unknown claim: {claim}")
        return tuple(
            sorted(
                (item for item in self.successors if item.target_claim == claim),
                key=lambda item: item.id,
            )
        )

    def to_metta(self) -> str:
        lines = [
            "; Four Color proof genealogy",
            f"(ProofGenealogy {self.name})",
            f"(Hypothesis {self.frozen_hypothesis} Frozen)",
        ]
        for finding in self.findings:
            status = "Supported" if finding.status == "supported" else "Falsified"
            lines.append(
                f"(Finding {finding.id} {finding.hypothesis} {finding.claim} {status})"
            )
        for successor in self.successors:
            status = (
                "MechanicallyPassed"
                if successor.status == "mechanically-passed"
                else "Planned"
            )
            lines.append(
                f"(SuccessorCandidate {successor.id} {successor.parent_hypothesis} "
                f"{successor.target_claim} {status})"
            )
        return "\n".join(lines) + "\n"


def four_color_proof_genealogy() -> ProofGenealogy:
    surface = four_color_ordered_surface()
    return ProofGenealogy(
        name="FourColorOrderedGenealogyV1",
        surface=surface,
        frozen_hypothesis="H0",
        findings=(
            ClaimFinding(
                id="F-C0-Degree4MissingColor",
                hypothesis="H0",
                claim="C0",
                status="falsified",
                artifact=(
                    "tests/test_ground_reduction.py::"
                    "test_c0_degree_four_all_colors_refutes_immediate_missing_color_step"
                ),
                note=(
                    "Four degree-four neighbors may use all four Q4 colors, so the frozen "
                    "immediate missing-color restoration sentence is false as written."
                ),
            ),
            ClaimFinding(
                id="F-C1-ExhaustiveNormalForm",
                hypothesis="H0",
                claim="C1",
                status="supported",
                artifact=(
                    "tests/test_ground_reduction.py::"
                    "test_c1_all_proper_saturated_q4_five_cycles_have_one_normal_form"
                ),
                note=(
                    "All 1024 labeled Q4 five-cycle assignments are enumerated; the 120 "
                    "proper saturated cases collapse to the A-B-A-C-D orbit."
                ),
            ),
        ),
        successors=(
            SuccessorCandidate(
                id="H1-C0-Degree4Kempe",
                parent_hypothesis="H0",
                target_claim="C0",
                artifact="docs/four-color-ground-repair-candidate.md",
                status="mechanically-passed",
            ),
        ),
    )

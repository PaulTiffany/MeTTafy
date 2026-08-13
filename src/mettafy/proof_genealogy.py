from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FindingStatus = Literal["supported", "falsified"]
CandidateStatus = Literal["planned", "mechanically-passed"]


@dataclass(frozen=True)
class ClaimFinding:
    id: str
    hypothesis: str
    claim: str
    status: FindingStatus
    artifact: str
    note: str


@dataclass(frozen=True)
class SuccessorCandidate:
    id: str
    parent_hypothesis: str
    target_claim: str
    artifact: str
    status: CandidateStatus

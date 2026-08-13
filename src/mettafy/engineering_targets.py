from __future__ import annotations

from dataclasses import dataclass

SemanticConcept = str

_SEMANTIC_ALIASES: dict[SemanticConcept, tuple[str, ...]] = {
    "replay": ("replay", "echo", "same input", "compile twice", "rerun", "re-observe", "reversible"),
    "novelty": ("fresh", "new knowledge", "derived", "new resolved", "novel"),
    "identity": ("canonical", "normalize", "normalized", "hash", "sha-256", "content-addressed", "same semantic result", "identity"),
    "persistence": ("retain", "retained", "frozen", "immutable", "ledger", "stored", "history"),
    "finite-order": ("finite", "ordered", "sequence", "in order", "first failure", "failed index", "traversal"),
    "closure": ("termination", "terminate", "success", "complete", "validation", "unresolved", "exhaust", "stops"),
    "temporal-locality": ("present state", "current state", "compile-time state", "future route", "future information", "later verification", "before the notebook"),
    "provenance": ("provenance", "audit", "certificate", "source sha", "source_sha", "commit", "trace"),
    "growth": ("grow", "growth", "enlarge", "enlargement", "strictly larger", "new carrier", "new vertices"),
    "projection": ("projection", "manifest", "render", "translate"),
}


def semantic_signature(text: str) -> frozenset[SemanticConcept]:
    """Map free engineering/math prose onto a small shared behavioral vocabulary."""

    lowered = " ".join(text.lower().replace("_", " ").split())
    return frozenset(
        concept
        for concept, aliases in _SEMANTIC_ALIASES.items()
        if any(alias in lowered for alias in aliases)
    )


@dataclass(frozen=True)
class EngineeringNeed:
    id: str
    claim: str
    description: str

    @property
    def concepts(self) -> frozenset[SemanticConcept]:
        return semantic_signature(self.description)


@dataclass(frozen=True)
class EngineeringExemplar:
    id: str
    repository: str
    commit: str
    artifact: str
    behavior: str

    @property
    def concepts(self) -> frozenset[SemanticConcept]:
        return semantic_signature(self.behavior)


@dataclass(frozen=True)
class EngineeringMatch:
    need: str
    exemplar: str
    concepts: frozenset[SemanticConcept]
    score: float


@dataclass(frozen=True)
class EngineeringIndex:
    needs: tuple[EngineeringNeed, ...]
    exemplars: tuple[EngineeringExemplar, ...]

    def need(self, need_id: str) -> EngineeringNeed:
        for need in self.needs:
            if need.id == need_id:
                return need
        raise ValueError(f"unknown engineering need: {need_id}")

    def rank(self, need_id: str, *, min_score: float = 0.25) -> tuple[EngineeringMatch, ...]:
        """Rank old implementations by shared canonical behavior, not shared nouns."""

        need = self.need(need_id)
        if not need.concepts:
            raise ValueError(f"engineering need has no semantic signature: {need_id}")

        matches: list[EngineeringMatch] = []
        for exemplar in self.exemplars:
            shared = need.concepts & exemplar.concepts
            score = len(shared) / len(need.concepts)
            if score >= min_score:
                matches.append(
                    EngineeringMatch(
                        need=need.id,
                        exemplar=exemplar.id,
                        concepts=frozenset(shared),
                        score=score,
                    )
                )
        return tuple(sorted(matches, key=lambda match: (-match.score, match.exemplar)))

    def all_matches(self, *, min_score: float = 0.25) -> tuple[EngineeringMatch, ...]:
        matches = [
            match
            for need in self.needs
            for match in self.rank(need.id, min_score=min_score)
        ]
        return tuple(sorted(matches, key=lambda match: (match.need, -match.score, match.exemplar)))

    def concept_voids(self) -> dict[str, tuple[SemanticConcept, ...]]:
        """Report mathematical behavior concepts with no retrieved implementation candidate."""

        available = frozenset().union(*(exemplar.concepts for exemplar in self.exemplars))
        return {
            need.id: tuple(sorted(need.concepts - available))
            for need in self.needs
            if need.concepts - available
        }

    def provenance_errors(self) -> tuple[str, ...]:
        errors: list[str] = []
        for exemplar in self.exemplars:
            if len(exemplar.commit) != 40:
                errors.append(f"unpinned exemplar commit: {exemplar.id}")
            if not exemplar.repository.startswith("PaulTiffany/"):
                errors.append(f"unexpected exemplar repository: {exemplar.id}")
            if not exemplar.artifact.endswith(".py"):
                errors.append(f"engineering exemplar is not flat Python: {exemplar.id}")
        return tuple(sorted(errors))

    def to_metta(self) -> str:
        """Project the deterministic retrieval index into MeTTa relations."""

        lines = [
            "; Four Color engineering-target search",
            "; Flat Python exemplars are reuse candidates, not theorem witnesses.",
            "; Generated from mettafy.engineering_targets.four_color_engineering_index().",
            "",
        ]
        for need in self.needs:
            lines.append(f"(EngineeringNeed {need.id} {need.claim})")
            for concept in sorted(need.concepts):
                lines.append(f"(NeedConcept {need.id} {concept})")

        lines.extend(["", "; --- pinned flat-Python exemplars ---"])
        for exemplar in self.exemplars:
            lines.append(f"(EngineeringExemplar {exemplar.id})")
            lines.append(f"; {exemplar.id} repository: {exemplar.repository}")
            lines.append(f"; {exemplar.id} commit: {exemplar.commit}")
            lines.append(f"; {exemplar.id} artifact: {exemplar.artifact}")
            lines.append(f"; {exemplar.id} behavior: {exemplar.behavior}")
            for concept in sorted(exemplar.concepts):
                lines.append(f"(ExemplarConcept {exemplar.id} {concept})")

        lines.extend(["", "; --- fuzzy behavioral matches ---"])
        for match in self.all_matches():
            lines.append(f"(EngineeringMatch {match.need} {match.exemplar} {match.score:.3f})")
            for concept in sorted(match.concepts):
                lines.append(f"(MatchConcept {match.need} {match.exemplar} {concept})")

        lines.extend(
            [
                "",
                "; Deliberately absent: (Covers ...) and (Witness ...).",
                "; Retrieval proposes an implementation target; adaptation plus a mechanical test",
                "; is required before the proof surface may claim witness coverage.",
                "",
            ]
        )
        return "\n".join(lines)


def four_color_engineering_index() -> EngineeringIndex:
    needs = (
        EngineeringNeed(
            "N-C5-PresentStateOnly",
            "C5",
            "Present state continuation must use current state only; do not store a future route "
            "or future information before the next realized state exists.",
        ),
        EngineeringNeed(
            "N-C6-FreshShapeProgress",
            "C6",
            "Replay or reversible relabeling of an already resolved component must not count as "
            "fresh progress; retained structural identity must survive irrelevant representation "
            "changes, while structural enlargement or a genuinely new resolved shape may count.",
        ),
        EngineeringNeed(
            "N-C7-FiniteClosure",
            "C7",
            "A finite ordered construction cannot terminate successfully while an unresolved "
            "continuation remains; closure occurs only after the ordered obligations are exhausted.",
        ),
    )
    exemplars = (
        EngineeringExemplar(
            "X-COME-DerivedOnly",
            "PaulTiffany/Come",
            "c3c09334c70fb1ee812e004c35fe2deb0ef51883",
            "come/adapters.py",
            "The adapter filters Input echoes and Selected scheduling; only Derived lines count as "
            "new knowledge. An echo of an existing statement is activity but not novelty.",
        ),
        EngineeringExemplar(
            "X-NB-DeterminismIdentity",
            "PaulTiffany/notebook_compiler",
            "67fe52d3820fff3b2d75c974137c68efdaaffb0c",
            "scripts/check_determinism.py",
            "Compile the same input twice in separate directories, normalize volatile representation "
            "fields, hash the normalized artifacts, and require identical semantic results.",
        ),
        EngineeringExemplar(
            "X-NB-FrozenArtifactGraph",
            "PaulTiffany/notebook_compiler",
            "67fe52d3820fff3b2d75c974137c68efdaaffb0c",
            "src/notebook_compiler/artifacts.py",
            "Frozen immutable typed artifact objects retain source SHA-256 identity, execution trace, "
            "certificate, manifest projection, and audit provenance across later renderings.",
        ),
        EngineeringExemplar(
            "X-NB-ControlBoardTemporalLocality",
            "PaulTiffany/notebook_compiler",
            "67fe52d3820fff3b2d75c974137c68efdaaffb0c",
            "src/notebook_compiler/control_board.py",
            "The control board contains only compile-time state before the notebook is written; "
            "later verification results live in a sibling certificate rather than future information "
            "being stored in the present state.",
        ),
        EngineeringExemplar(
            "X-NB-OrderedVerifier",
            "PaulTiffany/notebook_compiler",
            "67fe52d3820fff3b2d75c974137c68efdaaffb0c",
            "src/notebook_compiler/verifier.py",
            "Traverse a finite ordered sequence of cells in order, stop at the first failure, retain "
            "the failed index, and declare success only when execution completes with validation and "
            "no unresolved failure remains.",
        ),
    )
    return EngineeringIndex(needs=needs, exemplars=exemplars)

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ClaimLayer = Literal["Ground", "Frontier", "Flow", "Closure"]
WitnessStatus = Literal["planned", "local-passed", "ci-passed"]
MutationStatus = Literal["planned", "implemented"]


@dataclass(frozen=True)
class SurfaceClaim:
    id: str
    label: str
    layer: ClaimLayer
    artifact: str


@dataclass(frozen=True)
class SurfaceDependency:
    claim: str
    requires: str


@dataclass(frozen=True)
class EvidenceFiber:
    id: str
    claim: str
    kind: str
    artifact: str


@dataclass(frozen=True)
class MechanicalWitness:
    id: str
    covers: frozenset[str]
    artifact: str
    status: WitnessStatus


@dataclass(frozen=True)
class DestructiveMutation:
    id: str
    target: str
    description: str
    expected: str
    status: MutationStatus = "planned"
    artifact: str | None = None


@dataclass(frozen=True)
class ProofSurface:
    name: str
    frozen_proof: str
    frozen_commit: str
    claims: tuple[SurfaceClaim, ...]
    dependencies: tuple[SurfaceDependency, ...]
    evidence: tuple[EvidenceFiber, ...]
    witnesses: tuple[MechanicalWitness, ...]
    mutations: tuple[DestructiveMutation, ...]

    @property
    def claim_ids(self) -> frozenset[str]:
        return frozenset(claim.id for claim in self.claims)

    def reference_errors(self) -> tuple[str, ...]:
        ids = self.claim_ids
        errors: list[str] = []
        for dependency in self.dependencies:
            if dependency.claim not in ids:
                errors.append(f"unknown dependency conclusion: {dependency.claim}")
            if dependency.requires not in ids:
                errors.append(f"unknown dependency premise: {dependency.requires}")
        for fiber in self.evidence:
            if fiber.claim not in ids:
                errors.append(f"unknown evidence claim: {fiber.claim}")
        for witness in self.witnesses:
            for covered_claim in witness.covers:
                if covered_claim not in ids:
                    errors.append(f"unknown witness claim: {witness.id}->{covered_claim}")
        for mutation in self.mutations:
            if mutation.target not in ids:
                errors.append(f"unknown mutation target: {mutation.id}->{mutation.target}")
        return tuple(sorted(errors))

    def mutation_errors(self) -> tuple[str, ...]:
        errors = [
            f"implemented mutation has no evidence artifact: {mutation.id}"
            for mutation in self.mutations
            if mutation.status == "implemented" and not mutation.artifact
        ]
        return tuple(sorted(errors))

    def dependency_cycles(self) -> tuple[str, ...]:
        requires: dict[str, set[str]] = {claim.id: set() for claim in self.claims}
        for dependency in self.dependencies:
            if dependency.claim in requires and dependency.requires in requires:
                requires[dependency.claim].add(dependency.requires)

        visiting: set[str] = set()
        visited: set[str] = set()
        cycles: set[str] = set()

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in visiting:
                cycles.add(node)
                return
            visiting.add(node)
            for premise in requires[node]:
                visit(premise)
            visiting.remove(node)
            visited.add(node)

        for claim_id in sorted(requires):
            visit(claim_id)
        return tuple(sorted(cycles))

    def bare_claims(self) -> tuple[str, ...]:
        supported = {fiber.claim for fiber in self.evidence}
        return tuple(sorted(self.claim_ids - supported))

    def unwitnessed_claims(self) -> tuple[str, ...]:
        covered: set[str] = set()
        for witness in self.witnesses:
            if witness.status != "planned":
                covered.update(witness.covers)
        return tuple(sorted(self.claim_ids - covered))

    def unmutated_claims(self) -> tuple[str, ...]:
        targeted = {mutation.target for mutation in self.mutations}
        return tuple(sorted(self.claim_ids - targeted))

    def unexecuted_mutations(self) -> tuple[str, ...]:
        return tuple(
            sorted(mutation.id for mutation in self.mutations if mutation.status != "implemented")
        )

    def ancestors(self, target: str) -> frozenset[str]:
        if target not in self.claim_ids:
            raise ValueError(f"unknown claim: {target}")
        reverse: dict[str, set[str]] = {claim.id: set() for claim in self.claims}
        for dependency in self.dependencies:
            if dependency.claim in reverse and dependency.requires in reverse:
                reverse[dependency.claim].add(dependency.requires)

        seen: set[str] = set()
        frontier = list(reverse[target])
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(reverse[current])
        return frozenset(seen)

    def assert_structurally_sound(self) -> None:
        errors = self.reference_errors() + self.mutation_errors()
        if errors:
            raise AssertionError("; ".join(errors))
        cycles = self.dependency_cycles()
        if cycles:
            raise AssertionError(f"proof surface dependency cycle: {', '.join(cycles)}")
        bare = self.bare_claims()
        if bare:
            raise AssertionError(f"bare proof claims: {', '.join(bare)}")

    def voids(self) -> dict[str, tuple[str, ...]]:
        """Return the current falsification queue without converting gaps into verdicts."""

        return {
            "bare_claims": self.bare_claims(),
            "unwitnessed_claims": self.unwitnessed_claims(),
            "unmutated_claims": self.unmutated_claims(),
            "unexecuted_mutations": self.unexecuted_mutations(),
        }

    def to_metta(self) -> str:
        lines = [
            "; Four Color ordered-construction proof surface",
            "; Generated from mettafy.proof_surface.four_color_ordered_surface().",
            "; Mechanical witnesses are falsifiers; they are not theorem premises.",
            "",
            f"(ProofSurface {self.name})",
            f"(FrozenProof {self.name} sha-{self.frozen_commit})",
            f"; frozen proof artifact: {self.frozen_proof}",
            "",
            "; --- typed claims ---",
        ]
        for surface_claim in self.claims:
            lines.append(
                f"(Claim {surface_claim.id} {surface_claim.label} {surface_claim.layer})"
            )
            lines.append(f"; {surface_claim.id} artifact: {surface_claim.artifact}")

        lines.extend(["", "; --- dependency surface ---"])
        for dependency in self.dependencies:
            lines.append(f"(DependsOn {dependency.claim} {dependency.requires})")

        lines.extend(["", "; --- evidence fibers ---"])
        for fiber in self.evidence:
            lines.append(f"(EvidenceFiber {fiber.id} {fiber.claim} {fiber.kind})")
            lines.append(f"; {fiber.id} artifact: {fiber.artifact}")

        lines.extend(["", "; --- mechanical witnesses ---"])
        for witness in self.witnesses:
            lines.append(f"(Witness {witness.id} {witness.status})")
            lines.append(f"; {witness.id} artifact: {witness.artifact}")
            for covered_claim in sorted(witness.covers):
                lines.append(f"(Covers {witness.id} {covered_claim})")

        lines.extend(["", "; --- destructive mutation program ---"])
        for mutation in self.mutations:
            lines.append(
                f"(Mutation {mutation.id} {mutation.target} {mutation.expected} {mutation.status})"
            )
            lines.append(f"; {mutation.id}: {mutation.description}")
            if mutation.artifact:
                lines.append(f"; {mutation.id} artifact: {mutation.artifact}")

        lines.extend(
            [
                "",
                "; Intended surface queries:",
                "; !(match &self (EvidenceFiber $e $claim $kind) ($claim $e $kind))",
                "; !(match &self (Covers $w $claim) ($claim $w))",
                "; !(match &self (Mutation $m $claim $expected $status) ($claim $m $status))",
                "",
            ]
        )
        return "\n".join(lines)


def four_color_ordered_surface() -> ProofSurface:
    claims = (
        SurfaceClaim(
            "C0",
            "MinimalCounterexampleReduction",
            "Ground",
            "docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction",
        ),
        SurfaceClaim(
            "C1",
            "SaturatedBoundaryNormalForm",
            "Ground",
            "docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction",
        ),
        SurfaceClaim(
            "C2",
            "CleanFrontierTurnExistence",
            "Frontier",
            "docs/four-color-clean-turn-lemma.md",
        ),
        SurfaceClaim(
            "C3",
            "SingletonCleanTurnFinishes",
            "Flow",
            "docs/four-color-ordered-construction-proof.md#4-singleton-turns-finish",
        ),
        SurfaceClaim(
            "C4",
            "RepeatedTurnPairLemma",
            "Frontier",
            "docs/four-color-clean-turn-dynamics.md",
        ),
        SurfaceClaim(
            "C5",
            "PresentStateNoninverseContinuation",
            "Flow",
            "docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation",
        ),
        SurfaceClaim(
            "C6",
            "OrderedShapeProgress",
            "Frontier",
            "docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation",
        ),
        SurfaceClaim(
            "C7",
            "FiniteConstructionClosure",
            "Closure",
            "docs/four-color-ordered-construction-proof.md#7-closure",
        ),
        SurfaceClaim(
            "C8",
            "DegreeFiveExtension",
            "Closure",
            "docs/four-color-ordered-construction-proof.md#7-closure",
        ),
    )
    dependencies = (
        SurfaceDependency("C1", "C0"),
        SurfaceDependency("C2", "C1"),
        SurfaceDependency("C3", "C2"),
        SurfaceDependency("C4", "C1"),
        SurfaceDependency("C4", "C2"),
        SurfaceDependency("C5", "C4"),
        SurfaceDependency("C6", "C5"),
        SurfaceDependency("C7", "C2"),
        SurfaceDependency("C7", "C4"),
        SurfaceDependency("C7", "C5"),
        SurfaceDependency("C7", "C6"),
        SurfaceDependency("C8", "C0"),
        SurfaceDependency("C8", "C3"),
        SurfaceDependency("C8", "C7"),
    )
    evidence = tuple(
        EvidenceFiber(
            f"E{index}",
            claim.id,
            "Mathematical",
            claim.artifact,
        )
        for index, claim in enumerate(claims)
    )
    witnesses = (
        MechanicalWitness(
            "W-SequentialFrontier",
            frozenset({"C2", "C3", "C4", "C5"}),
            "tests/test_sequential_frontier.py",
            "ci-passed",
        ),
        MechanicalWitness(
            "W-FlipFamily4620",
            frozenset({"C2", "C3", "C4", "C5", "C7", "C8"}),
            "tests/test_ordered_construction_closure.py",
            "ci-passed",
        ),
        MechanicalWitness(
            "W-GeneratedDisks5000",
            frozenset({"C2", "C4", "C5", "C7"}),
            "docs/four-color-proof-status.md#5-mechanical-red-team",
            "local-passed",
        ),
    )
    mutations = (
        DestructiveMutation(
            "M0-DropMinimality",
            "C0",
            "Remove the smaller-counterexample induction premise and require the reduction to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M1-BreakBoundaryNormalForm",
            "C1",
            "Feed a nonproper or nonsaturated five-cycle and require normal-form certification to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M2-AllowPlanarCrossing",
            "C2",
            "Permit complementary bichromatic paths to cross without incidence and require the clean-turn lemma witness to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M3-DirtyFrontierTurn",
            "C3",
            "Allow a purported clean component to hit two frontier vertices and require turn certification to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M4-BreakRepeatedPair",
            "C4",
            "Force one repeated occurrence into the complementary locked component and require pair certification to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M5-StoreFutureRoute",
            "C5",
            "Inject future-route information into present-state continuation and require ontology/flow certification to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M6-ReplayResolvedShape",
            "C6",
            "Count an exact inverse replay of an already resolved physical component as fresh construction progress and require progress certification to fail.",
            "ExpectedFailure",
            status="implemented",
            artifact="tests/test_ordered_shape_progress.py::test_m6_exact_inverse_replay_is_not_fresh_progress",
        ),
        DestructiveMutation(
            "M7-AllowSaturatedExhaustion",
            "C7",
            "Declare termination at a saturated frontier while a clean unresolved continuation remains and require closure certification to fail.",
            "ExpectedFailure",
        ),
        DestructiveMutation(
            "M8-CorruptRestoredEdge",
            "C8",
            "Restore the degree-five focus with a color present in its neighborhood and require the edge ledger to reject the extension.",
            "ExpectedFailure",
        ),
    )
    return ProofSurface(
        name="FourColorOrderedV1",
        frozen_proof="docs/four-color-ordered-construction-proof.md",
        frozen_commit="7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b",
        claims=claims,
        dependencies=dependencies,
        evidence=evidence,
        witnesses=witnesses,
        mutations=mutations,
    )

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TypeAlias

from mettafy.dual_path_switching import disk_primal_edges
from mettafy.plane_dual_control import (
    DegreeFiveTriangulatedEmbedding,
    Edge,
    canonical_edge,
)
from mettafy.plane_parameterization import NONZERO_MODES, V4, color_difference
from mettafy.trivalent_dual_splice import DualNode, trivalent_dual_splice_signature

DualRelationPair: TypeAlias = tuple[DualNode, DualNode]


def _canonical_dual_arc(left: DualNode, right: DualNode) -> tuple[DualNode, DualNode]:
    if left == right:
        raise ValueError("dual involution arc cannot be a fixed point")
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True, order=True)
class InvolutionArc:
    """One physical dual arc carrying a single V4 matching mode."""

    left: DualNode
    right: DualNode
    primal_edge: Edge

    def __post_init__(self) -> None:
        left, right = _canonical_dual_arc(self.left, self.right)
        object.__setattr__(self, "left", left)
        object.__setattr__(self, "right", right)
        object.__setattr__(
            self,
            "primal_edge",
            canonical_edge(self.primal_edge[0], self.primal_edge[1]),
        )


@dataclass(frozen=True)
class ModePartialInvolution:
    """One V4 matching viewed as a fixed-point-free partial involution."""

    mode: V4
    arcs: tuple[InvolutionArc, ...]

    @property
    def domain(self) -> frozenset[DualNode]:
        return frozenset(
            node
            for arc in self.arcs
            for node in (arc.left, arc.right)
        )

    @property
    def primal_edges(self) -> frozenset[Edge]:
        return frozenset(arc.primal_edge for arc in self.arcs)

    def partner(self, node: DualNode) -> DualNode | None:
        for arc in self.arcs:
            if arc.left == node:
                return arc.right
            if arc.right == node:
                return arc.left
        return None

    @property
    def relation(self) -> frozenset[DualRelationPair]:
        return frozenset(
            (left, right)
            for arc in self.arcs
            for left, right in ((arc.left, arc.right), (arc.right, arc.left))
        )

    @property
    def valid(self) -> bool:
        if self.mode not in NONZERO_MODES or not self.arcs:
            return False
        nodes = tuple(
            node
            for arc in self.arcs
            for node in (arc.left, arc.right)
        )
        return (
            len(nodes) == len(set(nodes))
            and len(self.primal_edges) == len(self.arcs)
            and all(arc.left != arc.right for arc in self.arcs)
            and self.relation
            == frozenset((right, left) for left, right in self.relation)
        )


@dataclass(frozen=True, order=True)
class OrderedProductStep:
    """One defined two-step action i_left(i_right(source))."""

    source: DualNode
    middle: DualNode
    target: DualNode


@dataclass(frozen=True)
class OrderedInvolutionProduct:
    """Partial bijection obtained by composing two distinct mode involutions."""

    left_mode: V4
    right_mode: V4
    steps: tuple[OrderedProductStep, ...]

    @property
    def relation(self) -> tuple[DualRelationPair, ...]:
        return tuple((step.source, step.target) for step in self.steps)

    @property
    def inverse_relation(self) -> tuple[DualRelationPair, ...]:
        return tuple(sorted((target, source) for source, target in self.relation))

    @property
    def fragment_count(self) -> int:
        """Weak components of the two-step relation, retaining parity phase."""

        adjacency: dict[DualNode, set[DualNode]] = defaultdict(set)
        for source, target in self.relation:
            adjacency[source].add(target)
            adjacency[target].add(source)

        unseen = set(adjacency)
        fragments = 0
        while unseen:
            fragments += 1
            seed = min(unseen)
            stack = [seed]
            seen = {seed}
            while stack:
                node = stack.pop()
                for neighbor in adjacency[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            unseen.difference_update(seen)
        return fragments

    @property
    def valid(self) -> bool:
        if (
            self.left_mode not in NONZERO_MODES
            or self.right_mode not in NONZERO_MODES
            or self.left_mode == self.right_mode
            or not self.steps
        ):
            return False
        sources = tuple(step.source for step in self.steps)
        targets = tuple(step.target for step in self.steps)
        return (
            len(sources) == len(set(sources))
            and len(targets) == len(set(targets))
            and tuple(sorted(self.steps, key=lambda step: step.source)) == self.steps
        )


@dataclass(frozen=True)
class DualInvolutionPhaseSignature:
    """Three partial involutions and their ordered two-step phase algebra.

    Boundary pairings and alternating-cycle counts are projections of this
    object.  The ordered products retain which matching acts first, while the
    weak product fragments provide a finite scalar candidate for staged
    progress.
    """

    embedding: DegreeFiveTriangulatedEmbedding
    involutions: tuple[
        ModePartialInvolution,
        ModePartialInvolution,
        ModePartialInvolution,
    ]

    def involution(self, mode: V4) -> ModePartialInvolution:
        if mode not in NONZERO_MODES:
            raise ValueError("involution mode must be nonzero in V4")
        for involution in self.involutions:
            if involution.mode == mode:
                return involution
        raise AssertionError("valid phase signature lost a V4 involution")

    def product(self, left_mode: V4, right_mode: V4) -> OrderedInvolutionProduct:
        if left_mode == right_mode:
            raise ValueError("ordered phase product requires two distinct modes")
        left = self.involution(left_mode)
        right = self.involution(right_mode)
        steps: list[OrderedProductStep] = []
        for source in sorted(right.domain):
            middle = right.partner(source)
            if middle is None:
                raise AssertionError("partial involution domain lost its partner")
            target = left.partner(middle)
            if target is None:
                continue
            steps.append(OrderedProductStep(source, middle, target))
        product = OrderedInvolutionProduct(
            left_mode=left_mode,
            right_mode=right_mode,
            steps=tuple(steps),
        )
        if not product.valid:
            raise AssertionError("ordered involution product failed certification")
        return product

    @property
    def ordered_products(self) -> tuple[OrderedInvolutionProduct, ...]:
        return tuple(
            self.product(left, right)
            for left in NONZERO_MODES
            for right in NONZERO_MODES
            if left != right
        )

    @property
    def phase_fragment_rank(self) -> int:
        """Finite candidate rank from one orientation of each unordered mode pair."""

        return sum(
            self.product(NONZERO_MODES[left], NONZERO_MODES[right]).fragment_count
            for left in range(3)
            for right in range(left + 1, 3)
        )

    @property
    def phase_relation_key(
        self,
    ) -> tuple[tuple[V4, V4, tuple[DualRelationPair, ...]], ...]:
        return tuple(
            (
                product.left_mode,
                product.right_mode,
                product.relation,
            )
            for product in self.ordered_products
        )

    @property
    def valid(self) -> bool:
        if not self.embedding.valid:
            return False
        if tuple(involution.mode for involution in self.involutions) != NONZERO_MODES:
            return False
        if any(not involution.valid for involution in self.involutions):
            return False

        splice = trivalent_dual_splice_signature(self.embedding)
        if any(
            self.involution(mode).primal_edges != splice.matching_edges(mode)
            for mode in NONZERO_MODES
        ):
            return False

        face_nodes = frozenset(
            ("f", face_index)
            for face_index in range(len(self.embedding.disk_faces))
        )
        if any(
            not face_nodes <= self.involution(mode).domain
            for mode in NONZERO_MODES
        ):
            return False

        for index in range(5):
            terminal = ("t", index)
            boundary_edge = canonical_edge(
                self.embedding.boundary[index],
                self.embedding.boundary[(index + 1) % 5],
            )
            expected_mode = color_difference(
                self.embedding.state.coloring[boundary_edge[0]],
                self.embedding.state.coloring[boundary_edge[1]],
            )
            terminal_modes = tuple(
                mode
                for mode in NONZERO_MODES
                if terminal in self.involution(mode).domain
            )
            if terminal_modes != (expected_mode,):
                return False

        face_count = len(self.embedding.disk_faces)
        for left in NONZERO_MODES:
            for right in NONZERO_MODES:
                if left == right:
                    continue
                product = self.product(left, right)
                reverse = self.product(right, left)
                if len(product.steps) != face_count:
                    return False
                if product.inverse_relation != reverse.relation:
                    return False

        return self.phase_fragment_rank > 0


def dual_involution_phase_signature(
    embedding: DegreeFiveTriangulatedEmbedding,
) -> DualInvolutionPhaseSignature:
    """Derive the exact partial-involution phase algebra from the retained disk."""

    if not embedding.valid:
        raise ValueError("a valid retained triangulated embedding is required")

    boundary_edges = {
        canonical_edge(
            embedding.boundary[index],
            embedding.boundary[(index + 1) % 5],
        ): index
        for index in range(5)
    }
    edge_faces: dict[Edge, list[int]] = defaultdict(list)
    for face_index, face in enumerate(embedding.disk_faces):
        for index in range(3):
            edge_faces[
                canonical_edge(face[index], face[(index + 1) % 3])
            ].append(face_index)

    mode_arcs: dict[V4, list[InvolutionArc]] = {
        mode: [] for mode in NONZERO_MODES
    }
    for edge, incident_faces in edge_faces.items():
        mode = color_difference(
            embedding.state.coloring[edge[0]],
            embedding.state.coloring[edge[1]],
        )
        if edge in boundary_edges:
            if len(incident_faces) != 1:
                raise AssertionError("disk boundary edge must meet one disk face")
            left: DualNode = ("t", boundary_edges[edge])
            right: DualNode = ("f", incident_faces[0])
        else:
            if len(incident_faces) != 2:
                raise AssertionError("interior disk edge must meet two disk faces")
            left = ("f", incident_faces[0])
            right = ("f", incident_faces[1])
        mode_arcs[mode].append(InvolutionArc(left, right, edge))

    involutions = tuple(
        ModePartialInvolution(
            mode=mode,
            arcs=tuple(sorted(mode_arcs[mode])),
        )
        for mode in NONZERO_MODES
    )
    signature = DualInvolutionPhaseSignature(
        embedding=embedding,
        involutions=(involutions[0], involutions[1], involutions[2]),
    )
    if not signature.valid:
        raise AssertionError("dual involution phase signature failed certification")
    if frozenset(
        arc.primal_edge
        for involution in signature.involutions
        for arc in involution.arcs
    ) != disk_primal_edges(embedding):
        raise AssertionError("phase involutions lost a physical disk edge")
    return signature

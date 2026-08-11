from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Mapping

PALETTE = (0, 1, 2, 3)
BROWN = -1

Graph = Mapping[str, tuple[str, ...]]
Coloring = Mapping[str, int]
Edge = tuple[str, str]


def canonical_edge(u: str, v: str) -> Edge:
    if u == v:
        raise ValueError("self-loop is outside the simple-graph contract")
    return (u, v) if u < v else (v, u)


def edge_ledger(graph: Graph) -> frozenset[Edge]:
    edges: set[Edge] = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if v not in graph:
                raise ValueError(f"unknown endpoint: {v}")
            edges.add(canonical_edge(u, v))
    return frozenset(edges)


def terminal_coloring_valid(graph: Graph, coloring: Coloring) -> bool:
    if set(coloring) != set(graph):
        return False
    if any(value not in PALETTE for value in coloring.values()):
        return False
    return all(coloring[u] != coloring[v] for u, v in edge_ledger(graph))


def inherited_obligations_preserved(before: Graph, after: Graph) -> bool:
    """Every edge obligation from the source graph remains explicit after expansion."""
    return edge_ledger(before) <= edge_ledger(after)


@dataclass(frozen=True)
class ContractExpansionWitness:
    before_graph: Graph
    after_graph: Graph
    before_coloring: Coloring
    after_coloring: Coloring
    distortion: Fraction
    reserve: Fraction

    @property
    def finite_budget(self) -> bool:
        return Fraction(0) <= self.distortion <= self.reserve

    @property
    def preserves_species(self) -> bool:
        return (
            inherited_obligations_preserved(self.before_graph, self.after_graph)
            and terminal_coloring_valid(self.before_graph, self.before_coloring)
            and terminal_coloring_valid(self.after_graph, self.after_coloring)
            and self.finite_budget
        )


def cycle5_graph() -> dict[str, tuple[str, ...]]:
    names = ("u0", "u1", "u2", "u3", "u4")
    graph: dict[str, tuple[str, ...]] = {}
    for i, name in enumerate(names):
        graph[name] = (names[(i - 1) % 5], names[(i + 1) % 5])
    return graph


def cycle5_proper_assignments() -> tuple[tuple[int, ...], ...]:
    """Enumerate the entire 4^5 boundary cube and retain exactly proper C5 states."""
    out: list[tuple[int, ...]] = []
    for assignment in product(PALETTE, repeat=5):
        if all(assignment[i] != assignment[(i + 1) % 5] for i in range(5)):
            out.append(assignment)
    return tuple(out)


def center_extends_immediately(boundary: tuple[int, ...]) -> bool:
    """A center adjacent to all five boundary vertices extends iff a palette value is unused."""
    return len(set(boundary)) < len(PALETTE)


def classify_cycle5_boundary() -> dict[str, tuple[tuple[int, ...], ...]]:
    proper = cycle5_proper_assignments()
    immediate = tuple(b for b in proper if center_extends_immediately(b))
    saturated = tuple(b for b in proper if not center_extends_immediately(b))
    return {"immediate": immediate, "saturated": saturated}


@dataclass(frozen=True)
class FiniteDiffusionStep:
    """Small exact Markov diffusion witness for browning-out bookkeeping.

    The stochastic matrix is row-major.  Rows must sum to one and entries must
    be non-negative.  This is not the full Principia PDE; it is a finite
    mechanical witness for the same mass-preserving diffusion invariant.
    """

    transition: tuple[tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        n = len(self.transition)
        if n == 0 or any(len(row) != n for row in self.transition):
            raise ValueError("transition must be non-empty and square")
        for row in self.transition:
            if any(value < 0 for value in row):
                raise ValueError("diffusion weights must be non-negative")
            if sum(row, Fraction(0)) != 1:
                raise ValueError("each diffusion row must preserve total mass")

    def evolve(self, density: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        if len(density) != len(self.transition):
            raise ValueError("density dimension mismatch")
        if any(value < 0 for value in density):
            raise ValueError("density must be non-negative")
        if sum(density, Fraction(0)) != 1:
            raise ValueError("density must have unit mass")
        n = len(density)
        return tuple(
            sum(density[i] * self.transition[i][j] for i in range(n))
            for j in range(n)
        )


def decode_or_brown(density: tuple[Fraction, ...]) -> int:
    """Decode a unique maximal terminal basin; fail closed to BROWN on a tie."""
    if len(density) != len(PALETTE):
        raise ValueError("decoder expects exactly four terminal basin masses")
    peak = max(density)
    winners = [i for i, value in enumerate(density) if value == peak]
    return winners[0] if len(winners) == 1 else BROWN

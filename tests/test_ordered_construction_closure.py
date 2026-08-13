from __future__ import annotations

from collections import Counter, defaultdict, deque
from typing import TypeAlias

from mettafy.color_construction import PALETTE4, ConstructionState
from mettafy.ordered_shape import OrderedShapeLedger, certify_shape_progress
from mettafy.sequential_frontier import CleanFrontierTurn, clean_frontier_turns

Face: TypeAlias = tuple[str, str, str]
DiskFaces: TypeAlias = tuple[Face, ...]
Edge: TypeAlias = tuple[str, str]

BOUNDARY = ("a", "b", "c", "d", "e")
FOCUS = "v"
DISK_FACES: DiskFaces = (
    ("b", "x0", "x1"),
    ("x1", "x2", "x0"),
    ("e", "x2", "d"),
    ("a", "x0", "b"),
    ("x1", "d", "x2"),
    ("e", "x0", "a"),
    ("e", "x0", "x2"),
    ("c", "x1", "b"),
    ("c", "x1", "d"),
)
BASE_COLORING = {
    "a": 0,
    "b": 1,
    "c": 0,
    "d": 2,
    "e": 3,
    "x0": 2,
    "x1": 3,
    "x2": 1,
}


def _canonical_edge(left: str, right: str) -> Edge:
    return (left, right) if left < right else (right, left)


def _add_edge(adjacency: dict[str, set[str]], left: str, right: str) -> None:
    adjacency[left].add(right)
    adjacency[right].add(left)


def _face_key(faces: DiskFaces) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(sorted(face)) for face in faces))


def _graph(faces: DiskFaces) -> dict[str, tuple[str, ...]]:
    vertices = {FOCUS, *BOUNDARY, *BASE_COLORING}
    adjacency = {vertex: set() for vertex in vertices}
    for index, vertex in enumerate(BOUNDARY):
        _add_edge(adjacency, FOCUS, vertex)
        _add_edge(adjacency, vertex, BOUNDARY[(index + 1) % 5])
    for face in faces:
        for index, vertex in enumerate(face):
            _add_edge(adjacency, vertex, face[(index + 1) % 3])

    graph = {
        vertex: tuple(sorted(neighbors))
        for vertex, neighbors in adjacency.items()
    }
    graph[FOCUS] = BOUNDARY
    return graph


def _proper_color_preserving_flips(faces: DiskFaces) -> tuple[DiskFaces, ...]:
    edge_faces: dict[Edge, list[int]] = defaultdict(list)
    for face_index, face in enumerate(faces):
        for index in range(3):
            edge_faces[
                _canonical_edge(face[index], face[(index + 1) % 3])
            ].append(face_index)

    boundary_edges = frozenset(
        _canonical_edge(BOUNDARY[index], BOUNDARY[(index + 1) % 5])
        for index in range(5)
    )
    all_edges = frozenset(edge_faces)
    generated: dict[tuple[tuple[str, ...], ...], DiskFaces] = {}

    for diagonal, incident_faces in edge_faces.items():
        if diagonal in boundary_edges or len(incident_faces) != 2:
            continue
        first_index, second_index = incident_faces
        first_face = faces[first_index]
        second_face = faces[second_index]
        first_opposite = next(
            vertex for vertex in first_face if vertex not in diagonal
        )
        second_opposite = next(
            vertex for vertex in second_face if vertex not in diagonal
        )
        if first_opposite == second_opposite:
            continue

        replacement = _canonical_edge(first_opposite, second_opposite)
        if replacement in all_edges:
            continue
        if BASE_COLORING[first_opposite] == BASE_COLORING[second_opposite]:
            continue

        left, right = diagonal
        updated = [
            face
            for index, face in enumerate(faces)
            if index not in (first_index, second_index)
        ]
        updated.extend(
            (
                (first_opposite, second_opposite, left),
                (first_opposite, second_opposite, right),
            )
        )
        candidate = tuple(sorted(updated, key=lambda face: tuple(sorted(face))))
        generated[_face_key(candidate)] = candidate

    return tuple(generated[key] for key in sorted(generated))


def _flip_family() -> tuple[DiskFaces, ...]:
    queue: deque[DiskFaces] = deque([DISK_FACES])
    seen = {_face_key(DISK_FACES)}
    family: list[DiskFaces] = []

    while queue:
        faces = queue.popleft()
        family.append(faces)
        for candidate in _proper_color_preserving_flips(faces):
            key = _face_key(candidate)
            if key in seen:
                continue
            seen.add(key)
            queue.append(candidate)
    return tuple(family)


def _saturated_boundary(coloring: dict[str, int]) -> bool:
    return len({coloring[vertex] for vertex in BOUNDARY}) == 4


def _proper_boundary(coloring: dict[str, int]) -> bool:
    return all(
        coloring[BOUNDARY[index]] != coloring[BOUNDARY[(index + 1) % 5]]
        for index in range(5)
    )


def _proper_saturated_colorings(
    graph: dict[str, tuple[str, ...]],
) -> tuple[dict[str, int], ...]:
    """Enumerate theorem instances with one global color fixed by symmetry."""

    vertices = tuple(vertex for vertex in graph if vertex != FOCUS)
    order = ("a",) + tuple(
        vertex
        for vertex in sorted(vertices, key=lambda item: -len(graph[item]))
        if vertex != "a"
    )
    coloring: dict[str, int] = {"a": 0}
    results: list[dict[str, int]] = []

    def visit(index: int) -> None:
        if index == len(order):
            if _proper_boundary(coloring) and _saturated_boundary(coloring):
                results.append(dict(coloring))
            return

        vertex = order[index]
        if vertex in coloring:
            visit(index + 1)
            return

        forbidden = {
            coloring[neighbor]
            for neighbor in graph[vertex]
            if neighbor in coloring
        }
        for color in sorted(PALETTE4 - forbidden):
            coloring[vertex] = color
            visit(index + 1)
            del coloring[vertex]

    visit(0)
    return tuple(results)


def _singleton_and_repeated_turns(
    state: ConstructionState,
) -> tuple[tuple[CleanFrontierTurn, ...], tuple[CleanFrontierTurn, ...]]:
    turns = clean_frontier_turns(state, FOCUS, BOUNDARY)
    counts = Counter(state.coloring[vertex] for vertex in BOUNDARY)
    singleton_colors = {color for color, count in counts.items() if count == 1}
    repeated_color = next(color for color, count in counts.items() if count == 2)
    singleton = tuple(
        turn for turn in turns if state.coloring[turn.move.seed] in singleton_colors
    )
    repeated = tuple(
        turn for turn in turns if state.coloring[turn.move.seed] == repeated_color
    )
    return singleton, repeated


def _apply_finishing_turn(turn: CleanFrontierTurn) -> None:
    assert turn.valid
    assert turn.after.admissible_colors(FOCUS)


def _audit_noninverse_orientation(first: CleanFrontierTurn) -> tuple[int, int, int]:
    """Return persistent depth, strict refinements, and rejected label replays.

    The bound is an audit guard only.  The proof does not depend on `20`.
    """

    assert first.valid
    ledger = OrderedShapeLedger()
    first_certificate = certify_shape_progress(ledger, first)
    assert first_certificate.valid
    assert first_certificate.new_lineage
    assert first_certificate.consequential
    ledger = first_certificate.commit()

    current = first.after
    previous_seed = first.move.seed
    persistent_turns = 1
    strict_refinements = 0
    replay_rejections = 0

    for _ in range(19):
        singleton, repeated = _singleton_and_repeated_turns(current)
        if singleton:
            _apply_finishing_turn(singleton[0])
            return persistent_turns, strict_refinements, replay_rejections

        repeated_color = next(
            color
            for color, count in Counter(
                current.coloring[vertex] for vertex in BOUNDARY
            ).items()
            if count == 2
        )
        repeated_positions = {
            vertex
            for vertex in BOUNDARY
            if current.coloring[vertex] == repeated_color
        }
        clean_repeated_seeds = {turn.move.seed for turn in repeated}
        assert repeated_positions <= clean_repeated_seeds

        replay_certificates = []
        for candidate in repeated:
            certificate = certify_shape_progress(ledger, candidate)
            if certificate.equivalent_replay:
                replay_certificates.append(certificate)
        assert replay_certificates
        for certificate in replay_certificates:
            assert not certificate.fresh
            assert not certificate.consequential
            assert not certificate.valid
        replay_rejections += len(replay_certificates)

        noninverse = tuple(
            turn for turn in repeated if turn.move.seed != previous_seed
        )
        assert noninverse
        turn = noninverse[0]
        certificate = certify_shape_progress(ledger, turn)
        assert certificate.valid
        assert certificate.fresh
        assert certificate.consequential
        assert certificate.retains_prior_lineage
        if certificate.prior_lineage_shapes:
            assert certificate.strict_refinement
            strict_refinements += 1
        ledger = certificate.commit()

        current = turn.after
        previous_seed = turn.move.seed
        persistent_turns += 1

    raise AssertionError("saturated ordered construction did not expose a finishing turn")


def test_ordered_construction_survives_all_saturated_flip_family_colorings() -> None:
    family = _flip_family()
    assert len(family) == 154

    theorem_instances = 0
    immediate_finishes = 0
    nonterminal_orientations = 0
    strict_refinement_events = 0
    rejected_label_replays = 0
    persistent_depths: Counter[int] = Counter()

    for faces in family:
        graph = _graph(faces)
        for coloring in _proper_saturated_colorings(graph):
            theorem_instances += 1
            state = ConstructionState(graph, coloring)
            singleton, repeated = _singleton_and_repeated_turns(state)

            # Clean Frontier Turn Existence.
            assert singleton or repeated

            if singleton:
                immediate_finishes += 1
                _apply_finishing_turn(singleton[0])
                continue

            # Repeated-Turn Pair Lemma.
            repeated_color = next(
                color
                for color, count in Counter(
                    state.coloring[vertex] for vertex in BOUNDARY
                ).items()
                if count == 2
            )
            repeated_positions = {
                vertex
                for vertex in BOUNDARY
                if state.coloring[vertex] == repeated_color
            }
            assert repeated_positions <= {turn.move.seed for turn in repeated}

            # Attack both possible initial orientations.
            for first in repeated:
                nonterminal_orientations += 1
                depth, refinements, replays = _audit_noninverse_orientation(first)
                persistent_depths[depth] += 1
                strict_refinement_events += refinements
                rejected_label_replays += replays

    assert theorem_instances == 4620
    assert immediate_finishes == 3534
    assert nonterminal_orientations == 2172
    assert persistent_depths == Counter({1: 2052, 2: 60, 3: 60})
    # The proof's noninverse traversal never needs to revisit a lineage in this
    # exhaustive family.  The dedicated three-interior shortest-route witness
    # exercises the strict-refinement branch separately.
    assert strict_refinement_events == 0
    assert rejected_label_replays > 0

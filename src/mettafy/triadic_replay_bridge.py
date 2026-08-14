from __future__ import annotations

from dataclasses import dataclass

from mettafy.color_construction import ConstructionState
from mettafy.ordered_shape import (
    OrderedShapeLedger,
    ShapeProgressCertificate,
    certify_shape_progress,
    resolved_component_shape,
)
from mettafy.sequential_frontier import CleanFrontierTurn
from mettafy.triadic_evitability import TriadicHistory, TriadicSnapshot


def history_from_construction(state: ConstructionState) -> TriadicHistory:
    """Create one deterministic realized-history baseline from a construction snapshot.

    The helper is intentionally a baseline projection, not a claim about the
    construction's true historical placement route. Every currently colored
    lineage is placed once in lexical order; uncolored graph vertices remain
    unrealized loci.
    """

    history = TriadicHistory(frozenset(state.graph))
    for lineage, color in sorted(state.coloring.items()):
        history = history.place(lineage, color)
    return history


def apply_clean_turn_epoch(
    history: TriadicHistory,
    turn: CleanFrontierTurn,
) -> TriadicHistory:
    """Apply a valid whole-component turn as one atomic realization epoch."""

    if not turn.valid:
        raise ValueError("triadic replay bridge requires a valid clean frontier turn")

    snapshot = history.snapshot()
    expected_before = tuple(sorted(turn.before.coloring.items()))
    actual_before = snapshot.extensional_projection[1]
    if actual_before != expected_before:
        raise ValueError("triadic history does not match the turn's before identities")

    successors = {
        lineage: turn.after.coloring[lineage]
        for lineage in turn.component
    }
    after = history.transform_many(successors)
    if after.snapshot().extensional_projection[1] != tuple(sorted(turn.after.coloring.items())):
        raise AssertionError("atomic triadic turn failed to reproduce the public successor")
    return after


@dataclass(frozen=True)
class TriadicReplayBridgeCertificate:
    """Compare C6 physical replay with triadic historical non-return.

    C6 intentionally quotients orientation/relabeling and asks whether the
    resolved physical component shape has already been seen. The triadic layer
    retains realization history. These notions can therefore agree that the
    physical move is replay while disagreeing that the full constructional
    object has returned to its initial state.
    """

    initial: TriadicSnapshot
    after_first: TriadicSnapshot
    after_inverse: TriadicSnapshot
    first_shape: ShapeProgressCertificate
    inverse_shape: ShapeProgressCertificate

    @property
    def physical_shape_replay(self) -> bool:
        return (
            self.inverse_shape.equivalent_replay
            and self.inverse_shape.shape == self.first_shape.shape
        )

    @property
    def extensional_return(self) -> bool:
        return self.after_inverse.extensional_projection == self.initial.extensional_projection

    @property
    def lineage_order_return(self) -> bool:
        return (
            self.after_inverse.difference.lineage_birth_order
            == self.initial.difference.lineage_birth_order
        )

    @property
    def triadic_return(self) -> bool:
        return self.after_inverse == self.initial

    @property
    def held_difference_changed(self) -> bool:
        return self.after_inverse.difference != self.initial.difference

    @property
    def valid(self) -> bool:
        return (
            self.first_shape.valid
            and self.physical_shape_replay
            and not self.inverse_shape.consequential
            and self.extensional_return
            and self.lineage_order_return
            and self.held_difference_changed
            and not self.triadic_return
        )


def certify_triadic_inverse_replay(
    first: CleanFrontierTurn,
    inverse: CleanFrontierTurn,
) -> TriadicReplayBridgeCertificate:
    """Certify one exact public inverse under both C6 and triadic semantics."""

    if not first.valid or not inverse.valid:
        raise ValueError("triadic inverse replay requires two valid clean turns")
    if inverse.before != first.after:
        raise ValueError("inverse turn must begin at the first turn's actual successor")
    if dict(inverse.after.graph) != dict(first.before.graph):
        raise ValueError("inverse turn must restore the original public carrier")
    if dict(inverse.after.coloring) != dict(first.before.coloring):
        raise ValueError("inverse turn must restore the original extensional identities")

    first_certificate = certify_shape_progress(OrderedShapeLedger(), first)
    if not first_certificate.valid:
        raise ValueError("first turn must establish consequential C6 structure")
    shape_ledger = first_certificate.commit()
    inverse_certificate = certify_shape_progress(shape_ledger, inverse)

    if resolved_component_shape(inverse) != resolved_component_shape(first):
        raise ValueError("inverse is not an orientation-free physical shape replay")

    history0 = history_from_construction(first.before)
    history1 = apply_clean_turn_epoch(history0, first)
    history2 = apply_clean_turn_epoch(history1, inverse)

    certificate = TriadicReplayBridgeCertificate(
        initial=history0.snapshot(),
        after_first=history1.snapshot(),
        after_inverse=history2.snapshot(),
        first_shape=first_certificate,
        inverse_shape=inverse_certificate,
    )
    if not certificate.valid:
        raise AssertionError("C6/triadic replay correspondence failed")
    return certificate

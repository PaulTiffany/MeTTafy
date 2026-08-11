from __future__ import annotations

from collections import Counter

from mettafy.color_construction import ConstructionState
from mettafy.kempe_traversal import (
    KempeMove,
    KempeTraversalCertificate,
    apply_kempe_move,
    opening_single_moves,
    single_move_locked,
)


def planar_traversal_state() -> ConstructionState:
    graph = {
       
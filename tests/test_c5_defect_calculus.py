from __future__ import annotations

from itertools import product

import mettafy.c5_defect_calculus as defects


def test_every_proper_c5_has_311_derivative_signature() -> None:
    signatures: set[tuple[int, int, int]] = set()
    for boundary in product(range(4), repeat=5):
        state = defects.C5DefectState(boundary)
        if not state:
            continue
        signatures.add(state.signature)
    assert signatures == {(3, 1, 1)}

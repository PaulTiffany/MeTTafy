from __future__ import annotations

import json
from pathlib import Path

from mettafy.exemplars import blind_exemplar_view


def test_four_color_blind_view_removes_label_leaks() -> None:
    manifest_path = Path("exemplars/four_color/manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    blinded = blind_exemplar_view(manifest)

    assert "title" not in blinded
    assert "field" not in blinded
    assert "history" not in blinded
    assert "repository" not in blinded["upstream"]
    assert "paths" not in blinded["upstream"]

    for layer in blinded["proof_layers"]:
        assert "source" not in layer
        assert "theorem" not in layer

    # Ground-truth annotations remain part of the evaluation record; callers
    # decide whether to expose or hold them out from a classifier input.
    assert blinded["proof_layers"][0]["strategies"]

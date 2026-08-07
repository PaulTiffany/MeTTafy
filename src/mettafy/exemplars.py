from __future__ import annotations

from copy import deepcopy
from typing import Any


def blind_exemplar_view(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a benchmark-safe projection of an exemplar manifest.

    Historical and documentary metadata are removed so a strategy classifier
    cannot infer labels from famous theorem names, authors, filenames, or
    narrative context. Structural annotations remain available only when they
    are explicitly part of the benchmark target/evaluation record.
    """

    blinded = deepcopy(manifest)
    blinded.pop("title", None)
    blinded.pop("field", None)
    blinded.pop("history", None)

    upstream = blinded.get("upstream")
    if isinstance(upstream, dict):
        upstream.pop("repository", None)
        upstream.pop("paths", None)

    layers = blinded.get("proof_layers")
    if isinstance(layers, list):
        for layer in layers:
            if isinstance(layer, dict):
                layer.pop("source", None)
                layer.pop("theorem", None)

    return blinded

from __future__ import annotations

from copy import deepcopy
from typing import Any


def blind_exemplar_view(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return classifier input with documentary and answer-key fields removed."""

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
                layer.pop("strategies", None)

    return blinded


def exemplar_strategy_targets(manifest: dict[str, Any]) -> dict[str, list[str]]:
    """Extract held-out strategy labels keyed by proof-layer id."""

    targets: dict[str, list[str]] = {}
    layers = manifest.get("proof_layers", [])
    if not isinstance(layers, list):
        return targets

    for layer in layers:
        if not isinstance(layer, dict):
            continue
        layer_id = layer.get("id")
        strategies = layer.get("strategies")
        if isinstance(layer_id, str) and isinstance(strategies, list):
            targets[layer_id] = [str(item) for item in strategies]

    return targets

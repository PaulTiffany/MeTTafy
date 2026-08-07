#!/usr/bin/env python3
"""Attach deterministic byte-level integrity data to the generated Pages manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
MANIFEST = OUT / "build-manifest.json"
VENDOR_FILES = (
    OUT / "assets" / "vendor" / "mettascript-grapher" / "embed.js",
    OUT / "assets" / "vendor" / "mettascript-grapher" / "LICENSE",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not MANIFEST.is_file():
        raise SystemExit("site integrity: build-manifest.json is missing; build the site first")

    missing = [str(path.relative_to(OUT)) for path in VENDOR_FILES if not path.is_file()]
    if missing:
        raise SystemExit("site integrity: required deployed vendor files are missing: " + ", ".join(missing))

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["deployed_artifact_integrity"] = {
        str(path.relative_to(OUT)): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in VENDOR_FILES
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("Stamped deployed artifact integrity:")
    for relative, metadata in manifest["deployed_artifact_integrity"].items():
        print(f"  {relative}: {metadata['sha256']} ({metadata['bytes']} bytes)")


if __name__ == "__main__":
    main()

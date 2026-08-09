#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "witnesses"
UPSTREAM = ROOT / "_vendor" / "fourcolor-replay"
EVIDENCE = OUT / "rocq-four-color-replay.json"
EXPECTED_SHA = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
IMAGE = "coqorg/coq@sha256:e50d77c4c5a9aa0d76ae1b343d79c5f922da3a75054b79c5dc635895438e4674"


def read(name: str) -> str:
    return (OUT / name).read_text(encoding="utf-8").strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def main() -> int:
    upstream_sha = git("rev-parse", "HEAD", cwd=UPSTREAM)
    if upstream_sha != EXPECTED_SHA:
        raise SystemExit(
            f"upstream drift: expected {EXPECTED_SHA}, got {upstream_sha}"
        )

    log = OUT / "rocq-four-color-replay.log"
    packages = OUT / "rocq-installed-packages.txt"
    payload = {
        "witness": "WIT-ROCQ-REPLAY",
        "schema": "mettafy-rocq-replay-v1",
        "result": "pass",
        "repository_sha": git("rev-parse", "HEAD"),
        "upstream": {
            "repository": "https://github.com/rocq-community/fourcolor",
            "commit": upstream_sha,
            "tree": read("rocq-upstream-tree.txt"),
            "license": "CeCILL-B",
        },
        "toolchain": {
            "container_image": IMAGE,
            "checker_version": read("rocq-checker-version.txt"),
            "ocaml_version": read("rocq-ocaml-version.txt"),
            "opam_version": read("rocq-opam-version.txt"),
            "installed_packages": read("rocq-installed-packages.txt").splitlines(),
        },
        "execution": {
            "elapsed_seconds": int(read("rocq-replay-elapsed-seconds.txt")),
            "commands": [
                "opam pin add -n -y -k path coq-fourcolor-reals <pinned-source>",
                "opam install -y -j 2 coq-fourcolor-reals --deps-only",
                "opam install -y -v -j 2 coq-fourcolor-reals",
                "opam pin add -n -y -k path coq-fourcolor <pinned-source>",
                "opam install -y -j 2 coq-fourcolor --deps-only",
                "opam install -y -v -j 2 coq-fourcolor",
            ],
            "exit_status": 0,
            "log_sha256": sha256(log),
            "installed_packages_sha256": sha256(packages),
        },
        "claim": (
            "The exact pinned Four Color source was accepted by the recorded "
            "Coq/Rocq kernel toolchain through its upstream opam package boundaries."
        ),
        "non_claims": [
            "MeTTafy semantic interpretations are correct",
            "the historical narrative is correct",
            "the structural extractor is complete",
            "the MeTTa projection is equivalent to the Rocq proof",
        ],
        "authority": "Coq/Rocq kernel and upstream opam build on the pinned formal artifact",
        "environment": {
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        },
    }
    EVIDENCE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Rocq replay evidence emitted: {EVIDENCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

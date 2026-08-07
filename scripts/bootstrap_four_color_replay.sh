#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${ROOT}/_vendor/fourcolor"
OUT="${ROOT}/artifacts/witnesses"
IMAGE_TAG="coqorg/coq:8.20.1"
PINNED_SOURCE="f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"

if [[ ! -d "${SOURCE}/.git" ]]; then
  echo "missing pinned Four Color checkout at ${SOURCE}" >&2
  exit 1
fi
actual_source="$(git -C "${SOURCE}" rev-parse HEAD)"
if [[ "${actual_source}" != "${PINNED_SOURCE}" ]]; then
  echo "Four Color source drift: expected ${PINNED_SOURCE}, got ${actual_source}" >&2
  exit 1
fi

mkdir -p "${OUT}"

echo "Pulling discovery image ${IMAGE_TAG} (bootstrap only; not certifying)..."
docker pull "${IMAGE_TAG}"
repo_digest="$(docker image inspect "${IMAGE_TAG}" --format '{{index .RepoDigests 0}}')"
image_id="$(docker image inspect "${IMAGE_TAG}" --format '{{.Id}}')"

echo "Discovered immutable image identity:"
echo "  repo digest: ${repo_digest}"
echo "  image id:    ${image_id}"

start="$(date +%s)"
set +e
docker run --rm \
  --entrypoint bash \
  -v "${SOURCE}:/workspace/fourcolor:rw" \
  -w /workspace/fourcolor \
  "${IMAGE_TAG}" \
  -lc '
    set -euo pipefail
    echo "=== toolchain ==="
    coqc --version
    ocamlc -version
    opam --version
    echo "=== pin reals package ==="
    opam pin add -n -y coq-fourcolor-reals.dev .
    opam install -y --deps-only coq-fourcolor-reals
    opam install -y coq-fourcolor-reals
    echo "=== pin proof package ==="
    opam pin add -n -y coq-fourcolor.dev .
    opam install -y --deps-only coq-fourcolor
    opam install -y coq-fourcolor
    echo "=== resolved packages ==="
    opam list --installed --columns=name,version --short=false
  ' 2>&1 | tee "${OUT}/rocq-four-color-bootstrap.log"
status="${PIPESTATUS[0]}"
set -e
end="$(date +%s)"
elapsed="$((end - start))"

python - "${OUT}" "${PINNED_SOURCE}" "${IMAGE_TAG}" "${repo_digest}" "${image_id}" "${status}" "${elapsed}" <<'PY'
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

out = pathlib.Path(sys.argv[1])
source_sha, image_tag, repo_digest, image_id = sys.argv[2:6]
status = int(sys.argv[6])
elapsed = int(sys.argv[7])
log = out / "rocq-four-color-bootstrap.log"
text = log.read_text(encoding="utf-8", errors="replace")

versions: dict[str, str] = {}
patterns = {
    "coq": r"The Coq Proof Assistant, version ([^\n]+)",
    "ocaml": r"\n([0-9]+\.[0-9]+\.[0-9]+)\n=== pin reals package ===",
    "opam": r"opam version ([^\n]+)|\n([0-9]+\.[0-9]+\.[0-9]+)\n=== pin reals package ===",
}
coq_match = re.search(patterns["coq"], text)
if coq_match:
    versions["coq"] = coq_match.group(1).strip()

payload = {
    "witness": "WIT-ROCQ-REPLAY-BOOTSTRAP",
    "certifying": False,
    "claim_boundary": "Bootstrap discovery only: exercises the pinned upstream package build while discovering immutable toolchain and resolved dependency identities. It is not a production certificate.",
    "source": {
        "repository": "https://github.com/rocq-community/fourcolor",
        "commit": source_sha,
    },
    "container": {
        "discovery_tag": image_tag,
        "repo_digest": repo_digest,
        "image_id": image_id,
    },
    "exit_status": status,
    "elapsed_seconds": elapsed,
    "tool_versions_detected": versions,
    "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
    "result": "pass" if status == 0 else "fail",
    "next_step": "Pin the discovered repository digest and resolved dependency set, then replay from a clean environment before promoting WIT-ROCQ-REPLAY.",
}
(out / "rocq-four-color-bootstrap.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
PY

if [[ "${status}" -ne 0 ]]; then
  echo "Four Color replay bootstrap failed; inspect witness log" >&2
  exit "${status}"
fi

echo "Four Color replay bootstrap passed. This run is discovery evidence only, not certification."

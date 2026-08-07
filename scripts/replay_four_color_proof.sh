#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${ROOT}/_vendor/fourcolor"
OUT="${ROOT}/artifacts/witnesses"
SOURCE_COMMIT="f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
IMAGE="coqorg/coq@sha256:e50d77c4c5a9aa0d76ae1b343d79c5f922da3a75054b79c5dc635895438e4674"
EXPECTED_COQ="8.20.1"
EXPECTED_OCAML="4.13.1"
EXPECTED_OPAM="2.3.0"

if [[ ! -d "${SOURCE}/.git" ]]; then
  echo "missing pinned Four Color checkout at ${SOURCE}" >&2
  exit 1
fi
actual_source="$(git -C "${SOURCE}" rev-parse HEAD)"
if [[ "${actual_source}" != "${SOURCE_COMMIT}" ]]; then
  echo "Four Color source drift: expected ${SOURCE_COMMIT}, got ${actual_source}" >&2
  exit 1
fi

mkdir -p "${OUT}"
LOG="${OUT}/rocq-four-color-replay.log"
PACKAGES="${OUT}/rocq-four-color-packages.txt"
: > "${LOG}"
: > "${PACKAGES}"

# The digest, rather than a tag, is the production toolchain identity.
docker pull "${IMAGE}" | tee -a "${LOG}"
resolved="$(docker image inspect "${IMAGE}" --format '{{index .RepoDigests 0}}')"
if [[ "${resolved}" != "${IMAGE}" ]]; then
  echo "immutable image identity mismatch: expected ${IMAGE}, got ${resolved}" | tee -a "${LOG}" >&2
  exit 1
fi

coq_version="$(docker run --rm "${IMAGE}" coqc --version | sed -n 's/^The Coq Proof Assistant, version \([^ ]*\).*/\1/p')"
ocaml_version="$(docker run --rm "${IMAGE}" ocamlc -version | tr -d '\r\n')"
opam_version="$(docker run --rm "${IMAGE}" opam --version | tr -d '\r\n')"

for pair in "Coq:${coq_version}:${EXPECTED_COQ}" "OCaml:${ocaml_version}:${EXPECTED_OCAML}" "opam:${opam_version}:${EXPECTED_OPAM}"; do
  IFS=: read -r name actual expected <<<"${pair}"
  if [[ "${actual}" != "${expected}" ]]; then
    echo "${name} version drift: expected ${expected}, got ${actual}" | tee -a "${LOG}" >&2
    exit 1
  fi
done

{
  echo "=== immutable toolchain ==="
  echo "image=${IMAGE}"
  echo "coq=${coq_version}"
  echo "ocaml=${ocaml_version}"
  echo "opam=${opam_version}"
  echo "source_commit=${SOURCE_COMMIT}"
} | tee -a "${LOG}"

start="$(date +%s)"
set +e
docker run --rm \
  --entrypoint bash \
  -v "${SOURCE}:/workspace/fourcolor:rw" \
  -w /workspace/fourcolor \
  "${IMAGE}" \
  -lc '
    set -euo pipefail
    echo "=== upstream package contract: reals ==="
    opam pin add -n -y --kind=path coq-fourcolor-reals.dev .
    opam install -y --deps-only coq-fourcolor-reals
    opam install -y coq-fourcolor-reals

    echo "=== upstream package contract: proof ==="
    opam pin add -n -y --kind=path coq-fourcolor.dev .
    opam install -y --deps-only coq-fourcolor
    opam install -y coq-fourcolor

    echo "=== installed dependency closure ==="
    opam list --installed --columns=name,version --color=never
  ' 2>&1 | tee -a "${LOG}"
status="${PIPESTATUS[0]}"
set -e
end="$(date +%s)"
elapsed="$((end - start))"

# Preserve the resolved package table separately from the full build log.
awk '/^=== installed dependency closure ===$/{capture=1; next} capture{print}' "${LOG}" > "${PACKAGES}"

python - "${OUT}" "${SOURCE_COMMIT}" "${IMAGE}" "${coq_version}" "${ocaml_version}" "${opam_version}" "${status}" "${elapsed}" <<'PY'
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

out = pathlib.Path(sys.argv[1])
source_commit, image, coq, ocaml, opam = sys.argv[2:7]
status = int(sys.argv[7])
elapsed = int(sys.argv[8])
log = out / "rocq-four-color-replay.log"
packages = out / "rocq-four-color-packages.txt"

sha256 = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
payload = {
    "witness": "WIT-ROCQ-REPLAY",
    "certifying": True,
    "claim_boundary": (
        "The pinned Four Color formal artifact was accepted by the pinned Coq/Rocq-compatible "
        "checker/toolchain through the upstream opam package build contract."
    ),
    "non_claims": [
        "MeTTafy's semantic interpretation is correct",
        "MeTTafy's extracted dependency graph is correct",
        "the historical narrative is correct",
        "the proof establishes claims beyond those checked by the upstream formal artifact",
    ],
    "source": {
        "repository": "https://github.com/rocq-community/fourcolor",
        "commit": source_commit,
        "license": "CeCILL-B",
    },
    "toolchain": {
        "container": image,
        "coq": coq,
        "ocaml": ocaml,
        "opam": opam,
        "opam_repository": "snapshot embedded in the immutable container image",
    },
    "build_contract": [
        "path-pin and install coq-fourcolor-reals.dev from pinned source",
        "resolve/install declared reals dependencies from pinned image opam snapshot",
        "path-pin and install coq-fourcolor.dev from pinned source",
        "resolve/install declared proof dependencies from pinned image opam snapshot",
    ],
    "exit_status": status,
    "elapsed_seconds": elapsed,
    "evidence": {
        "log_sha256": sha256(log),
        "resolved_packages_sha256": sha256(packages),
    },
    "result": "pass" if status == 0 else "fail",
}
(out / "rocq-four-color-replay.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
PY

if [[ "${status}" -ne 0 ]]; then
  echo "Four Color formal replay failed; witness evidence retained" >&2
  exit "${status}"
fi

echo "Four Color formal replay passed under immutable toolchain ${IMAGE}."

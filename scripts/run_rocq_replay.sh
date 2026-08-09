#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/work}"
UPSTREAM="${ROOT}/_vendor/fourcolor-replay"
OUT="${ROOT}/artifacts/witnesses"
EXPECTED_SHA="f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
mkdir -p "${OUT}"

# GitHub checks out the pinned repository on the host and bind-mounts it into
# the replay container. The host/container UIDs differ, so Git correctly
# requires an explicit trust decision before it will inspect the mounted repo.
# Scope that exception to this one exact replay checkout; all SHA/tree/dirty
# checks below remain in force.
git config --global --add safe.directory "${UPSTREAM}"

actual_sha="$(git -C "${UPSTREAM}" rev-parse HEAD)"
if [[ "${actual_sha}" != "${EXPECTED_SHA}" ]]; then
  echo "pinned Four Color source drift: expected ${EXPECTED_SHA}, got ${actual_sha}" >&2
  exit 1
fi
if [[ -n "$(git -C "${UPSTREAM}" status --porcelain --untracked-files=no)" ]]; then
  echo "pinned Four Color tracked source is dirty before replay" >&2
  exit 1
fi

git -C "${UPSTREAM}" rev-parse 'HEAD^{tree}' > "${OUT}/rocq-upstream-tree.txt"
coqc --version > "${OUT}/rocq-checker-version.txt"
ocamlc -version > "${OUT}/rocq-ocaml-version.txt"
opam --version > "${OUT}/rocq-opam-version.txt"

start_epoch="$(date +%s)"
{
  echo "WIT-ROCQ-REPLAY start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "upstream_sha=${actual_sha}"
  echo "upstream_tree=$(cat "${OUT}/rocq-upstream-tree.txt")"
  echo "checker=$(head -n 1 "${OUT}/rocq-checker-version.txt")"

  opam pin add -n -y -k path coq-fourcolor-reals "${UPSTREAM}"
  opam update -y
  opam install -y -j 2 coq-fourcolor-reals --deps-only
  opam install -y -v -j 2 coq-fourcolor-reals

  opam pin add -n -y -k path coq-fourcolor "${UPSTREAM}"
  opam install -y -j 2 coq-fourcolor --deps-only
  opam install -y -v -j 2 coq-fourcolor

  echo "installed package closure:"
  opam list --installed --columns=name,version --sort
  echo "WIT-ROCQ-REPLAY finish=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} 2>&1 | tee "${OUT}/rocq-four-color-replay.log"

opam list --installed --columns=name,version --sort > "${OUT}/rocq-installed-packages.txt"
end_epoch="$(date +%s)"
printf '%s\n' "$((end_epoch - start_epoch))" > "${OUT}/rocq-replay-elapsed-seconds.txt"

# The opam build is expected to create ignored build products. Tracked upstream
# source must remain byte-identical to the pinned commit.
if [[ -n "$(git -C "${UPSTREAM}" status --porcelain --untracked-files=no)" ]]; then
  echo "tracked pinned Four Color source changed during replay" >&2
  exit 1
fi

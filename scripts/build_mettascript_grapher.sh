#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly VENDOR="${ROOT}/_vendor/MeTTaScript"
readonly EXPECTED_COMMIT="abe13439196bccdb48b6636773a46ec9772a7aaf"
readonly EXPECTED_PNPM="11.2.2"
readonly BUNDLE="${VENDOR}/packages/grapher/dist/embed.js"
readonly LICENSE="${VENDOR}/LICENSE"

fail() {
  printf 'MeTTaScript build boundary: %s\n' "$*" >&2
  exit 1
}

[[ -d "${VENDOR}/.git" ]] || fail "missing pinned checkout at ${VENDOR}"
actual_commit="$(git -C "${VENDOR}" rev-parse HEAD)"
[[ "${actual_commit}" == "${EXPECTED_COMMIT}" ]] || \
  fail "expected ${EXPECTED_COMMIT}, got ${actual_commit}"

corepack enable
corepack prepare "pnpm@${EXPECTED_PNPM}" --activate
actual_pnpm="$(pnpm --version)"
[[ "${actual_pnpm}" == "${EXPECTED_PNPM}" ]] || \
  fail "expected pnpm ${EXPECTED_PNPM}, got ${actual_pnpm}"

pnpm --dir "${VENDOR}" install --frozen-lockfile
# Grapher's declaration build imports workspace packages such as @mettascript/hyperon.
# The trailing ellipsis asks pnpm to build Grapher and its dependency closure in order.
pnpm --dir "${VENDOR}" --filter '@mettascript/grapher...' build

[[ -s "${BUNDLE}" ]] || fail "Grapher build did not produce ${BUNDLE}"
[[ -s "${LICENSE}" ]] || fail "upstream MIT license is missing"

echo "MeTTaScript Grapher verified"
echo "  commit: ${actual_commit}"
echo "  pnpm:   ${actual_pnpm}"
echo "  bundle: $(sha256sum "${BUNDLE}" | cut -d' ' -f1)"

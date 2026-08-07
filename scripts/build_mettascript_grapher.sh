#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly VENDOR="${ROOT}/_vendor/MeTTaScript"
readonly EXPECTED_COMMIT="abe13439196bccdb48b6636773a46ec9772a7aaf"
readonly EXPECTED_PNPM="11.2.2"
readonly DIST="${VENDOR}/packages/grapher/dist"
readonly ESM_BUNDLE="${DIST}/embed.js"
readonly GLOBAL_BUNDLE="${DIST}/embed.global.js"
readonly STAGED_BUNDLE="${DIST}/embed.standalone.js"
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

[[ -s "${ESM_BUNDLE}" ]] || fail "Grapher build did not produce ${ESM_BUNDLE}"
[[ -s "${GLOBAL_BUNDLE}" ]] || fail "Grapher build did not produce ${GLOBAL_BUNDLE}"
[[ -s "${LICENSE}" ]] || fail "upstream MIT license is missing"

# MesTTo intentionally emits both a small ESM entrypoint (which imports a generated
# sibling chunk) and a self-contained browser IIFE. MeTTafy's static Pages artifact
# deploys the self-contained form so a single attributed file is sufficient at runtime.
cp "${GLOBAL_BUNDLE}" "${STAGED_BUNDLE}"

[[ -s "${STAGED_BUNDLE}" ]] || fail "failed to stage standalone Grapher bundle"

echo "MeTTaScript Grapher verified"
echo "  commit:     ${actual_commit}"
echo "  pnpm:       ${actual_pnpm}"
echo "  esm entry:  $(sha256sum "${ESM_BUNDLE}" | cut -d' ' -f1)"
echo "  standalone: $(sha256sum "${STAGED_BUNDLE}" | cut -d' ' -f1)"

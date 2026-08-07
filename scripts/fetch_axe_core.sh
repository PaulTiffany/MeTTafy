#!/usr/bin/env bash
set -euo pipefail

VERSION="4.12.1"
URL="https://registry.npmjs.org/axe-core/-/axe-core-${VERSION}.tgz"
EXPECTED_INTEGRITY="s7iGf5GaVMxEG0ENN9x+xTr7GFZCb1ZP/1uATUpCEK2X78nDB3RwbtFCo9pGAf9ru+VwoQ464DkaLEeRM08wJA=="
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/_vendor/axe-core"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

curl --fail --silent --show-error --location "${URL}" --output "${TMP}/axe-core.tgz"
actual="$(openssl dgst -sha512 -binary "${TMP}/axe-core.tgz" | base64 -w0)"
if [[ "${actual}" != "${EXPECTED_INTEGRITY}" ]]; then
  echo "axe-core integrity mismatch" >&2
  echo "expected: ${EXPECTED_INTEGRITY}" >&2
  echo "actual:   ${actual}" >&2
  exit 1
fi

mkdir -p "${DEST}"
tar -xzf "${TMP}/axe-core.tgz" -C "${TMP}"
install -m 0644 "${TMP}/package/axe.min.js" "${DEST}/axe.min.js"
install -m 0644 "${TMP}/package/LICENSE" "${DEST}/LICENSE"
printf '%s\n' "${VERSION}" > "${DEST}/VERSION"
printf '%s\n' "${EXPECTED_INTEGRITY}" > "${DEST}/NPM-SHA512"

echo "axe-core witness dependency verified"
echo "  version: ${VERSION}"
echo "  npm sha512: ${EXPECTED_INTEGRITY}"
echo "  axe.min.js sha256: $(sha256sum "${DEST}/axe.min.js" | cut -d' ' -f1)"

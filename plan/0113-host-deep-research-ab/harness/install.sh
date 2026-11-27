#!/usr/bin/env bash
# Materialize the pinned OpenCode release into .prefix/ and prove its digest and
# version. The archive and the extracted binary are both checked; the archive
# digest is the release's own SHA256SUMS line, and the binary digest is the
# value the draws' pre-flight reads.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=pin.env
source "$here/pin.env"

download=$here/.download
prefix=$here/.prefix
url="$OPENCODE_BASE_URL/$OPENCODE_TAG"

mkdir -p "$download" "$prefix"

if [ -x "$prefix/opencode" ] && "$here/preflight.sh" >/dev/null 2>&1; then
  echo "install: pinned binary already present in $prefix"
  "$here/preflight.sh"
  exit 0
fi

if [ ! -s "$download/SHA256SUMS" ]; then
  curl -fsSL -o "$download/SHA256SUMS" "$url/SHA256SUMS"
fi
if [ ! -s "$download/$OPENCODE_ASSET" ]; then
  curl -fsSL -o "$download/$OPENCODE_ASSET" "$url/$OPENCODE_ASSET"
fi

(
  cd "$download"
  grep "  $OPENCODE_ASSET\$" SHA256SUMS | sha256sum -c -
)

rm -rf "$prefix"
mkdir -p "$prefix"
tar -xzf "$download/$OPENCODE_ASSET" -C "$prefix"

"$here/preflight.sh"

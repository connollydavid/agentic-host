#!/usr/bin/env bash
# The draw pre-flight: the pinned binary's digest and version, checked before
# every draw. `--check digest` and `--check version` isolate the two branches so
# the probe can prove each rejection on its own; the default checks both.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=pin.env
source "$here/pin.env"

bin="$here/.prefix/opencode"
check=all

while [ $# -gt 0 ]; do
  case "$1" in
    --bin)
      [ $# -ge 2 ] || { echo "usage: preflight.sh [--bin PATH] [--check all|digest|version]" >&2; exit 2; }
      bin=$2
      shift 2
      ;;
    --check)
      [ $# -ge 2 ] || { echo "usage: preflight.sh [--bin PATH] [--check all|digest|version]" >&2; exit 2; }
      check=$2
      shift 2
      ;;
    *)
      echo "usage: preflight.sh [--bin PATH] [--check all|digest|version]" >&2
      exit 2
      ;;
  esac
done

case "$check" in
  all | digest | version) ;;
  *)
    echo "usage: preflight.sh [--bin PATH] [--check all|digest|version]" >&2
    exit 2
    ;;
esac

if [ ! -f "$bin" ]; then
  echo "preflight: REJECT binary missing: $bin" >&2
  exit 1
fi

if [ "$check" != "version" ]; then
  got_digest=$(sha256sum "$bin" | awk '{print $1}')
  if [ "$got_digest" != "$OPENCODE_BINARY_SHA256" ]; then
    echo "preflight: REJECT digest: $bin is $got_digest, pinned $OPENCODE_BINARY_SHA256 ($OPENCODE_TAG)" >&2
    exit 1
  fi
fi

if [ "$check" != "digest" ]; then
  got_version=$("$bin" --version 2>&1 | head -n 1)
  if [ "$got_version" != "$OPENCODE_VERSION" ]; then
    echo "preflight: REJECT version: $bin reports '$got_version', pinned '$OPENCODE_VERSION' ($OPENCODE_TAG)" >&2
    exit 1
  fi
fi

echo "preflight: ok $OPENCODE_TAG digest=$OPENCODE_BINARY_SHA256 version=$OPENCODE_VERSION"

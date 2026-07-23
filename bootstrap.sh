#!/bin/bash
# Fresh-clone seed for agentic-host (plan/0074).
#
# This script does one thing the generic orchestrator cannot do for this project:
# seed host-lifecycle itself. agentic-host materializes host-lifecycle as one of
# its own components, so the materializer cannot be served from what it
# materializes; the pin recorded in .host-software is the authority for which
# revision to seed. Everything after the seed is generic and belongs to the tool:
# submodules, materialize, skill links, the gating build, the commit hooks, the
# re-deriver on PATH, then the completeness gate.
#
# A normal adopter installs a released host-lifecycle and runs
# `host-lifecycle bootstrap <dir>` directly; no wrapper is needed there.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
REV=$(awk '/\[software "host-lifecycle"\]/{f=1} f && /pin/{print $3; exit}' "$DIR/.host-software")
if [ -z "$REV" ]; then
    echo "bootstrap: no host-lifecycle pin in .host-software" >&2
    exit 2
fi

echo "seed     host-lifecycle @ $REV (the recorded pin)"
# --force, because `cargo install` exits 0 having installed NOTHING when a package
# of the same version is already tracked at this root. The one thing this wrapper
# exists to guarantee is that the materializer is the recorded revision, so it
# reinstalls rather than trusting whatever is already there.
cargo install --force --git https://github.com/connollydavid/host-lifecycle --rev "$REV" --root "$HOME/.local"

BIN="$HOME/.local/bin/host-lifecycle"
if [ ! -x "$BIN" ]; then
    echo "bootstrap: the seed did not produce $BIN" >&2
    exit 1
fi

exec "$BIN" bootstrap "$DIR"

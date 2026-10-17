#!/bin/bash
# Fresh-clone seed for agentic-host (plan/0074).
#
# This script does one thing the generic orchestrator cannot do for this project:
# seed host-lifecycle itself. agentic-host materializes host-lifecycle as one of
# its own components, so the materializer cannot be served from what it
# materializes; the pin recorded in .host-software is the authority for which
# revision to seed. Everything after the seed is generic and belongs to the tool:
# submodules, materialize, skill links, the commit hooks, the re-deriver on PATH,
# then the completeness gate.
#
# Two steps the orchestrator defers, this wrapper finishes (recorded in
# MEMORY.md, 2026-10-17): the gating build and the PATH link for host-lint.
# The tool proves the canonical artifact in its recorded container and will not
# build ambiently (bootstrap.rs prints "owed"), but the hooks only need an
# honest local build of the pin — install-hooks itself reports local provenance
# as an informational note — so the wrapper builds it and links it, because
# nothing else puts the lint on PATH (cargo installs host-lifecycle and
# host-prove, never host-lint).
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

# The orchestrator's pass is idempotent but ends red on a fresh clone: it
# defers the gating artifact and so cannot install hooks yet (its own gate
# reports both). Do not abort on its exit; the completeness gate at the end
# is this script's exit truth.
set +e
"$BIN" bootstrap "$DIR"
set -e

GATE="$DIR/software/host-lint/main/target/x86_64-unknown-linux-musl/release/host-lint"
if [ ! -x "$GATE" ]; then
    echo "step     build the gating artifact locally (an honest build of the pin; the canonical hash stays the container's to prove, via software --verify-build)"
    rustup target add x86_64-unknown-linux-musl
    # The seed install above warms the cargo and git caches (same host-grammar
    # rev), so --offline holds; a cold cache is the one case it cannot, so fall
    # back to an online build rather than failing the setup.
    (cd "$DIR/software/host-lint/main" && \
        RUSTUP_TOOLCHAIN=stable CARGO_INCREMENTAL=0 cargo build --release --locked --offline --target x86_64-unknown-linux-musl) || \
    (echo "         offline build failed (cold cache); retrying online" && \
        cd "$DIR/software/host-lint/main" && \
        RUSTUP_TOOLCHAIN=stable CARGO_INCREMENTAL=0 cargo build --release --locked --target x86_64-unknown-linux-musl)
    if [ ! -x "$GATE" ]; then
        echo "bootstrap: the gating artifact did not build at $GATE" >&2
        exit 1
    fi
    # The orchestrator's pass could not gate anything (no artifact); gate now.
    echo "step     install the commit hooks (host repository and every materialized worktree)"
    "$BIN" software --install-hooks "$DIR"
fi

# PATH link: tracks the worktree's build of the pin, so a rebuild refreshes it
# and a cargo clean leaves it dangling until the next bootstrap re-run repairs
# it. The canonical-hash discipline is attested separately (--verify-build);
# this link serves scanning.
echo "step     link host-lint onto PATH"
mkdir -p "$HOME/.local/bin"
ln -sfn "$GATE" "$HOME/.local/bin/host-lint"

exec "$BIN" software --verify-setup "$DIR"

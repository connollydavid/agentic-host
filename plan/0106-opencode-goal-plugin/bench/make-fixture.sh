#!/usr/bin/env bash
# Build the ready-frontier state fixture in a scratch git project (plan/0106 #stage-kit).
# Runs under WSL bash; needs git and a host-lifecycle binary (HL_BIN).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
HL_BIN="${HL_BIN:-/mnt/c/Users/dconnolly/Development/agentic-host/software/host-lifecycle/main/target/x86_64-unknown-linux-musl/release/host-lifecycle}"
FIXTURE_DIR="${FIXTURE_DIR:-$(mktemp -d /tmp/fixture-ready-frontier-XXXXXX)}"

mkdir -p "$FIXTURE_DIR/plan/0001-smoke"
cd "$FIXTURE_DIR"

cat > PLAN.md <<'EOF'
# PLAN

| Plan | Status |
|---|---|
| [plan/0001-smoke](plan/0001-smoke/README.md) | cut 2026-10-29, in build (the kit fixture milestone). |
EOF

cat > plan/0001-smoke/README.md <<'EOF'
# plan/0001-smoke: the fixture milestone

**Status: cut 2026-10-29, in build** (the A/B kit's ready-frontier fixture; not real work).

## Why

One mechanical task with a verify line, so the loop's continuation prompt has a real
NEXT line to answer and the rubric has a real receipt to expect.

## Build sequence

### Run the smoke verify {#smoke}

- verify: echo smoke-ok
- inputs: README.md
EOF

git init -q
git config user.name "fixture"
git config user.email "fixture@local"
git add -A
git commit -qm "fixture: the ready-frontier state"

"$HL_BIN" goal set plan/0001-smoke .
"$HL_BIN" goal show . > emission.txt
"$HL_BIN" tasks . > tasks.txt || true

echo "FIXTURE_DIR=$FIXTURE_DIR"
echo "--- emission ---"
cat emission.txt

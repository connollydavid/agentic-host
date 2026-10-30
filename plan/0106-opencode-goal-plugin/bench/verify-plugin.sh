#!/usr/bin/env bash
# The plan/0106 #prototype live verify (bench/README.md's channel discipline applies
# to whatever model the caller points at; credentials arrive via the environment and
# are never written to disk).
#
#   HOST_LIFECYCLE_BIN=<a host-lifecycle binary> \
#   OPENCODE_BIN=<an opencode 2.x binary> \
#   HOST_LOOP_MODEL=<provider/model> \
#   TOKENHUB_KEY=<the provider key, exported, never echoed> \
#   bash verify-plugin.sh
#
# Builds a fresh ready-frontier fixture, registers the plan-room plugin by file://
# URL in a scratch opencode.json, isolates XDG state into the fixture, and runs one
# /host-goal turn headlessly. The loop's continuations, tool calls, and stop reasons
# land in the fixture's run.log; the receipts land in the fixture's ledger.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
: "${HOST_LIFECYCLE_BIN:?set HOST_LIFECYCLE_BIN}"
: "${OPENCODE_BIN:?set OPENCODE_BIN}"
: "${HOST_LOOP_MODEL:?set HOST_LOOP_MODEL, e.g. opencode/glm-5.3-flash-free}"
# TOKENHUB_KEY is optional: set it only for the tencent models; the opencode
# gateway models (the catalog plus the auth store) need no key at all.

PLUGIN_URL="file:///mnt/c/Users/dconnolly/Development/agentic-host/plan/0106-opencode-goal-plugin/plugin"

FIX="$("${HERE}/make-fixture.sh" | grep '^FIXTURE_DIR=' | cut -d= -f2)"
if [ -n "${TOKENHUB_KEY:-}" ]; then
  cat > "${FIX}/opencode.json" <<EOF
{
  "\$schema": "https://opencode.ai/config.json",
  "plugins": ["${PLUGIN_URL}"],
  "model": "${HOST_LOOP_MODEL}",
  "provider": {
    "tencent": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "tencent",
      "options": {
        "baseURL": "https://tokenhub-intl.tencentcloudmaas.com/plan/v3",
        "apiKey": "{env:TOKENHUB_KEY}"
      },
      "models": {
        "glm-5.2": { "name": "GLM-5.2" },
        "kimi-k2.6": { "name": "Kimi-K2.6" }
      }
    }
  }
}
EOF
else
  # The catalog-served models (the opencode gateway) need only the auth store.
  printf '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugins": ["%s"],\n  "model": "%s"\n}\n' "${PLUGIN_URL}" "${HOST_LOOP_MODEL}" > "${FIX}/opencode.json"
fi
if [ -n "${ROPE_BEARER:-}" ]; then
  # The rope router (Fen's channel): qwen3.5-4b over the WAN edge, the bearer
  # env-only, never echoed, never committed.
  python3 - "${FIX}" <<'PYEOF'
import json, sys, pathlib
fix = pathlib.Path(sys.argv[1])
cfg = json.loads((fix / "opencode.json").read_text())
cfg["provider"] = {"rope": {"npm": "@ai-sdk/openai-compatible", "name": "rope router",
  "options": {"baseURL": "https://api.d07yx58.net/v1", "apiKey": "{env:ROPE_BEARER}"},
  "models": {"qwen3.5-4b": {"name": "Qwen3.5-4B (rope text)", "limit": {"context": 65536, "output": 8192}}}}}
(fix / "opencode.json").write_text(json.dumps(cfg, indent=2))
PYEOF
fi

echo "fixture: ${FIX}"
cd "${FIX}"
# A second task, dependent on the first, so the frontier still holds work after the
# first turn: the idle continuation must fire with an armed goal and remaining work.
# SECOND_VERIFY overrides the verify command ("false" is the forcing shape; a passing
# command is the #fen work acceptance). DIRTY_START=1 leaves the tree dirty, which
# reads NEEDS YOU non-none at the first orientation: the stop-half acceptance.
cat >> plan/0001-smoke/README.md <<EOF

### Run the second verify {#second}

- depends: plan/0001#smoke
- verify: ${SECOND_VERIFY:-false}
EOF
git add -A && git commit -qm "fixture: the second task"
if [ -n "${DIRTY_START:-}" ]; then echo "uncommitted" >> tasks.txt; fi
if [ -n "${NEEDS_YOU_START:-}" ]; then
  # The unresolved-closure state (the #37 shape): a complete receipt whose Status
  # write never landed reads NEEDS YOU non-none at the first orientation. Fixture
  # construction, not governance: the state exists so the stop half is measurable.
  printf "\n[receipt \"goal\" \"complete\"]\n    disposition = done\n    target = plan/0001-smoke\n" >> .host-lifecycle-receipts
fi
DATA=$(mktemp -d /tmp/verify-data-XXXXXX)
mkdir -p "$DATA/config" "$DATA/share"
export XDG_CONFIG_HOME="$DATA/config"
export XDG_DATA_HOME="$DATA/share"
export VERIFY_DATA="$DATA"
export HOST_LIFECYCLE_BIN
"${OPENCODE_BIN}" run --standalone --print-logs -m "${HOST_LOOP_MODEL}" "/host-goal" 2>&1 | tee run.log
echo "--- ledger after the run ---"
tail -5 .host-task-receipts 2>/dev/null || echo "(no receipts recorded)"
echo "FIXTURE_DIR=${FIX}"
echo "VERIFY_DATA=${VERIFY_DATA}"

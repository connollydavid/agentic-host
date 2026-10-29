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
: "${HOST_LOOP_MODEL:?set HOST_LOOP_MODEL, e.g. tencent/glm-5.2}"
: "${TOKENHUB_KEY:?export TOKENHUB_KEY (never committed, never echoed)}"

PLUGIN_URL="file:///mnt/c/Users/dconnolly/Development/agentic-host/plan/0106-opencode-goal-plugin/plugin"

FIX="$("${HERE}/make-fixture.sh" | grep '^FIXTURE_DIR=' | cut -d= -f2)"
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

echo "fixture: ${FIX}"
cd "${FIX}"
mkdir -p xdg-config xdg-data
export XDG_CONFIG_HOME="${FIX}/xdg-config"
export XDG_DATA_HOME="${FIX}/xdg-data"
export HOST_LIFECYCLE_BIN
"${OPENCODE_BIN}" run -m "${HOST_LOOP_MODEL}" "/host-goal" 2>&1 | tee run.log
echo "--- ledger after the run ---"
tail -5 .host-task-receipts 2>/dev/null || echo "(no receipts recorded)"
echo "FIXTURE_DIR=${FIX}"

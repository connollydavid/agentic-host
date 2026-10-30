#!/usr/bin/env bash
# The plan/0106 tier-2 harness: real headless OpenCode 2.2.2 runs asserting the
# host-ledger effects (receipt stanzas, GOAL.md, the sidecar), the loop bounds, and
# the printed stop reasons. Scenarios build isolated fixtures in known states; every
# assertion prints ok/MISS and the summary is the exit code.
#
#   HOST_LIFECYCLE_BIN=<binary> OPENCODE_BIN=<2.x binary> \
#   HOST_LOOP_MODEL=<provider/model> [TOKENHUB_KEY=...] bash tier2.sh
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
: "${HOST_LIFECYCLE_BIN:?set HOST_LIFECYCLE_BIN}"
: "${OPENCODE_BIN:?set OPENCODE_BIN}"
: "${HOST_LOOP_MODEL:?set HOST_LOOP_MODEL}"

CHECKS=0
FAILS=0
ok() { echo "  ok  $1"; CHECKS=$((CHECKS + 1)); }
bad() { echo "  MISS $1"; FAILS=$((FAILS + 1)); }
has() { grep -q "$2" "$1" 2>/dev/null && ok "$3" || bad "$3"; }
lacks() { grep -q "$2" "$1" 2>/dev/null && bad "$3" || ok "$3"; }
count_is() { local n; n=$(grep -c "$2" "$1" 2>/dev/null || true); [ "${n:-0}" -eq "$3" ] && ok "$4 (n=$n)" || bad "$4 (n=$n, want $3)"; }
report_disk() { # $1 fixture — the run's cost observables: the log volume and the
  # git-spawn count (the snapshot storm's signature)
  echo "  (run.log: $(du -h "$1/run.log" 2>/dev/null | cut -f1) | git spawns: $(grep -c 'spawning process" command=git' "$1/run.log" 2>/dev/null))"
}

run_session() { # $1 fixture. The server's data dir lives OUTSIDE the fixture: the
  # snapshot machinery commits the observed tree per step, so a data dir inside the
  # worktree feeds itself (the 23G explosion, a harness-design lesson recorded in
  # the plan README). A watchdog still kills the run if storage passes 1G.
  cd "$1"
  local data
  data=$(mktemp -d /tmp/tier2-data-XXXXXX)
  # The pinned binary on the session's PATH: the model's own `host-lifecycle`
  # calls run the recorded pin (the receipts' tool= line is the proof).
  mkdir -p bin
  ln -sf "${HOST_LIFECYCLE_BIN}" bin/host-lifecycle
  XDG_CONFIG_HOME="$data/config" XDG_DATA_HOME="$data/share" \
    HOST_LIFECYCLE_BIN="$HOST_LIFECYCLE_BIN" \
    PATH="$1/bin:${PATH}" \
    "${OPENCODE_BIN}" run --standalone --print-logs -m "${HOST_LOOP_MODEL}" "/host-goal" > run.log 2>&1 &
  local pid=$!
  (
    while kill -0 "$pid" 2>/dev/null; do
      sz=$(du -sk "$data" 2>/dev/null | cut -f1)
      [ "${sz:-0}" -gt 1048576 ] && {
        echo "[tier2] watchdog: the server storage passed 1G; killing the runaway run" >> run.log
        kill "$pid" 2>/dev/null
        break
      }
      sleep 5
    done
  ) &
  local watchdog=$!
  wait "$pid" 2>/dev/null
  kill "$watchdog" 2>/dev/null
  rm -rf "$data"
  return 0
}

fixture() { # prints the fixture dir; $1 = the second task's verify command ("" = none)
  local fix
  fix="$("${HERE}/make-fixture.sh" | grep '^FIXTURE_DIR=' | cut -d= -f2)"
  if [ -n "${1:-}" ]; then
    cat >> "${fix}/plan/0001-smoke/README.md" <<EOF

### Run the second verify {#second}

- depends: plan/0001#smoke
- verify: ${1}
EOF
    cd "${fix}" && git add -A && git commit -qm "fixture: the second task"
  fi
  printf '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugins": ["file:///mnt/c/Users/dconnolly/Development/agentic-host/plan/0106-opencode-goal-plugin/plugin"],\n  "model": "%s"\n}\n' "${HOST_LOOP_MODEL}" > "${fix}/opencode.json"
  echo "${fix}"
}

register_provider() { # the tencent block only when the key is handed over
  if [ -n "${TOKENHUB_KEY:-}" ]; then
    python3 - "$1" <<'EOF'
import json, sys, pathlib
fix = pathlib.Path(sys.argv[1])
cfg = json.loads((fix / "opencode.json").read_text())
cfg["provider"] = {"tencent": {"npm": "@ai-sdk/openai-compatible", "name": "tencent",
  "options": {"baseURL": "https://tokenhub-intl.tencentcloudmaas.com/plan/v3", "apiKey": "{env:TOKENHUB_KEY}"},
  "models": {"glm-5.2": {"name": "GLM-5.2"}, "kimi-k2.6": {"name": "Kimi-K2.6"}}}}
(fix / "opencode.json").write_text(json.dumps(cfg, indent=2))
EOF
  fi
}

echo "=== scenario A: the success path, the host-ledger effects ==="
FIX="$(fixture "echo second-ok")"
register_provider "${FIX}"
run_session "${FIX}"
# The outcome asserts, not the turn shape: the model may discharge both tasks in
# the command turn itself (no admission needed); the ledger effects are the claim.
count_is "${FIX}/.host-task-receipts" "disposition = done" 2 "two done receipt stanzas landed"
has "${FIX}/.host-task-receipts" 'plan/0001#smoke' "the smoke stanza is in the ledger"
has "${FIX}/.host-task-receipts" 'plan/0001#second' "the second stanza is in the ledger"
has "${FIX}/GOAL.md" "plan/0001-smoke" "GOAL.md carries the active goal"
has "${FIX}/.host-goal" "target = plan/0001-smoke" "the sidecar carries the claim"
has "${FIX}/run.log" "host-loop. boot: seam ok" "the boot probe exercised the seam"
report_disk "${FIX}"

echo "=== scenario B: the parked hold, silence and the surfaces ==="
FIX="$(fixture "")"
register_provider "${FIX}"
(cd "${FIX}" && "${HOST_LIFECYCLE_BIN}" goal park --reason "tier2 hold" .) > /dev/null
run_session "${FIX}"
lacks "${FIX}/run.log" "admit #" "a parked goal dispatches nothing"
has "${FIX}/run.log" "host-loop. boot: seam ok" "the boot probe still reads the parked surface"
has "${FIX}/.host-goal" "target = plan/0001-smoke" "the sidecar claim stands"
has "${FIX}/GOAL.md" "plan/0001-smoke" "GOAL.md stands"
report_disk "${FIX}"

echo "=== scenario C: the cap fails closed, the printed reason ==="
# The second task cannot pass, so the frontier holds work at the idle boundary
# and the cap check is reached (the refusal line prints only then).
FIX="$(fixture "false")"
register_provider "${FIX}"
# The config-plumbed cap (the plugins entry's options), the path that reaches the
# plugin where the env does not (the tier-2 env-contract finding).
python3 - "${FIX}" <<'PYEOF'
import json, sys, pathlib
fix = pathlib.Path(sys.argv[1])
cfg = json.loads((fix / "opencode.json").read_text())
url = cfg["plugins"][0]
cfg["plugins"] = [{"package": url, "options": {"maxIterations": 0}}]
(fix / "opencode.json").write_text(json.dumps(cfg, indent=2))
PYEOF
cd "${FIX}"
DATA=$(mktemp -d /tmp/tier2-data-XXXXXX)
XDG_CONFIG_HOME="$DATA/config" XDG_DATA_HOME="$DATA/share" \
  HOST_LIFECYCLE_BIN="$HOST_LIFECYCLE_BIN" \
  "${OPENCODE_BIN}" run --standalone --print-logs -m "${HOST_LOOP_MODEL}" "/host-goal" > run.log 2>&1
rm -rf "$DATA"
has "${FIX}/run.log" "HOST_LOOP_MAX_ITERATIONS is not a positive integer; refusing to arm" "the unknown cap prints its refusal"
lacks "${FIX}/run.log" "admit #" "a refused cap admits nothing"
report_disk "${FIX}"

echo "=== scenario D: the ready-but-failing task, the integrity of the ledger ==="
FIX="$(fixture "false")"
register_provider "${FIX}"
run_session "${FIX}"
has "${FIX}/run.log" "admit #" "the loop admitted onto the failing frontier"
has "${FIX}/run.log" "cannot pass\|refused\|exit 1\|failed" "the model reported the failing verify"
lacks "${FIX}/.host-task-receipts" 'plan/0001#second' "no false receipt for the failing task"
count_is "${FIX}/.host-task-receipts" "disposition = done" 1 "only the honest receipt landed"
has "${FIX}/GOAL.md" "plan/0001-smoke" "the goal stands uncompleted"
report_disk "${FIX}"

echo "=== summary: ${CHECKS} ok, ${FAILS} MISS ==="
# The fixtures stay on disk: they are the evidence; the watchdog guards their size.
[ "${FAILS}" -eq 0 ]

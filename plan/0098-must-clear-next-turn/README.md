# plan/0098 must-clear-next-turn: the lanes' outcomes enforce at the turn boundary

Operator-directed ("do we have an effective must-clear-CI-failures-on-next-turn?
I am getting too many emails from agentic-* host folders" — ruling: go). The
honest answer at the ask: **no**. The per-turn duty was prose; the judge ran only
when remembered; the witness lane disclosed without obligating; and GitHub's
notification emails did the only tripwire work — email does not drive an agent
loop. This plan wires the judge to the turn boundary.

## The design, as built

Two ZCode hooks in this workspace's `.zcode/config.json` (machine-local, like the
MCP registration; the adopter pattern is the same config in each host), both
calling the shipped judge:

- **SessionStart** — `host-lifecycle ci .` runs read-only and its findings ride
  the session context as `additionalContext`: the turn's first fact is the
  lanes' state, with run URLs. A red lane cannot be discovered late.
- **Stop** — `host-lifecycle ci . --gate` gates the turn's end: every discovered
  lane must carry a receipt at the judged revision. Absence and staleness block
  the stop (the model is pulled back to record or fix); a **receipted failure
  passes the gate** — the receipt is the blocker record, the fix rides the next
  turn, and the session-start context carries it until then. The witness
  pattern holds: the judge discloses; it never reddens a build.

The gate mode ships in host-lifecycle v0.57.0 (c93076bb, artifact
43a2959bf3ec7731b9f20705afb99ba27231c7f1b1d71aa3c3c682cadfe5564d, feature
class): `ci <dir> --gate` counts only lanes without a receipt at the judged
revision; the full judge (default) still names receipted failures beside them.

## The cascade

The forge adopted v0.57.0 in the same motion (the pin, the template's prose rev
and tools submodule, the receipt), with the pin/artifact replaces anchored by
regex against the file's actual current values after the earlier silent no-op
lesson. Lint's v0.22.4 tag run (its kani rung) records the lint lane's receipt
when it concludes.

## Results

Recorded at closure.

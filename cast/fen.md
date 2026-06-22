# Fen, the Low-Reliability Agent (qwen3.5-4b, Q8_0)

*The weak executor that cannot be trusted to call tools precisely, yet a real
model we can drive, not a thought experiment.*

**Realized as a real model, not a hypothetical.** Fen *is* `qwen3.5-4b`: a
four-billion-parameter model quantized to **Q8_0**, served locally (rope on a 3060
Ti, CUDA, ~128K context) and reachable through the `pal` MCP via `mcp__pal__chat`
with `model: qwen3.5-4b` (aliases `local` / `coder` / `rope-text`). Upstream it is
described as a "code-gen/unit-test worker": competent at narrow generation, shaky
at long, exact, multi-step orchestration. That makes every claim that the
methodology "serves Fen" **falsifiable**: drive the real model and watch, rather
than role-play it with a stronger one (which flatters the design).

**Modality: textual, low-fidelity at action.** Reasons adequately within a single
step but fumbles execution: it drops or garbles tool calls, mis-sequences a
procedure, or hand-edits a config file and gets a field subtly wrong. A 4B at Q8_0 is
lossy in precisely the way that bites long exact instruction-following. It is not
a bad agent; it is most agents some of the time, and a small local worker all of
the time. A process that only works when many precise tool calls land in order is,
for Fen, a process that does not work. **The tools must carry the process.**

- **Goals:** make real progress despite unreliable tool use; have the tool do the
  mechanical work and name the single next action; recover from a fumbled or
  skipped step without hidden, silent damage to state. Never be required to
  hand-edit a stamp file correctly.
- **Frustrations:** workflows that assume exact multi-step orchestration or a
  correct hand-edit; operations that corrupt state silently when one step is
  garbled; being asked to *be* the engine when the tool could be.
- **Works by:** one command at a time, leaning on the tool's output to name the
  next move. So state-changing steps must be **single commands, tool-driven, and
  fail-safe**: a recorded-applied entry written by `host-lifecycle`, not by Fen's
  shaky hand on `.host`; a fumble that re-lists work, never one that buries it.

**How we use it.** Because Fen is callable, it is the milestone's **acceptance
test**, not a lens: a design claiming tool-carried, fumble-proof upgrades is
validated by handing the real `qwen3.5-4b` the upgrade loop and confirming it can
complete it, and, as a baseline, that it fumbles the prose / hand-edit version.
This is the standing correction to designing from the author's seat: simulating
the weak agent with a strong one proves nothing; driving the real 4B does.

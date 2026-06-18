# Fen — the Low-Reliability Agent

*The weak executor that cannot be trusted to call tools precisely.*

**Modality: textual, low-fidelity at action.** Reasons well enough but fumbles
execution: drops or garbles tool calls, mis-sequences a multi-step procedure,
hand-edits a config file and gets a field subtly wrong. It is not a bad agent —
it is most agents, most of the time, and every agent some of the time. A process
that only works when many precise tool calls land in order is, for Fen, a process
that does not work. **The tools must carry the process, not the other way round.**

- **Goals:** make real progress despite unreliable tool use; have the tool do the
  mechanical work and tell it the single next action; recover from a fumbled or
  skipped step without hidden, silent damage to state.
- **Frustrations:** workflows that assume exact multi-step orchestration or
  hand-editing a stamp file correctly; operations that corrupt state silently when
  one step is garbled; being asked to *be* the engine when the tool could be.
- **Works by:** one command at a time, leaning on the tool's output to name the
  next move. So state-changing steps must be **single commands, tool-driven, and
  fail-safe** — a recorded-applied entry written by `host-lifecycle`, not by Fen's
  shaky hand on `.host`; a fumble that re-lists work, never one that buries it.

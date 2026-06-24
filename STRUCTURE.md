# Structure

`agentic-host` is the methodology's meta repo **and** an agentic project instance.
Its rooms:

| W | room | holds |
|---|---|---|
| Who | `cast/` | personas |
| What | with the software | specs (`.allium` / `.tla`), co-located in each component's repo <!-- host-reconcile: spec-path --> |
| When | `plan/` | milestone index and folders (see `PLAN.md`) |
| Where | `software/<name>/main/` | the `host-*` family under development, bare stores with worktrees (`.host-software`) <!-- host-reconcile: where-root --> |
| Why | `call/` | decisions about the software (MADR); **instance-only; binds no adopter**. Settled methodology decisions stay as immutable history, marked `Status: superseded by the spine` |
| How | `CLAUDE.md` + tooling | this repo's manual and the `host-*` tools |

**Adopter boundary.** The normative methodology lives in `host-template/` (the
versioned source you copy-at-version), not in this repo's top-level rooms. This
repo's `call/` is its own Why room; do not read it as normative. See `README.md`.

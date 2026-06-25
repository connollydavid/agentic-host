# Structure

`agentic-host` is the methodology's meta repo **and** an agentic project instance.
Its rooms:

| W | room | holds |
|---|---|---|
| Who | `cast/` | personas |
| What | with the software | specs (`.allium` / `.tla`) at the [spec-home](#spec-home), co-located in each component's repo |
| When | `plan/` | milestone index and folders (see `PLAN.md`) |
| Where | `software/<name>/main/` | the `host-*` [components](#components) under development in the [software-root](#software-root): bare stores with worktrees (`.host-software`) |
| Why | `call/` | decisions about the software (MADR); **instance-only; binds no adopter**. Settled methodology decisions stay as immutable history, marked `Status: superseded by the spine` |
| How | `CLAUDE.md` + tooling | this repo's manual and the `host-*` tools |

**Adopter boundary.** The normative methodology lives in `host-template/` (the
versioned source you copy-at-version), not in this repo's top-level rooms. This
repo's `call/` is its own Why room; do not read it as normative. See `README.md`.

## Concepts

The methodology concepts this project defines once and points at from everywhere else. Each has a stable `{#id}` anchor; other docs link to it rather than restate it.

### Components {#components}

The `host-*` components under development: host-lint, host-lifecycle, host-prove, host-grammar. Each is a bare store with worktrees under `software/<name>/main/`, pinned in `.host-software`. The single-file `host` entrance is set apart (it is the `member` of the `[entrance]` stanza), not a component; agentic-host, the development environment, is not one either.

### Verifiers {#verifiers}

The verification ladder's drivers, base to deep: host-lint (naming hygiene), allium (requirements and property-based testing), specula (bounded timing via TLA+), host-prove (the deeper symbolic, proof, and conformance rungs).

### Software-root {#software-root}

Where the software under development lives: `software/`.

### Spec-home {#spec-home}

Where specifications live: with their software, co-located in each component's repo, never under `plan/`.

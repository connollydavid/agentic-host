# gather-data: naming probe and settled conditionals (2026-07-20 / 2026-07-21)

This records the #gather-data task. The Fen naming probe (2026-07-20) settled the
two names; the remaining conditionals (the receipt kind, the envhash file format,
the env-check and verify-setup exit codes, whether `--check` runs the completeness
gate, the image-digest probe, the spine-change split) are settled below
(2026-07-21), each traced to a row so every conditional in the README has a
grounding. The new issue was filed and #18 reconciled as part of this task.

## Channel

`~/.local/bin/fen-probe` (Unsloth direct, `unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL`),
`max_tokens` 400. Two temperatures (0.2, 0.6) with the option order rotated
between them, so a first-option artifact is detectable. Script
`/tmp/plan0074-naming-probe.sh`; transcripts
`/tmp/plan0074-naming-transcripts.txt`.

## Decision 1: the orchestrator that runs the whole fresh-clone setup

Given the sibling commands (`--materialize` clones worktrees, `--install-hooks`
installs hooks, `--check` verifies pins) and a description of a new all-in-one
command that runs the complete setup, the model chose:

| Candidate | temp 0.2 (order) | temp 0.6 (order) |
|---|---|---|
| **bootstrap** | **A, chosen** | **D, chosen** |
| setup | B | C |
| provision | C | B |
| realize | D | A |

`bootstrap` at both temps. Rotation-proof: it was option A at temp 0.2 and
option D at temp 0.6, chosen both times. The model's reason: "bootstrap is the
standard technical term for initializing a system by running a comprehensive
sequence of setup tasks to make it ready for use."

**Settled: `host-lifecycle bootstrap <dir>`.**

## Decision 2: the gate that checks the setup is complete

Given the sibling checks (`software --check` for pins, `env --check` for drift)
and a description of a new check that fails if any required piece of the setup
is missing, the model chose:

| Candidate | temp 0.2 (order) | temp 0.6 (order) |
|---|---|---|
| **--verify-setup** | **A, chosen** | **C, chosen** |
| --verify-env | B | B |
| --verify-host | C | A |

`--verify-setup` at both temps. Rotation-proof: it was option A at temp 0.2 and
option C at temp 0.6, chosen both times. It reads as "verify the setup is
complete", distinct from `env --check` (drift) and `--check` (pins). The
operator had leaned toward `--verify-env` / `--verify-host`; the 4B bar prefers
`--verify-setup`, and "env" collides with the sibling `env` subcommand.

**Settled: `host-lifecycle software --verify-setup <dir>`.**

## The remaining conditionals (settled 2026-07-21)

Each README "Open design questions" bullet, grounded and settled. Two were
operator decisions (2026-07-21): the envhash format and whether `--check` runs
the completeness gate.

### The receipt kind (#18)

Its own kind. Grounded in the existing writer: `.host-lifecycle-receipts`
stanzas are keyed `[receipt "<phase>" "<component>"]` (see `receipt_stanza`,
src/main.rs), so the materialize receipt is a new phase value —
`[receipt "materialize" "<component>"]` — not a re-opening of the `embed`
recheck. Event-level fields only (disposition, evidence, pin-by-reference,
image reference, tool, recorded), matching the append-only shape the `embed`
receipt already uses.

### The envhash file format (operator decision, 2026-07-21)

**TOML stanzas.** Matches host-lifecycle's state-file idiom (`.host-software`,
`.host-lifecycle-receipts` are both TOML-stanza). Per-input sub-hash as
`[envhash "<dimension>"]` stanzas (worktree paths, hook binary hash, image
digest, submodule init state, repo abspath), so `env --check` diffs
dimension-by-dimension and prints only the moved rows. Rejected: flat
key:value, which would diverge from the idiom for no gain.

### The `env --check` exit code

Advisory, three outcomes: `0` clean (envhash present, no delta), `0` with delta
(envhash present, dimensions moved — prints the route, never fails), `2`
cannot-proceed (no `.host-envhash` on disk — a prompt to materialize, not a
gate failure). Never exit 1; `env --check` is a sanity aid, never a gate (#19's
framing, and Fen's weak-agent trap: it must not read as a gate).

### The completeness-gate exit code

A gate: `0` complete, non-zero HAZARD on any missing required artifact, matching
the `software --check` HAZARD convention. Host-role-aware: a non-build host does
not HAZARD on an absent build artifact (it was never required to build it).

### Does `--check` run the completeness gate? (operator decision, 2026-07-21)

**No — `--verify-setup` stays a distinct invocation.** Consistent with operator
ruling #7 (a separate verify mode) and with `env --check` being separate:
`--check` answers pin-vs-recorded, `env --check` answers drift-from-recorded,
`--verify-setup` answers complete-vs-recipe. `bootstrap` runs `--verify-setup`
as its final self-check; an operator runs it explicitly. Rejected: folding it
into the `--check` sweep, which would couple the recipe-vs-live question into
the pin gate.

### The image-digest probe

Shells to `docker` / `podman inspect` for the locally pulled image digest. With
no container runtime on PATH, the envhash records `runtime = none` for the image
dimension and stays silent on it — `env --check` never reports a moved image
digest it cannot read, and the completeness gate does not HAZARD on it.

### The spine-change split

Methodology (spine, host-template CLAUDE.md): the materialize receipt (#18, a
fourth receipt kind) and the bootstrap-plus-completeness doctrine (a fresh clone
runs `host-lifecycle bootstrap <dir>`, setup completeness is gated not assumed).
Tooling-only (no spine change): the envhash (#19), which is local, gitignored,
and advisory.

## Issue filing and #18 reconciliation (2026-07-21)

- **Filed [#20](https://github.com/connollydavid/host-lifecycle/issues/20)** for
  the bootstrap orchestrator and completeness gate (with Bug A folded in). Title
  linted clean (`host-lint --stdin`, exit 0).
- **Reopened [#18](https://github.com/connollydavid/host-lifecycle/issues/18).**
  It was CLOSED/COMPLETED at the plan-cut timestamp (2026-07-19T15:40) but
  `implement-receipt` is an unbuilt node and no receipt code exists — closed for
  work that had not happened. `release-and-re-pin` closes it when the writer
  ships.

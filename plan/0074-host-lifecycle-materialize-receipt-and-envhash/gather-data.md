# gather-data: the Fen naming probe (2026-07-20)

This records the naming decisions of the #gather-data task. The other
gather-data conditionals (the receipt kind, the envhash file format, the
env-check and verify-setup exit codes, whether `--check` runs the completeness
gate, the image-digest probe) remain open and are settled when gather-data runs
in full; only the two names are settled here, per the operator ruling that Fen
decides them.

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

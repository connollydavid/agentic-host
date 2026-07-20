# plan/0074 formal materialization: provenance, coherence, bootstrap, and completeness for the Where room

Closes [connollydavid/host-lifecycle#18](https://github.com/connollydavid/host-lifecycle/issues/18) and [connollydavid/host-lifecycle#19](https://github.com/connollydavid/host-lifecycle/issues/19), plus a new issue for the formal bootstrap and completeness gate (to be filed at #gather-data). Paired by operator ruling (2026-07-19), then broadened by operator ruling (2026-07-20): the receipt, the envhash, the bootstrap orchestrator, and the completeness gate all share the same materialize / install-hooks call sites and the same Where-room state, so building them together under one explicit non-overlap discipline avoids the duplication that separate plans would risk.

## Why

The fresh-clone materialization of an agentic project is currently unmechanized prose. The spine (host-template CLAUDE.md) and this host's CLAUDE.md describe a sequence of manual steps an agent hand-executes in order: seed the materializer, init submodules, `software --materialize`, link skills, build the gating binary, `--install-hooks`, install the PATH re-derivers, then `software --check`. Prose is not a gate. Steps get skipped silently, and nothing catches it.

The evidence is this repository. During the 2026-07-20 session the host-repo commit hooks were found absent: `--install-hooks` had never been run in the clone, and `software --check` stayed green the whole time, because it verifies pins and receipts but is blind to whether the local environment was actually set up. Four gaps, one root (materialization is realized but neither driven nor verified as a whole):

- **#18 (provenance).** After a clone plus materialize, an operator cannot tell from the audit trail when, where, or by whom the worktrees were last realized, even though the gating binary they then trust was produced by that materialization.
- **#19 (coherence).** After a repo move, a partial `submodule` re-init, an image bump, or an ambient rebuild of the gating binary, the local tree differs from what the operator last touched, with no signal that it moved.
- **Bootstrap (new).** There is no single entrypoint that RUNS the fresh-clone sequence. Each step is prose an agent executes by hand, so a step is skipped and the tree is silently half-materialized.
- **Completeness (new).** There is no gate that asserts the setup COMPLETED. `software --check` passes on a clone whose hooks were never installed, whose PATH re-derivers are absent, or whose skills are unlinked. A companion bug: `--install-hooks` gates only the host repo, leaving every materialized worktree (a real commit surface) with no local tell-gate.

## Scope

Four host-lifecycle concerns, one release, one non-overlap discipline:

1. **The materialize receipt (#18).** An operational receipt in `.host-lifecycle-receipts` written on `software --materialize` (and on a recorded `git submodule update` / checkout that touches the Where room), in the same append-only shape as the `embed` receipt. Records the EVENT.
2. **The environment hash (#19).** A gitignored `.host-envhash`, recomputed on demand, compared by `host-lifecycle env --check`. Records the recorded STATE; advisory, never fails the gate.
3. **The bootstrap orchestrator (new).** A thin, tracked `bootstrap.sh` that does only the self-seed (read the host-lifecycle pin from `.host-software`, `cargo install` it) then delegates to a new, generic, recipe-driven `host-lifecycle bootstrap <dir>` subcommand that RUNS the rest of the sequence idempotently. Drives the sequence.
4. **The completeness gate (new).** A new verify mode (a `software` subcommand; leaf name decided by the Fen naming probe) that reads the RECIPE plus the live tree and HAZARDs when the setup is incomplete: a worktree unmaterialized, a hook uninstalled (host or worktree), a declared re-deriver off PATH, a skill unlinked, host-role-aware. Gates COMPLETENESS. Folds in the worktree-hook fix (Bug A): `--install-hooks` gates every materialized worktree, not just the host repo.

### Not overfit to agentic-host (operator ruling, 2026-07-20)

`bootstrap` and the completeness gate are **generic host-lifecycle capabilities driven by `.host-software`** and the declared rungs, and they serve any adopter with a materialized Where room. The one agentic-host-specific piece is the self-seed: because this host materializes `host-lifecycle` itself (the materializer cannot be served from what it materializes), its `bootstrap.sh` seeds host-lifecycle from the pin before delegating. A normal adopter installs a released host-lifecycle and runs `host-lifecycle bootstrap <dir>` directly, with no self-seed wrapper. Nothing about agentic-host's component set, its musl target, or its host-prove rung is hardcoded; all of it comes from the recipe.

### Operator rulings

**2026-07-19 (original pair):**
1. **Paired in one plan.** The shared call sites are wired once.
2. **Two distinct files.** `.host-lifecycle-receipts` (checked-in provenance) and `.host-envhash` (gitignored coherence). Never the same file.
3. **Two distinct subcommands.** The receipt writes via `software --materialize` (automatic); the envhash reads via `host-lifecycle env --check` (advisory, explicit).
4. **Full methodology.** Gather-data, cast consultation, adversarial review, then build.

**2026-07-20 (the broadening):**
5. **Absorb the bootstrap and completeness gate into this plan.** They share the materialize / install-hooks call sites and the Where-room state; building them here under one discipline avoids the third-feature duplication a separate plan would risk.
6. **Thin script plus tool core.** `bootstrap.sh` does only the self-seed; the mechanized sequence is a tested `host-lifecycle bootstrap` subcommand, not untested shell (the "one command, internalise for weak agents" idiom that folded host-prove's wrappers into its binary).
7. **The completeness gate is a separate verify mode, not folded into `--check`.** It reads the recipe-vs-live completeness question, distinct from the pin-vs-recorded question `--check` already answers and the state-vs-recorded question `env --check` answers.
8. **Spine-aware, do not overfit.** The bootstrap and completeness pattern is spine doctrine (every adopter with a Where room has this problem); agentic-host's self-seed is instance config.
9. **Fen decides the names.** The `bootstrap` orchestrator name and the completeness-gate leaf name are settled by a Fen naming probe in gather-data, not chosen by the author.

## The non-overlap discipline (load-bearing, now three-way)

Four concerns touch the same call sites and the same state. What keeps them from duplicating is that each answers a different question against a different reference point, and defers on every fact another owns:

| Concern | Question | Reference point | Result kind |
|---|---|---|---|
| Receipt (#18) | What happened, by what authority, when? | the event | append-only provenance line |
| Envhash (#19) | Did the tree drift from what I last recorded? | `.host-envhash` (recorded state) | advisory delta, exit 0 |
| Completeness gate (new) | Is the setup complete per the recipe? | `.host-software` (required state) | HAZARD / clean gate |
| Bootstrap (new) | (does not verify) it MAKES the state | the recipe | side effects, then defers verification to the gate |

The event-vs-state field table (receipt vs envhash) stays exactly as designed:

| Fact | Receipt (#18) | Envhash (#19) |
|---|---|---|
| Materialization happened | yes (the event) | no |
| Disposition (done/skip) | yes | **forbidden** |
| Evidence (e.g. "git submodule update --init") | yes | **forbidden** |
| Timestamp | yes | **forbidden** (a digest has no time) |
| Component realized | yes (by name) | yes (by worktree presence) |
| Pin SHA | **reference only** | **never** (pin adherence is `software --check`'s job) |
| Toolchain image reference | yes | no |
| Toolchain image digest | **never** | yes |
| Hook binary hash | **never** | yes |
| Repo abspath | **never** | yes |
| Submodule init state | **never** | yes |

And the completeness gate defers cleanly to all three: it never writes a receipt (it verifies, it does not act), never recomputes the envhash (it reads the recipe and the live tree, not the recorded fingerprint), and never checks pin adherence (that is `software --check`'s row). It owns exactly one question no other concern answers: **is every required local artifact present?**

## The call-site wiring

Every state-changing op writes the receipt and/or the envhash, but the two record orthogonal facts:

- `software --materialize`: writes a materialize receipt (event, components realized, pin-by-reference, image reference, timestamp) and writes `.host-envhash` (worktree paths, hook binary hash, image digest, submodule init state, repo abspath).
- `software --install-hooks`: writes `.host-envhash` (new hook binary hash) and writes **no** receipt. Now gates the host repo AND every materialized worktree (Bug A).
- `software --verify_build`: writes `.host-envhash` (image digest confirmed), no receipt.
- image pull: writes `.host-envhash` only.
- `host-lifecycle bootstrap <dir>`: calls the above ops in sequence, so the receipt and envhash are written by the ops it drives, not by bootstrap itself. Bootstrap adds no new writer.

`host-lifecycle env --check` recomputes the envhash from current state, diffs against the stored one, prints only the delta (advisory). The completeness gate recomputes required-vs-present from the recipe and HAZARDs on any gap. `software --check` reports the envhash state alongside the gate result, never as part of pass/fail; whether `--check` also runs the completeness gate, or the completeness gate stays a separate invocation, is a gather-data question.

## The bootstrap sequence (generic, recipe-driven)

`host-lifecycle bootstrap <dir>` runs, idempotently, whatever the recipe implies (each step a no-op if already satisfied):

1. `git submodule update --init` for the declared tool/template submodules (read from `.gitmodules`).
2. `software --materialize <dir>` for every `.host-software` component (writes the receipt and envhash).
3. link the skill symlinks (the generic form of this host's `link-skills.sh`).
4. build each artifact-bearing component this host is a build host for, at its recorded target.
5. `software --install-hooks <dir>` (host repo plus every worktree, Bug A).
6. install each declared PATH re-deriver (a component the recipe or the declared rungs mark as needing PATH presence for the gate, plan/0048).
7. run the completeness gate as the final self-check.

The thin `bootstrap.sh` (this host only) does the self-seed alone, then `exec host-lifecycle bootstrap .`.

## Open design questions

The gather-data and cast pass rule on these:

- **The names (Fen probe).** The `bootstrap` orchestrator name (candidates: `bootstrap`, `setup`, `provision`, `realize`; `materialize` is taken and is a subset) and the completeness-gate leaf name (candidates: `software --verify-setup`, `software --verify-env`, `software --verify-host`). The Fen probe decides which read at the 4B bar as "runs the setup" and "checks the setup is complete", distinct from `materialize` (clone worktrees), `--check` (pins/receipts), and `env --check` (drift).
- **The receipt kind.** #18's open question: its own kind vs re-opening the `embed` recheck. Our read is its own kind.
- **The envhash format.** TOML (host-lifecycle's idiom) vs flat key:value.
- **The `env --check` exit code.** Advisory: `0` clean, `0` with delta, `2` cannot-proceed (no envhash on disk).
- **The completeness-gate exit code.** A gate: `0` complete, non-zero HAZARD on any missing required artifact (matching the `software --check` HAZARD convention), host-role-aware so a non-build host does not HAZARD on an absent build artifact.
- **Does `--check` run the completeness gate?** Fold it into the existing gate sweep, or keep it a distinct invocation the bootstrap runs and an operator can run explicitly.
- **The image-digest probe.** Reading the locally pulled image digest shells out to docker / podman inspect; with no runtime the envhash records "no runtime" and stays silent on the image dimension.
- **The spine change.** #18 (receipt) and the bootstrap-plus-completeness doctrine are methodology-level. #19 (envhash) is tooling-only.

## Verification

- **Unit tests** for the receipt writer (every field, append-only, no-state-fields), the envhash writer (every dimension, per-input sub-hash, no-event-fields), the bootstrap step planner (each step derived from the recipe, each idempotent), and the completeness gate (each required-artifact class detected present and absent, host-role-aware).
- **Integration tests** for the non-overlap discipline: a single `software --materialize` writes both files sharing no data field by name; the completeness gate writes neither. A test asserts the schema disjointness directly.
- **Integration tests** for `env --check` (a move, a hook rebuild, a submodule toggle, a missing envhash each produce the expected advisory and exit 0) and for the completeness gate (an unmaterialized worktree, an uninstalled host hook, an uninstalled worktree hook, an off-PATH re-deriver, an unlinked skill each HAZARD; a fully bootstrapped tree is clean; a non-build host does not HAZARD on the absent build artifact).
- **Integration test** for bootstrap: on a fixture missing hooks and skills, `host-lifecycle bootstrap` makes the completeness gate go clean, and a second run is a no-op.
- **Allium spec** for the `MaterializeRun`, `EnvHash`, `BootstrapRun`, and `Completeness` entities, the no-overlap invariant (a `Reads` field on one is a `NeverReads` field on the others), the append-only receipt rule, and the worktree-hook coverage invariant (a materialized worktree implies an installed worktree hook after bootstrap). `allium check` + `analyse` + `plan` exit 0; obligations discharged by tests; Kani for the schema disjointness and the worktree-hook coverage invariants.
- **Fen probe** (gather-data.md): the naming probe (above); the `env --check` delta reads as a route (which dimension moved); the completeness-gate HAZARD reads as "install the missing thing", not "your tree drifted"; the receipt, envhash, and completeness gate read as three different concerns, not three names for one.
- **Cast consultation** (cast/*.md): Bly (overstates-completeness; the envhash is NOT an audit and the completeness gate is NOT provenance), Orin (fails-unsafe; a missing envhash is a prompt, the completeness gate is the actual gate, the bootstrap must be idempotent), Fen (weak-agent-trap; `env --check` must not read as a gate, and the completeness gate must not read as drift).
- **Adversarial design review** (design-review.md): five independent lenses, with the duplication risk as a named lens (a reviewer whose sole job is to find overlap among receipt, envhash, and completeness gate) and the overfit risk as a named lens (a reviewer whose job is to find any agentic-host specific baked into the generic bootstrap or gate).
- `host-lifecycle software --check .` clean at the new pin; the host-lifecycle release receipt recorded; #18, #19, and the new issue closed.

## Build sequence

The tasks are anchored receipted nodes (plan/0042), built as a forward graph:

### gather-data {#gather-data}
Grounds the conditionals: the Fen naming probe (bootstrap name, completeness-gate name), the receipt-kind question (#18), the envhash file format, the env-check and completeness-gate exit codes, whether `--check` runs the completeness gate, and the image-digest probe. Files the new issue for the bootstrap plus completeness gate.
- verify by: every conditional in this README traces to a gather-data.md row; the Fen naming probe transcript is recorded
- depends: none

### write-spec {#write-spec}
The `MaterializeRun`, `EnvHash`, `BootstrapRun`, and `Completeness` Allium surface, the no-overlap invariant, the append-only receipt rule, the envhash-is-not-a-receipt rule, the completeness-gate-is-not-drift rule, and the worktree-hook coverage invariant. Lives in the host-lifecycle repo.
- verify by: `allium check` + `allium analyse` exit 0, zero findings
- depends: #gather-data

### write-obligations {#write-obligations}
Every `allium plan` obligation dispositioned in a `<spec>.obligations` manifest. The schema-disjointness and worktree-hook-coverage obligations are Kani harnesses.
- verify by: `host-lifecycle obligations <spec> --tests tests --strict-discharge` clean
- depends: #write-spec

### implement-receipt {#implement-receipt}
The materialize receipt writer: a new entry in `.host-lifecycle-receipts` on `software --materialize`, event-level fields only.
- verify by: `cargo test` green; a materialize run appends exactly one receipt with no state-level data
- depends: #write-obligations

### implement-envhash {#implement-envhash}
The envhash writer and the `env --check` reader: `.host-envhash` (gitignored), written by `--materialize` / `--install-hooks` / `--verify_build` / image pull, read by `env --check`. Per-input sub-hash; advisory exit codes.
- verify by: `cargo test` green; each state-changing op refreshes the envhash; `env --check` prints the delta and exits 0
- depends: #write-obligations

### fix-worktree-hooks {#fix-worktree-hooks}
Bug A: `software --install-hooks` gates every materialized worktree (the dispatch script plus the binary into each worktree's hooks dir), not just the host repo, gating on each worktree at its pin, host-role-aware.
- verify by: `cargo test` green; after `--install-hooks`, a tell-laden commit in a worktree is blocked; a fresh fixture's worktrees are all gated
- depends: #write-obligations

### implement-completeness-gate {#implement-completeness-gate}
The completeness gate (Fen-named): reads the recipe plus the live tree, HAZARDs on any missing required artifact (worktree, host hook, worktree hook, PATH re-deriver, linked skill), host-role-aware. Writes nothing.
- verify by: `cargo test` green; each missing-artifact class HAZARDs; a bootstrapped tree is clean; a non-build host does not HAZARD on the absent build artifact
- depends: #fix-worktree-hooks, #implement-envhash

### implement-bootstrap {#implement-bootstrap}
The generic `host-lifecycle bootstrap <dir>` subcommand (Fen-named): the recipe-driven step planner running submodules / materialize / link-skills / build / install-hooks / install-re-derivers / completeness-gate, idempotently. The thin `bootstrap.sh` (this host) self-seeds then delegates.
- verify by: `cargo test` green; on a fixture missing hooks and skills, `bootstrap` makes the completeness gate clean; a second run is a no-op; `bootstrap.sh` seeds then delegates
- depends: #implement-completeness-gate

### wire-shared-call-sites {#wire-shared-call-sites}
Wire `software --materialize` to write both files in one call; `--install-hooks` / `--verify_build` / image-pull to write `.host-envhash` only. Assert the call-site-level non-overlap: one call site, orthogonal writers, no shared data field; the completeness gate and bootstrap write no data files.
- verify by: a `software --materialize` run produces both artifacts; `--install-hooks` produces only the envhash; a test asserts the wiring writes each file exactly when the design says to
- depends: #implement-receipt, #implement-bootstrap

### write-tests {#write-tests}
Integration tests covering every call site, every envhash dimension, every env-check delta path, every completeness-gate HAZARD class, the bootstrap idempotence, and the schema-disjointness and worktree-hook-coverage properties.
- verify by: full test suite green; Kani proofs of schema disjointness and worktree-hook coverage
- depends: #wire-shared-call-sites

### cast-consult {#cast-consult}
Cast consultation across Mara, Wren, Bly, Orin, Fen on the three-way non-overlap discipline, the bootstrap idempotence, and the overfit boundary. Recorded in design-review.md.
- verify by: each cast persona's concern addressed or recorded as a follow-up
- depends: #write-tests

### adversarial-review {#adversarial-review}
A multi-lens adversarial review with one lens dedicated to overlap among receipt / envhash / completeness gate, and one lens dedicated to any agentic-host specific baked into the generic bootstrap or gate. Findings recorded in design-review.md; the re-cut staged there.
- verify by: every blocking finding fixed or recorded; the re-cut executed
- depends: #cast-consult

### write-spine-doctrine {#write-spine-doctrine}
The host-template CLAUDE.md gains the materialize-receipt doctrine (a fourth receipt kind), the bootstrap doctrine (a fresh clone runs `host-lifecycle bootstrap <dir>`, or a thin self-seed wrapper that delegates to it), and the completeness-gate doctrine (setup completeness is gated, not assumed). No spine doctrine for the envhash (tooling-only, local). An UPGRADING entry keys the new revision.
- verify by: `host-lifecycle upgrade` lists the entry on a pre-revision host; `upgrade --record` clears it
- depends: #adversarial-review

### release-and-re-pin {#release-and-re-pin}
`host-lifecycle release host-lifecycle --change-class adds-flag`, re-pin `.host-software`, record the release receipt, close #18, #19, and the new issue.
- verify by: `host-lifecycle software --check .` clean at the new pin; the issues closed
- depends: #write-spine-doctrine

### fen-acceptance {#fen-acceptance}
The real `qwen3.5-4b` runs `env --check` on a moved repo and a rebuilt hook binary (the delta reads as a route), runs the completeness gate on a half-bootstrapped tree (the HAZARD reads as "install the missing thing"), and distinguishes the receipt, the envhash, and the completeness gate given a one-line description of each. Separately, it drives `bootstrap` on a fresh fixture and confirms the tree goes clean.
- verify by: Fen routes each delta correctly, reads each HAZARD as an install action, distinguishes the three artifacts, and bootstraps a fixture clean
- depends: #release-and-re-pin

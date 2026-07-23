# plan/0074 design-review: the cast reads the built diff

Date: 2026-07-23. Subject: `fd7c632..d3848f2` in host-lifecycle (the materialize receipt, the environment fingerprint, the worktree gate fix, the completeness gate, the orchestrator, the test matrix and the proof).

## Who read it

Mara, Bly, Orin and Wren each read the plan README, the built diff and the sources their own lens calls for, and returned findings with file and line evidence. **Fen was not simulated**: `cast/fen.md` makes Fen a real model rather than a hypothetical, so Fen's consultation is the weak-agent acceptance recorded in [fen-acceptance.md](fen-acceptance.md), which ran the real `qwen3.5-4b` against the built output and caught a real defect (the drift delta read as nothing-to-do). That probe is Fen's contribution to this review.

## What they converged on

Three findings arrived independently from more than one chair, and those are the ones that matter most.

**The completeness gate fails open on any probe it cannot run.** Bly (1, 3), Orin (1). `setup.rs` drops a requirement with `let Some(..) else { continue }` in three places: a hooks-declaring component with no artifact stanza, an unresolvable host hooks directory, an unresolvable worktree hooks directory. A requirement that is never constructed can never be a gap, and the run then prints "setup complete: every artifact the recipe requires of this host is present". Bly reproduced it on a fixture: the installer said it could gate nothing, and the gate said the setup was complete. This is the plan's own founding evidence (hooks absent for two weeks under a green check) reappearing inside the gate built to catch it.

**The gate is blind to work the orchestrator performs.** Bly (2), Orin (12), Wren (3). Bootstrap links skills from worktrees *and* submodules and inits submodules; the gate reads only worktree `skills/` directories and has no submodule requirement at all. On this repo the gate lists ten skill requirements while the tree carries twenty-seven links, and de-initializing every submodule leaves the gate clean. Wren found the sharper edge: `link-skills.sh` also links a component that ships a single root `SKILL.md` (this is how `.claude/skills/host-lint` exists), which bootstrap never creates and the gate never misses, so replacing the script with bootstrap would silently drop that link.

**Bootstrap builds the commit gate with ambient cargo.** Mara (1), Wren (4). The build step shells the recorded `build` string through `sh -c` in the worktree, while the same tool states, seven hundred lines away, that a build is only meaningful inside the digest-pinned toolchain container. On a genuine fresh clone the recorded recipe (musl target, `--offline`, vendored deps) fails and the run dies with no remedy; on a warm machine it succeeds and installs a binary that is not the canonical one, which is the plan/0032-retired workaround reintroduced by an orchestrator.

## The rest of the blocking set

- **The gate and the orchestrator read the recipe through different accessors** (Orin 2). The gate expands per-platform `[build]` subsections; bootstrap reads the flat fields. For an adopter on the form the upgrade ledger tells them to migrate to, bootstrap reports the build step satisfied, the gate hazards on the missing artifact, and re-running never converges.
- **Remedies are not runnable** (Wren 1, 2). Six gate remedies print a literal `<dir>`, and the four drift routes drop the `host-lifecycle` prefix, so they name a subcommand as if it were a binary. The weak-agent transcript shows the model faithfully mirroring both defects.
- **Agentic-host is baked into generic code** (Mara 2, 5, 9; Orin 17; Bly 5; Wren 14). The re-deriver step matches the literal string `host-prove` against `deploy`, which is the deployed-line field rather than the component name, so an adopter who writes `deploy = main` gets the step silently skipped and then hazarded. The fingerprint reads only a binary literally named `host-lint`. The remedies name `link-skills.sh` and `software/host-prove/main`, neither of which exists in an adopter's tree.
- **The materialize receipt dirties a shared tracked file on every clone** (Orin 3). `.host-lifecycle-receipts` is committed; materialize appends to it; bootstrap runs materialize. The instruction the doctrine is about to give every adopter leaves a modified tracked file behind, once per contributor per clone, recording a purely local event.
- **The host's own CLAUDE.md is not a deliverable of any node** (Wren 5). Only the template's spine doctrine is. On release day a cold session reads the seven-step hand sequence and runs it, which is now the wrong sequence.

## The finding that explains the others

Bly (7): `CompleteSetupCoversWorktreeHooks` is dispositioned to a test of the `hooks_installed` helper, which never constructs a run, never calls `verify_setup` and never calls `setup_requirements`. No test anywhere passes a recipe with a hooks-declaring component into `setup_requirements`, so the entire host-and-worktree hook requirement generator, which carries the two blocking gate findings, is uncovered. The strict-discharge check passes because the token appears in the body; body containment cannot tell a helper from the surface under test. Writing the missing test makes both gate findings fail immediately.

## Dispositions

Every blocking finding above is fixed at [#adversarial-review](README.md#adversarial-review), which re-reads the fixed diff, except where noted:

| Finding | Disposition |
|---|---|
| Gate fails open on unreadable probes | Fix: an unreadable probe constructs a requirement that is absent, never omits one |
| Gate blind to submodules and to root-`SKILL.md` skills | Fix: the gate reads the same sources the orchestrator writes |
| Ambient build of the gating binary | Fix: bootstrap does not shell the recorded recipe; it reports the gap with the documented local build |
| Two recipe accessors | Fix: both read through `builds_view()` |
| Remedies not runnable | Fix: interpolate the real root, prefix the binary name |
| Overfit leaks (re-deriver name and field, gate binary name, remedy paths) | Fix: derive from the recipe |
| Materialize receipt dirties a tracked file | Operator decision, carried to the end of this document |
| Host CLAUDE.md not owned by any node | Fix: folded into #write-spine-doctrine, whose scope now includes the host's own manual |
| Hollow discharge of the coverage invariant | Fix: repoint at a test that runs `setup_requirements` over a hooks-declaring recipe |

Should-fix findings carried into the same pass: the `n-a` line's false reason (Mara 3, Bly 6, Wren 8), the silent `.gitignore` write (Mara 7, Bly 10, Orin 11, Wren 12), the clean-verdict overstatement when dimensions went unread (Bly 4, Orin 4), a recorded dimension that becomes unreadable never reporting moved (Orin 4), one toolchain image per fingerprint (Mara 6), no route from `--check` to `--verify-setup` (Mara 4, Wren 6), unevaluable hedges in two drift remedies (Wren 7), absolute skill links where the script writes relative ones (Wren 11), the missing subcommands in the usage line (Wren 10), and the manifest's overclaim about what the proof establishes (Bly 8, 9).

Deferred with a reason: `sha256sum` portability (Orin 5) is a real narrowing of the fingerprint on non-GNU machines and is filed rather than fixed here, because it touches the pre-existing `sha256_file` used by the artifact attestation. The `.host-lintignore` breadth (Mara 8, Bly 14, Wren 15) is recorded as owed narrowing, with the remap-fixture split named as its exit.

## The operator decision this review surfaced

Orin's finding 3 is not a defect to fix in code without a ruling. The materialize receipt was designed as checked-in provenance (#18, operator ruling 2, 2026-07-19), and the review shows what that means once bootstrap runs materialize on every clone: one appended stanza per contributor per clone, in a shared append-only file, recording an event that is purely local. The options are to keep it as designed and accept the accretion, to record only authoritative materializations, to deduplicate by content so a repeat realization appends nothing, or to move the record to the local tier and revisit the checked-in ruling. Carried to the operator.

## The adversarial round (2026-07-23, on the fixed diff)

Five lenses re-read the diff after the cast's blocking set was fixed: duplication, overfit, fail-open, and discharge-integrity (the weak-agent lens is the acceptance). Three of them reproduced their findings against the built binary; the discharge lens proved its findings by mutation, editing a scratch copy and re-running the whole suite to see whether anything caught the change.

### What survived probing

The receipt-versus-fingerprint split holds under attack: no cross-artifact reads, correct write attribution at every call site, and the receipt provably carries no state fact. The gate writes nothing, and the verifying-ops assertion is real. Three of the gate's requirement classes have no counterpart anywhere else. The minimal-adopter path is exercised end to end.

### What did not

**The verification is thinner than its numbers.** Four obligations are discharged by a test whose own doc comment describes the opposite behaviour; two invariants survive mutation of the exact code they name (deleting host-role awareness, or blanking every worktree hook target, leaves all 277 tests green); one invariant is discharged by a test of `.gitignore`. The mechanism is systemic: test names were fitted to obligation ids while their bodies tested something else, and the strict-discharge check is a substring match that cannot tell.

**The proof proves less than the manifest says.** Two of its three assertions are tautologies over a two-variant enum. The third restates the function it checks, 550 lines away in the same file. The quantification runs over a hand-maintained array rather than the enum, so a new fact mapped to the wrong artifact verifies clean; and the writer's real dependency, the positional pairing of stanza name to value, is neither proved nor tested (swapping two entries records the repo path under the submodule stanza with everything green).

**Two fresh fail-opens, both reproduced.** Hooks are checked by filename alone, so a tree whose hooks are present, non-executable and byte-wrong reads "setup complete" while git ignores them and the commit lands. And a requirement whose source directory is empty or unreadable ceases to exist rather than becoming a gap, so gutting a submodule's working tree turns two required skills into no requirement at all.

**Bootstrap leaves a false drift on every fresh clone.** Its hooks step calls the counting loop rather than the op that refreshes the fingerprint, so the first `env --check` after a successful bootstrap reports the gate binary as moved and hands the operator a no-op remedy. That is the one dimension this work was founded on, and the weak-agent acceptance passed on exactly that output.

**A receipt survives an aborted materialize.** The append is inside the per-component loop and the abort exits mid-loop, so a two-component recipe whose second component fails leaves provenance for a run that never realized.

**Declared parallel worktrees are invisible to the gate and to bootstrap's materialize step**, while the installer gates them: removing a declared `worktrees =` line leaves the gate clean and bootstrap declining to re-create it.

**One boundary was broken to make a fix work.** Reporting a recorded-then-unreadable dimension as moved (the fix that stopped the fingerprint staying silent about a deleted gate binary) contradicts two spec invariants, and the test written for it asserts the counterexample of the invariant it discharges. The `env --check` and `--verify-setup` remedies for that state are now byte-identical, which is the overlap the whole plan is organized against.

**Bootstrap re-implements the gate's predicates** rather than deferring to them, and the two have already drifted: a gate provider with an artifact and no build line makes the gate hazard while bootstrap reports the step satisfied.

### Disposition

Recorded here, carried to the operator: the blocking set above is a second round of work of the same size as the first, and one of its findings (the requirement set deriving from directory listings rather than from the recipe and the pin) is a structural change to how the gate enumerates. The release waits on it.

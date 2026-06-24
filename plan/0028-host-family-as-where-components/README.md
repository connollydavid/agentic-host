# plan/0028: The host-* family as Where-room software components

> **Decision:** `call/0020`. agentic-host is a multi-software development host; everything `host-*`
> is software developed here and belongs in `.host-software` as a Where component, while `tools/`
> holds only the external referenced tools (allium, specula). This milestone is the migration that
> realizes that decision, and it folds in the deferred `plan/0025` #41/#50 dogfood (`release` on the
> tools), which becomes possible exactly because the tools become resolvable Where components.
>
> **Re-cut after adversarial review** (`design-review.md`, *proceed only with major revisions*) and the
> operator rulings recorded below. The blocking *spine-contradiction* is **resolved by `plan/0029`**,
> which folded the tool-residency clause into the spine, so `call/0020` now *applies* that clause rather
> than forking it. The remaining open decisions are settled in **Operator rulings**. The invalid linear
> build order is replaced by the **two-pass bootstrap** (Readiness then Cutover) that names and breaks the
> genuine host-lifecycle bootstrap cycle. This milestone now **depends on `plan/0029`** for the nested
> layout, addressing, recipe-dispatch, and skill-link integrity it builds on.

## Status: landed (2026-06-22)

Both passes are complete and pushed; the whole suite is green. The Readiness pass hardened
and spec-bore the producers; the Cutover pass made the atomic agentic-host change. Each
release was cut by the tool-carried `host-lifecycle release <component> --change-class neither`
(the tool computes the version), the producer tag is the release, and the orchestration
consumed it (re-pin plus receipt):

| Component | Release | Pin | Recorded artifact sha256 |
|-----------|---------|-----|--------------------------|
| host-grammar | v0.3.0 | `9d51468` | repo-only (no artifact; the version-bump commit sits directly on the proofs HEAD `fbd2e6c`, so ruling #3 holds) |
| host-lint | v0.8.1 | `1386e9a` | `4e76682b1893…` (re-released onto the new grammar) |
| host-lifecycle | v0.19.2 | `6fa94cf` | `ad3bf89a55c9…` |
| host-prove | v0.2.1 | `135539b` | `8e3742f8b7d7…` |

The atomic agentic-host commit (`e7d952d`) added the three stanzas, re-pinned host-lint,
dropped the two submodules (with `.git/modules` pruned), generalized `link-skills.sh` to wire
both `tools/` submodules and `software/<name>/main/` worktrees, and back-filled every embed and
release receipt in the one commit. The released pinned host-lifecycle (`6fa94cf`, installed by
`cargo install --rev`) gates this repo (self-cert): `software --check` and `--verify-build` are
green (all three artifacts reproduce in the recorded container), all eleven software-skill links
resolve, `book --check` renders, and the commit-hook tell test passes. `CLAUDE.md` §0 carries the
seed-first fresh-clone order, and a cold-clone CI job guards the seed path and link integrity.

One note against the plan as written: the version cuts are host-lifecycle 0.19.2, host-prove
0.2.1, and host-lint 0.8.1 (the producers had already advanced past the `0.19.0` placeholder the
plan used; the tool computed each from the change class).

## Context

`plan/0025` shipped the receipt gate and a tool-carried `release` phase, but it surfaced a false
"tooling vs Where-room software" binary: host-lint is a `.host-software` Where component, while
host-lifecycle and host-prove are `tools/` submodules and host-grammar is a git-dep library, so
`release host-lifecycle` could not resolve, and the dogfood was deferred. `call/0020` corrects this:
the methodology already supports more than one software-under-development (`.host-software` is
"one or more components"; `embed`/`release` are `recurring-per-component`; agentic-host already
carries two). The fix is to make the residency uniform, the host-lint model for the whole family.

`plan/0029` then made the multi-component Where room first-class and generic (the nested
`software/<component>/<branch>/` layout, `--item` addressing, recipe-dispatch on `artifact?`/`build?`,
the generated-link integrity check) and folded the residency clause into the spine. agentic-host is
already migrated to the nested layout (`software/host-lint/main/`, `software/host/main/`). This milestone
is what proceeds on top: add the rest of the family as components.

## Operator rulings (2026-06-22)

The design-review left four decision-level findings. One is discharged by `plan/0029`; the other three
were ruled by the operator:

1. **Spine-first vs owned divergence, RESOLVED by `plan/0029`.** `plan/0029` amended `host-template` so
   the spine distinguishes an *adopter* (references the host-* tools as submodules, "reference, don't
   vendor") from a *development host* (develops and embeds the tools it authors as Where components).
   `call/0020` now applies that spine clause; there is no isolated fork. No further action here beyond
   confirming the applied baseline carries it.

2. **Self-certification: gate with the *released, pinned* host-lifecycle.** agentic-host's
   `software --check`, `--verify-build`, and `release` are run by the **released, pinned** host-lifecycle
   (its producer-CI tagged build, recorded in `.host-software`), never by the worktree build. The worktree
   build is only ever the *next version under development*. The rationale the operator named is
   **avoiding mixed state**: a moving, possibly-uncommitted worktree binary certifying its own release
   conflates the thing being developed with the thing vouching for the release, whereas a released pin is
   a fixed, known-good, immutable certifier. This preserves the independent-verifier rung (the analogue,
   one rung up, of the spine's "self-referential software is excluded, not bypassed").

3. **host-grammar pin: converge on a new tag at proofs HEAD, and re-release host-lint.** Cut a host-grammar
   tag at the proofs HEAD (`fbd2e6c`, which carries the `plan/0023` Apalache/TLAPS work) and pin **both**
   host-lifecycle and host-lint to it, restoring the "what host-lifecycle emits is what host-lint accepts"
   symmetry on a current grammar. host-lint therefore changes too: its `Cargo.lock`, its binary bytes, and
   its recorded `artifact` sha256 all move, so it is **re-released** (re-pinned, new release receipt, green
   `--verify-build`). The rejected alternative was freezing the grammar at the stale `8091261`, which would
   drop the verification-ladder proofs from what the toolchain compiles against.

4. **Spec lane: host-lifecycle and host-prove become spec-bearing.** Uniform with host-lint: author an
   `.allium` spec plus `.obligations` for each, and wire the **allium lane** in each tool's producer CI.
   This activates the spec/obligation MUST and re-derivation digests for those components; it is real
   authoring work (via the `elicit`/`distill` skills) and a standing gate obligation, deliberately
   accepted.

## Per-target audit (the migration is heterogeneous; do not treat as one case)

| Component | Now | Shape | Producer CI | Becomes | Release |
|-----------|-----|-------|-------------|---------|---------|
| host-lint | `.host-software` Where, yes | Rust **binary** (artifact), spec-bearing | own | **re-release** onto new host-grammar tag (new artifact hash plus receipt) | artifact-bearing |
| host-lifecycle | `tools/` submodule | Rust **binary** (artifact), **7** phase skills | `ci.yml` | `.host-software` Where, artifact-bearing, **now spec-bearing** | build, re-derive, tag |
| host-prove | `tools/` submodule | Rust **binary** plus `install/`+`tools.lock`, **3** skills | `ci.yml` | `.host-software` Where, artifact-bearing, **now spec-bearing** | build, re-derive, tag (verifiers stay pinned in `tools.lock`; the artifact is only `target/release/host-prove`) |
| host-grammar | git dep (host-lifecycle **unpinned**) | **library** crate (no binary) | own repo | `.host-software` Where, repo-only (no `artifact`/`build`, so the recipe-dispatch tag-only path, `plan/0029`) | **tag-only**; dependents keep git-rev dep, pinned to its tag |
| allium, specula | `tools/` submodule | external (JUXT / specula-org) | upstream | **stay** in `tools/` (external by *source*, not by name) | n/a |

Membership criterion (per `plan/0029`'s residency clause): a `.host-software` component is **software whose
canonical source repo is developed in this host**, not "anything name-prefixed `host-*`". allium and specula
are external by source; a hypothetical externally-developed `host-foo` would correctly *not* be a component.

## The migration: two passes (Readiness, then Cutover)

The single-artifact authority rule throughout: **the producer repo's tag is the release**; the
orchestration *consumes* it (re-pins `.host-software`, records the receipt) and never mints a competing
tag (the design-review's *dual-release-authority* fix).

### Readiness pass (producer repos; software-first; no component additions, no orchestration releases yet)

1. **host-grammar (pushed first).** Confirm or cut the tag at the proofs HEAD (`fbd2e6c`); its own CI green
   (allium/TLA plus the `plan/0023` Apalache/TLAPS lanes). This is the grammar both dependents converge on.
2. **host-lifecycle.** Rev-pin **both** git deps in `Cargo.toml`, host-grammar to the new tag and
   host-lint to its project pin, and **commit `Cargo.lock`** (it is gitignored today). Ensure exactly
   **one** host-grammar entry in the lockfile, equal to host-lint's pin (`cargo tree -d` clean; today the
   lock carries two, `8091261` via host-lint and a floating `fbd2e6c` direct). Add the reproducibility
   hardening host-lint already uses (`strip = true`, `.cargo/config.toml` `-C link-arg=--build-id=none`).
   Author its `.allium` plus `.obligations` and wire the allium lane in `ci.yml` (spec-bearing ruling).
   Prove a clean double-build reproduces a hash in its own repo and CI (container build in the pinned
   toolchain). Do **not** tag a release through the orchestration here; the 0.19.0 cut belongs to the
   Cutover.
3. **host-prove.** Same reproducibility hardening and double-build proof (its Rust binary has **zero**
   external deps and its lockfile is already committed; the recorded `artifact` is **only**
   `target/release/host-prove`, never the `tools.lock` verifiers, since TLAPS is Linux-only and Kani is
   `sha256=n/a`). Author its `.allium` plus `.obligations` and wire the allium lane. Linux-only, so
   `attest-host = linux` (WSL2 counts as linux).

### Cutover pass (agentic-host; atomic where the receipt gate demands it)

Run by the **released, pinned** host-lifecycle (self-cert ruling), with the worktree binary used only to
perform the release dogfood. One coherent change, because the `recurring-per-component` receipt gate goes
RED the instant a new component appears in `.host-software` without its back-filled receipts, and
`reproducible-build.yml` runs `software --check .` on every push to main (a main-only-triggered failure,
the `complete-means-whole-suite-green` trap):

1. **Drop the submodules fully:** remove `tools/host-lifecycle` and `tools/host-prove` from `.gitmodules`
   **and** prune `.git/modules/tools/host-{lifecycle,prove}` (de-registration, not just a `.gitmodules`
   edit).
2. **Add the `.host-software` stanzas** under the nested layout: `[software "host-lifecycle"]` and
   `[software "host-prove"]` (artifact-bearing: `toolchain`/`build`/`artifact`/`deploy`, `attest-host`),
   and `[software "host-grammar"]` (repo-only: no `artifact`/`build`, the recipe-dispatch tag-only path).
   The uniform `/software/` ignore from `plan/0029` already covers their worktrees (no per-component
   triplets to add).
3. **Re-release host-lint** onto the new host-grammar tag: re-pin its `.host-software` `pin` and `artifact`
   sha256, with a green `--verify-build` and a new `release host-lint` receipt (ruling #3, host-lint's
   bytes move with the new grammar).
4. **Skill wiring:** the generated-link walk and the component-skill dir-shape port already exist from
   `plan/0029`'s link-integrity deliverable; the cutover wires host-lifecycle's **7** and host-prove's
   **3** skills from their worktrees and folds the manual host-lint `ln -s` step into the same mechanism so
   no link is created twice.
5. **Fresh-clone order:** rewrite `CLAUDE.md` §0 step by step with the **seed-first** sequence,
   `cargo install --git <host-lifecycle> --rev <pin>` where the seed `--rev` **MUST equal** the
   `.host-software` host-lifecycle pin (else seed and materialized source diverge silently), because the
   materializer cannot be served from the thing it materializes (the genuine bootstrap cycle).
6. **Materialize** the new components via the seed binary; **back-fill the receipts in the same commit**
   as the `.host-software` add (atomic, so the gate is never RED on a push to main). Define host-grammar's
   **tag-only** `release` receipt shape (it has no artifact).
7. **Release dogfood:** cut each tool through `host-lifecycle release <component>` run by the freshly-built
   **worktree** binary (0.18.1 cutting **0.19.0**, version N releases N+1), the **producer tag being
   authoritative**; the orchestration consumes it and records the receipt. (This is the one place the
   worktree build acts; the standing gate stays on the released pin.)
8. **CI rewire last,** pinned to the sha the cutover produced, and add a **cold-clone CI job** that
   exercises the documented seed path and asserts all **eleven** software-skill links resolve (host-lint 1
   plus host-lifecycle 7 plus host-prove 3; `host` 0) and none are tracked. No such job exists today, and
   `link-skills.sh` is run by zero workflows, so the generated-link regression has no gate backstop
   otherwise (`software --check`'s symlink HAZARD only catches *tracked* symlinks).

### Records

This plan, `call/0020`, `PLAN.md`, `MEMORY.md`; re-pins and re-records as the migration lands, each pushed
in its own audited commit.

## Verification (whole-suite green, `complete-means-whole-suite-green`)

- The **released, pinned** `host-lifecycle software --check .` clean: every new Where component at its
  pin, no tracked-symlink-into-unmaterialized hazards, every phase receipt present (now recurring over the
  enlarged component set), every recheck holding.
- `software --verify-build .` green for each artifact-bearing component (host-lint, host-lifecycle,
  host-prove), reproducible from the pin in the recorded toolchain; host-grammar's no-artifact stanza is a
  clean `--check` and tag-only case (recipe-dispatch, `plan/0029`).
- The allium lane is green in host-lifecycle's and host-prove's own CI, and their `.obligations`
  re-derivation digests hold in agentic-host's gate (spec-bearing ruling).
- The generated-link walk resolves the host-lifecycle (7) and host-prove (3) skills from their worktrees;
  `book --check` renders from stubs with all stanzas present and no worktrees materialized; the commit-hook
  tell test passes.
- Each tool's **own** producer CI green; `release` dogfooded on host-lifecycle (0.19.0 cut through the
  orchestration by the worktree binary, producer tag authoritative, receipt recorded).
- A **cold-clone CI job** reaches green via the seed-first path (the bootstrap-cycle proof).
- Whole-suite green across every repo.

## Risks / honesty

- **Bootstrap circularity is real, not hand-waved:** host-lifecycle materializes itself, so the cutover
  names the seed-from-pin step and pins the seed `--rev` to the `.host-software` pin; the cold-clone CI job
  proves it.
- **Reproducibility substrate is bigger than "one unpinned dep":** both git deps in host-lifecycle must be
  rev-pinned, `Cargo.lock` committed, exactly one host-grammar entry, strip/build-id hardening on both
  host-lifecycle and host-prove, done in Readiness before any artifact hash is recorded.
- **Spec-bearing is added scope:** two new `.allium` specs plus obligations plus lanes, accepted by ruling
  #4; authored via the wired skills, not by hand.
- **Self-cert sequencing:** the standing gate runs the released pin; the worktree binary acts only in the
  release dogfood step. Keeping these separate is what avoids the mixed state the operator flagged.
- **Skill-wiring is a real mechanism** (generated, untracked links with no tracked-symlink backstop); the
  cold-clone link-resolution job is the guard.
- **Multi-repo, software-first:** sequence strictly producer-first; report any unpushable commit and stop
  rather than proceeding with a dangling pin.

## Spine follow-up

The residency clause this milestone needs is **already in the spine** (`plan/0029` amended `host-template`:
adopter references versus development-host embeds). The remaining spine-shaped item (that the template
prose gain a first-class notion of an artifact-free *library* component) is already covered by
`plan/0029`'s recipe-dispatch model, where a stanza with no artifact takes the tag-only path, together with
its `STRUCTURE.md` update. This project-scoped migration carries it no further. **Closed**: `plan/0029` shipped
the recipe-dispatch model (a no-artifact stanza takes the tag-only path) and the
residency clause; nothing remains here.

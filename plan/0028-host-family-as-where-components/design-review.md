# plan/0028 — adversarial design review

Five independent adversarial reviewers, each a distinct failure-mode lens: bootstrap/dependency
cycles; reproducible-build feasibility; decision soundness; skill-wiring and worktree-absence;
sequencing, scope and whole-suite green. Each was told to *break* the plan, not validate it. Findings
below are deduplicated and named for content; cross-reviewer confirmation is noted because it raises
confidence.

**Verdict: the decision's kernel is sound, but do not build as written.** Proceed only with major
revisions — and two findings reopen `call/0020` itself, not just the plan (named *spine-contradiction*
and *self-certification* below). The build order is not a valid topological sort (the dependency graph
is genuinely cyclic, because host-lifecycle is both the tool that performs the migration and a thing
being migrated), and a pre-existing host-grammar reproducibility defect must be closed first and is
larger than the plan states.

## Sound kernel — attacks that failed (recorded for honesty)

- **`release <tool>` genuinely cannot resolve on a `tools/` submodule** — the dogfood is really
  blocked today; making the tool a Where component really fixes it. The decision's strongest leg.
- **Multi-component Where rooms are first-class** (`STRUCTURE.md` "one or more components";
  `call/0010`; agentic-host already carries two). Not invented.
- **`recurring-per-component` machinery already exists** (`call/0017`); reusing it is not new code.
- **"A project per tool" is rightly rejected** — fragmenting one coupled roadmap for one developer is
  real over-separation.
- **Pinning host-grammar is a genuine reproducibility fix** — the dep is really unpinned.

## Decision-level findings — resolve before, or atomically with, the migration

- **Spine-contradiction — the spine classifies host-* tools (including host-lint) as `tools/`; the
  "developer is exempt from reference-don't-vendor" carve-out is invented. [BLOCKING]** The spine states
  "Reference, don't vendor — each tool is a git submodule … do not copy its code into this repository"
  *unconditionally*, and positively lists `tools/host-lint`, `tools/host-lifecycle`, `tools/host-prove`
  in three normative places (five-rooms table, verification ladder, STRUCTURE.md). `call/0020`'s
  carve-out exists nowhere in the spine. Worse, **host-lint-as-Where is itself an unreconciled
  *instance* divergence, not the "settled model" the decision leans on** — so generalizing it deepens
  drift rather than removing an accident. Per copy-at-version ("change the spine, re-run the migration —
  do not fork the spine in isolation"), residency is a spine change delivered through the template + an
  UPGRADING entry, not an instance change with a deferred "may warrant" follow-up. **Fix:** amend the
  spine first (or atomically) and apply it via `upgrade`; or have `call/0020` explicitly own the
  divergence and cite the tracking UPGRADING entry. As written it contradicts the pinned spine silently.

- **Self-certification — the worktree-built host-lifecycle would gate and release itself. [HIGH]** Today
  host-lifecycle is a *pinned external artifact* that audits the Where room at arm's length — the checker
  and the checked are different artifacts at different pins. As a Where component built from the
  worktree, host-lifecycle's `software --check`/`verify`/`release` certify the repo developing it; a bug
  in its own check logic cannot be caught by its own check. This is the analogue, one rung up, of the
  spine's "self-referential software is excluded, not bypassed." **Fix:** gate and release agentic-host
  with the *released, pinned* host-lifecycle (its producer CI's tagged build); develop the next version
  in the worktree; never let the worktree build certify its own release. State the independent rung.

- **Dual-release-authority — two release paths, one artifact, no authority rule. [MED, HIGH if
  unresolved before the release dogfood]** Each tool keeps "its own producer CI release" *and* is
  "released through the orchestration" — both tag `vX.Y.Z`, both build artifacts, possibly in different
  toolchains → divergent hashes and a silent provenance split (`.host-software` pin vs the repo's tag).
  **Fix:** the **producer repo's tag is the release**; the orchestration *consumes* it (re-pins
  `.host-software`, records the receipt) and does not mint a competing tag.

- **Membership-by-branding — the criterion is a name prefix, not structure. [MED]** "Everything
  `host-*`" is the same kind of line the decision just called an "accident." **Fix:** pin
  `.host-software` membership to **"software whose canonical source repo is developed in this host"**
  (provenance), so allium/specula are external by *source*, and a future externally-developed `host-foo`
  is correctly not a component.

- **Spec-lane-activation — reclassifying activates the spec/obligation MUST. [MED]** host-lifecycle and
  host-prove carry no specs today; "uniform with host-lint" (which *is* spec-bearing) implies authoring
  `.allium`, which then obliges the allium lane + `.obligations` + re-derivation digests **in
  agentic-host's gate**. State whether they become spec-bearing or are deliberately spec-free.

## Build-order findings — the linear order is not a valid topological sort

- **Bootstrap-cycle — "build host-lifecycle from its worktree first" is impossible. [BLOCKING, three
  reviewers]** The worktree is the *output* of `software --materialize`, which needs the host-lifecycle
  binary. Genuine cycle. The repo's CI already breaks it with a **seed step** (`cargo install --git
  host-lifecycle --rev <pin>`) the plan never names. **Fix:** name the seed-from-pin step explicitly; the
  seed `--rev` MUST equal the `.host-software` host-lifecycle pin (else seed and materialized source
  diverge silently); add a carve-out that the *materializer* cannot be "served from the thing it
  materializes."

- **Release-before-component — the 0.19.0 cut is placed before the component exists. [HIGH]** `release
  host-lifecycle` resolves only against `.host-software` (added in the cutover), but the order puts "cut
  0.19.0 tag" in the readiness step — the same release described twice. If the readiness step tags it
  manually, the orchestration was never dogfooded. **Fix:** the 0.19.0 cut belongs wholly in the cutover,
  performed by the freshly-built worktree binary (0.18.1 releasing 0.19.0).

- **Receipt-gate-red — adding three components turns the receipt gate RED on a push-to-main job.
  [HIGH]** The `recurring-per-component` gate demands `embed`/`release` receipts for the new components
  the instant they appear in `.host-software`; `reproducible-build.yml` runs `software --check .` on
  every push to main, so the first push that adds them but has not back-filled receipts is red (a
  main-only-triggered failure — the `complete-means-whole-suite-green` trap). **Fix:** make the
  `.host-software` add and the receipt back-fill **one atomic commit**; define host-grammar's tag-only
  `release` receipt shape (it has no artifact).

## Reproducibility-substrate findings — bigger than "one unpinned dep"

- **Grammar-pin-mess — host-grammar pinning is three-way broken and the grammar symmetry is violated
  *today*. [HIGH, two reviewers, confirmed in Cargo.lock]** `tools/host-lifecycle/Cargo.toml` pins
  *neither* git dep: host-grammar floats, and host-lint floats and is stale (locked `0.4.3 @ 83acb53` vs
  the project pin `bbd0687`/v0.7.0). Its `Cargo.lock` carries **two** host-grammar entries — `8091261`
  (via host-lint) and floating `fbd2e6c` (its own direct dep) — and the lockfile is **gitignored**. So
  the generator compiles host-grammar `fbd2e6c` while the host-lint it bundles checks with `8091261`:
  "what host-lifecycle emits is what host-lint accepts" is violated in the artifact now. **Fix:**
  rev-pin *both* git deps, **commit `Cargo.lock`**, ensure exactly one host-grammar entry equal to
  host-lint's pin (`cargo tree -d` clean), and add host-lint's reproducibility hardening
  (`strip = true`, `.cargo/config.toml` `--build-id=none`) to both host-lifecycle and host-prove.

- **host-lint-must-re-release — host-lint is NOT "unchanged". [HIGH]** Re-pinning host-lint to a new
  host-grammar tag changes its `Cargo.lock` → binary bytes → recorded `artifact` sha256 → `software
  --verify-build` fails until re-recorded, plus a new `release host-lint` receipt. The only way to leave
  host-lint truly untouched is to set host-grammar's tag to exactly `8091261` — but then host-lifecycle
  moves *backward* off the proofs HEAD (`fbd2e6c`). **Decide and state** which: re-release host-lint, or
  freeze the grammar at `8091261`.

- **host-prove-is-easy — the plan over-worries host-prove. [MED]** Its Rust binary has **zero** external
  deps and its lockfile is already committed; the recorded `artifact` is **only**
  `target/release/host-prove`, NOT the external verifiers (`tools.lock` is a separate, existing
  provenance mechanism — TLAPS is Linux-only, Kani is `sha256=n/a`). State this so nobody folds the
  verifier install into `--verify-build`.

- **Multi-platform-attest — `attest-host` unaddressed. [MED]** host-lifecycle's own CI builds a
  six-target matrix; the `.host-software` artifact must scope platform (single `attest-host = linux`,
  with WSL2 counting as linux, vs the multi-`[build]` form). host-prove is Linux-only — the asymmetry is
  unstated.

- **Library-component-slot — a library Where component is an unhandled methodology slot. [LOW to MED]**
  host-grammar produces no binary, so it has neither an `artifact` hash nor a `repro-exempt` reading, and
  the `release` phase's evidence ("build … re-derive the artifact hash") has no shape for it. **Verify in
  host-lifecycle's source** that a no-artifact stanza is valid for `--check`/`--verify-build` and that
  `release` emits a defined tag-only receipt — or build that branch. Strong candidate for the spine
  follow-up (the template prose has no concept of an artifact-free component).

## Skill-wiring findings — under-budgeted (one bullet hides the real scope)

- **New-link-loop-no-backstop — `link-skills.sh` needs a brand-new `.host-software`-walking loop, and
  the dangling-link regression has no gate backstop. [HIGH]** The host-lint software link is created by a
  *manual* `ln -s` in `CLAUDE.md` §0 and the `embed` skill — NOT by `link-skills.sh`, which only iterates
  `tools/*/`. So this is a new loop (parse `.host-software`, find materialized worktrees, three-way shape
  branch: root `SKILL.md` / `skills/*` / none, with an absence guard), and the manual step must be folded
  in or host-lint's link is created twice by two mechanisms. Critically, **`software --check`'s symlink
  HAZARD only catches *tracked* symlinks** — these are generated/untracked, so a dangling generated link
  has *no* gate backstop except a tree-walker tripping (the failure that turned Site CI red once before).
  **Fix:** specify the loop + absence guard; add a cold-clone CI job asserting all eleven software-skill
  links resolve (host-lint one + host-lifecycle seven + host-prove three; `host` zero) and none are
  tracked. No such CI job exists today, and `link-skills.sh` is run by zero workflows.

- **Gitignore-and-deregister — `.gitignore` and submodule de-registration. [MED]** `.gitignore` has
  per-component triplets for `/host-lint/` and `/host/` but none for `/host-lifecycle/`, `/host-prove/`,
  `/host-grammar/` — after materialize those worktrees are untracked noise a careless `git add -A` would
  track. The dropped submodules also need full de-registration (`.git/modules/tools/host-*`), not just a
  `.gitmodules` edit. Do both in the same commit as the `.host-software` add.

- **Fresh-clone-order-rewrite — `CLAUDE.md` §0 must be rewritten literally, not "reconciled." [MED]** §0
  today says materialize then `submodule update --init`; after the migration that order is wrong (the
  tools no longer arrive by submodule init) and the seed step must lead. Write the new sequence step by
  step.

- **Book-check-untested — `book --check` against the enlarged, un-materialized component set is
  untested. [MED]** The doc-site CI deliberately does not materialize; confirm `book --check` renders
  from stubs only with all eleven stanzas present and no worktrees, or it is a worktree-absence
  regression.

## Recommended re-cut

Replace the five-step linear order with a two-pass bootstrap that names the cycle and breaks it:

1. **Readiness pass (producer repos; no releases, no component additions).** Cut/confirm a host-grammar
   tag; rev-pin both git deps and commit `Cargo.lock` in host-lifecycle (and re-pin host-lint per the
   host-lint-must-re-release finding); add strip/build-id hardening; prove a clean double-build
   reproduces a hash in each tool's own repo and CI. Nothing tagged as a release through the
   orchestration yet.
2. **Cutover pass (agentic-host, atomic where the gate demands it).** In one coherent change: drop the
   submodules (with `.git/modules` prune + `.gitignore` triplets), add the three `.host-software`
   stanzas, generalize `link-skills.sh` + rewrite `CLAUDE.md` §0 with the seed-first order, materialize
   via the seed binary, and back-fill the receipts in the same push. Then cut each tool through
   `host-lifecycle release` (the worktree binary, 0.18.1, cutting 0.19.0), the producer tag being
   authoritative (per dual-release-authority). Finalize the CI rewire **last**, pinned to the sha the
   cutover produced, and add the cold-clone green job that exercises the same seed path it documents.

Plus the decision amendments: resolve spine-contradiction (spine-first or owned divergence),
self-certification (gate with the released pinned binary, not the worktree build), dual-release-authority
(single tag authority), and tighten the membership criterion to repo provenance.

## Decisions for the operator

1. **Spine first, or owned divergence?** Amend `host-template` (the "development host embeds its tools as
   Where software" clause) + an UPGRADING entry and apply by `upgrade` *before* the migration, or land
   the instance change with `call/0020` explicitly citing the divergence and the tracking entry.
2. **Self-certification.** Accept that agentic-host gates/releases itself with the *released pinned*
   host-lifecycle (worktree only for developing the next version), or specify a different independent
   rung.
3. **Does host-lint move?** Re-release host-lint onto the new host-grammar tag (accept the new artifact
   hash + receipt), or freeze the grammar at `8091261` and accept host-lifecycle losing the proofs HEAD.

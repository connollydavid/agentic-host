# plan/0028 — The host-* family as Where-room software components

> **Decision:** `call/0020` — agentic-host is a multi-software development host; everything `host-*`
> is software developed here and belongs in `.host-software` as a Where component, while `tools/`
> holds only the external referenced tools (allium, specula). This milestone is the migration that
> realizes that decision, and it folds in the deferred `plan/0025` #41/#50 dogfood (`release` on the
> tools) — which becomes possible exactly because the tools become resolvable Where components.

## Context

`plan/0025` shipped the receipt gate and a tool-carried `release` phase, but it surfaced a false
"tooling vs Where-room software" binary: host-lint is a `.host-software` Where component, while
host-lifecycle and host-prove are `tools/` submodules and host-grammar is a git-dep library — so
`release host-lifecycle` could not resolve, and the dogfood was deferred. `call/0020` corrects this:
the methodology already supports more than one software-under-development (`.host-software` is
"one or more components"; `embed`/`release` are `recurring-per-component`; agentic-host already
carries two). The fix is to make the residency uniform — the host-lint model for the whole family.

## Per-target audit (the migration is heterogeneous — do not treat as one case)

| Component | Now | Shape | Producer CI | Becomes | Release |
|-----------|-----|-------|-------------|---------|---------|
| host-lint | `.host-software` Where ✓ | Rust **binary** (artifact) | own | unchanged (reference model) | artifact-bearing |
| host-lifecycle | `tools/` submodule | Rust **binary** (artifact), **7** phase skills | `ci.yml` | `.host-software` Where, artifact-bearing | build + re-derive + tag |
| host-prove | `tools/` submodule | Rust **binary** + `install/`+`tools.lock`, **3** skills | `ci.yml` | `.host-software` Where, artifact-bearing | build + re-derive + tag (verifiers stay pinned in `tools.lock`) |
| host-grammar | git dep (host-lifecycle **unpinned**) | **library** crate (no binary) | own repo | `.host-software` Where, repo-only | **tag-only** (no artifact); dependents keep git-rev dep, pinned to its tag |
| allium, specula | `tools/` submodule | external (JUXT / specula-org) | upstream | **stay** in `tools/` | n/a |

## Deliverables

1. **Producer-side readiness (each in its own repo, pushed first — software-first).**
   - **host-grammar:** confirm/cut a released tag the dependents can pin to; its own CI green.
   - **host-lifecycle:** pin its `host-grammar` dependency to that tag (closes the current *unpinned*
     dep — a reproducibility hole), prove a reproducible build (record `toolchain` + `artifact`
     sha256 from a container build, host#14), and cut its deferred **0.19.0** version + tag (folds in
     `plan/0025` #41/#50 — disambiguating the 0.18.1-labeled feature build).
   - **host-prove:** same reproducible-build readiness; confirm `tools.lock` provenance is checked in
     its own CI; tag at its current `0.2.0` (or bump as warranted).
2. **agentic-host structural migration.**
   - `.gitmodules`: drop the `tools/host-lifecycle` and `tools/host-prove` submodules.
   - `.host-software`: add `[software "host-lifecycle"]`, `[software "host-prove"]` (artifact-bearing,
     with `toolchain`/`build`/`artifact`/`deploy`), and `[software "host-grammar"]` (repo-only,
     tag-only).
   - **Skill wiring:** generalize `link-skills.sh` so a `.host-software` Where component's skills wire
     from its worktree (host-lifecycle's 7, host-prove's 3) — the host-lint pattern, extended to
     multi-skill components; reconcile the fresh-clone setup in `CLAUDE.md` §0 accordingly. The
     tracked-symlink-into-an-unmaterialized-path hazard (`call/0005`) still governs: generated, never
     tracked.
   - **Bootstrap:** host-lifecycle is the tool that materializes `.host-software`, including itself —
     the fresh-clone order becomes build-host-lifecycle-from-its-worktree, then materialize the rest.
3. **Dogfood the orchestration on the tools.** With the tools now resolvable Where components, cut
   each through `host-lifecycle release <component>` and record the receipts in the project ledger —
   the `plan/0025` dogfood, now on rails (and `release host-lifecycle` is the bootstrap dogfood:
   version N releases N+1).
4. **Records:** this plan, `call/0020`, `PLAN.md`, `MEMORY.md`; re-pin/re-record as the migration
   lands (each pushed in its own audited commit).

## Build / push order (software-first; each pushed before its dependents)

1. **host-grammar** — released tag; CI green.
2. **host-lifecycle** — pin host-grammar, reproducible build, 0.19.0 tag.
3. **host-prove** — reproducible build, tag.
4. **agentic-host** — `.gitmodules` + `.host-software` + `link-skills.sh` + CI; materialize; back-fill
   / cut release receipts through the orchestration.
5. **Records** — plan row, MEMORY, re-pins.

## Verification (whole-suite green — `complete-means-whole-suite-green`)

- `host-lifecycle software --check .` clean: every new Where component at its pin, no
  tracked-symlink-into-unmaterialized hazards, every phase receipt present (now recurring over the
  enlarged component set), every recheck holding.
- `host-lifecycle software --verify-build .` green for each artifact-bearing component (host-lint,
  host-lifecycle, host-prove) — reproducible from the pin in the recorded toolchain.
- `link-skills.sh` resolves the host-lifecycle (7) and host-prove (3) skills from their worktrees;
  `book --check` renders; the commit-hook tell test passes.
- Each tool's **own** producer CI green; `release` dogfooded on host-lifecycle (0.19.0 cut through the
  orchestration, receipt recorded).
- Whole-suite green across every repo.

## Risks / honesty

- **Bootstrap circularity** — host-lifecycle materializes itself; mitigated by the existing
  build-from-worktree-first setup, but the fresh-clone path needs care (and a CI proof that a cold
  clone reaches green).
- **Reproducibility prerequisites** — host-lifecycle's host-grammar dep is currently unpinned, so its
  build is not yet reproducible; that must be fixed *before* it can carry an `artifact` hash. Same
  diligence for host-prove.
- **Skill-wiring is a real mechanism change**, touching `link-skills.sh` and the fresh-clone setup —
  a regression there dangles skills or trips a tree-walker (`call/0005`); guard with the
  software-check symlink hazard and a cold-clone CI check.
- **host-grammar as a library Where component** has no deployable artifact — `release` is tag-only;
  confirm the orchestration's tag-only branch covers a repo-only component cleanly.
- **Scope** — this is a multi-repo structural migration, not a relabel; sequence strictly
  software-first and report any unpushable commit rather than proceeding.

## Spine follow-up (separate, not in this milestone)

The general pattern — *a development host embeds the tools it develops as Where software; an adopter
references them* — may warrant a clarification in `host-template` (the spine), so a future
tool-developing host has it stated. That is a methodology change (made in the template, propagated by
migration), tracked separately from this project-scoped migration.

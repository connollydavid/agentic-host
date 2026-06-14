# Embed the software as a bare store with named worktrees

- Status: accepted
- Date: 2026-06-14
- Relates: `call/0003` (compose tools as referenced submodules — the software
  embedding is the counterpart question for the "Where" room).

## Context and Problem Statement

The "Where" room (the software under test) has been a single git **submodule** —
one gitlink, one pinned SHA, one working tree. That gives audit/reproducibility
but only one live checkout, which serializes work. Two realistic needs break that:
**parallel agents** on one codebase (the prevailing idiom is a bare repo +
worktrees), and **multiple production release branches live simultaneously** (a
maintained project servicing several shipped versions cannot have its single tree
flip between them). The established "many live branches, one object store" idiom is
a **bare clone + worktrees**; but that is fundamentally not a gitlink, so adopting
it means deciding what the host pins and how audit survives.

## Decision

Embed each software component as a **bare object store plus named worktrees**, with
the pin recorded in host config rather than as a gitlink:

- **Layout.** `<name>.git/` is the bare clone (shared object store, no working
  tree). `<name>/` is the **canonical worktree** — the audited state, where CI and
  the verification lanes run. Parallel lines are sibling worktrees `<name>.<line>/`,
  one per agent or release branch; worktrees are never nested inside another
  worktree (it breaks `.git` resolution).
- **Recipe, not trees.** The bare store and all worktrees are local artifacts
  (gitignored). The host commits a recipe (`.host-software`) — `url`, the **pinned
  canonical SHA**, and the worktree set — that a setup step materializes:
  `clone --bare` → set the `+refs/heads/*:refs/remotes/origin/*` fetch refspec →
  `fetch` → `worktree add <name>` at the pinned SHA → init nested submodules per
  worktree → add the parallel worktrees.
- **Audit moves to our tooling.** With no gitlink, `host-lifecycle` owns the "is
  `<name>/` at its recorded SHA?" check; the recipe's pinned SHA is the
  reproducibility anchor the gitlink used to be.
- **Nested submodules stay native.** If the software has submodules, each worktree
  initializes them with `git submodule update --init --recursive` (worktrees share
  superproject objects, not submodule checkouts).

### Migration (an existing submodule → a bare store)

A project already embedding its software as a gitlink converts mechanically,
**preserving the software exactly** — no software commit is created, rewritten, or
moved:

1. **Preserve the pin.** Record the current gitlink SHA as the recipe's pinned
   canonical SHA — the bare+worktree state begins at precisely the commit the
   submodule pinned.
2. **De-register the gitlink.** `git rm --cached <name>`, delete the
   `[submodule "<name>"]` stanza from `.gitmodules`, remove `.git/modules/<name>`.
   The path `<name>/` is freed.
3. **Write `.host-software`** with `url`, `pin` (the preserved SHA), and the
   worktree set (at minimum the canonical `<name>`).
4. **Gitignore the layout:** `/<name>/`, `/<name>.git/`, `/<name>.*/` — all rebuilt
   from the recipe.
5. **Path continuity is the win.** The canonical worktree keeps the path `<name>/`,
   so every reference that pointed at `<name>/…` (build commands, hook paths,
   routing tables) still resolves — only the embedding mechanism changed. Audit
   references for the few that named the submodule *qua* submodule.
6. **Pointer-bump becomes pin-update.** "Merge in the software repo, then bump the
   submodule pointer in the host as a separate commit" becomes "…then update the
   recipe `pin` as a separate commit." Same audit trail (a tracked one-line commit
   recording the software's new SHA), different mechanism — update `CLAUDE.md` and
   the completion step accordingly.

## Consequences

- Good: parallel agents and multiple live release branches coexist on one object
  store; the canonical worktree stays the single audited, CI-run state.
- Good: symmetric, idiomatic layout — the bare store is visibly infrastructure; the
  canonical worktree keeps the conventional path, so migration is
  reference-preserving.
- Neutral: audit shifts from native `git submodule status` to a `host-lifecycle`
  check against the recorded SHA; a fresh host clone no longer auto-fetches the
  software — the setup step (recipe → materialize) replaces `submodule update
  --init` and must be documented/scripted.
- Bad / accepted: worktrees share git objects but **not** environment — each carries
  its own build output and submodule checkouts; heavy-vendor repos pay real disk per
  live line. This cost is **required**, not incidental: it is the price of holding
  several production releases (or several agents' branches) materialized at once,
  which a single tree cannot do.

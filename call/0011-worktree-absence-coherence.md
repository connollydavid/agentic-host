# References to the software worktree must survive its absence

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-15
- Refines: `call/0010` (the bare-store-with-worktrees embedding).

## Context and Problem Statement

`call/0010` moved the software from a gitlink submodule to a bare store with
worktrees. A submodule gave the software **auto-presence**: `git checkout` always
left at least an empty directory, so symlinks into it resolved and tree-scans did
not choke. The bare-store model **removes that** — the worktree is genuinely
absent in any fresh clone or CI job until `host-lifecycle software --materialize`
runs.

This bit immediately: the self-migration turned the host's mdBook **Site CI red**.
`.claude/skills/host-lint -> ../../host-lint` is a tracked symlink into the
worktree; with `book.toml src = "."`, mdBook scanned the dangling link (the
worktree is not materialized in CI) and failed. `call/0010`'s "path continuity"
(references resolve to the same *path*) was not enough — it assumed the path was
*populated*. The missing guarantee is about **presence**, not path. And: a feature
was declared "complete" while this sibling CI was red — **complete must mean the
whole suite is green**, not one artifact built.

## Decision

Treat every host reference into a software worktree as valid only where the
worktree is materialized, and harden against the gap three ways:

1. **Prevention (don't track the hazard).** Do not git-track an artifact that
   depends on the worktree existing. The skill symlink `.claude/skills/host-lint`
   is now **gitignored and local** — recreated after `software --materialize` — so
   a fresh clone has no dangling worktree symlink at all.
2. **Detection (mechanical, bounded).** `host-lifecycle software --check` flags a
   **`HAZARD`** for any host-tracked symlink whose target resolves into a worktree
   path — it would dangle wherever the software is not materialized. Bounded to
   symlinks deliberately: a path-*string* reference in a script or config cannot be
   told from prose statically, so widening the scan would only reproduce the
   `host-lint --all` noise. Those stay on the rule + an un-materialized CI job.
3. **The un-materialized context must be exercised, and gate "done."** CI's docs
   build *is* a fresh-clone-without-materialize context; it already catches this
   class — the failure was not looking at it. So: an un-materialized CI job must
   exist for each runtime-critical artifact, and "done" is gated on the **whole**
   CI sweep being green, not on the feature alone.

**Docs-vs-skills semantics (resolved):** the published site does **not** include
the tool skills (they were never in `SUMMARY.md`). The Site build prunes dangling
symlinks; with the skill symlink now untracked, there is nothing to prune for it.

## Consequences

- Good: the exact break is now caught mechanically (`--check` reports the hazard,
  exit 1) and prevented (the symlink is untracked), and the CI is green again.
- Good: the rule generalises to the upcoming migrations (Win32s, pgs, greenfield),
  which all carry skill symlinks, hooks, and CI that assume the old auto-presence.
- Neutral: a fresh clone must run `software --materialize` and recreate the local
  skill symlink before host-lint's skill is discoverable — the honest cost of the
  software being absent until materialized.
- Limit: detection covers the symlink class only; path-string references (a hook's
  binary path, a build `--manifest-path`) remain a rule-and-CI concern, not a tool
  gate.

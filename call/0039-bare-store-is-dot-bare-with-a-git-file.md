# The bare object store is `.bare` with a `.git` file, not a bare repo named `.git`

- Status: accepted (supersedes the bare-store placement of plan/0029)
- Date: 2026-07-04
- Scope: the on-disk materialisation layout for a `.host-software` component's bare object
  store. This is tooling behaviour of host-lifecycle `software --materialize` and `--check`,
  and binds no adopter beyond the tool's output. The milestone is `plan/0056`; surfaced as
  connollydavid/host-lifecycle#8. It supersedes `plan/0029`'s choice to name the bare store
  `.git` inside the component directory.
- Relates: `plan/0029` (the branch-keyed worktree layout this amends); `plan/0056` (the
  robustness superset); `call/0010` (software as a bare store with worktrees pinned in
  `.host-software`).

## Context and Problem Statement

`plan/0029` clustered each component under a single `software/<name>/` directory: the bare
object store at `software/<name>/.git` and the branch worktrees at `software/<name>/<branch>/`.
The clustering goal was sound (one directory per component), but the realisation named the bare
store `.git`, and a bare repo named `.git` fights git tooling. `.git` conventionally denotes a
working tree's repository, so `git status` run inside `software/<name>/` finds the bare `.git`,
reads `core.bare = true`, and errors; IDEs and any tool that detects a repository by a `.git`
entry flag `software/<name>/` as a repository root and then choke because it is bare, with the
real worktrees nested inside what git reads as a bare repo.

The docs drifted too: the `.host-software` header and a doc comment still describe the pre-0029
sibling `software/<name>.git`, a third layout that matches neither the code nor best practice.

The operator's ruling: follow git best practice and do not fight tooling.

## Decision

Materialise a component's bare object store as `software/<name>/.bare`, with a `.git` file at
`software/<name>/.git` holding `gitdir: ./.bare`, and keep the branch worktrees at
`software/<name>/<branch>/`.

- This keeps `plan/0029`'s one-directory-per-component clustering: everything stays under
  `software/<name>/`.
- It stops fighting tooling: `.git` is a file, a gitdir link every git tool understands, and
  the bare store carries the conventional `.bare` name. A `git` command run inside
  `software/<name>/` resolves through the `.git` file to `.bare`, and no tool mistakes the
  directory for a stray bare repository.
- The docs reconcile to this layout: the `.host-software` header, the materialize doc comment,
  the store-dir doc comment, and the `plan/0029` comment all describe `.bare` plus the `.git`
  file, so no stale `<name>.git` or bare-`.git` reference remains.
- Already-materialised components re-materialise from `url` and `pin`, which the recorded pin
  reproduces deterministically.

The sibling `software/<name>.git` (the layout the stale docs described) was the runner-up. It is
idiomatic, but it scatters two entries per component under `software/`, undoing `plan/0029`'s
clustering. The `.bare` plus `.git` file layout is the one that satisfies both clustering and
tooling.

## Consequences

- `store_dir` returns `.bare`; materialize writes the `.git` file; `--check` asserts both; the
  docs and tests move to the new layout. The change sites are in `plan/0056`'s
  `implementation.md`.
- A one-time re-materialise for existing components.
- host-lifecycle's materialisation output stops surprising git and IDEs, which serves the cold
  reader and the heavily-quantized operator the superset targets.

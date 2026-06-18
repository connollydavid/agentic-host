# Materialized worktrees must live under the host tree

Resolves connollydavid/host#2.

## Why

The Where-room invariant is "every materialized worktree appears under the host
folder tree" (cf. *Worktree-absence coherence*), but nothing enforced it. A
component whose backing store must live on another filesystem or platform — e.g.
a native-Windows MSVC build that has to sit on a Win11 Dev Drive, not WSL ext4 —
ended up as a bare external path (`D:\dev\…`) disjoint from the host root, with no
in-structure handle. An agent then edited the in-tree Linux worktree (the
default-cwd path) while building the disjoint Windows worktree: edits landed in a
tree not under test, builds silently recompiled unchanged source, probes "never
fired". Several build/test cycles burned before a `diff` exposed it. The failure
is structural, not operator error — a cross-filesystem line is exactly the case
that escapes the unenforced invariant.

## The fix (host-lifecycle v0.13.0)

A parallel worktree line may name an external backing store and an OS gate:

```
worktree = <dir> <branch> <pin> [store=<path>] [host=<os>]
```

- `<dir>` is **always** the in-structure handle, under the host root.
- `store=<path>` is where the git worktree physically lives (may be off-tree /
  off-filesystem). `materialize` adds the worktree there and creates `root/<dir>`
  as a **symlink** (unix) / **directory junction** (windows) to it — never a bare
  external path. So an agent editing `root/<dir>/…` writes the files under test.
- `host=<os>` gates the line to one OS (mirrors `attest-host`): off-platform,
  `materialize` and `--check` skip it, so a foreign-OS CI does not choke.

`software --check` now HAZARDs:
1. any recorded worktree path (canonical name, bare `worktrees`, or a line `dir`)
   that **escapes the host root** — absolute, or `..`-climbing — the structural
   invariant with teeth;
2. a `store`-backed line whose in-tree handle is **missing or does not resolve to
   the store** (the pin/branch check then runs against the resolved store).

Link-kind is inferred by platform and `--check` is kind-agnostic (it
`canonicalize`s the handle), so a hand-made bind-mount also satisfies it; the kind
is not recorded.

## Spine

The Where-room invariant — *every materialized worktree surfaces under the host
root; an external backing store is reached only through an in-tree handle* —
becomes an enforced MUST in host-template `CLAUDE.md` + an UPGRADING entry.

## Verification

- Unit tests: `escapes_root` (absolute, `..`-climb, in-tree); `parse_software`
  reads `store=`/`host=` and stays back-compatible on 3-token lines; a temp-repo
  materialize of a `store`-backed line creates an in-tree symlink resolving to the
  store, and `--check` passes; a bare external `dir` HAZARDs.
- `cargo test` + clippy green; version bumped + tagged `v0.13.0`.
- Applied here: re-pin `tools/host-lifecycle`, bump CI install rev, re-stamp
  `.host`; `software --check .` clean (this host has no external-store line, so
  the new HAZARDs stay silent).

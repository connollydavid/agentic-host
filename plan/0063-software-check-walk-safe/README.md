# plan/0063 software-check-walk-safe: the software --check tree walk must not follow a symlink into a cycle

`host-lifecycle software --check` recursively walks each component worktree, and three of its lanes did
so unsafely: they followed symlinks and had no cycle guard. A gitignored directory whose symlinks form a
cycle (a Wine prefix, `node_modules`, a virtualenv) made the walk never terminate. On a WSL2 `/mnt/c` 9P
mount, which is exactly this development host, each `openat` blocked in `p9_client_rpc`, so the process
wedged in uninterruptible sleep that even a kill signal could not reap, and repeated invocations piled up
wedged walkers. The gate that verifies pins, spec lanes, obligations, and build reproducibility became
unrunnable.

Reported as [connollydavid/host-lifecycle#15](https://github.com/connollydavid/host-lifecycle/issues/15).

## The defect

Three recursive walks, `read_obligations_text`, `find_specs`, and `read_dir_recursive`, tested each entry
with `p.is_dir()`, which dereferences a symlink, so a link pointing at an ancestor produced unbounded
recursion. They also descended into gitignored, untracked scratch, which is where a Wine prefix or a
`node_modules` places the arbitrary symlink structures that trigger the cycle. The sibling `collect_files`
walk was already safe: it reads the type from the `DirEntry` (an `lstat`, which does not follow the link)
and treats a symlink as a leaf.

## Decided direction

One shared symlink-safe, depth-bounded walker, `walk_files_safe`, that the three lanes route through, so
no lane can re-introduce the unguarded walk. A symlink is always a leaf and is never followed, which
breaks the cycle by construction; a depth cap is defence-in-depth against a non-symlink cycle such as a
bind mount; an unreadable directory is skipped rather than fatal. `read_dir_recursive` keeps an empty
skip list so the file set its input digest is taken over is unchanged.

## As-built

`walk_files_safe` is added and the three lanes call it. A `#[cfg(unix)]` regression test builds a
directory whose child symlinks back to an ancestor, walks it, and asserts the walk terminates, still
reaches the real files under the cycle, and never descends the link. Under the old `is_dir` walk the test
would not terminate. clippy is clean and the full inline suite passes. The obligations manifest is
unchanged (the lanes keep their names and `exercises=` links), so no discharge re-derivation is owed.

## Verification

Ships in the host-lifecycle release with the lifecycle batch, then re-vendor and propagate to consumers,
with the whole-suite verify gate green. The cheap-verification bar: a worktree carrying a gitignored
symlink cycle passes `software --check` in bounded time rather than hanging.

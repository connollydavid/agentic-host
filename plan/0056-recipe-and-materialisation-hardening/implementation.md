# plan/0056 implementation: addressing #6, #7, #8, #9

A detailed plan for each defect in the superset. Line citations are anchors into the current
`software/host-lifecycle/main/src/main.rs`; confirm them at edit time.

## Ordering and release

Address the defects in the order #7, #6, #8, #9. `#7` is fully designed and self-contained;
`#6` is mechanical and well-scoped; `#8` carries a layout migration and a `call/` decision;
`#9` changes the release command and adds a gate, and is recorded as `call/0038`.

Recommendation: one host-lifecycle release carries the `#6`, `#7`, `#8` code, and `#9` folds
into that release's own outward instructions. One pin bump, one re-vendor, one propagate. Split
`#8` into its own release only if the layout migration proves large enough to warrant it.

## #7 remap: a fail-safe no-op that still audits

Goal: `remap` treats an empty or absent `.host-remap` as a fail-safe no-op with an informational
line; a malformed dictionary still errors; the `--check` case still audits, so an empty
dictionary never yields a clean verdict without a scan.

Changes:

- `remap` (`main.rs:714`): remove the `rules.is_empty()` guard, so an empty dictionary reaches
  the `--check` / `--apply` dispatch.
- `load_remap` (`main.rs:731`): an absent file (a NotFound read error) yields an empty rule set;
  any other read error keeps the loud exit. The malformed-line errors (`main.rs:744`, `749`)
  stay.
- `remap_apply` (`main.rs:974`): when the rule set is empty, print
  `remap --apply: no rules in .host-remap; nothing to rename (0 files changed)` and return,
  ahead of the clean-tree guard, because a no-op writes nothing and needs no clean tree.
- `remap_check` (`main.rs:926`): count the targets scanned, and give the summary line a rule
  count and an outcome clause: `; clean` when zero tells remain, or
  `; author a .host-remap or allow entry` when any remain. Keep the exit code keyed on the
  remaining tells.

Tests (`remap_tests`, `main.rs:7982`):

- an empty `--apply` writes nothing and prints the no-op line.
- a `--check` over an empty and over an absent `.host-remap`, against a target holding a tell,
  still reports the tell and exits non-zero. This is the anti-hollow guard.
- `load_remap` on a directory with no `.host-remap` returns an empty set.

Testability note: `remap_check` and `remap_apply` end in `process::exit`. Extract the
scan-and-decide core into a function returning an exit code, and keep the `process::exit` at the
boundary, so a test asserts the code directly.

Verify: `cargo test`, plus a manual `remap --check` on a tree with no dictionary, which exits 0
when the tree is clean.

## #6 recipe value normalization

Goal: every `.host-software` value line is normalized (a `"..."` wrapper stripped, a stray
quote rejected) before it reaches git, curl, the filesystem, or a hash compare, matching the
`.host` stamp reader that already does this.

Changes:

- Add a shared helper, or reuse `stamp_value_after_eq` (`main.rs:437`), that strips a single
  surrounding double-quote pair, else takes the trimmed token, and rejects an unbalanced quote
  with a line error.
- Apply at `parse_software` (`main.rs:3825`) for every field: `url`, `pin`, `branch`,
  `worktrees`, `toolchain`, `deploy`, `artifact` (both whitespace tokens), `hooks`,
  `deps-bundle` (both tokens), and the `worktree` line `store=` token.
- Apply at `parse_project_facts` (`main.rs:1400`) for `document`, `member`, `drivers`.
- Apply at `parse_rung` and the obligation manifest (`main.rs:5340`, `5606`) for the `spec=`,
  harness, and `bound=` tokens.
- A stray or unbalanced quote in a value is a loud line error (exit 2), matching the
  malformed-line discipline already in `parse_software`.

Tests:

- helper units: a wrapped value, a bare value, an unbalanced value, an empty value.
- a stanza with `worktrees = "main"`, `pin = "<sha>"`, and `artifact = "path" "<sha>"` parses to
  unquoted values.
- an unbalanced `pin = "abc` exits 2.

Verify: `cargo test`, plus the audit flow, where a quoted value no longer reaches git.

## #8 git layout: `.bare` plus a `.git` file

Goal: materialisation produces `software/<name>/` holding `.bare/`, a `.git` file
(`gitdir: ./.bare`), and the `<branch>/` worktrees; git tooling resolves the container through
the `.git` file; the docs match; existing components re-materialize.

Changes:

- `store_dir` (`main.rs:4051`) returns `component_dir(root, name).join(".bare")`. The existing
  callers (`main.rs:3619`, `4133`, `4255`, `4367`) keep operating on the returned path.
- Materialize (`main.rs:4133`): after the bare clone (now into `.bare`), write the `.git` file
  at `component_dir(root, name).join(".git")` with `gitdir: ./.bare` and a trailing newline.
  Confirm `git -C software/<name> worktree add` and `worktree list` resolve through it.
- `--check` (`main.rs:4367`): keep the bare-store existence check on `.bare`, and assert the
  `.git` file exists and points at `.bare`, so a half-migrated component is caught.
- `collect_files` skip set (`main.rs:880`): add `.bare` beside `.git`, as a guard if the walker
  ever descends into a component directory.
- Docs and reconcile: update the `.host-software` header, the materialize doc comment
  (`main.rs:1201`), the `store_dir` doc (`main.rs:4049`), the `plan/0029` comment
  (`main.rs:4001`), and the `.gitignore` note, so no stale `<name>.git` or `<name>/.git`
  bare-store reference remains.
- Tests (`main.rs:9171`, `9132`): assert `.bare` plus the `.git` file, in place of a `.git`
  directory.

Migration of already-materialized components: re-materialize from `url` and `pin` (a teardown
then a materialize), which the recorded pin reproduces deterministically. The milestone
documents the one-time operator action.

Decision owed: a `call/` decision records superseding `plan/0029`'s bare-store placement: the
layout, the migration, and the rationale that a bare repo named `.git` fights git tooling.

Verify: `cargo test`; an end-to-end re-materialize with a clean `--check`; a `git status` inside
`software/<name>/` that no longer errors on a bare repo, and an IDE that no longer flags the
directory as a stray repo.

## #9 template pin on release (call/0038)

Goal: a tool release leaves the template's pin of that tool equal to the released version,
carried by the release command and enforced by a gate. The durable policy is `call/0038`.

Changes:

- The release sequence for a tool the template pins bumps the template's pin (the `prose.yml`
  revision today), commits and pushes it inside the template, then bumps the submodule pointer
  in the host.
- `host-lifecycle release` prints the template-pin bump as an explicit outward instruction,
  beside the re-pin and re-vendor instructions.
- A release gate reads the template's pinned tool versions and fails when any is older than the
  latest release of that tool.

Tests:

- a gate unit over a fixture template whose pin sits behind the released version fails; an equal
  pin passes.

Verify: a dry release confirms the outward instruction is printed and the gate fires on a stale
pin.

## Cross-cutting verification and release

- Build and test in the host-lifecycle worktree (`cargo test`, the integration script).
- Cut one host-lifecycle release carrying the `#6`, `#7`, `#8` code, with `#9` changing the
  release command and gate. Determine the change-class at release: `#6` and `#7` add no detector
  flags, and a new `--` output line or gate may set it.
- Re-vendor and propagate to the consumers that pin host-lifecycle (`plan/0032`, `call/0021`),
  and bump the template pin per `call/0038`.
- The whole-suite verify gate is green across host-lifecycle and every consumer.
- The Fen acceptance probe drives the real 4B through the four flows (author a quoted
  `.host-software` value, run `remap` on an empty dictionary, read the materialized layout, and
  run a release), and confirms each is legible and fail-safe where the un-hardened forms fumble
  it.

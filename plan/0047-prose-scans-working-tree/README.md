# plan/0047: the prose lane audits the authored working tree, not just the tracked subset

`host-lint --docs` and the `host-lifecycle prose` recheck that embeds it audit authored markdown by
walking `git ls-files`, which lists tracked and staged files only. A brand-new authored doc that has
not been staged yet is silently skipped, so a pre-commit `prose` run reads clean over it and then the
same doc fails the `verify` recheck once committed, with no content change.
connollydavid/host-lint#17 reports it. This milestone widens the walk to the authored working tree,
so a new doc is audited before it is staged and a clean result is never silently partial.

## Problem and investigation

The skip is real and partly intentional. The walk uses `git ls-files` precisely to exclude
gitignored output, vendored deps, un-materialized worktrees, and submodules, which is why the prose
lane never trips over generated content. Skipping an untracked authored file is a side effect of that
choice. Two facts narrow the gap: staging closes it, because `git ls-files` includes staged files (a
`git add` makes the new doc scanned), so the window is only the moment between creating a file and
staging it; and the workaround (stage before checking) is documented. So the question is whether a
pre-commit check should cover the unstaged case at all.

The cast answers it. A `prose: clean` that silently skipped a new file is the record that
**overstates completeness** Bly is built to catch, the **silent trap** Fen fumbles into (clean
pre-commit, HAZARD post-commit), and the instruction that **fails unsafe when followed literally**
that Orin guards against. By the methodology's own fail-safe principles a silent partial-clean is a
defect, even where the scan scope is intentional. The operator chose to widen the walk.

## The design

`run_docs`, the shared engine (host-lint library, used by both `host-lint --docs` and
`host-lifecycle prose` since plan/0045), walks two sets: `git ls-files` (tracked and staged) and
`git ls-files --others --exclude-standard` (untracked files git would offer to add). The two sets are
disjoint, so no dedup is needed. `--exclude-standard` keeps gitignored output, vendored deps, and
un-materialized worktrees out, exactly as the bare `git ls-files` walk did, so only authored markdown
that is or is about to be in the repo is audited. The per-file logic is unchanged: `.md` only,
`.host-lintignore` honored, symlinks skipped.

The walk scope is a host-lint implementation detail, not spine doctrine (the spine never states the
mechanism), so this milestone needs no doctrine change and no adopter `UPGRADING` entry. A fresh CI
checkout carries no untracked authored files, so CI behaviour is unchanged; only a local pre-commit
or working-tree run gains the new coverage.

## Validation

Confirmed end to end before release. The `#17` reproduction now flags an untracked authored doc
while the gitignored generated tree stays excluded. On agentic-host, `git ls-files --others
--exclude-standard` finds no markdown (the generated `mdBook/` and `book.toml` are gitignored), so
`--docs` stays clean and the verify recheck is unchanged. A unit test pins all three cases: a tracked
doc scanned, a new untracked doc scanned, a gitignored generated doc excluded.

The real qwen3.5-4b judged the fix at the weak-agent bar (rope, true system prompt): handed a new
unstaged doc with an error, it said the new working-tree walk catches it in every run, and the old
tracked-only walk misses it in every run. The five cast personas confirmed the change serves them.

## Build sequence

### Investigate and decide {#investigate-decide}

Reproduce the skip, confirm it is intentional and that staging closes it, and weigh fix against the
documented workaround through the cast. Operator chose to widen the walk.

- verify: attested operator

### Scan the authored working tree {#scan-working-tree}

Widen `run_docs` to `git ls-files` plus `git ls-files --others --exclude-standard`; the per-file
logic and the gitignore exclusion are unchanged. A unit test pins the three cases.

- depends: #investigate-decide
- verify: cd software/host-lint/main && cargo test

### Validate with Fen and the cast {#validate}

Confirm the fix end to end (untracked caught, generated excluded, CI unchanged) and at the weak-agent
bar with the real qwen3.5-4b, and consult the cast.

- depends: #scan-working-tree
- verify: attested operator

### Release host-lint and cascade host-lifecycle {#release-cascade}

Re-derive the kani digests before tagging (the `src/lib.rs` edit stales them), release host-lint,
bump host-lifecycle's host-lint dependency, regenerate the offline bundle as `vendor-v3`, release
host-lifecycle, and re-pin `.host-software`.

- depends: #validate
- verify: attested operator

### Re-pin, close, and verify the suite {#close-and-verify}

Bump the CI install pins, record the receipts, close the issue, and confirm the whole suite is green.

- depends: #release-cascade
- verify: attested operator

## Risks

- The walk now reads untracked authored markdown, so a working-tree draft a developer has not chosen
  to commit is audited. That is the intended coverage, and a genuine scratch file is gitignored, which
  the `--exclude-standard` filter excludes.
- The change is in the shared `run_docs`, so it cascades through a host-lint release and a
  host-lifecycle release with a regenerated bundle, the same shape as plan/0045.

## Status

in progress.

# plan/0060 host-lint-pre-commit-hook: the hook skips a gitlink instead of failing closed on it

The host-lint pre-commit hook blocks any commit that stages a submodule pointer. Found while bumping
the host-template pointer during the plan/0057 release, and worked around there with a gitlink-only
`--no-verify` commit.

## The defect

[connollydavid/host-lint#18](https://github.com/connollydavid/host-lint/issues/18): the hook lints each
staged path via `git show ":$file" | host-lint --stdin-as "$file"` under `set -o pipefail` (the
pipefail was added by the fail-open hardening). For a submodule gitlink, `git show ":<submodule>"`
exits 128 (a gitlink is not a blob), and pipefail propagates that 128 to the hook's `rc`, which the
default case treats as fail-closed:

```
host-lint: error linting <submodule> (exit 128); failing closed
```

So the pipefail hardening, correct in itself, regressed submodule-pointer commits: every commit that
stages a gitlink is now blocked. A gitlink carries no text to lint, so failing on it is wrong.

## Decided direction

Skip the gitlink rather than fail on it: drop mode-160000 entries from the staged path list (read the
mode with `git diff --cached --raw` and skip `160000`), or treat a `git show` exit 128 on a gitlink as
clean. Preserve the fail-closed behaviour for every real failure (a usage error, a panic, a genuine
`git show` failure on a blob), so the hardening the pipefail bought is not lost.

## Verification

A regression test that stages a submodule pointer and confirms the hook exits clean rather than fail
closed, plus the existing fail-closed tests still passing on a real error. Ships as a host-lint
release with the hook asset rebuilt, re-vendored and propagated to the consumers, whole-suite verify
green.

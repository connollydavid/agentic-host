# plan/0064 prose-audits-the-repo: --prose with no files and --all audit the tracked doc set

`host-lint --prose` with no file arguments did not audit the repository. It once reported clean at exit 0
with no output, a fail-open for a script that trusts the exit code, and after the plan/0055 hardening it
exited with an error instead. Either way there was no `host-lint` CLI invocation that prose-audited a
whole repository, and `--all` ran only the naming lane, so no single command matched the authoritative
`host-lifecycle prose` gate. An author who ran `host-lint --prose` as a local pre-flight saw a result
that disagreed with the CI gate on the same tracked docs.

Reported as [connollydavid/host-lint#20](https://github.com/connollydavid/host-lint/issues/20).

## The defect

The prose audit ran only when explicit file paths were passed. `--prose` with no files had no repo-wide
behaviour, and `--all` covered the naming lane alone. The repo-wide prose audit existed as `--docs`, but
nothing tied it to `--prose` or `--all`, so the obvious pre-flight commands missed the tropes the gate
catches.

## Decided direction

One shared `audit_tracked_docs` helper runs the tracked-doc prose audit, and `--all`, `--docs`, and
no-file `--prose` all route through it. `--all` becomes the comprehensive repository audit: the naming
lane over tracked files plus the prose lane over tracked authored docs, so one command matches the
host-lifecycle naming and prose gate. `--prose` with no files audits the tracked docs rather than
erroring; `--prose <files>` still scans exactly those files.

## As-built

The dispatch is reordered so `--all` is handled before `--prose`, which lets `--all --prose` fold into
the comprehensive audit rather than erroring. Integration tests assert that `--prose` with no arguments,
`--all`, and `--all --prose` each flag a tracked-doc trope; the existing `--all` symlink and termination
tests stay green, and `--docs` behaviour is unchanged. The README records that `--all` now runs both
lanes. clippy is clean and the unit and integration suites pass.

## Verification

Ships in the host-lint release that carries the pre-commit-hook gitlink fix (plan/0060, host-lint#18 and
host-lint#19), then re-vendor and propagate to consumers, with the whole-suite verify gate green. The
cheap-verification bar: `host-lint --prose` and `host-lint --all` in a repository with a tracked-doc
trope both report it, matching `host-lifecycle prose`.

# plan/0092 front-door ledger walk: the forge follows its own front door

Operator-directed: read and follow `https://github.com/connollydavid/host`, with the
caution that this forge is the methodology's developer, not an adopter. The door
applied here classifies case (c), the `.host` stamp at `baseline = ff04a94`, and
its procedure runs through the root `AGENTS.md` as sole authority: no re-adoption,
no history rewrite, the stamp touched only by `host-lifecycle upgrade`, and any
defect in the published procedure filed upstream on `connollydavid/host` (the
family's issue tracker) rather than worked around. The entrance worktree
(`software/host/main`) sits exactly at the public main the operator named
(`bcbf449`), so the procedure followed is the procedure published.

## The ledger is current

The recording debt the cutting session anticipated is already paid.
`host-lifecycle upgrade .` reports `up to date (baseline ff04a94, 15 applied out of
order)`; `.host-receipts` carries all 15 `applied` claims, each `via=verify`, dated
2026-07-20 through 2026-09-14 in ledger position order, recorded as each entry
landed (plan/0073's two-tier memory through plan/0089's lem lane), not batched
afterward. The front door's case-(c) walk on this forge is therefore a
verification, not a migration.

## Setup drift, repaired

`software --verify-setup .` opened with 9 HAZARDs, all one shape: the installed
commit hooks in the host repo and the eight materialized worktrees did not match
the built host-lint binary. `host-lifecycle software --install-hooks .` installed
them, each verified against the canonical hash; the re-run gate is green (exit 0).

## Preview

- `classify` prints `c`.
- `host-lint --all`: no flag, 159 warnings (exit 3), advisory, read by kind (the
  trailing-token census: bare-numeral versions `0.2` through `11.4`, `section`
  anchors, CI run ids, quoted probe prose in the plan/0080 and plan/0090 harness
  files), each kind confirmed a genuine version or identifier, the door's own
  reading rule.
- `host-lint --prose`: no flag, 8 warnings (exit 3): an ing-tail and a false-range,
  both on the untracked root debris below, notes in the plan/0090 and plan/0091
  variant corpora.
- `host-lint --log`: 11 tells in history (exit 1), informational: the ordinal
  wave/stage naming of the 2026 record, acknowledged, never rewritten outside Deep.
- Two untracked files at the root, `a-t1-3.md` and `c-t2-2.md`, are debris from
  plan/0088's A/B harness (their tracked siblings live in
  `plan/0088-prose-guidance-ab/fen-samples/`). Reported, not deleted: removal is
  the operator's call.

## Spine alignment

The front door's step 4 (re-apply the spine doc changes across the span) finds
nothing owed:

- The `lem` section is byte-identical to the template manual at `b917d4d`, heading
  apart; the LEM-address-direction and LEM-exemplar-section landings copied it here
  as they landed (plan/0090 records the copy).
- The declared-corpus section restates the doctrine with its sentences verbatim and
  its opening instantiated (`.host-corpus`, the three declared files), the intended
  shape for an instance manual; `CLAUDE.md` is the one-line text pointer the
  ACTIVE-corpus entry requires.
- The four-principles section differs from the template's terse text, and is not
  drift: the terse text was already in place at the baseline (the rewrite `b67a328`
  predates `ff04a94`), so the host's longer text is the long-standing, declared
  restatement, watched by `entrance --check` and `reconcile`, both clean.

## Verify

Recorded at closure.

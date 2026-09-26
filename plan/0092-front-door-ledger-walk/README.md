# plan/0092 front-door ledger walk: the forge follows its own front door

**Complete 2026-09-26.** The standing protocol is call/0059.

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

- `validate plan/` and `validate call/`: ok.
- `refs --gate .`: every register reference resolves (215 docs read, 272 issue
  refs carried as legibility debt, 47 record-layer docs excluded and disclosed).
- `software --check .`: green at the close, every worktree at its pin, every
  applied ledger entry's post-condition re-verified.
- `host-lint --all` / `--prose`: no flag; warnings advisory, per the preview.
- The hook tell test: a flag-tier message (blocking noun plus numeral) is blocked
  (exit 1, no commit created); warn-tier messages commit by design, which the
  first probe confirmed by passing clean: the slop words are the grammar's gray
  zone, not flags.
- The site builds: `book .` wrote 192 pages, `book --check` renders every room,
  `mdbook build` exits 0.

**The one live find beyond the records: the verify receipt had stood red since
2026-09-14.** The recheck is strict-zero on authored-doc prose warns, and
plan/0089's landing left five decoration dashes in its README, so
`software --check` re-opened the receipt on every sweep after. The walk tripped
the same bar with four warns of its own (two decoration in call/0059, a
negative-parallelism and an ing-tail in call/0059 and the index row); all nine
were reworded plain and the receipt closed green. The 2026-09-14/15
release-cascade receipts (host-grammar v0.7.0, host-lint v0.20.0 through v0.22.0,
host-lifecycle v0.54.0 through v0.54.2) were found uncommitted and are recorded
with this walk. Closing lesson: the gate sweep is part of every landing, run
before the last push, not a closing-time formality.

# plan/0113 cast review redo: the corrected harness before the redo

- Review date: 2026-11-27.
- Reviewed: the corrected plan README and the harness at its current state, the
  native adapters, the 10800s two-way budget, the Opus 5.5 judge, the fresh
  held-out set, the smoke gate and the re-run rule, plus the all-arm smoke
  record and the first review (`design-review.md`).
- The five seats reviewed independently. Their findings continue the first
  review's numbering: M5-M10, W6-W11, B5-B10, O5-O10, F5-F10.
- Every finding is dispositioned below. The accepted fixes are folded into the
  two existing redo tasks (`#selection-redo`, `#confirmation`) and the
  component scaffold, so the task graph does not grow; the operator rulings
  below are the only items that are not the agent's to decide.

## The findings

### Confirmation: hard-wired to `weizhena`, judge-blind, void-blind

**M5, W6, B5, O6, F5: blocker.** `confirm.py` reads a locked arm but computes
`margin` and the floor from `"weizhena"`, falls back to `weizhena` when
`round-redo.json` is absent, never reads `judge.json`, counts a void as a
measured zero, and does not randomise the block order. A redo lock on hffmnnj
or kanatami raises `KeyError` after the 20 draws; a missing lock silently
confirms an excluded arm.

**Disposition: accepted.** Folded into `#confirmation`: the locked arm is read
once and used in the margin, floor, print and `verdict.json`; a missing or
invalid lock refuses; `--key` is required; `--check` does not decrypt; the
judge runs on the held-out draws; a void is a gate, not a zero; the block order
is randomised; a non-`weizhena` lock test is required.

### Caps: declared, not enforced; the aggregate is unapproved

**M6, W7, B9, O7, F9: blocker.** `contract.CAPS` declares 200000 prompt /
50000 completion / 60 tools / 10800 wall, but only the wall is enforced.
The kanatami smoke records 61,492 completion tokens against 50,000 and is
still `valid: true` at 9.818/16. The 30 selection + 20 confirmation draws at
10800s two-way are 75-84 hours, which the operator approved only per draw.
`PLAN.md` still cites the old null smoke's 435.6s, not the 5021.9s smoke; the
budget README title still says “3600 seconds.”

**Disposition: accepted.** Folded into `#selection-redo`: `used <= caps` is
checked in the driver, the receipt and the smoke; an over-cap draw is a void
with the used counts; the caps state what each bounds; the budget title and
PLAN row are corrected. The cap values and the aggregate need the operator
ruling below.

### The re-run rule: budget exhaustion is not a harness break; attempts are deleted

**M8, W8, B7, F6: blocker.** The rule calls a budget-exhausted draw a
re-runnable harness break, which would loop the cap. The driver has no re-run
path, `--force` deletes the only attempt, a void contributes to the pooled
score, a fully invalid round can still lock, and the judge scores void draws.

**Disposition: accepted.** Folded into `#selection-redo`: a harness break is a
draw not executed as specified (crash, missing binary, adapter exception,
wrong model/provider/harness); a budget-exhausted draw is an arm result,
recorded, not re-run. Every attempt is retained with a `break_class` and a
`rerun.json`; `round.py`/`confirm.py` refuse a lock or verdict while a harness
break lacks a later recorded re-run; the judge scores only valid draws.

### The lock: zero-valid arms and a suite-fit of four constants

**M9, W11, B6, O8, F7: blocker/should-fix.** `round.py` can lock an arm with
no valid draw; the band does not require a candidate to clear the null; the
six-row suite-fit is four literal `True`s and one duplicated boolean; the
band is stated as 1.0/16 in one place and 1.5/24 in another; the prose
component is 0/3 on every smoke draw.

**Disposition: accepted.** Folded into `#selection-redo`: a pre-declared
valid-draw floor and a null-relative gate refuse a lock when no candidate
clears them; the six-row evidence table is computed from the draws and arm
snapshots, with the null marked control; the band is stated once as 1.5/24;
the prose component's near-constant status is recorded.

### The kanatami fetch log: the report is the evidence

**O5, F4: blocker.** The driver synthesizes `workers.json` from every URL in
the run text and writes the report paragraph as the fetch-log snapshot. The
rubric then finds the report's quote in the report's own paragraph; the 32/33
citation support and the phantom pass are self-referential. The 9.818 is not
an arm result.

**Disposition: accepted.** Folded into `#selection-redo`: the report-to-fetch
fallback is removed. Only a completed `webfetch` event or an arm-written
fetched-page record whose snapshot is the page may enter the log; a kanatami
draw without one is an exclusion or a void; the smoke is re-run.

### The samber/weizhena exclusions: a parser miss, an ungated gate, 12 draws

**M10, W9, B8, O9, F8: blocker/should-fix.** The samber notes carry inline
URLs and verbatim quotes but no `url:` labels; the adapter excludes them. The
suspect-exclusion gate checks only hffmnnj and kanatami. The weizhena
`results` JSON carries a `sources` array with URLs but no quote/locator. The
12 excluded-arm draws cost about 11.4 hours of two-way wall clock.

**Disposition: accepted.** Folded into `#selection-redo`: the samber adapter
parses inline markdown links and quoted passages; the weizhena source array is
checked; the suspect gate covers every arm; a native URL+quote+locator record
is a harness break, not an exclusion. Whether the two arms draw or the round
drops to 18 draws is the operator ruling below.

### Model and provider: receipts are declarations

**M7, W10, B12, O10, F3: blocker/should-fix.** The receipt's model is copied
from the pin; no `replies.jsonl` is written; the model pre-flight is never
called; a foreign reply passes. Four of five smoke receipts say
`search_provider: "none"` with no `websearch`; the one-provider rule is
unexercised for the research arms. The judge's model and validity gate are
unchecked. The hffmnnj embedding model and the arms' native search paths are
outside the pins.

**Disposition: accepted.** Folded into `#selection-redo` and
`#component-scaffold`: replies are extracted to `replies.jsonl` and
pre-flighted; the receipt carries the reply digest; a foreign reply voids;
the judge checks model/route/validity, retries and gates the lock; the native
search is measured or recorded, and the one-provider claim is scoped; the
hffmnnj embedding, native search and third-party notice are pinned or off.

### Smoke gate and records

**F6, B7, M6: should-fix.** `--skip-probe` and `--record-only` can write
`passed: true` without the isolation probe; `--only null` overwrites the
all-arm record; the smoke history does not retain the 3600s kanatami void or
the 969.1s hffmnnj exclusion; the null prompt names a task file and output
directory the driver does not provide.

**Disposition: accepted.** Folded into `#selection-redo`: the smoke record is
append-only, requires the isolation probe for a PASS, refuses a partial
`--only` overwrite, retains the attempt history, and the prompt paths are
supplied.

### The fresh held-out set and the key

**W2, B3, F note: blocker.** The first fresh set was read by
`confirm.py --check`, which decrypts before checking the lock; its key sits
under `/tmp`; the plaintext is outside the tree but the set is burned.

**Disposition: accepted.** Folded into `#confirmation`: a second fresh set
with new SimpleQA rows and new house tasks is sealed with a new key; the
operator holds it and passes `--key`; `--check` reads only the sealed digests;
the first fresh set is recorded as read and burned.

## Operator rulings needed

1. **The aggregate wall clock.** 30 selection + 20 confirmation draws at
   10800s two-way is 75-84 hours. Approve, or cut the round to 18 draws.
2. **The caps.** Enforceable budgets, raised to 300000 prompt / 100000
   completion / 60 tools / 10800 wall, or recorded costs with the “cap” claim
   removed. L recommends enforceable budgets at the raised values.
3. **The weizhena and samber arms.** Parse their native reports (the latitude
   direction) and keep 30 draws, or exclude them at the round level and run
   18. L recommends the parsers; if a parser cannot recover the record, the
   arm is excluded with evidence.
4. **The fresh key.** The operator holds the new set's key; the driver takes
   `--key` and never reads a default path.
5. **The optional sixth and the one-provider claim.** Record whether
   `gptr-mcp` enters; pin or turn off the hffmnnj embedding; scope the
   one-provider claim to the measured null/search or record each arm's native
   route.

## Dispositions

The findings above are accepted. The fixes are folded into `#selection-redo`
(caps, replies, re-run/attempts, suite-fit, kanatami fetch capture, samber and
weizhena parsers, two-way probe, smoke redo) and `#confirmation` (locked arm,
key, fresh-2, judge, valid gate, random order), with the component pin and
third-party clauses in `#component-scaffold`. The redo selection does not start
until the operator rulings above are recorded and the smoke is re-run under
the corrected machinery.

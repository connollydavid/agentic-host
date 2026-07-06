# plan/0062 plan-index-coverage: gate that PLAN.md indexes every milestone directory

The audited-plan rule says every milestone gets a row in PLAN.md's index. CLAUDE.md asserts it, and
nothing checks it, so the milestone directories plan/0056 through plan/0060 sat unindexed for five
milestones before the gap was noticed by eye. This is the self-blindness class plan/0036 and plan/0038
already named: a rule with a home but no gate.

## The defect

PLAN.md is the human-readable index of the plan/ room, and its rows are authored by hand on each
milestone. No check compares the rows against the directories on disk, so a milestone can ship its
directory and README, be committed and pushed, and never appear in the index, with no complaint from
any gate. The work itself is tracked truthfully by the receipts and `software --check`; what drifts is
only the index a reader navigates by, which is the artifact a cold reader trusts to find the milestones.

## Decided direction

A coverage check, in the shape reconcile already uses for `.host-software`: derive the owed set from
repo state each run. List the `plan/NNNN-slug` directories, list the rows PLAN.md links, and HAZARD any
directory with no row. The check reads the repo, holds no stored state, and re-lists on the next run, so
a partial fix never buries the remainder. This is a coverage invariant rather than a receipt: no action
is being attested, only a correspondence between the directories and their index.

## The cast's throughline

- **Bly** (writes now, reads cold): the index is what a memoryless read navigates by, so an unindexed
  milestone must surface as owed, over-reporting, never silently absent.
- **Orin** (maintainer): express the rule once and gate it where it lives; an asserted rule with no gate
  is the recurring defect.
- **Fen** (acceptance test): one check names the gap and the directory that owes a row, so the weak
  agent fixes it in one move rather than auditing the index by hand.

## Open questions

- Whether the check lives in `validate` (which already owns plan/ naming) or `reconcile` (which owns the
  repo-level coverage pattern).
- Whether it is spine doctrine. PLAN.md and the plan/ room are methodology structure that every adopter
  carries, so a plan-index coverage check reads as spine, which would need a host-template ledger entry,
  gated by the anti-ouroboros scope rule. The milestone settles this.
- Whether the reverse direction is checked too (a PLAN.md plan-row that points at no directory), the same
  coverage read from the other side.

## Verification

Ships as one host-lifecycle release, then re-vendor and propagate to consumers, with the whole-suite
verify gate green. The check HAZARDs a synthetic unindexed milestone directory and passes once the row
is added. A real qwen3.5-4b probe confirms the weak agent reads the HAZARD and adds the missing row.

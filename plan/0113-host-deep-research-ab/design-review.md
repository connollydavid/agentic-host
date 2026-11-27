# plan/0113 cast review: the design before the first draw

- Review date: 2026-11-27.
- Reviewed: the plan README's design and the harness artifacts at their pins
  (arm snapshots and licenses, OpenCode v2.4.2 harness, the named
  `qwen3.6-27b` route, the run contract and dry runs, the frozen task sets, the
  rubric and its controls).
- No live draw has run. The review is recorded before the selection round, and
  the dispositions below are the changes that landed before it.

## Mara, the operator

### M1. The protocol's numbers were prose, not a freeze

The protocol said "a pre-declared band", "a minimum margin", "a per-task
floor", and "the size of each round ... bounded by cost", with no number
fixed. The lock and the ship gate could be read after the table. That is the
winner's-curse opening the plan itself names.

**Disposition: accepted.** The plan README's protocol now freezes one selection
round of 30 draws (5 arms × 6 tasks × 1), a band of 1.0 point of the 16-point
applicable maximum, 20 confirmation draws (2 arms × 5 tasks × 2), a margin of
1.0 point and a per-task floor of 8 of 16. The numbers sit above the table.

### M2. The suite-fit score had no evidence row

The lock takes the highest suite-fit among arms within the band. The six
criteria were listed, but a score of 4 could be a naked judgment; the operator
could not audit which criterion carried which arm.

**Disposition: accepted.** The selection record now carries a six-row table,
one row per criterion, with the evidence for every arm in the band. A suite-fit
score without the row is not a score; the plan's `#selection` verify names the
table.

### M3. The operator's two approvals can diverge

The goal's `goal accept` closes the milestone; the ship gate's default change
also needs the operator's approval. The plan did not say they are the same
decision.

**Disposition: confirmed, no change.** `#ship` already says the default changes
only with the operator's approval; that approval is separate from the goal's
acceptance, and the ship record cites it separately.

### M4. The spend was unbounded

"Bounded by cost" is not a bound.

**Disposition: accepted with M1.** The frozen 50-draw plan and the contract's
per-draw caps (200000 prompt tokens, 50000 completion tokens, 40 tool calls,
1800 wall seconds) bound the spend. The operator may halt a round; the halt is
recorded, never silently absorbed.

## Wren, context and budget

### W1. The arm agents hard-code foreign models

The weizhena agent at its pin carries `model: openai/gpt-5.4`; the kanatami
worker carries `model: opencode-go/deepseek-v4-flash`. The reference model is
the only subject. A draw that runs either agent as written is a draw on a
foreign model, and the model pre-flight would void it.

**Disposition: accepted.** The per-arm draw config overrides every role's model
to `api.d07yx58.net/qwen3.6-27b`; the arm's own files are never edited. The
override is a house config, its digest is in the receipt, and the plan's Roles
bullet and the contract README now say so.

### W2. The search provider was still open

The dry-run receipt said `exa`, but the plan's open questions still asked which
provider. A draw on another provider would record a different receipt.

**Disposition: accepted.** Exa is the one provider, with
`OPENCODE_ENABLE_EXA=1`; every receipt records `exa`. The plan's constants and
open questions now say so.

### W3. The budget caps lived only in the contract

The plan's budget bullet said "the same per-draw cap" without the numbers; a
plan reader could not audit a receipt.

**Disposition: accepted.** The plan's Budget bullet carries the contract's
numbers and says every receipt carries the caps with the used counts.

### W4. The source snapshots are on disk, not in the context

The ledger keeps the short quote; the snapshot is a file. The report does not
carry page text into the model's window.

**Disposition: confirmed, no change.** The ledger, fetch log and snapshots are
the on-disk surfaces; the budget caps the model's tokens.

### W5. The weizhena agent's own tools may block its output

The weizhena agent at its pin has `write: false`; the research-deep prompt tells
it to write JSON to a path. A weak executor would not find a shell workaround.

**Disposition: accepted.** The per-arm draw config overrides the agent's tool
permissions for the scratch draw; the arm file is untouched. The contract
README names the override.

## Bly, the cold reader

### B1. The rubric reads a fetch log the contract never names

`harness/rubric/rubric.py` voids a phantom source by reading
`fetch-log.jsonl`, but the run contract's output table listed only
`report.md`, `sources.json` and `receipt.json`. A cold reader of the contract
could not know the log was required.

**Disposition: accepted.** The contract now names `fetch-log.jsonl` (one line
per fetch: `url`, `status`, `snapshot`) as a live-draw output;
`contract.py` gains the log validator, and the rubric's dependency is explicit.

### B2. The prose score's tool version was not recorded

The rubric runs `host-lint --prose`, but the record did not name the version; a
later host-lint could score the same report differently.

**Disposition: accepted.** The rubric record names `host-lint 0.24.1`, the
version the controls ran.

### B3. The held-out key sits under /tmp

`sets.json` points at `/tmp/opencode/plan0113/held-out.key`; a reboot loses it,
and a cold reader cannot verify the held-out contents without it.

**Disposition: custody note.** The key is outside the repo by construction; the
operator must move it to their custody. The pointer is a location, not a
secret. The selection driver never reads it; confirmation decrypts with the
operator-held key.

### B4. The per-draw receipt and score are the audit surface

The selection round's value to the cold reader is the receipt and the rubric's
JSON per draw.

**Disposition: confirmed.** `#selection` records every draw's receipt and
score, and the frozen numbers make the table readable.

## Orin, the adopter

### O1. The component scaffold did not require the harness and model pins

The scaffold said bare store, worktree, Unlicense, third-party notice and the
arm; an adopter could ship the shim without the pinned OpenCode release or the
reference model.

**Disposition: accepted.** `#component-scaffold` now requires the component's
run contract to carry the v2.4.2 archive and binary digests and the model pin,
and the recipe check reads them.

### O2. The third-party notice and the arm's license

The plan says the shimmed arm keeps its license, pinned and unmodified, in a
third-party notice; house adaptations are house files.

**Disposition: confirmed.** The arm snapshots are unmodified, the adapters live
in `harness/contract/adapters`, and the notice is the scaffold's verify.

### O3. One harness authority

The operator ruled "consider only v2.4.2"; the house `tools/opencode` is 2.2.5.
An adopter could read the house pin as the authority.

**Disposition: confirmed.** The plan's open question is ruled, the component
carries the v2.4.2 pin, and the house pin is outside the milestone.

### O4. The component command is one command

The run contract is one task file in; the shim runs the arm; the weak executor
does not hand-edit a config.

**Disposition: confirmed for the design.** `#fen-acceptance` tests the real 4B
through the command, and `#ship` carries the recorded verdict.

## Fen, the weak executor

### F1. The hard-coded models again

Fen cannot repair a config or a model field.

**Disposition: accepted with W1.**

### F2. The weizhena write permission again

A weak executor cannot route around `write: false`.

**Disposition: accepted with W5.**

### F3. The null arm's prompt is a house file

The null arm is a fair control only if its frozen prompt is in the component's
files and its digest is in the receipt, not in the model's memory.

**Disposition: confirmed.** `harness/contract/prompts/null.md` is the file, its
digest is in the null receipt, and the component scaffold carries it.

### F4. The command's one human gate

The acceptance task allows at most one human gate inside a draw. The design's
draws have none; the task file is the input.

**Disposition: confirmed.** `#fen-acceptance` records the baseline and the
component run.

## The dispositions at a glance

| # | Seat | Finding | Disposition | Record |
|---|---|---|---|---|
| M1 | Mara | the protocol numbers were not frozen | accepted: 30 + 20 draws, band 1.0, margin 1.0, floor 8/16 | plan README protocol |
| M2 | Mara | the suite-fit could be a naked judgment | accepted: six-row evidence table | plan README `#selection` |
| M3 | Mara | the goal accept and the ship approval can diverge | confirmed: recorded separately | plan README `#ship` |
| M4 | Mara | the spend was unbounded | accepted with M1: the caps bound it | plan README protocol and constants |
| W1 | Wren | the arm agents hard-code foreign models | accepted: per-arm model override | plan README roles, contract README |
| W2 | Wren | the search provider was open | accepted: Exa | plan README constants and open questions |
| W3 | Wren | the budget caps were not in the plan | accepted: the numbers are in the plan | plan README constants |
| W4 | Wren | the snapshots are on disk | confirmed: the ledger and fetch log are the surface | contract README |
| W5 | Wren | the weizhena agent's `write: false` | accepted: per-arm tool override | contract README |
| B1 | Bly | the contract did not name the fetch log | accepted: `fetch-log.jsonl` named and validated | contract README, `contract.py` |
| B2 | Bly | the prose tool version was unrecorded | accepted: host-lint 0.24.1 | rubric README |
| B3 | Bly | the held-out key is under /tmp | custody note: the operator moves it | tasks README, `sets.json` |
| B4 | Bly | the per-draw receipt and score are the audit surface | confirmed | plan README `#selection` |
| O1 | Orin | the scaffold did not require the harness/model pins | accepted: the component carries them | plan README `#component-scaffold` |
| O2 | Orin | the third-party notice and the arm's license | confirmed | plan README licensing |
| O3 | Orin | one harness authority | confirmed: v2.4.2 only | plan README open questions |
| O4 | Orin | one command, no config edit | confirmed | plan README `#fen-acceptance` |
| F1 | Fen | the hard-coded models again | accepted with W1 | contract README |
| F2 | Fen | the `write: false` again | accepted with W5 | contract README |
| F3 | Fen | the null prompt is a house file | confirmed | contract `prompts/null.md`, receipts |
| F4 | Fen | the one human gate | confirmed | plan README `#fen-acceptance` |

The review is complete: every finding above is dispositioned in the plan
README, the contract README, the rubric README, or this record. The selection
round may start.

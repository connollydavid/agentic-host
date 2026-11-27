# plan/0114: host-deep-research, the A/B at the adapter layer

**Status: cut 2026-11-27, not started** (operator direction after plan/0113's
abandon: the live harness injected the ledger in the wrapper prompt rather than
the arm's native prompt and adapter, the selection and confirmation draws are
void, and the A/B data is invalid). The wrapper, the arms, the harness pin, the
reference model, the task sets and the rubric carry from
[plan/0113](../0113-host-deep-research-ab/README.md). The live driver, the
search provider, the budget and the held-out set are re-cut.; active goal since 2026-11-27

## Why

The premise of plan/0113 stands: research reaches the record as findings, not
as sources, and `host-deep-research` shims the arm that wins the A/B. The first
attempt did not measure the arms. It measured a harness defect.

## What plan/0113 taught

- **The ledger lives in the adapter.** The live driver sent every arm a wrapper
  postscript asking for `report.md`, `sources.json` and `fetch-log.jsonl`; the
  per-arm adapters built at plan/0113's `#run-contract` were never called. The
  skill arms ran their own workflows, spent the budget, and usually never wrote
  the house ledger. Evidence: the plan/0113
  [selection record](../0113-host-deep-research-ab/harness/selection/README.md)
  and `round.json`; 29 of 30 selection draws and 3 of 4 confirmation draws are
  void, while the null's frozen contract prompt and one weizhena draw produced
  a valid 13/16.
- **The provider was declared, not measured.** The receipts say `exa`; the
  null's fetch log goes to `html.duckduckgo.com` through `webfetch`. The
  "one provider" constant was never enforced.
- **The budget and the waves starve the model.** Every draw ran to the
  1800-second cap; the five-arm selection waves and four-arm confirmation waves
  left the reference model unable to finish. The cap and the wave width are
  house choices, not arm properties.
- **The held-out set is burned.** The plan/0113 confirmation read the sealed
  set; its five tasks are known. A fresh set is required for a fresh
  confirmation.

The artifacts that worked carry: the arm snapshots, the OpenCode v2.4.2 pin,
the `qwen3.8-flash-next` route, the contract and its adapters, the selection
set, the rubric and its controls, and the plan/0113 cast review's accepted
findings.

## The corrected harness

### The ledger's layer

The live driver sends each arm its own task prompt. The arm's adapter reads the
arm's native output and writes the contract: the null's frozen contract prompt
is the control; the hffmnnj adapter reads the library notes; the kanatami
adapter reads the worker results; the weizhena and samber adapters record the
exclusions their native outputs force. The wrapper postscript is gone.

### The provider

One provider, configured and measured. The receipt records the provider the
tool actually used, and a draw on another provider is void. Exa is the
candidate; if the probe cannot reach it, the operator re-rules the provider
before the round starts, and the choice is recorded.

### The budget and the waves

The per-draw caps and the draw order are re-decided and frozen before the first
draw: serial or two-way, never the five-arm waves. The receipt records the used
tokens, calls and wall time against the caps.

### The held-out set

The plan/0113 selection set carries forward; its held-out set does not. A fresh
held-out set is frozen and sealed with its own key, and its plaintext digest
and ciphertext digest are recorded before the first draw. The old held-out
plaintext is archived with plan/0113 as burned evidence, never reused.

## The A/B

The arms, the rubric, the suite-fit score, the lock rule and the confirmation
criteria carry from plan/0113. The frozen numbers are re-declared in this
plan's budget task and reviewed by the cast before the corrected selection.
The component's licensing carries: house files are `Unlicense`; a shimmed arm
keeps its own license, pinned and unmodified, in a third-party notice. On a
`NO-SHIP` the component ships the null arm's native agent under the contract.

## Build sequence

### Search provider {#search-provider}

Configure and probe one search provider under the pinned harness, and record
the provider the tool actually calls.

- verify: the provider probe passes; a draw's receipt records the provider the
  fetch log shows; a foreign provider voids the draw
- depends: none

### Budget {#budget}

Re-decide the per-draw caps and the draw order, and record the numbers before
any draw.

- verify: the caps and the wave width are recorded before the first draw; a
  smoke draw reports the used counts against them
- depends: none

### Task sets {#task-sets}

Carry the plan/0113 selection set; freeze a fresh held-out set and seal it with
its own key.

- verify: every task validates; the new held-out set is ciphertext with no
  plaintext in the tree; both set digests are recorded
- depends: none

### Live driver {#live-driver}

Send each arm its native prompt and call its adapter; the null keeps the frozen
contract prompt, and the weizhena and samber exclusions are recorded.

- verify: a smoke draw per arm produces a contract-valid output or the arm's
  recorded exclusion, and each receipt names the adapter used
- depends: #search-provider, #budget

### Cast review {#cast-review}

The design goes to the five seats before any draw: Mara on trust, Wren on
context and budget, Bly on the records, Orin on the adopter, Fen on the weak
executor.

- verify: every finding is dispositioned in this README or in a review record,
  and the review is recorded before the selection
- depends: #live-driver, #task-sets

### Selection {#selection}

The corrected round over the selection set with the frozen numbers, and the
lock rule applied mechanically.

- verify: every draw's receipt, adapter and score are recorded; the suite-fit
  table carries its evidence; the lock follows the frozen rule
- depends: #cast-review

### Confirmation {#confirmation}

The locked arm against `null` on the fresh held-out set, fresh and interleaved,
and the printed verdict.

- verify: the verdict prints from the recorded criteria; a `NO-SHIP` records
  every criterion missed; a `SHIP` records margin, per-task floor and the
  phantom count
- depends: #selection

### Fen acceptance {#fen-acceptance}

The real Fen runs one task through the component's single command and reaches
the output contract, with the untaught baseline beside it.

- verify: Fen completes the command and the output validates; the untaught
  baseline is recorded
- depends: #confirmation

### Component scaffold {#component-scaffold}

`host-deep-research` under the `.host-software` recipe: bare store, worktree,
`Unlicense` plus the third-party notice, the confirmed arm or the null agent,
the harness and model pins, and the release gate green.

- verify: `software --check` reads the stanza clean; the artifact re-derives
  under `software --verify-build`; the harness and model pins match this plan's
- depends: #confirmation

### Ship {#ship}

The shim carries the confirmed arm, or, on a `NO-SHIP`, the null arm's native
agent under the same contract. The default changes only with the operator's
approval.

- verify: one command runs a task end to end on the reference model, and the
  recorded verdict matches the shipped arm
- depends: #component-scaffold, #fen-acceptance

### weco refinement {#weco-refinement}

Optional. The confirmed arm or the shim's prompt surface is optimised against
the selection set, and the refined variant re-confirms on the held-out set.

- verify: the baseline is measured before the loop; the refined variant passes
  confirmation, or the original stays
- depends: #ship

## Open questions

- The live adapters' formats: the hffmnnj library notes and the kanatami worker
  results need their live readers; the plan/0113 adapters cover the fixtures.
- The provider: Exa's reachability under the pinned harness, and the fallback
  if the probe fails.
- The budget: the cap and the wave width for a model that spends its budget on
  research.
- The held-out set: the new rows and house tasks, and the new key's custody.
- The component: the null arm's third-party notice and the shim's licence
  boundary.

# plan/0113: host-deep-research, the A/B that selects it

**Status: cut 2026-11-26, in build (updated 2026-11-27)** (operator
direction: claim a plan and design the A/B for a deep-research integration). The wrapper is ruled
`host-deep-research`, a house component that shims whichever arm the test
selects. This milestone is the design and its build sequence, not a shipped
component. The arm snapshots are pinned with their licenses recorded
([arms/README.md](arms/README.md)): the four roster arms qualify, and the
optional verification pipeline is excluded for a missing license at its pin.
The run harness is pinned at OpenCode v2.4.2, with its draw pre-flight and
isolation probes recorded ([harness/README.md](harness/README.md)), and the
reference route is strata's `qwen3.8-flash-next`, pinned through the router's
`qwen*` entry with its deployment id
([model-pin/README.md](harness/model-pin/README.md)). The run contract and
its per-arm adapters are recorded
([contract/README.md](harness/contract/README.md)). The task sets are frozen,
with the selection set public and the held-out set sealed
([tasks/README.md](harness/tasks/README.md)). The mechanical rubric and its
controls are recorded ([rubric/README.md](harness/rubric/README.md)). The cast
review is recorded with every finding dispositioned
([design-review.md](design-review.md)). The first selection round is recorded
as harness-defective: the only contract-valid draw is the null's host-lint
task, so its lock carries no measurement of the arms
([selection/README.md](harness/selection/README.md)). The corrections are the
new tasks in the build sequence, and the redo selection follows the smoke test
and the redo cast review.

## Rulings

The operator's rulings of 2026-11-26, and the facts the design rests on.

- **The roster.** The control and the arms: the null arm, the Weizhena skills,
  the hffmnnj plugin, the Kanatami skill, and a verification arm. For the
  fourth, the licensed origin replaces the copy: `Thomashighbaugh/opencode`
  carries no license file and dropped samber's MIT notice, so the arm is
  `samber/cc-skills` `deep-research`, where the validation and the confidence
  ladder live. The optional sixth is `199-biotechnologies/claude-deep-research-skill`,
  or `gptr-mcp` in its place, and it enters only if a license file appears
  upstream before this milestone reaches the selection round.
- **The wrapper.** A new house component, `host-deep-research`, shimmed to the
  objectively best arm, and the one that fits the suite best.
- **The reference model.** `Qwen3.8-Flash-Next` on strata, for every role of
  every arm. `Fen` (qwen3.5-4b) stays the acceptance test, never the subject.
- **The harness pin.** One exact OpenCode release for every arm, checked by
  digest before each draw.
- **The licensing.** House files are `Unlicense`; the shimmed arm keeps its own
  license, pinned and unmodified, listed in a third-party notice.

## Why

Research reaches the record as findings, not as sources. The house's plans cite
what a run concluded, and nothing between a fetched page and a plan line
verifies that the page said it. The five candidates answer that in five
different ways, from a ledger plus a checker to a confidence ladder that the
same model awards lself, and the methodology can test them: the same tasks, the
same pinned harness, the same model, and a mechanical rubric.

The endpoint that carried the installed research skills retired in November, so
the house has no working deep-research tool. The incumbent is therefore the null
arm, and a candidate that cannot beat a plain agent with the built-in web tools
has not earned the vendoring, the dependency tree and the token cost.

## The first attempt's corrections

The first round ran before its ledger injection was smoke-tested. The
corrections are tasks in this plan's build sequence, not a replacement plan.

- **The ledger's layer.** The live driver sends each arm its native prompt,
  and the arm's adapter writes the contract. The wrapper postscript is gone.
- **The smoke test.** One draw per arm through the full pipeline, gating the
  ledger injection, the harness, model, provider, isolation, fetch log,
  receipt and rubric before any scored draw.
- **The measured provider.** One provider is configured and probed; the
  receipt records the provider the tool actually called. The first attempt's
  receipts said Exa while the draws fetched DuckDuckGo.
- **The budget and the waves.** The cost is recorded, never scored; the draws
  run serial or two-way, not the five-arm waves.
- **The judge.** Opus 5.5 scores completeness and creativity, subject to the
  dokimi validity gate. The token count no longer breaks the lock.
- **The fresh held-out set.** The first held-out set was read at the failed
  confirmation; a fresh set is sealed with its own key.
- **The selection and confirmation.** The first selection is recorded as
  harness-defective; the corrected round is the `#selection-redo` task, and
  the confirmation waits for it.

## The re-run rule

A draw that fails because the harness, an adapter, the search provider or the
driver broke is a harness break, not an arm result. It is void, the breakage is
recorded, the harness is fixed, and the draw is re-run once under the same task
and config; the first attempt stays in the record with a `rerun.json` naming
the break. A budget-exhausted draw is an arm result: void, recorded, never
re-run, because re-running the same cap loops. An arm whose native output shape
cannot satisfy the contract is an exclusion with evidence. A low score is never
a re-run reason; this rule is fixed before the redo.

An adapter that excludes a draw whose native output already carries a fetched
source record is a harness break: hffmnnj finding notes, kanatami worker
results with a fetched page, or a samber/weizhena report carrying a URL, quote
and locator. The report's own source list is not a fetched page. The smoke
fails it, the adapter is fixed, and the draw is re-run.

## The A/B design

### The arms

One driver model, one harness pin, one search provider. The arms differ only in
the tool.

| Arm | What runs | Pin |
|---|---|---|
| `null` | the harness agent with its built-in `websearch` and `webfetch`, and a frozen prompt that asks for the same output contract as every arm | none |
| `weizhena` | the staged skill: outline, then parallel item agents, then a generated report | `6ce38f6` |
| `hffmnnj` | the OpenCode plugin: research tools, a notes library with a SQLite index, three subagents | `d977301` |
| `kanatami` | the single-commit V1 skill with one worker agent per query | `9f46968` |
| `samber` | the confidence-ladder skill, the licensed origin of the fourth candidate | `50a33836` |
| `verify` (optional) | the pipeline whose citation and claim checks run as scripts | `f2f2c0f`, excluded: no license at the pin |

`weizhena`, `samber` and `verify` keep no per-claim source record that a
checker can read; that is a finding about the arm, not a defect the rubric
hides.

### The constants

These are fixed for selection and confirmation alike. Each is recorded in every
run's receipt.

- **OpenCode.** One release tag, installed into a scratch prefix, its binary
  checked by version and `sha256` before each draw. `OPENCODE_DISABLE_AUTOUPDATE=1`,
  the models catalog frozen (`OPENCODE_DISABLE_MODELS_FETCH=1` with a committed
  snapshot), and the per-arm config supplied inline with its digest recorded.
- **Isolation.** A scratch `HOME` and scratch XDG directories per draw. The v2
  engine discovers skills and instructions under the home directory as well as
  the project, so XDG isolation alone would load the retired research skills into
  the null arm. The work directory sits outside any tree that carries a manual.
- **Reference model.** `Qwen3.8-Flash-Next` on strata, for every role. The
  router has no exact named `qwen3.8-flash-next` entry; the name resolves
  through the `qwen*` entry, and the pin is that entry's deployment id, checked
  in pre-flight. A draw on a foreign model is void. The legacy `qwen3.6-27b`
  name is foreign.
- **Search.** One provider, measured and probed. Every arm uses that provider,
  and every receipt records the provider the tool actually called. The first
  attempt declared Exa while the draws fetched DuckDuckGo; the
  `#search-provider` task fixes the measurement.
- **Budget.** The same per-draw cap on tokens, tool calls and wall time, and the
  same prompt for the arm plus the tasks. The contract's caps are 200000 prompt
  tokens, 50000 completion tokens, 60 tool calls and 10800 wall seconds; the
  draw order is two-way, interleaved by task, and serial when the provider is
  under load. The caps are enforced, and the values and the aggregate wall
  clock are the operator ruling recorded in
  [design-review-redo.md](design-review-redo.md); the smoke's kanatami draw
  used 198518 prompt and 61492 completion tokens, so the 50000 completion cap
  is under review. The cost is recorded, never scored.
- **Arm isolation.** Each arm draws in its own scratch tree with its own library
  and its own config. No arm's skills, plugins or notes are shared with another.
- **Roles.** The reference model is the only subject. Fen drives the component's
  single command in the acceptance task. A judge other than the reference,
  Opus 5.5, scores completeness and creativity; its scores count only after
  dokimi's validity gate. The per-arm draw config overrides every agent's model
  to the reference route; the arm's own files are never edited, because the
  weizhena and kanatami agents pin foreign models at their commits. The override
  is part of the config digest.

### The task sets

Two sets, frozen before any draw: a selection set for the rounds, and a held-out
set read for the first time in confirmation. The held-out set is never run
during selection. The first held-out set was read at the failed confirmation;
the fresh set is frozen and sealed with its own key.

- **Known-answer tasks** come from a public short-answer benchmark, referenced
  by item id and fetched at run time rather than embedded, so the dataset's own
  terms apply (call/0055's referenced-not-embedded rule).
- **House tasks** are ones the house will use: a technical decision between
  candidates, a tool comparison, and a release fact. Each is scored against a
  must-cover list of entities, each with its aliases.
- **The freeze.** Every task carries its key, its must-cover list and a digest,
  recorded before the first draw.

### The rubric

Mechanical where it can be; the hard gate is a count.

1. **Phantom sources, the hard gate.** Every cited URL must appear in the run's
   own fetch log. A cited source the run never fetched is invented. Zero
   tolerance: a draw with one is void.
2. **Cited-quote support, six points.** Each cited sentence must carry a quote
   and a locator, and the quote must appear in the run's snapshot of that page
   after whitespace and unicode normalisation. The pass threshold is frozen
   before the draws.
3. **Known-answer correctness, four points.** Normalised match against the
   frozen key.
4. **Must-cover recall, four points.** Share of the pre-registered entities the
   report names.
5. **Numerals, three points.** A numeral must appear in a cited snapshot. Each
   unsupported numeral counts against the draw.
6. **Prose, three points.** The house's prose lane over the report, inverted
   into a score.

Cost is recorded, not scored: completion and prompt tokens, tool calls, wall
time, and the exit status and contract compliance of each draw.

The judge is Opus 5.5 through the host's `claude` CLI (`claude-agent/opus`,
resolved `claude-opus-5-5`). It scores completeness and creativity, 0-4 each,
on the blind report and ledger; the judge score is 0-8. The pooled selection
score is the mechanical score (0-16) plus the judge score (0-24). The judge's
model and route are checked against the pin, its validity gate must pass, and
it retries on a transient failure; a failing judge contributes 0. With no
passing judge, the mechanical score stands alone. The confirmation runs the
same judge on the held-out draws and records both sub-scores.

### The protocol

- **Selection** is one frozen round, because the budget bounds it: every arm
  draws once on every selection task (5 × 6 = 30 draws), interleaved by task.
  A re-baseline would need a new pre-declared round before its draws; numbers do
  not compare across rounds. The first attempt's round is recorded as
  harness-defective; the corrected round is the `#selection-redo` task.
- **Lock.** The pooled selection score is mechanical (0-16) plus judge (0-8),
  a 24-point maximum. Among arms within 1.5 points of the best, only a
  candidate with at least one valid draw and a pre-declared null-relative
  clearance may lock; the tie-break is the six-row suite-fit evidence table,
  then the judge score, then name order. The judge's model, route and validity
  gate are checked. The token count is recorded, never a tie-break.
- **Confirmation** pits the locked arm against `null`, on the fresh held-out
  tasks, with two fresh draws per held-out task per arm (2 × 2 × 5 = 20 draws)
  and randomised order within each task block. The locked arm is read from
  `round-redo.json`, never `weizhena`; the fresh set is sealed with its own key;
  `--key` is required and `--check` does not decrypt. A void is a gate, not a
  measured zero. The pre-declared criteria: a margin of 1.0 point, a per-task
  floor of 8 of 16, zero phantom sources, no foreign-model reply, every draw
  valid or a recorded harness-break re-run, and the judge's completeness and
  creativity recorded.
- **Ship.** The component ships the confirmed arm when every criterion passes,
  and prints `SHIP`; otherwise it prints `NO-SHIP`, reports the criteria it
  missed, and the incumbent (null) stands. The operator may direct another
  attempt; the criteria are not moved to fit a result.
- **Refinement after a ship** is a weco optimisation pass on the confirmed arm,
  or on the shim, scored with the selection set. A refined variant has to
  re-confirm on the held-out set before it ships, for the same winner's-curse
  reason the confirmation stage exists.

### The suite-fit score

Scored mechanically against this design when the arm is locked, out of six.
These are the integrations that make the winner a component of this suite
rather than a skill dropped into it.

1. Every role runs on the reference model through `models`, `model`, or the
   session model, without a config edit.
2. It produces an evidence ledger the rubric can read: claims, quotes and
   locators, machine-readable.
3. Source snapshots can be pinned and digested through the run contract.
4. Artifacts land under the run directory, never in the home directory.
5. One command runs a task: at most one human gate inside a draw.
6. The vendored tree is reproducible and its license file permits it: a
   lockfile for the runtime, and a license at the pinned commit.

A shippable arm scores at least four, and clears the first and the sixth.

The selection record carries a six-row table, one row per criterion, with the
evidence for every arm in the band. A suite-fit score without the row is not a
score.

### The component's licensing

- Our own files are `Unlicense`: the shim, the run contract, the checker, the
  kit and the tasks the house writes. The repo carries the Unlicense text and
  the manifest field.
- The shimmed arm keeps its own: pinned and unmodified, its `LICENSE` and its
  copyright notices intact, listed in the third-party notice with pin, SPDX id
  and the path to its notice.
- House adaptations live in house files, never as edits to upstream files.
- A copyleft arm runs out of process, behind an arm's-length boundary such as
  `host-reference-openscad`'s (call/0033).

## Build sequence

### Arm snapshots {#arm-snapshots}

Each arm is pinned at a recorded commit, one snapshot directory away from the
run harness, with its license state recorded. An arm qualifies for a draw only
when a license file exists at its pinned commit.

- verify: every pin resolves and its commit date is recorded; every candidate
  carries a license file at that commit, or its exclusion is recorded
- depends: none

### Harness pin {#harness-pin}

One OpenCode release tag, its binary and digest in the scratch prefix, and the
pre-flight that checks them. Each isolation check is proven by its own probe: a
planted skill and a planted manual in the home directory must not load.

- verify: the pre-flight rejects a wrong digest and a wrong version; every arm
  loads under the pinned binary; the null arm's resolved configuration lists no
  skill, plugin or instruction
- depends: #arm-snapshots
- Landed 2026-11-27: OpenCode `v2.4.2`, its archive `452912…` and binary
  `523b15…`; the pre-flight, the four arm loads and the isolation probes are
  recorded in [harness/README.md](harness/README.md).

### Model pin {#model-pin}

The exact named route for strata, its deployment record, and the pre-flight
that refuses a draw on a foreign model. The check is proven with a planted
reply recorded under another model id.

- verify: the pre-flight voids a draw that carries one foreign-model reply, and
  passes a clean one
- depends: #harness-pin
- Landed 2026-11-27: the reference route is strata's `qwen3.8-flash-next`
  through the router's `qwen*` entry (deployment `64e4a374…`, backend
  `openai/qwen3.8-flash-next`, 500000/524288); the legacy `qwen3.6-27b` name is
  foreign. The pre-flight voids a foreign reply, an empty ledger, the `*`
  wildcard's deployment and a record without the `qwen*` entry. Record:
  [harness/model-pin/README.md](harness/model-pin/README.md).
- Reopened 2026-11-27 by the cast review: the live driver writes the pin into
  the receipt and never parses the reply's model or provider, so the
  pre-flight is not called and a foreign reply passes. The reply ledger and
  the pre-flight are [selection-redo](#selection-redo)'s first work.

### Run contract {#run-contract}

What `host-deep-research` runs: one task file in; one report and one source
ledger out, the ledger recording each source with its URL, its
verbatim quote and its locator, plus the run's receipt with the harness, model,
search provider, budget and config digests. Every arm's adapter maps its own
output shape to the contract, in the arm's own directory.

- verify: every arm's dry run produces a contract-valid output and a receipt;
  an arm whose output cannot satisfy the contract records why in its exclusion
- depends: #harness-pin
- Landed 2026-11-27: the task, report, ledger and receipt contract with the
  five arm adapters; the dry runs pass for `null`, `hffmnnj` and `kanatami`,
  and `weizhena` and `samber` record their exclusions (no per-source quote and
  locator). Record: [harness/contract/README.md](harness/contract/README.md).
- Reopened 2026-11-27 by the cast review: the receipt's model is the pin, not
  the reply; the `replies.jsonl` ledger and the reply digest are missing; the
  fetch-log fallback that wrote the report's own source list as snapshots is
  removed; the samber parser missed inline citations. The corrections are
  [selection-redo](#selection-redo)'s first work.

### Task sets {#task-sets}

The selection set and the held-out set, each with its key, its must-cover list
and its digest. Benchmark items are referenced by id. House tasks are written
here.

- verify: every task validates against its key's schema; the digests are
  recorded before the first draw; the held-out set is unread until confirmation
- depends: #run-contract
- Landed 2026-11-27: six selection tasks (three SimpleQA rows, three house
  tasks) and five held-out tasks (two SimpleQA rows, three house tasks); the
  selection digest is `128d1354…`, the held-out plaintext digest `97c44bd2…`,
  and the held-out set is sealed in `held-out.json.enc`. The held-out plaintext
  was read at the failed confirmation, so that set is burned and
  `#fresh-held-out` seals a fresh one. Record:
  [harness/tasks/README.md](harness/tasks/README.md).
- Also burned 2026-11-27: the first fresh set was read by `confirm.py --check`,
  which decrypts before checking the lock. The confirmation seals a fresh-2
  set with new tasks and a new key; `--check` will read only the sealed
  digests.

### Rubric {#rubric}

The checker, with controls: a planted phantom citation must void its draw, a
planted wrong answer must miss its key, a clean draw must score full, and a
draw on a foreign model must be refused.

- verify: the controls pass and each one is recorded with its output
- depends: #task-sets
- Landed 2026-11-27: the checker, its gates and five controls; the citation
  threshold is frozen at 5 of 6. A clean house draw scores 16/16; a phantom
  citation and a foreign model void; a wrong answer scores 12/16; an
  unsupported quote falls below the threshold. Record:
  [harness/rubric/README.md](harness/rubric/README.md).
- Reopened 2026-11-27 by the cast review: the phantom gate is only as good as
  the fetch log. The kanatami log was the report's own source list; the
  report-to-fetch fallback is removed in
  [selection-redo](#selection-redo), and the smoke is re-run.

### Cast review {#cast-review}

The design goes to the cast before any live draw. The seats that matter here:
`Mara` on what the operator would trust, `Wren` on context and budget,
`Bly` on what a cold reader can audit from the run records, `Orin` on what
binds an adopter, and `Fen` on whether the component's command survives a weak
executor.

- verify: every finding is dispositioned in this README or in a follow-up
  record, and the review is recorded before the selection round
- depends: #rubric
- Landed 2026-11-27: the five-seat review in
  [design-review.md](design-review.md); the accepted findings froze the
  protocol numbers, added the fetch log to the contract, added the per-arm
  model and tool overrides, named Exa as the search provider, added the
  suite-fit evidence table and the component's harness and model pins. Every
  finding is dispositioned in the review or the named record. The provider
  finding is superseded by `#search-provider`: the receipts and the fetch log
  disagreed, so the provider is measured rather than named.

### Selection {#selection}

Interleaved draws over the selection set, one frozen round of 30, and the lock
rule applied mechanically.

- verify: every draw's receipt and score are recorded; the suite-fit table
  carries one row per criterion with its evidence; the locked arm follows from
  the rule rather than from a judgment made after seeing the table
- depends: #cast-review
- Landed 2026-11-27, **harness-defective**: the 30 draws are recorded in
  [harness/selection/README.md](harness/selection/README.md) and
  `round.json`; only `null/house-host-lint-docs` produced the contract (13/16),
  the other 29 hit the 1800-second cap without a ledger, the pooled scores are
  null 2.17 and the candidates 0, and the lock is `weizhena` by fewer tokens
  after the 4-point suite-fit tie. The round measured the wrapper prompt and
  the waves, not the arms; `#selection-redo` is the corrected round.

### Confirmation {#confirmation}

The arm locked by `round-redo.json` against `null` on the fresh held-out set,
fresh and interleaved, with the judge's completeness and creativity, and the
printed verdict.

- verify: the locked arm is read from `round-redo.json` and used in the
  margin, floor, print and `verdict.json`; a missing or invalid lock refuses;
  the fresh-2 set is sealed with a new key; `--key` is required and `--check`
  does not decrypt; the 20 draws are randomised; every draw is valid or has a
  recorded harness-break re-run; the judge's per-draw completeness and
  creativity are recorded; the verdict prints from the recorded criteria; a
  `NO-SHIP` records every criterion missed; a `SHIP` records margin, floor,
  phantom count and judge scores; a low score is never a re-run reason
- depends: #selection-redo, #fresh-held-out, #judge
- Wired 2026-11-27: `confirm.py` reads `held-out-fresh.json.enc`,
  `sets-fresh.json` and the fresh key, writes `draws-fresh/`, and takes the
  locked arm from `round-redo.json`. The cast review re-opened this wiring:
  the locked arm, the fresh-2 set, `--key`, the judge and the valid gate are
  the confirmation's remaining work. The old partial draws stay under
  `draws/`. The verdict is not run yet.

### Fen acceptance {#fen-acceptance}

The real Fen runs one task through the component's single command and reaches
the output contract, and the same probe without the component's guidance is the
baseline.

- verify: Fen completes the command and the output validates against the
  contract; the untaught baseline is recorded beside it
- depends: #confirmation

### Component scaffold {#component-scaffold}

`host-deep-research` under the `.host-software` recipe: bare store, worktree,
`Unlicense` plus the third-party notice, the confirmed arm vendored or
materialised as the arm's licensing requires, and the release gate green. The
component's run contract carries the OpenCode v2.4.2 archive and binary digests
and the reference model pin; the recipe check reads them.

- verify: `software --check` reads the stanza clean, the artifact re-derives
  under `software --verify-build`, the recorded harness and model pins match
  the plan's; the hffmnnj embedding and each arm's native search are pinned or
  off with a license and digest; the third-party notice and the build include
  them; the optional `gptr-mcp` is recorded in or out
- depends: #confirmation

### Ship {#ship}

The shim carries the confirmed arm, or, on a `NO-SHIP`, the null arm's native
agent under the same contract. The default changes only with the operator's
approval.

- verify: one command runs a task end to end on the reference model, and the
  recorded verdict matches the shipped arm
- depends: #component-scaffold, #fen-acceptance

### weco refinement {#weco-refinement}

Optional. The confirmed arm, or the shim's prompt surface, is optimised against
the selection set with `weco local run`, and the refined variant re-confirms on
the held-out set before it ships.

- verify: the baseline is measured before the loop; the refined variant passes
  confirmation, or the original stays
- depends: #ship

### Search provider {#search-provider}

Configure and probe one provider under the pinned harness; the receipt records
the provider the tool actually called.

- verify: the provider probe passes; a draw's receipt records the provider the
  fetch log shows; a foreign provider voids
- depends: none
- Landed 2026-11-27: Exa is selected in the per-draw config
  (`"websearch": {"provider": "exa"}` with `OPENCODE_ENABLE_EXA=1`), and the
  driver takes the provider from the completed `websearch` event's metadata.
  The live probe returned 8 results with `provider: exa` in 62.2s; a receipt
  naming another provider and a DuckDuckGo fetch are both void. The first
  round's receipts said Exa while the cancelled form sent the model to
  DuckDuckGo. Record:
  [search-provider/README.md](harness/search-provider/README.md).

### Budget {#budget}

Re-decide the per-draw caps and the draw order; the cost is recorded, never
scored.

- verify: the caps and the wave width are recorded before the first draw; a
  smoke draw reports the used counts; no lock or tie-break reads them
- depends: none
- Landed 2026-11-27: the caps are 200000 prompt tokens, 50000 completion
  tokens, 60 tool calls and 10800 wall seconds; the draw order is two-way,
  interleaved by task, serial under provider load. The first round's 1800s cap
  and five-arm waves voided 29 of 30 draws; the one valid draw used 103k
  prompt tokens, 47 tools and the full 1800s. The first corrected cap was
  3600s; the kanatami smoke hit it in `background_wait` after three of the
  skill's five-to-ten research rounds, so the operator ruled the cap up to
  10800s.
  `contract.CAPS` is the single source; `run.py` reads the wall cap and
  defaults to two-way. Record: [budget/README.md](harness/budget/README.md).
- Reopened 2026-11-27 by the cast review: the caps are declared but not
  enforced (the kanatami smoke records 61492 completion tokens against the
  50000 cap), the budget README title still says 3600 seconds, and the
  75-84 hour aggregate is not approved. The caps, aggregate and enforcement
  are the operator ruling in
  [design-review-redo.md](design-review-redo.md); the fix is in
  [selection-redo](#selection-redo).

### Adapter layer {#adapter-layer}

The live driver sends each arm its native prompt; the arm's adapter writes the
contract. The null keeps the frozen contract prompt; the weizhena and samber
exclusions are recorded.

- verify: the driver runs one draw per arm to the arm's native output; each
  receipt names the adapter; the wrapper postscript is gone; an exclusion whose
  native output already carries a source record is a harness break, not a pass,
  and a pseudo-tool-call transcript is a void
- depends: #run-contract, #search-provider, #budget
- Landed 2026-11-27: the native prompts and `prepare_native` are in `run.py`;
  the adapters dispatch from `contract/adapters/`. The wrapper postscript is
  gone from the non-null prompts. The contract dry run is 8/8. The live smoke
  passed: null valid 9.615/16, hffmnnj valid 5.09/16, kanatami valid 9.818/16,
  weizhena and samber excluded with evidence. The hffmnnj adapter accepts bare
  `rn_...` ids and balanced URL parentheses; the kanatami adapter harvests the
  final report, corpus and run text into workers and the fetch log; a
  pseudo-tool-call transcript is a void. Record:
  [adapters/README.md](harness/adapters/README.md).
- Reopened 2026-11-27 by the cast review: the kanatami fetch log was
  synthesized from the report's own source list, so the citation support was
  self-referential, and the samber parser missed inline markdown citations.
  The smoke result is not an arm result. The actual-fetch capture and the
  samber/weizhena parsers are in [selection-redo](#selection-redo); the smoke
  is re-run there.

### Judge {#judge}

Opus 5.5, a model other than the reference, scores completeness and creativity
on the blind report and ledger; the dokimi validity gate must pass.

- verify: the judge model is Opus 5.5; the prompt and the blind-scoring rule
  are recorded; the dokimi validity gate passes on the clean and broken
  samples; a failing judge is not used
- depends: none
- Landed 2026-11-27: the judge runs on `claude-agent/opus`, which resolves to
  `claude-opus-5-5`; it scores 0-4 completeness and 0-4 creativity from the
  blind report and ledger. The validity gate passed: clean 6/8, broken 0/8,
  and a malformed reply is rejected. `judge.json` records the model, the
  prompt and reply digests, the cost and the scores. A failing judge writes
  `valid: false` and contributes 0; the mechanical rubric alone scores.
  Record: [judge/README.md](harness/judge/README.md).
- Reopened 2026-11-27 by the cast review: the judge's model and route are not
  checked, the validity gate is not read per draw, the judge scores void draws,
  and the confirmation never runs it. The guard and the held-out judge are in
  [selection-redo](#selection-redo) and [confirmation](#confirmation).

### Fresh held-out {#fresh-held-out}

The first held-out set was read at the failed confirmation; freeze a fresh set
and seal it with its own key.

- verify: every task validates; the fresh set is ciphertext with no plaintext
  in the tree; both set digests are recorded
- depends: none
- Landed 2026-11-27: two new SimpleQA rows (10, 50) and three house tasks
  (serde_json/simd-json, cargo-nextest/cargo test, verify-setup/check); the
  plaintext set digest is `9c409589…`, the ciphertext `bb60b746…`, sealed in
  `held-out-fresh.json.enc`; the key is at
  `/tmp/opencode/plan0113/held-out-fresh.key`, the plaintext is deleted, and
  `sets-fresh.json` records both digests. The old `held-out.json.enc` and
  `sets.json` stay as the burned set's history. Record:
  [tasks/sets-fresh.json](tasks/sets-fresh.json).
- Reopened 2026-11-27 by the cast review: this fresh set was read by
  `confirm.py --check`, which decrypts before checking the lock, and its key
  sits under `/tmp`. The set is burned. The confirmation seals a fresh-2 set
  with new tasks and a new operator-held key; `--check` will read only the
  sealed digests.

### Smoke test {#smoke-test}

One draw per arm through the full pipeline and the controls: the ledger
injection, the harness, model, provider, isolation, fetch log, receipt and
rubric; a planted skill and manual must not load; a missing ledger is an
exclusion or a void.

- verify: the null and each mapped arm produce the contract or the recorded
  exclusion; the harness, model, provider, isolation, fetch-log and rubric
  controls pass; a suspect exclusion whose native notes or workers carry a
  source record fails the smoke; the smoke record is committed
- depends: #adapter-layer, #search-provider, #budget, #harness-pin, #model-pin, #rubric
- Landed 2026-11-27: `smoke/smoke.json` PASS. The isolation probe is 11/11;
  null valid 9.615/16 (5021.9s, provider exa), hffmnnj valid 5.09/16 (928.8s,
  reused recorded draw), kanatami valid 9.818/16 (8231.4s, reused recorded
  draw), weizhena excluded 7204.8s and samber excluded 6514.2s with evidence.
  The suspect-exclusion and pseudo-tool-call gates pass. Record:
  [smoke/smoke.json](harness/smoke/smoke.json).
- Reopened 2026-11-27 by the cast review: the kanatami fetch log is
  self-referential, the samber parser missed inline citations, the isolation
  probe can be skipped, and the `--only` run overwrites the all-arm record.
  The smoke is re-run under the corrected machinery in
  [selection-redo](#selection-redo); this record is history, not a pass.

### Cast review redo {#cast-review-redo}

The corrected design goes to the five seats before the redo selection.

- verify: every finding is dispositioned in this README or in the review
  record; the review is recorded before the redo selection
- depends: #smoke-test, #judge, #fresh-held-out
- Landed 2026-11-27: the five-seat review in
  [design-review-redo.md](design-review-redo.md); the findings continue the
  first review's numbering (M5-M10, W6-W11, B5-B10, O5-O10, F5-F10) and every
  one is accepted and dispositioned. The fixes are folded into
  [selection-redo](#selection-redo), [confirmation](#confirmation) and
  [component-scaffold](#component-scaffold); the operator rulings are in the
  review. The redo does not start until those rulings are recorded and the
  smoke is re-run.

### Selection redo {#selection-redo}

The corrected round with the native adapters, the measured provider, the frozen
budget, the judge and the lock rule.

- verify: the review's blockers are closed before a scored draw: the caps
  enforced at the operator-ruled values; `replies.jsonl` and the model
  pre-flight; the attempt and re-run rule; the six-row suite-fit; the actual
  kanatami fetch capture; the samber and weizhena parsers; the two-way probe;
  the smoke redo. Every draw's receipt, adapter, mechanical score and judge
  score are recorded; every harness-break void has a recorded re-run;
  budget exhaustion is an arm result, not a re-run; the judge's model, route
  and validity gate passed; the lock uses the valid floor, the null-relative
  gate, the 24-point pooled score, the 1.5-point band, the six-row suite-fit
  and the judge score; the cost is recorded, not scored
- depends: #cast-review-redo, #smoke-test, #judge, #budget, #adapter-layer
- Wired 2026-11-27: `round.py` reads each draw's `judge.json`, pools the
  mechanical 0-16 with the judge 0-8, and applies the 1.5-point band, the
  suite-fit, the judge score and name order. The first round's `round.json`
  is historical; the corrected round writes `round-redo.json` with
  `--draws draws-redo --out round-redo.json`. The cast review's fixes are this
  task's first work, before any scored draw; the round is not run yet.

## Open questions

- **Ruled 2026-11-27: the reference route is strata's `qwen3.8-flash-next`.**
  The name resolves through the `qwen*` wildcard (deployment `64e4a374…`); an
  exact named entry remains a change in `api-litellm`, outside this repository.
  The legacy `qwen3.6-27b` name is not the route.
- **The provider is measured in `#search-provider`.** The first attempt's
  receipts said Exa while the draws fetched DuckDuckGo; the corrected task
  records the provider the tool actually called.
- **Ruled 2026-11-27: the experiment considers only `v2.4.2`.** Every draw and
  check runs under the pinned `v2.4.2` binary; the house `tools/opencode` pin
  is outside this milestone's harness decision.
- **The round sizes are 30 selection draws and 20 confirmation draws**, with the
  contract's caps, the frozen band, margin and per-task floor, and the
  `#selection-redo` and `#confirmation` tasks.
- **The judge is Opus 5.5** through `claude-agent/opus` (resolved
  `claude-opus-5-5`). It scores completeness and creativity, subject to the
  validity gate.
- The optional sixth arm, if and when a license file appears upstream.
- Web drift: selection and confirmation run weeks apart, so the benchmark items
  are referenced rather than embedded, and each draw records its fetch log.

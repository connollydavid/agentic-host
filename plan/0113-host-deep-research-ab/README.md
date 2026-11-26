# plan/0113: host-deep-research, the A/B that selects it

**Status: cut 2026-11-26, in build** (operator direction: claim a plan and
design the A/B for a deep-research integration). The wrapper is ruled
`host-deep-research`, a house component that shims whichever arm the test
selects. This milestone is the design and its build sequence, not a shipped
component. The arm snapshots are pinned with their licenses recorded
([arms/README.md](arms/README.md)): the four roster arms qualify, and the
optional verification pipeline is excluded for a missing license at its pin.;
active goal since 2026-11-26

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
  router's `/model/info` record is pinned by an exact named entry and its
  deployment id, checked in pre-flight. A draw on a foreign model is void.
- **Search.** One provider, from the harness's own web tools, recorded once.
  Every arm uses that provider.
- **Budget.** The same per-draw cap on tokens, tool calls and wall time, and the
  same prompt for the arm plus the tasks.
- **Arm isolation.** Each arm draws in its own scratch tree with its own library
  and its own config. No arm's skills, plugins or notes are shared with another.
- **Roles.** The reference model is the only subject. Fen drives the component's
  single command in the acceptance task. Any judge that ever scores reports it
  must differ from the reference model and must pass dokimi's validity gate;
  otherwise the mechanical rubric alone scores.

### The task sets

Two sets, frozen before any draw: a selection set for the rounds, and a held-out
set read for the first time in confirmation. The held-out set is never run
during selection.

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

An optional judge may score citation support as well. It must be a model other
than the reference, and its scores count only if it passes the validity gate.
With no passing judge, the rubric stands alone, which is the state after the
2026-10-20 verdict.

### The protocol

- **Selection** is exploratory, with in-round re-baselines. Numbers do not
  compare across rounds.
- **Lock.** The lock rule is mechanical. Among arms whose pooled selection score
  is within a pre-declared band of the best, the lock goes to the highest
  suite-fit score; a remaining tie goes to the arm with fewer tokens, then to
  name order.
- **Confirmation** pits the locked arm against `null`, on held-out tasks not
  used in any round, with fresh interleaved draws and randomised order within
  each task block. The pre-declared criteria: a minimum margin, a per-task
  floor, zero phantom sources, and no foreign-model reply.
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

### Model pin {#model-pin}

The exact named route for strata, its deployment record, and the pre-flight
that refuses a draw on a foreign model. The check is proven with a planted
reply recorded under another model id.

- verify: the pre-flight voids a draw that carries one foreign-model reply, and
  passes a clean one
- depends: #harness-pin

### Run contract {#run-contract}

What `host-deep-research` runs: one task file in; one report and one source
ledger out, the ledger recording each source with its URL, its
verbatim quote and its locator, plus the run's receipt with the harness, model,
search provider, budget and config digests. Every arm's adapter maps its own
output shape to the contract, in the arm's own directory.

- verify: every arm's dry run produces a contract-valid output and a receipt;
  an arm whose output cannot satisfy the contract records why in its exclusion
- depends: #harness-pin

### Task sets {#task-sets}

The selection set and the held-out set, each with its key, its must-cover list
and its digest. Benchmark items are referenced by id. House tasks are written
here.

- verify: every task validates against its key's schema; the digests are
  recorded before the first draw; the held-out set is unread until confirmation
- depends: #run-contract

### Rubric {#rubric}

The checker, with controls: a planted phantom citation must void its draw, a
planted wrong answer must miss its key, a clean draw must score full, and a
draw on a foreign model must be refused.

- verify: the controls pass and each one is recorded with its output
- depends: #task-sets

### Cast review {#cast-review}

The design goes to the cast before any live draw. The seats that matter here:
`Mara` on what the operator would trust, `Wren` on context and budget,
`Bly` on what a cold reader can audit from the run records, `Orin` on what
binds an adopter, and `Fen` on whether the component's command survives a weak
executor.

- verify: every finding is dispositioned in this README or in a follow-up
  record, and the review is recorded before the selection round
- depends: #rubric

### Selection {#selection}

Interleaved draws over the selection set, and the lock rule applied
mechanically.

- verify: every draw's receipt and score are recorded; the locked arm follows
  from the rule rather than from a judgment made after seeing the table
- depends: #cast-review

### Confirmation {#confirmation}

The locked arm against `null` on the held-out set, fresh and interleaved, and
the printed verdict.

- verify: the verdict prints from the recorded criteria; a `NO-SHIP` records
  every criterion missed; a `SHIP` records margin, per-task floor and the
  phantom count
- depends: #selection

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
materialised as the arm's licensing requires, and the release gate green.

- verify: `software --check` reads the stanza clean and the artifact re-derives
  under `software --verify-build`
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

## Open questions

- The strata route: the experiment needs an exact named entry,
  `qwen3.8-flash-next`. Today that name resolves through a family wildcard, and
  a named entry is a change in `api-litellm`, outside this repository. The
  fallback is the named `qwen3.6-27b` entry with its deployment id recorded.
- The house OpenCode pin: whether `tools/opencode` moves to the experiment's
  tag, one authority for the house, with host-loop's tier-2 re-verified there.
- The search provider under the pinned harness, chosen once and recorded.
- The size of each round, in tasks and draws, bounded by cost.
- The optional sixth arm, if and when a license file appears upstream.
- Web drift: selection and confirmation run weeks apart, so the benchmark items
  are referenced rather than embedded, and each draw records its fetch log.

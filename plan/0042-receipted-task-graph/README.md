# plan/0042: receipted task graph

The numbered tasks inside a milestone become first-class: each is an anchored node
with a stable identity, each emits a receipt when discharged, and a prerequisite
edge (within a milestone or across milestones) turns the project's build sequences
into one schedulable graph a coordinator can fan out to parallel sub-agents.
Adopter-facing and mandatory. The design was settled by operator ruling after a
five-lens adversarial review (see design-review.md).

## Problem

A milestone's `Build sequence` is a numbered prose list, where each step pairs an
action with a verification check. Three gaps:

- **No receipt.** Each lifecycle phase emits a receipt (done with re-derivable
  evidence, skip with a cited reason, HAZARD if missing), so a phase claim is
  audited. The in-plan tasks have no such discipline: a step marked done in prose
  is an unverifiable claim, the same defect the phase receipts close, one level
  down.
- **A task has no stable identity.** A position renumbers when a plan is re-cut,
  so neither a receipt nor a dependency edge can key on it. A receipt that points
  at "step three" breaks the moment a step is inserted above it. The fix is a
  content-named anchor, the stable URI a receipt and an edge hang on.
- **The sequence is implicitly serial.** A prose list cannot say which steps are
  independent or which depend on a task in another milestone. An
  arbitrary-complexity project (the methodology's real audience, not this repo's own
  linear history) has genuinely independent and cross-milestone tasks, and the list
  cannot express the graph a coordinator would schedule.

A separate matter is the bare `#N` GitHub issue reference, which is a fragment
rather than a full URL. It is real and out of scope here: a future plan will
enforce full URLs for `#N` references. plan/0042's task references already use a
full relative-path anchor (`plan/NNNN/README.md#anchor`), so this milestone does
not depend on that future one.

## Decision (operator, this session, after the adversarial review)

- **Anchored task nodes, for stable identity.** A task is a `### ` step-heading
  under the `## Build sequence` section whose anchor sits at the heading end
  (`### Gather data {#gather-data}`, the placement stock mdBook honors). A `### `
  heading elsewhere is ordinary prose; the parser rejects an anchored task outside
  the build-sequence section and a build-sequence task heading without an anchor.
  References use the plan/0039 anchored form (`[text](plan/NNNN/README.md#anchor)`).
- **A receipt per task, in a new `.host-task-receipts` ledger.** Tool-written,
  keyed by `plan/NNNN#anchor`, never a hand-edited inline status. This is a
  deliberate third receipt kind beside the plan/0037 two-file ontology, recorded in
  a `call/` decision and a short ontology note; the review flagged the ontology
  cost and the operator accepted it for the physical separation.
- **A project-wide dependency graph, built now.** A task may declare `depends`, a
  local `#anchor` or a cross-milestone `plan/NNNN#anchor`. A task with no `depends`
  depends on the previous task, so the default is linear. The tool resolves the
  edges into one project-wide graph and derives the ready frontier (the tasks whose
  `depends` all carry a done receipt); a coordinator may dispatch the frontier to
  parallel sub-agents. Built as forward infrastructure for arbitrary-complexity
  adopters, not gated on this repo's own linear milestones.
- **Adopter-facing and mandatory.** The spine carries the task model and an
  `UPGRADING` entry; the receipt-per-task gate is a hard rule, the strongest
  discipline. agentic-host implements the capability and migrates its own plans
  (plan/0040 and plan/0041) as the dogfood.

### The authoring rule, and why it holds at the weak-agent bar

The dependency graph was gated on a Qwen-3.5-4B investigation and passed: six of six
on within-milestone authoring and reading (including the serialize-when-unsure
instinct), and four of four on cross-milestone references (read a `plan/NNNN#anchor`
dependency, and author a mixed local-plus-cross-plan `depends` from a menu). A
free-form probe confirmed the danger boundary: asked to find what can run in
parallel, the 4B invents false independence to increase parallelism, which races
two sub-agents, while a missing edge only over-serializes. So the rule is: **an
author declares each task's prerequisites (what must finish before it), and the
tool derives parallelism.** The prerequisite question is local and conservative;
the parallelism is the tool's to compute.

## The design (settled, the review's fixes folded in)

- **One global graph.** Because an anchor is a project-wide URI and the ledger is
  keyed globally, the graph spans milestones. Cycle detection and the
  dangling-dependency check run over the whole resolved edge set, not one milestone,
  so a cross-plan cycle or a `depends` on a removed cross-plan anchor is a HAZARD.
- **Per-task gating, not per-milestone-complete.** The review found that a
  milestone's completeness is prose with no structured referent. So the gate fires
  per task: a declared anchored task with no receipt is a HAZARD, exactly as the
  receipt gate already HAZARDs a manifest phase with no receipt. There is no new
  milestone-status surface.
- **The verify field, mechanical or attested.** A task's check is a first-class
  field, either mechanical (a command the gate re-runs) or attested (an operator
  confirmation or a `call/NNNN` citation the gate resolves). A mechanical `done`
  with no command is a HAZARD; an attested `done` is discharged by the citation
  resolving, which is weaker than re-derivation and labeled as such. The command
  runs through a guarded runner (no recursion into the gate, a decided
  cross-platform path), which reuses the existing recheck mechanism rather than a
  new grammar.
- **Staleness, both halves of call/0018.** A task records the input set its verify
  covers; `--record-digests` fingerprints them into the ledger, and a later offline
  run raises a STALE HAZARD if those inputs drift without a fresh re-derivation, with
  full re-derivation in the verify lane. This is the obligations digest mechanism
  applied to task receipts, the half the first draft dropped.
- **A separate task-anchor link checker.** Resolving a
  `[text](plan/NNNN/README.md#anchor)` reference is a new checker, path-shape gated,
  in a namespace disjoint from the reconcile concept ids (a task heading must never
  shadow a concept home). Only link-integrity transfers; the declared-anchor and
  coverage bites do not apply to an open per-milestone anchor set. The parser also
  enforces the heading-end placement directly, so a misplaced anchor is caught
  before it can 404.
- **Skip is cited, drift is caught.** A substantive `skip` carries a resolvable
  `call/NNNN` citation (parity with call/0017); the gate is non-omission assurance
  for declared work, not a completeness proof, and the doctrine says so. A reverse
  check holds every ledger key to a live anchor, so a renamed or removed task cannot
  leave a stale done behind.
- **Two task systems, one of record.** The durable ledger is the audit record the
  tool writes after re-derivation; the agent's own ephemeral session task list is
  scratch scheduling and is never the source of a `done`.
- **Resource isolation is the parallel-dispatch precondition.** A `depends` is an
  ordering constraint, not a mutual-exclusion lock, so a coordinator fans a frontier
  out to parallel sub-agents only when they are resource-isolated (separate
  worktrees); two tasks with disjoint prerequisites that write the same file are not
  safe to parallelize, and the doctrine states the assumption.

## Build sequence

1. Record the `call/` decision for the third receipt ledger and the ontology note,
   and settle the `depends` syntax (a host-lint-clean grammar, the first-task base
   case, the insertion semantics of the linear default). Verify: `validate call/`
   ok; the syntax is lint-clean by `host-lint --all`.
2. Implement in host-lifecycle: parse the anchored tasks and `depends` (with the
   heading disambiguation and the end-placement check), build and validate the
   global graph (cross-plan resolution, cycle detection, dangling-dependency
   HAZARD), the `.host-task-receipts` ledger with input-digest staleness, the
   per-task gate, the verify-field runner, the status read, and the task-anchor link
   checker. Verify: unit tests, and a synthetic fixture that exercises a
   cross-milestone diamond and a broken reference.
3. Add the spine doctrine (the anchored receipted task model, the
   prerequisite-not-parallelism rule, the resource-isolation precondition, the
   mandatory gate) and an `UPGRADING` entry. Verify: host-template prose clean; the
   entry's verify post-condition holds.
4. Validate the full task form at the weak-agent bar (author a task with an anchor,
   a verify field, a local and a cross-plan `depends`, and its receipt). Verify: a
   recorded Qwen-3.5-4B run authors them correctly.
5. Migrate agentic-host: re-express plan/0040 and plan/0041 as anchored receipted
   tasks and back-fill their receipts through the tool. Verify: `validate plan/`,
   the per-task gate, and the link checker clean; the two milestones read unchanged
   in meaning.
6. Release host-lifecycle, re-pin `.host-software`, record the receipt and the
   `call/` decision, and bump the CI install pins. Verify: the released binary gates
   green; `software --check`, `--verify-build`, and the whole-suite CI green.

## Risks

- The mandatory per-task gate raises the bar for every adopter, so the line between
  a task worth a receipt and a trivial step must stay crisp (an anchored `### ` under
  `## Build sequence` is a task, a trivial step's receipt is a cheap attested or
  skip entry) or the gate becomes ritual.
- The global graph spans milestones, so a cross-plan edge couples two milestones'
  lifecycles; the dangling-dependency check must run on every gate so a re-cut in
  one milestone cannot silently wedge another.
- Author-written verify commands run during the gate, so the guarded runner and the
  no-recursion rule are load-bearing for safety.

## Status

complete, released as host-lifecycle v0.26.0 (2026-06-25). The `tasks` subcommand,
the `.host-task-receipts` ledger (call/0024), the completion-aware per-task gate in
`software --check`, the task-anchor link checker, and the `tasks --new` scaffolding
shipped; the spine doctrine is in host-template (`2229dbb`) and adopted. plan/0040 and
plan/0041 are dogfooded (their build sequences re-expressed as anchored task graphs).
Whole-suite CI green across all three repos.

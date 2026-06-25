# plan/0042: receipted task graph

Make the numbered tasks inside a milestone first-class: each is an anchored node,
references use the concept-as-URI pattern (never a bare number), each emits a
receipt when discharged, and an optional prerequisite edge turns the build
sequence into a schedulable graph a coordinator can fan out to parallel
sub-agents. Grows out of the operator ask to receipt in-plan tasks and to stop the
`#N` collision with GitHub bug references.

## Problem

A milestone's `Build sequence` is a numbered prose list, where each step pairs an
action with a verification check. Three gaps:

- **No receipt.** Each lifecycle phase emits a receipt (done with re-derivable
  evidence, skip with a cited reason, HAZARD if missing), so a phase claim is
  audited. The in-plan tasks have no such discipline: a step marked done in prose
  is an unverifiable claim, the same defect the phase receipts close, one level
  down.
- **Number references collide with GitHub bugs.** Referencing a task by position
  (a bare number, or the `#N` form) collides with a GitHub issue reference (`#1`,
  `owner/repo#N`): a reader cannot tell whether a reference names a task or a bug,
  host-lint polices the bare `#N` form, and renumbering a step breaks every
  reference to it.
- **The sequence is implicitly serial.** A prose list says nothing about which
  steps are independent, so a coordinator runs them in order even when some could
  proceed at once.

## Decision (operator, this session)

In-plan tasks become an anchored, receipted, optionally-ordered graph.

- **Anchored nodes, never bare numbers.** A task is a `### ` step-heading whose
  anchor sits at its end (`### Gather data {#gather-data}`, the heading-end
  placement that resolves under stock mdBook). References use the plan/0039
  concept-as-URI pattern (`[text](plan/NNNN/README.md#gather-data)`). The anchor is
  stable under renumbering and removes the `#N` collision.
- **A receipt per task, in a separate tool-written ledger.** Each task emits a
  receipt (done with re-derivable evidence, skip with a cited reason, tool-computed
  n-a), written by host-lifecycle into a ledger keyed by the task anchor. This is
  the `.host-*-receipts` precedent, chosen over an inline status the author
  hand-edits.
- **Per-heading granularity.** A task is a named step-heading; its sub-bullets are
  detail. One receipt per heading, so the discipline does not swamp a small
  milestone.
- **An optional prerequisite edge (the graph).** A task may declare `depends`, the
  anchors that must finish before it can start. A task with no `depends` depends on
  the previous task, so the default is linear and an author who ignores the graph
  still gets safe serial order. The coordinator derives the parallel frontier (the
  tasks whose `depends` all carry a done receipt) and may dispatch it to parallel
  sub-agents.

### The graph passes the weak-agent bar, with one framing rule (investigated this session)

The optional graph was gated on a Qwen-3.5-4B investigation. Result: six of six on
the constrained form (read the frontier, author `depends` from a menu, and
serialize when unsure). A free-form authoring probe confirmed the boundary: asked
to find what can run in parallel, the 4B can talk itself into false independence to
"increase parallelism", the dangerous mode, since a false independence claim races
two sub-agents on conflicting work while a missing edge only over-serializes.

So the authoring rule is: **an author declares each task's prerequisites (what must
finish before it); the parallelism is the tool's to derive.** The prerequisite
question is local, conservative, and fill-in-the-blank, which the 4B handles.
Deriving the parallel frontier from the edges and the receipts is the tool's job,
so the weak agent states only a per-task prerequisite and defaults to serial when
unsure.

## The design (proposed, for the review)

- host-lifecycle reads a milestone's task anchors and `depends`, validates the
  graph (every `depends` resolves to an existing anchor, no cycle), and tracks a
  receipt per anchor in the task-receipts ledger.
- A task's verification check becomes a first-class field, either mechanical (a
  command the gate re-runs, the phase `recheck =` shape) or attested
  (operator-confirmed or `call/NNNN`-cited), the same shape as the obligation
  dispositions. A done receipt re-derives its mechanical verify, so it is checkable
  rather than asserted (the call/0018 re-derivation doctrine).
- The verify gate HAZARDs a task with no receipt in a milestone marked complete,
  and a status read reports the discharged count and the ready frontier.
- reconcile's link-integrity extends to task anchors, so a `[text](path#anchor)`
  reference that breaks fails the gate.

## Open decisions (settle in the review or early build)

- **Ledger identity.** The file name and key (a `.host-task-receipts` keyed by
  `plan/NNNN#anchor`), set against the plan/0037 receipts ontology as a third
  receipt kind, the per-milestone work item.
- **The completion trigger.** How the tool learns a milestone is complete (a
  structured status it reads), so the all-tasks-discharged gate has a trigger;
  today the status is prose in PLAN.md.
- **Migration reach.** plan/0040 and plan/0041 are re-expressed in the new form as
  the dogfood; older closed milestones are frozen records and stay as written.

## Build sequence

1. Adversarial design review of the graph, the ledger, the verify field, and the
   completion trigger. Verify: a recorded design-review subdoc with a proceed
   verdict.
2. Implement in host-lifecycle: parse the task anchors and `depends`, validate the
   graph, the task-receipts ledger, the verify-field re-derivation, the status
   read, and the link-integrity extension. Verify: unit tests, and a synthetic
   milestone fixture that exercises a diamond graph and a broken reference.
3. Add the spine doctrine (the anchored, receipted, optional-graph task model and
   the prerequisite-not-parallelism authoring rule) and an `UPGRADING` entry.
   Verify: host-template prose clean; the entry's verify post-condition holds.
4. Validate the full task form at the weak-agent bar (the anchor, the verify field,
   a `depends` prerequisite). Verify: a recorded Qwen-3.5-4B run authors a correct
   task and its receipt.
5. Migrate agentic-host: re-express plan/0040 and plan/0041 as the new task graph
   and back-fill their receipts through the tool. Verify: `validate plan/`, the
   task gate, and reconcile clean; the two milestones read unchanged in meaning.
6. Release host-lifecycle, re-pin `.host-software`, record the receipt and a
   `call/` decision, and bump the CI install pins. Verify: the released binary
   gates green; `software --check`, `--verify-build`, and the whole-suite CI green.

## Risks

- Receipt overhead per task must stay proportionate; the receipt is tool-carried
  and cheap, the bar the phase receipts meet.
- The graph must stay opt-in with a linear default, so a milestone an author never
  thinks about as a graph still runs correctly in order.
- The prerequisite-not-parallelism rule is load-bearing for the weak-agent bar; the
  spine doctrine and any skill prompt state it as the needs-question, the
  parallelism stays the tool's to derive.

## Status

Open, design phase. Operator rulings recorded (anchored nodes; a separate
tool-written receipts ledger; per-heading granularity; adopter-facing, with
agentic-host implementing and migrating; the optional graph gated on and passing
the 4B bar). Awaiting the adversarial review before building. Independent of
plan/0040 and plan/0041, which become its first consumers.

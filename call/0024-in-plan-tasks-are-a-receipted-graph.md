# In-plan tasks are a receipted graph: anchored nodes, a third ledger, prerequisite edges

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (the task-graph feature: the task-block parser, the
  `.host-task-receipts` ledger, the global dependency graph, the per-task gate, the
  verify-field runner, and the task-anchor link checker). The software implementation of
  the `plan/0042` spine doctrine.
- Relates: `plan/0042` (which designed this and carries the five-lens adversarial review and
  the operator re-cut); the spine doctrine authored in `host-template` for `plan/0042`;
  `plan/0037` (the receipts ontology this extends to a third kind); `plan/0039` and
  `call/0023` (the anchored-reference pattern); `call/0018` (re-derivation plus input-digest
  staleness).

## Context and Problem Statement

A milestone's build sequence is numbered prose, so an in-plan task has no receipt (a step
marked done is an unverifiable claim, the same defect the phase receipts close) and no stable
identity (a position renumbers when a plan is re-cut, so neither a receipt nor a dependency
edge can key on it). An arbitrary-complexity project also has independent and cross-milestone
tasks a prose list cannot express. `plan/0042` makes the tasks first-class; this records the
software decision and the grammar, settled after the adversarial review.

## Decision

A task is a `### ` heading under the `## Build sequence` section that ends in `{#<anchor>}`
(the placement stock mdBook honors). A `### ` heading outside that section, or one inside it
without an anchor, is rejected, so a task is never confused with an ordinary subsection.
Structured fields follow the heading as bullets:

```
## Build sequence

### Gather data {#gather-data}

- verify: cargo test gather

### Implement the parser {#implement-parser}

- depends: #gather-data, plan/0041#fail-closed
- verify: cargo test parser
- inputs: src/parser.rs

### Record the decision {#record-decision}

- depends: #implement-parser
- verify: attested call/0024
```

- `depends` lists the prerequisites: a local `#<anchor>` or a cross-milestone
  `plan/NNNN#<anchor>`. Omitting the bullet means the task depends on the previous task in
  document order (the linear default); the first task in the section is a root. The author
  declares prerequisites only; the tool derives the parallel frontier (the tasks whose
  prerequisites all carry a done receipt), never the author.
- `verify` is either a shell command the gate re-runs (mechanical), or `attested
  <call/NNNN | operator>` (attested by a decision the gate resolves, or an operator
  confirmation). A mechanical `done` with no command is a HAZARD.
- `inputs` lists the files a mechanical verify covers, fingerprinted for digest staleness;
  without it the gate re-runs the command on every check (no cheap offline staleness).

Each task emits a receipt into a new `.host-task-receipts` ledger, tool-written, keyed by the
global anchor `plan/NNNN#anchor`, in the git-config stanza form the other receipt ledgers
use:

```
[receipt "plan/0042#implement-parser"]
    disposition = done
    verify = cargo test parser
    inputs = src/parser.rs
    digest = <git-hash-object of inputs>
    evidence = <the re-derivation record>
    tool = host-lifecycle@X.Y.Z
    recorded = 2026-06-25
```

The graph is project-wide: because an anchor is a global URI and the ledger is keyed
globally, a `depends` may cross milestones, so cycle detection and the dangling-dependency
check run over the whole resolved edge set. The gate fires per task (a declared anchored task
with no receipt is a HAZARD, the way the receipt gate already HAZARDs a manifest phase with
no receipt), so it needs no per-milestone completion signal. A substantive `skip` carries a
resolvable `call/NNNN` citation; the gate is non-omission assurance for declared work, not a
completeness proof. A reverse check holds every ledger key to a live anchor, so a renamed or
removed task cannot leave a stale done behind. A coordinator dispatches a frontier to
parallel sub-agents only when they are resource-isolated (separate worktrees), since
`depends` is an ordering constraint, not a mutual-exclusion lock.

## Considered Options

1. **An inline status the author hand-edits.** Rejected: it is not tamper-evident, so the
   gate could be cleared by hand under pressure.
2. **Task receipts in the existing operational `.host-lifecycle-receipts` keyspace.** The
   review's recommendation (a task receipt is operational by the `plan/0037` discriminant).
   Rejected by the operator for physical separation.
3. **A new `.host-task-receipts` ledger, a third receipt kind (chosen).** Physically
   separate, tool-written, keyed by the global anchor. The operator accepted the ontology
   cost.

## Consequences

- Good: a task gains auditable, re-derivable completion and a stable identity; the project
  becomes one schedulable graph for parallel sub-agents; the anchored reference reuses the
  `call/0023` pattern; the form holds at the weak-agent bar (the Qwen-3.5-4B authored the
  within-milestone and cross-milestone forms).
- Costs: a third receipt kind beside the `plan/0037` two-file ontology; a mandatory per-task
  gate raises the adopter bar, so the line between a task and a trivial step stays at the
  anchored heading; author-written verify commands run during the gate, so a guarded,
  non-recursive runner is load-bearing.

## Confirmation

The grammar is `host-lint --all` clean, and the real Qwen-3.5-4B authored the local and
cross-milestone `depends` forms (`plan/0042`). The host-lifecycle implementation and its
tests (a cross-milestone diamond and a broken-reference fixture) land with the `plan/0042`
build, and the spine doctrine after it; `host-lifecycle validate call/` passes on this
decision.

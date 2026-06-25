# plan/0042 design review

Five independent adversarial lenses ran against the plan: methodology coherence,
weak-agent followability, mechanism soundness, simplicity, and failure modes.
Verdicts: three re-scope, two proceed-with-revisions. Net: re-scope to a minimal
evidenced core, defer the speculative machinery until a consumer exists, and close
several soundness holes before building.

## Verdicts by lens

- Methodology coherence: re-scope
- Weak-agent followability: proceed-with-revisions
- Mechanism soundness: proceed-with-revisions
- Simplicity and YAGNI: re-scope
- Failure modes: re-scope

## What the lenses converged on (highest confidence)

### The `#N`-collision premise is not in the corpus

(failure-modes, simplicity, followability) A grep of every plan, PLAN.md, `call/`,
and MEMORY.md found that every `#N` is a GitHub issue reference; no plan references
another's build step by number. The "name the milestone, not the step" convention
already prevents the collision, and host-lint does not gate an intra-doc step
number. So anchoring a task to remove the `#N` collision solves a hypothetical.
The evidenced need is the receipt, an auditable record of task completion.

### The optional graph has no consumer

(simplicity, failure-modes, coherence) No milestone in the project's history has
carried independent tasks, and both named consumers (plan/0040, plan/0041) are
linear. The Qwen-3.5-4B investigation proved the graph is safe to author, which is
not the same as needed. The graph is inert until declared, so deferring it costs
nothing, and re-adding it is a one-field addition to an already-anchored node when
a real parallel milestone exists.

### The third receipt file breaks the plan/0037 ontology

(coherence, mechanism, simplicity) plan/0037 partitions receipts by one rule: a
methodology-version event lives in `.host-receipts`, everything host-lifecycle
executes lives in `.host-lifecycle-receipts`. A task receipt is host-lifecycle
executing a discharge, so it is operational by that rule and belongs in the
operational ledger, distinguished by a key shape (`plan/NNNN#anchor`), not a third
top-level file. The operator requirement (tool-written, never a hand-edited inline
status) is met by the operational ledger keyspace.

### The completion trigger is unbuildable as written

(mechanism, the crux risk; coherence; failure-modes) The gate fires on "a milestone
marked complete", but a milestone's status is prose with no structured referent the
tool reads. The fix every mechanism reviewer reached: drop the per-milestone
predicate. Gate per task, where a declared anchored task with no receipt is a
HAZARD exactly as the existing receipt gate HAZARDs a manifest phase with no
receipt; or fire on the verify or release act and let the absence of a clean run be
the not-complete signal.

### Link-integrity over task anchors is a new subsystem, not an extension

(coherence, mechanism, simplicity, failure-modes) reconcile is built on a closed
four-concept vocabulary (`CONCEPT_IDS`) with one-home and coverage semantics. Task
anchors are open-ended, per-milestone, and multi-home. So it needs a separate
checker, path-shape gated on `plan/NNNN/README.md#anchor`, in a namespace disjoint
from the concept ids (or a task heading `{#components}` shadows the concept home),
and only link-integrity transfers; the declared-anchor and coverage bites do not.

## Soundness holes to close before building

### Staleness takes only half of call/0018 (the single worst failure)

(failure-modes) call/0018 is re-derivation plus input-digest staleness. The plan
records the command to re-run but not the inputs the receipt covers, so a `done`
receipt goes stale silently, or the gate re-runs every command on every check,
which is too expensive and so gets skipped in practice. Either way a milestone
ships a `done` that no longer holds, the unverifiable-claim defect one level down,
now wearing an audited badge. Fix: adopt the obligations digest-ledger that the
project already ships (record per-task input digests, raise a cheap offline drift
HAZARD, re-derive in the verify lane).

### Task heading versus prose heading is undefined

(followability, the blocking finding; coherence) The `### ` level is already the
ordinary subsection across the corpus, including this plan's own `### The graph
passes the weak-agent bar` heading. The tool cannot tell a task from a prose
heading, and neither can the weak agent. Fix: a task is a `### ` heading that
carries an anchor under the one `## Build sequence` section; a `### ` elsewhere is
prose; the parser rejects the ambiguous forms.

### The verify field's attested branch cannot re-derive, and a mechanical one is arbitrary code

(mechanism, followability) "A done re-derives its verify" is false for an attested
verify, which has nothing to run; define attested discharge as cite-resolution,
weaker than the re-derivation the plan claims. A mechanical verify is author prose
run as a shell command on every check, so guard it (the recursion and the
POSIX-only path are real), and make a mechanical `done` with no command a HAZARD.

### Skip-to-green and under-writing

(failure-modes, followability) A task marked `skip` clears the gate, and the gate
counts only declared tasks, so under-writing the hard tasks games it. Fix: a
substantive skip carries a resolvable `call/NNNN` citation (parity with call/0017),
and the doctrine states plainly that the gate is non-omission assurance for
declared work, not a completeness proof.

### Ledger drift and orphan receipts

(mechanism, failure-modes) A renamed or deleted anchor orphans its receipt, and a
renamed task re-does work while the old receipt lingers claiming done. Fix: a
reverse check, where every ledger key resolves to a live anchor, mirroring the
existing obligations stale-id rule.

### Two task systems

(failure-modes) The agent harness has its own ephemeral task list. State the
relationship: the durable ledger is the audit record the tool writes after
re-derivation; the harness list is scratch and never the source of a `done`.

### Resource exclusion, if the graph stays

(failure-modes) A `depends` models ordering, not mutual exclusion, so two tasks
with disjoint prerequisites can still race on a shared file. Parallel dispatch is
safe only when sub-agents are resource-isolated (separate worktrees); state the
assumption.

### Anchor-end placement has no pre-ship catch

(followability, failure-modes) A start-placed task anchor renders a different id
and the cross-reference 404s, and link-integrity fires only when something else
references it. Fix: the parser enforces heading-end placement directly.

## Recommended re-cut (the minimal evidenced core)

Ship first, the evidenced need:

1. Anchored task nodes, disambiguated: an anchor-carrying `### ` heading under
   `## Build sequence`, the anchor at the heading end, both enforced by the parser.
2. A per-task receipt in the operational ledger keyspace, with input-digest
   staleness (both halves of call/0018), gated per task rather than per
   milestone-complete.
3. A separate task-anchor link checker (path-shape gated), so a cross-task
   reference that breaks fails the gate.

Defer until a consumer exists:

- The dependency graph, the frontier derivation, the cycle check, and the
  coordinator fan-out. Keep the node design graph-ready (a later one-field add).

Drop:

- The third receipt file (use the operational keyspace).
- A general verify-disposition grammar (a mechanical verify is a command string;
  everything else is attested and cite-resolved).
- The per-milestone-complete trigger.

## Decisions for the operator (the review touches three rulings)

1. **The graph.** Defer until a real parallel milestone, or build it now as a
   forward capability for parallel sub-agents? The reviewers find no consumer and
   recommend defer; the original rationale was forward-looking. The node design
   stays graph-ready either way.
2. **The ledger.** Honor "separate tool-written" as a keyspace inside the
   operational `.host-lifecycle-receipts` (ontology-clean) rather than a third
   top-level file?
3. **Scope.** Dogfood meta-repo-only first (the plan/0038 test for an adopter
   obligation), or stay adopter-facing with the receipt obligation made opt-in per
   milestone (the inert-until-declared ladder pattern)? A blanket mandatory
   receipt-per-task gate taxes adopters who write small linear plans.

## Status

Recorded. Awaiting the operator re-cut on the three decisions, then the plan/0042
README is re-cut to the minimal core.

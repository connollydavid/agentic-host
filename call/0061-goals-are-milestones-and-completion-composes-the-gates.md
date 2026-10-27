# call/0061: a goal is a milestone, and completion composes the gates

- Status: superseded by the spine
- Scope: agentic-host, the host-template spine it carries, and host-lifecycle
- Date: 2026-10-18
- Relates: plan/0101, [host#26](https://github.com/connollydavid/host/issues/26), call/0060, plan/0042, plan/0041

## Context and problem

An operator invoked `/goal complete plan/0007` in a harness where no such
command existed; it arrived as prose and the agent improvised a receipt-less
channel. The structural vacuum was filed as host#26. The operator ruled the
ambition larger than a plugin: a properly worked goal and loop subsystem for
the `host-*` family, designed through the ruling chain (cast, blind external
judge, the real weak model), and then ruled again on form: an idiomatic
extension of the host methodology, not a port of how other implementations
function.

The first design was serviceable and foreign-rooted: a Manus-style
recitation hook, BDI commitment vocabulary (park as a live state), an
authorization token, plugin custom tools, and a closure gate deferred behind
a refactor. The cast's second convening, charged with idiom fidelity, found
each of these and named the house-native form.

## Decision

The modality, adopted in bounded form:

- **A goal is a `plan/NNNN` milestone.** No new artifact class; the record
  the rooms already keep is the goal record.
- **State splits by volatility.** Durable facts (set, parked, owed,
  abandoned, complete) are tracked surfaces the tool already authors: the
  milestone Status line, `[receipt "goal"]` stanzas, OWED entries in
  PLAN.md's closure queue. Machine state (this worktree's execution claim)
  is a gitignored sidecar re-derivable from the tracked record. One active
  goal per repo. A lost sidecar under-reports nothing.
- **The audited commit is the authority.** No authorization tokens; the
  operator-ruling line and the committed declaration are the act. The
  agent-side path proposes and never mutates.
- **Parking is re-queuing.** The existing queue surfaces own deferral; no
  parallel state machine.
- **Completion composes the existing gates as subprocesses.** The tool
  invokes its own verbs and reads their exits; HAZARD lines pass through
  intact; nothing is weakened, nothing duplicated. Every hazard prints,
  ordered, each with its exact fix command (the verify-setup shape).
- **The emission reuses house shapes.** NEEDS YOU is a HAZARD line traced
  to a tracked row; FRONTIER is the `tasks` frontier line verbatim; the
  last line is the exact bare command. No inline execution-class markers:
  the section is the class.
- **The MCP server and the corpus are the seams.** Goal verbs join the
  shipped MCP server; the goal declaration becomes a corpus surface (the
  plan/0083 shape), which is the house's recitation answer. Plugin custom
  tools and compaction re-injection are cut. The seam defers until the core
  is housegrown, and it renders, never actuates: the turn trigger stays
  human.
- **The teaching layer states none of this as new.** Per call/0060, the
  manual section reads present tense; the foreign lineage (Manus, BDI,
  Anthropic, the harness docs) lives here in the record layer.

## Consequences

plan/0101 executes this modality. The ledger entry that carries it to
adopters must state its applies-alone status, the stamp migration with the
re-stamp command and proof an old tool tolerates the new surfaces, the
sidecar re-derivation path, and the degraded mode as legible standing
without any verb. The weak-model battery gates the emission freeze and
reruns on real output. What is deliberately not built: plugin custom tools,
a compaction hook, and any actuating kick.

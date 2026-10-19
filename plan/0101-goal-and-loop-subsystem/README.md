# plan/0101: the goal and loop subsystem

**Status: cut and in build** (operator ruling 2026-10-18: build it, after a — active goal since 2026-10-19
reflection pause because it is core functionality; second ruling the same
day: the design must be an idiomatic extension of the host methodology, not
a port of foreign implementations). The modality itself is
[call/0061](../../call/0061-goals-are-milestones-and-completion-composes-the-gates.md);
this plan executes it.

## Why

The agent loop (orient, claim, work, bank a receipt, pass the gate) and any
goal layer exist today as prose discipline plus scattered verbs. In a live
session an operator invoked `/goal complete plan/0007` in a harness where no
such command existed; it arrived as prose and the agent improvised a
receipt-less channel ([host#26](https://github.com/connollydavid/host/issues/26)).
The operator ruled the ambition larger than the plugin that issue proposes,
and then ruled its form: housegrown first.

## Decision (the idiomatic form)

A goal **is** a `plan/NNNN` milestone. No new artifact class exists to
drift from the record.

**State splits by volatility**, the house's own division: durable facts are
tracked surfaces the tool already authors (the milestone Status line,
`[receipt "goal"]` stanzas in `.host-lifecycle-receipts`, OWED entries in
PLAN.md's closure queue), and machine state is a gitignored `.host-goal`
sidecar holding only this worktree's execution claim, re-derivable by
`goal repair` from the tracked record. A lost sidecar under-reports nothing:
the tracked declaration stands. One active goal per repo, because the
tracked record is singular; the sidecar is the per-worktree claim on it.

**Verbs** (single words, fail closed, usage on bad args, the `tasks` and
`next` family shape):

- `goal set <plan/NNNN>` writes the Status-line declaration and a receipt
  stanza, and refreshes the sidecar. No authority token: the audited commit
  of the declaration is the act, and the operator-ruling line names whose
  hand it was. The agent-side path is `goal propose`, which prints the
  command and never mutates.
- `goal show` is the orientation emission: labeled lines in fixed order
  (PURPOSE, GOAL, POSITION, NEEDS YOU, CI, FRONTIER, TREE, NEXT), reusing
  house shapes wherever they exist (NEEDS YOU is a HAZARD line that each
  trace to a tracked row and name the ask; CI is gate output; FRONTIER is
  the `tasks` ready-frontier line verbatim), the exact bare command alone on
  the last line, no inline execution-class markers (the section a move
  prints under is its class; command lines stay bare), a pure function of
  the working tree with no clock, and a loud refusal on unreadable state.
- `goal park --reason` / `goal unpark` are re-queuing, not a state machine:
  they write the Status line and the closure-queue entry and a receipt.
  A temporary block never gets recorded as an exit.
- `goal abandon --reason` appends the closure-queue OWED entry through the
  tool, writes the Status line and a receipt, and clears the sidecar. Debt
  lives where a cold reader looks first.
- `goal repair <plan/NNNN>` reconciles toward the tracked record and
  re-points a renamed plan, refusing ambiguity, with a receipt.
- `goal complete <plan/NNNN>` composes the existing gates as subprocesses
  (the tool invoking its own verbs and reading their exits; HAZARD lines
  pass through intact): the verify gate, the ci judge, task receipts for
  the milestone, the tree clean with nothing unpushed, and the PLAN.md row.
  No gate is weakened and none is duplicated; the tool drives the tools,
  [host#26](https://github.com/connollydavid/host/issues/26)'s constraint
  applied inward. A refusal is a full no-op; every hazard prints, ordered,
  each with its exact fix command (the verify-setup shape, not progressive
  disclosure); success writes one atomic `[receipt "goal"]` stanza, updates
  the Status line, and prints the next move or the no-goal state.

**The seam defers until the core is housegrown.** When it lands: goal tools
join the shipped MCP server (harnesses mount MCP natively), the goal
declaration becomes readable as a corpus surface (the plan/0083 shape, the
house's always-loaded mechanism, which is the recitation answer), and the
only harness-specific artifact is the nested `/host/goal` command family.
Plugin custom tools are cut (a duplicate tool surface), the compaction hook
is cut (the corpus is the recitation), and the kick stays unruled: the seam
renders and never actuates.

## Rulings

The chain ran in order, twice for the cast.

- **Cast, first convening** (design review): Mara ruled suggest never
  sanction, the PURPOSE and NEEDS YOU lines, and mid-goal maintenance
  sanctioned; Wren ruled the escape hatch, park, propose, and weak-model
  acceptance before freeze; Fen ruled the no-op refusal and ordered hazards;
  Bly ruled legibility without the verbs and the OWED discipline; Orin ruled
  the seam renders and never decides, and caught the tracked-key collision
  that first sent the pointer to a sidecar.
- **Codex** (blind bench, gpt-6-luna, one-shot): approve the CLI-first
  direction, do not freeze the contract yet; seventeen defects clustered on
  display versus authorization, state identity, revision-bound evidence,
  transactional closure, owed lifecycle, bounded retries. Transcript:
  [bench/codex-bench-2026-10-18.txt](bench/codex-bench-2026-10-18.txt).
- **Fen** (real qwen3.5-4b, mock emissions): eight of eight probes passed at
  deployment sampling, including the ordered-hazard refusal and the
  needs-you stop. Protocol and results: [fen-results.md](fen-results.md).
  The refusal shape changed after this battery (all hazards, each with its
  command), so the battery reruns against real output before the freeze.
- **Cast, second convening** (idiom fidelity, the operator's charge): the
  over-fit inventory and the house-native replacements recorded in
  [convening.md](convening.md) and adopted above. The token is cut (the
  audited commit is the authority), parking is re-queuing, the gate
  deferral is cut (subprocess composition), every hazard prints, class
  markers fold into sections, the emission reuses house shapes, goal tools
  belong to the MCP server, the corpus is the recitation surface, and the
  ruling itself belongs in call/.

## Prior art

Cited, with the lineage living in the record layer (call/0061) and never in
the mechanism's self-description: Manus 2025 (recitation, filesystem
context, stable prefixes), Anthropic 2024 (composable patterns, gates with
environmental ground truth), OpenCode v2 docs (the seam surfaces), BDI
(Rao and Georgeff 1995, commitment moves), make and ninja (the task DAG
with per-node receipts), ReAct (Yao et al. 2022) and Reflexion (Shinn et
al. 2023) for the loop and failure retention, the todo ledgers of Claude
Code and OpenCode plan mode, and Copilot Workspace for gated decomposition.

Where we stand: better on per-task receipts as audit, completion as a
refusing gate that composes the existing gates, a deterministic emission
with no clock, weak-model-first validation on the real 4B, one generated
seam versioned by the ledger, and display never equaling authorization;
worse on cross-session learning beyond MEMORY, swarm goals, frontier
ranking, and telemetry; different in that git history is the ledger,
degraded means legible without any verb, and the turn trigger stays human.

## Build sequence

### Land the design record {#design-record}
   This README, the bench records, and the call/0061 modality.
### Implement the goal module {#goal-module}
   `src/goal.rs`: the volatility split, the verbs, the emission in house
   shapes, the subprocess-composed closure gate; dispatch in `main()`;
   tests for sidecar round-trips, emission determinism, refusal no-op, and
   the composed gates on a fixture tree.
### Land the command family {#command-family}
   `.opencode/commands/host/goal.md` in this host (the dogfood), the
   `.host-goal` gitignore entry, verified by invoking `/host/goal`.
### Dogfood the loop {#dogfood-loop}
   Set this milestone as the goal under the operator's build ruling, drive
   the remaining tasks through `goal show`, receipt them, and close the
   milestone with `goal complete` (or record honestly why v1 could not
   close its own milestone).
### Fen battery on real output {#fen-real-output}
   The battery rerun against real `goal show` and `goal complete` output
   under the house refusal shape; the freeze gate. Riding beside it, one
   fresh codex bench (gpt-6.1 if available, for judge freshness: no lineage
   to the v2 bench) scoped to the implemented contract: the real output
   samples plus the unresolved nails (transactional ordering at the closure
   receipt, the owed-item lifecycle, receipt freshness).
### Goal tools on the MCP server {#mcp-tools}
   The verbs join the shipped MCP server so any harness mounts them
   natively; the plugin custom-tool family stays cut.
### The corpus surface {#corpus-surface}
   The goal declaration readable as an always-loaded surface, the plan/0083
   shape, so every session and every harness loads it with no plugin.
### Spine and ledger {#spine-ledger}
   The manual section in present tense per call/0060 and call/0061; the
   UPGRADING.md entry carrying applies-alone status, the stamp migration
   with the re-stamp command and old-tool tolerance, the sidecar
   re-derivation, and the degraded mode stated as legible-without-verbs.

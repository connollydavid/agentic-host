# plan/0101: the goal and loop subsystem

**Status: cut and in build** (operator ruling 2026-10-18: build it, after a; active goal since 2026-10-19; parked (the composed gate holds on host-lint's kani lane (cancelled at its pin, host-lint thirty-two); resume when that lane greens) since 2026-10-20 — active goal since 2026-10-29
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
  pass through intact): the full verify sweep, equal to what the verify
  skill runs (the software gate, the ci judge, `book --check`, the refs
  gate, and obligations per discovered spec), then task receipts for
  the milestone, the tree clean with nothing unpushed, and the PLAN.md row.
  No gate is weakened and none is duplicated; the tool runs its own verbs,
  [host#26](https://github.com/connollydavid/host/issues/26)'s constraint
  applied inward. A refusal is a full no-op; every hazard prints, ordered,
  each with its exact fix command (the verify-setup shape, not progressive
  disclosure); success writes one atomic `[receipt "goal"]` stanza, updates
  the Status line, and prints the next move or the no-goal state.

**The install is a generated door family, folded in early (the operator's
ruling).** The `install` verb owns the front doors as one source inside the
binary and emits the per-harness renderings: flat, hyphenated `/host-<verb>`
doors (`/host-goal`, `/host-tasks`, `/host-ci`) for OpenCode and Claude
alike, each injecting its verb's emission and closing with the re-orient
link; `install --check` guards the files against hand edits with the
regenerate remedy. The universal-form ruling behind it: the spine states
the token once, and each harness's sigil is chrome. Goal tools join the
shipped MCP server (harnesses mount MCP natively), the goal declaration
becomes readable as a corpus surface (the plan/0083 shape, the house's
always-loaded mechanism, which is the recitation answer). Plugin custom
tools stay cut (a duplicate tool surface), the compaction hook stays cut
(the corpus is the recitation), and the kick stays unruled: the install
renders and never actuates.

## Rulings

The chain ran in order, twice for the cast.

- **Cast, first convening** (design review): Mara ruled suggest never
  sanction, the PURPOSE and NEEDS YOU lines, and mid-goal maintenance
  sanctioned; Wren ruled the escape hatch, park, propose, and weak-model
  acceptance before freeze; Fen ruled the no-op refusal and ordered hazards;
  Bly ruled legibility without the verbs and the OWED discipline; Orin ruled
  the install renders and never decides, and caught the tracked-key collision
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
environmental ground truth), OpenCode v2 docs (the install surfaces), BDI
(Rao and Georgeff 1995, commitment moves), make and ninja (the task DAG
with per-node receipts), ReAct (Yao et al. 2022) and Reflexion (Shinn et
al. 2023) for the loop and failure retention, the todo ledgers of Claude
Code and OpenCode plan mode, and Copilot Workspace for gated decomposition.

Where we stand: better on per-task receipts as audit, completion as a
refusing gate that composes the existing gates, a deterministic emission
with no clock, weak-model-first validation on the real 4B, one generated
install surface versioned by the ledger, and display never equaling authorization;
worse on cross-session learning beyond MEMORY, swarm goals, frontier
ranking, and telemetry; different in that git history is the ledger,
degraded means legible without any verb, and the turn trigger stays human.

## Contract closure (the final consult, 2026-10-19)

The final-design consult ran the cast and a blind external bench over the
settled form. The cast: Mara signed off (the real-output rerun tracked, not
blocking); Wren signed off short of a watched item (a window cut that keeps
NEXT but drops PURPOSE loses the why; watched at the fen rerun, not
pre-fixed); Fen signed off conditional on the rerun passing with a resolved
key on the last line; Bly refused until two holes were answered; Orin signed
off with two wording amendments. The bench (transcript:
[bench/codex-final-design-2026-10-19.txt](bench/codex-final-design-2026-10-19.txt))
ruled the shape sound, freeze not yet, four blockers. The rulings that
follow close them.

- **Authority order, stated once**: receipt stanzas over the Status line
  over the sidecar. A crash between writes reconciles downward by
  `goal repair`; no journal is owed because the authority order makes every
  partial state recoverable by re-derivation.
- **The no-op defined**: the sweep's composed gates are check-mode verbs
  that write nothing; a refusal forbids every write, including the
  sidecar. The only writes the verb ever makes are the closure's own
  receipt and Status line, after all gates pass.
- **The closure names its own commit**: complete demands a clean tree and
  then dirties it with exactly two files; the success output names both and
  the commit-and-push that follows (landed in the component, `cd440d8`).
- **A divergent sidecar is a hazard**: absent is no claim (fine); a claim
  on another goal while the closure names this one refuses with the repair
  remedy (landed, `cd440d8`). Park's tracked trace is built as ruled: the
  receipt stanza and the Status transition, never sidecar-only.
- **The offline boundary**: the sweep runs no network; the unpushed count
  reads the local remote-tracking ref, which can itself be stale, and the
  emission's `revision-unbound` label is the standing disclosure of that
  class.
- **The last line is never placeholder-shaped**: every NEXT line carries a
  resolved key or a runnable command as printed (Fen's ruling); the
  emission asserts it.
- **Spine wordings (Orin)**: the spine states the closed verb list the
  binary enforces, with ASD-STE100 as provenance of the list, not the rule;
  and it names the sidecar-authority boundary as the checkable form (no
  verb reads the sidecar as authority) rather than the rationale word. The
  door family is data the adopter owns: a third harness is an edit, not a
  fork.

The freeze bench (transcript:
[bench/codex-freeze-bench-2026-10-19.txt](bench/codex-freeze-bench-2026-10-19.txt))
ruled the outputs coherent and named three blockers, all now closed. The
crash window is steel: a complete or abandon receipt whose Status
transition never landed reads as an unresolved closure and repair finishes
the write (component `bf0e7a3`). The owed lifecycle takes the bench's
minimal rule: the row names its owner, discharge is evidence recorded on
the row, and owed work never outranks the active goal unless that goal
depends on it (the design text's outranking claim is corrected here; the
v1 code never implemented it). And revision binding was never absent from
the gate: the composed ci judge compares receipts against the judged
revision (the live refusal shows that hazard firing), so the
`revision-unbound` label is display honesty about the emission, not a
gate gap. With the fen gate passed at sixteen of sixteen and the three
blockers closed, the freeze stands. The teaching lines carry a measured
scorecard (2026-10-20): the dokimi paired-arms run, subject qwen3.5-4b with
qwen3.6-27b as judge, scored baseline 30.8 against profile 89.0 (paired
delta +58.2, CI [+28.7, +87.8]); the instrument is adopted at `tools/dokimi`
and the transcript files in the plan's bench.

## Build sequence

### Land the design record {#design-record}

- verify: this README and its bench records are committed, and the PLAN.md row names the milestone
   This README, the bench records, and the call/0061 modality.
### Implement the goal module {#goal-module}

- verify: cargo test green and clippy clean in the lifecycle worktree, with the verbs failing closed on bad args
- inputs: software/host-lifecycle/main/src/goal.rs
   `src/goal.rs`: the volatility split, the verbs, the emission in house
   shapes, the subprocess-composed closure gate; dispatch in `main()`;
   tests for sidecar round-trips, emission determinism, refusal no-op, and
   the composed gates on a fixture tree.
### Land the command family {#command-family}

- verify: the door resolves and injects the emission from the host root
   `.opencode/commands/host-goal.md` in this host, the `.host-goal`
   gitignore entry, verified end to end through the binary in-session.
   Originally receipted under the nested `/host/goal` form; superseded by
   the universal-form ruling and the generated family: the doors are now
   `install`-written, flat `/host-<verb>`, one source in the binary, two
   harness renderings, guarded by `install --check`.
### Run loop {#run-loop}

- verify: the goal set on this milestone, the tasks run through goal show, and the milestone closed with goal complete (or the failure recorded honestly)
   Set this milestone as the goal under the operator's build ruling, run
   the remaining tasks through `goal show` and receipt them. Close the
   milestone with `goal complete`; if the composed gate refuses on a lane
   this milestone does not own, park with the reason and record it.
### Fen battery on real output {#fen-real-output}

- verify: the battery transcripts on real output filed and passing under the house refusal shape
   The battery rerun against real `goal show` and `goal complete` output
   under the house refusal shape; the freeze gate. Riding beside it, one
   fresh codex bench on gpt-6-luna, the account-served judge (gpt-6.1 is
   not served to this codex account), with the limitation stated in its
   transcript: sessions are stateless, so per-question blindness holds, but
   the judge-model lineage matches the earlier bench. Scope: the real
   output samples plus the unresolved nails (transactional ordering at the
   closure receipt, the owed-item lifecycle, receipt freshness).
### Goal tools on the MCP server {#mcp-tools}

- verify: the verbs answer through the shipped MCP server
   The verbs join the shipped MCP server so any harness mounts them
   natively; the plugin custom-tool family stays cut.
### The corpus surface {#corpus-surface}

- verify: the goal declaration loads as an always-loaded surface with no plugin in the path
   The goal declaration readable as an always-loaded surface, the plan/0083
   shape, so every session and every harness loads it with no plugin.
### Spine and ledger {#spine-ledger}

- verify: the manual section present-tense with the UPGRADING entry carrying applies-alone status and the stamp migration, and the teaching lines carrying a dokimi arms scorecard
   The manual section in present tense per call/0060 and call/0061; the
   UPGRADING.md entry carrying applies-alone status, the stamp migration
   with the re-stamp command and old-tool tolerance, the sidecar
   re-derivation, and the degraded mode stated as legible-without-verbs.
### Release and re-pin {#release-and-re-pin}

- verify: the verify gate green at the tag, the artifact hash re-derived in the recorded toolchain, and the re-pin receipted
   Release host-lifecycle carrying the goal verbs and the install verb through the
   tool-carried sequence. The doors go live off PATH and `/host-goal`
   stops depending on a debug binary; the composed closure gate can then
   close this milestone without the pin hazard.

**The close (2026-10-20).** All nine tasks receipted. The composed closure
gate refused on exactly one hazard, a lane this milestone does not own:
host-lint's kani lane, cancelled at its pin (the six-hour runner ceiling,
[host-lint#32](https://github.com/connollydavid/host-lint/issues/32)). Per
this task's own verify, the goal parks with the reason rather than exiting:
the close resumes with `goal unpark .` the day that lane greens at a pin.
Everything else the gate composes passed: the full verify sweep, all nine
task receipts, the plan row, and a clean pushed tree.

Deferred elsewhere, named so the queue does not lose them: a
milestone-cutting primitive (number allocation plus README scaffold)
belongs to [host#27](https://github.com/connollydavid/host/issues/27)'s
minting work, and Mara's semantic-acceptance line (a `goal accept`
operator verb writing the ack onto the closure receipt) awaits the
operator's fold ruling.

# plan/0073 host-lifecycle-dream: advisory memory-consolidation pass (two-store, recall-aware)

Closes [connollydavid/host-lifecycle#16](https://github.com/connollydavid/host-lifecycle/issues/16).

## Why

`host-lifecycle validate` checks room structure and naming; it has no notion of
memory-content staleness. A recalled memory that a later decision silently
superseded is invisible until an agent anchors on it. The motivating failure (in
the issue) was exactly that: a session anchored a megakernel base on a recalled
note that was a one-day-later *workaround* description, and missed the standing
operator decision that locked the base to F16-ssm_out. When sent back, it
re-asserted the stale reading instead of reconciling to the standing decision. A
`dream` pass would have flagged the contradiction, the unlinked supersession, and
the workaround-vs-plan framing before any build.

## Scope

Add `host-lifecycle dream <dir>`: an **advisory**, read-mostly audit that
reconciles the project's memory against the record and flags staleness,
contradictions, drift, and append-only violations. It emits findings; it does not
auto-rewrite. Memory is high-value and the repo store is append-only, so the
default is report-only.

### Operator rulings (2026-07-19)

1. **Both stores audited.** The repo `MEMORY.md` (append-only) and the per-user
   memory store (editable) are both in scope. The asymmetry is encoded in what
   `dream` suggests: an *append* for repo-store findings, an in-place edit
   suggestion for editable-store findings.
2. **Per-user store is auto-detected per harness.** `dream` probes each of the
   six harnesses from the plan/0071 allowlist (opencode, claude, codex, qwen,
   cursor-agent, pi), reads whichever memory layout each uses, and merges them.
   The harness memory-store survey is a gather-data row.
3. **Spine doctrine.** The per-user memory-store convention (path, format, the
   editable-vs-append-only asymmetry) lands in host-template's CLAUDE.md, with
   an adopter UPGRADING entry. `dream` is the gate; the spine names the rule.
4. **Full methodology.** Gather-data (harness survey + Fen probes), cast
   consultation, adversarial design review, then build.

## The two-store asymmetry (load-bearing)

1. **Repo `MEMORY.md`**: append-only (CLAUDE.md §6). `dream`:
   - never proposes an in-place edit;
   - suggests an *append* with the correction text and a forward `[[link]]` from
     the superseded entry;
   - **detects** any edit to an existing entry as an append-only violation (the
     one and only sanctioned §6 escape is the archive-first map-only rename;
     every other in-place edit is a violation).
2. **Per-user store**: editable. `dream`:
   - may propose in-place rewrites, prunes, relinks;
   - reconciles the index one-liner with the corrected file `description`;
   - keeps durable measured lore even inside a stale entry (mark the state
     superseded, do not delete the facts).

## Detectors (candidate `dream` checks)

Each is grounded in a real failure mode observed in the motivating run.

- **description-vs-body drift.** A file's `description:` (what recall keys on)
  contradicts its own self-corrected body. Recall surfaces the stale one-liner.
- **index-vs-file drift.** The `MEMORY.md` index pointer is staler than the file
  it points to (the file was corrected; the index was not).
- **superseded-but-unlinked.** A conclusion that a later memory overturns, with
  no forward `[[link]]` between them, so the overturned entry still reads as
  current.
- **stale STATE markers over durable lore.** A large snapshot memory whose state
  is done but whose measured lore is still valid. Needs a dated current-state
  block, not a rewrite.
- **workaround-vs-plan conflation.** Two entries asserting contradictory current
  facts, neither pointing at the other, where one is a fix-of-the-moment and the
  other is the plan.
- **dangling `[[links]]`** on either store.
- **append-only violations** on the repo store (any edit to an existing entry
  that is not the sanctioned §6 archive-first rename).

## Routing (the cross-harness discipline)

`dream` is read-only and routes findings; it never writes.

- **editable-store hygiene** -> suggested edits, printed verbatim.
- **repo-store staleness** -> suggested **append** with the correction text and
  the forward `[[link]]` to add, printed verbatim.
- a finding that touches a `call/` or `plan/` **room** -> route to the MADR path
  (`Status: superseded` on the immutable record + audited commit), **not** a
  memory edit. `dream` names the room and the record; it does not touch them.
- **anti-ouroboros**: `dream` is methodology hygiene, not a software decision.
  It must **not** propose minting a `call/` for the audit itself. The durable
  output is the corrected store plus a `feedback`-type memory capturing the
  lesson.

`dream` also sits at the intersection of:

- **the two memory stores** (different rules),
- **the recall injector** (which per-user descriptions get surfaced into
  context; staleness there is what misleads the agent),
- **`host-lint`** (which gates any repo-store commit; the suggested appends must
  be lint-clean),
- **the room discipline** (findings that touch `call/`/`plan/` route to
  `validate`/MADR, not to a memory edit).

A memory-only linter that ignored any one of those would give unsafe advice.

## The CLI shape

- `host-lifecycle dream <dir>`: read-mostly. Print findings, do not write.
- `host-lifecycle dream <dir> --fix`: apply **only** the mechanical, safe class
  (index/description reconciliation, dangling-link repair) on the **editable**
  store, never the repo store. Refuses the repo store even with `--fix`.
- `host-lifecycle dream <dir> --json`: machine-readable findings (a weak agent
  can route them).
- Exit codes follow the host-lint convention: `0` clean, `1` findings, `2`
  cannot-proceed-on-input (no repo, no per-user store found).

The `--fix` set is conservative and grows one class at a time. Anything that
touches meaning (the workaround-vs-plan class, the supersession class) is
report-only forever; only structure (the index one-liner, the dangling link)
is `--fix`-able.

## Open design questions

The gather-data and cast pass rule on these:

- **Harness memory-store survey.** The exact paths and formats for each of the
  six harnesses. Claude Code is `~/.claude/memory/*.md` + `MEMORY.md` index; the
  other five need to be confirmed from each harness's docs. A harness with no
  memory store is a clean skip (no findings, no error).
- **The per-user store format.** Is the `description:` + free-form body format
  Claude Code's convention or ours? The spine must name a format; the question
  is whether we adopt Claude Code's verbatim or define our own and document the
  mapping per harness.
- **The detection ordering.** Some detectors are cheap and structural
  (dangling-link, index-vs-file); some are semantic
  (workaround-vs-plan, supersession). The semantic detectors need a
  weaker-agent-bar phrasing: what does the detector actually key on, and is it
  a signal a 4B can read? The Fen probe settles this.
- **The Allium spec scope.** Per plan/0014, a stateful feature earns an Allium
  spec. The detector state machine (each finding is a `Check` over a
  `MemoryEntry` entity) is the natural model. Open: does the spec live in the
  host-lifecycle repo (specs-live-with-software, plan/0012)? Yes.
- **The cast-consultation frame.** Bly, Fen, Orin each see a different failure
  mode (overstates-completeness, weak-agent-trap, fails-unsafe). The cast
  review shapes the `--fix` set and the report format.

## The spine doctrine (host-template CLAUDE.md)

The spine gains:

- a **per-user memory store convention**: a documented path, a documented format
  (file per memory, `MEMORY.md` index), and the editable rule;
- a restatement of the **append-only asymmetry** at the per-user level: the repo
  `MEMORY.md` is append-only; the per-user store is editable; `dream` is the
  gate that holds both;
- a `dream` cadence: when to run it (e.g. at the start of a session that will
  rely on recall, at the end of a session that superseded a decision).

An adopter UPGRADING entry keys the new revision and requires the host-lifecycle
release that carries `dream`.

## Verification

- **Unit tests** for every detector: each fires on a constructed fixture and is
  silent on a clean fixture. The append-only-violation detector fires on a
  hand-edited repo `MEMORY.md` and is silent on the append-only one.
- **Integration tests** for the routing: a repo-store finding suggests an append;
  an editable-store finding suggests an edit; a finding that touches a `call/`
  record names the room and does not propose an edit.
- **Allium spec** models the detector state machine; `allium check` + `analyse`
  + `plan` exit 0; obligations discharged by tests; Kani for the structural
  invariants (e.g. the `--fix` set never touches the repo store).
- **Fen probe** (gather-data.md): the detector phrasing reads as a finding to a
  4B, and the routing reads as a route (not an action). The cross-harness
  memory-store probe is grounded in a survey, not a guess.
- **Cast consultation** (cast/*.md): the `--fix` set and the report format clear
  Bly (overstates-completeness), Fen (weak-agent-trap), Orin (fails-unsafe).
- **Adversarial design review** (design-review.md): the load-bearing questions
  (the auto-detect harness probe, the `--fix` safety boundary, the spine
  doctrine scope) get five independent lenses.
- `host-lifecycle software --check .` clean at the new pin; the host-lifecycle
  release receipt recorded; #16 closed.

## Build sequence

The tasks are anchored receipted nodes (plan/0042), built as a forward graph:

### gather-data {#gather-data}
Grounds every conditional in data: the six-harness memory-store survey (paths,
formats, presence/absence), and the Fen probe on detector phrasing and routing
legibility.
- verify by: every conditional in this README traces to a gather-data.md row
- depends: none

### write-spec {#write-spec}
The `DreamRun` Allium surface with the detector state machine, the routing
rules, and the append-only-violation invariant. Lives in the host-lifecycle
repo (specs-live-with-software).
- verify by: `allium check` + `allium analyse` exit 0, zero findings
- depends: #gather-data

### write-obligations {#write-obligations}
Every `allium plan` obligation dispositioned in a `<spec>.obligations` manifest,
discharged by the unit and integration tests.
- verify by: `host-lifecycle obligations <spec> --tests tests --strict-discharge`
  clean
- depends: #write-spec

### implement-dream {#implement-dream}
The `dream` subcommand, the per-harness store probes, the detector set, the
routing, and the report formatter. `--fix` is the conservative structural-only
set on the editable store, refusing the repo store.
- verify by: `cargo test` green; `dream <fixture>` emits the expected findings;
  `--fix` refuses a repo-store fixture
- depends: #write-obligations

### write-tests {#write-tests}
Integration tests covering every detector, every routing path, and the
append-only-violation guard. The `--fix` safety property is a Kani harness.
- verify by: full test suite green; Kani proof of the `--fix` no-repo-store
  invariant
- depends: #implement-dream

### cast-consult {#cast-consult}
Cast consultation across Mara, Wren, Bly, Orin, Fen: the `--fix` boundary, the
report format, the detector phrasing. Recorded in design-review.md.
- verify by: each cast persona's concern addressed or recorded as a follow-up
- depends: #implement-dream

### adversarial-review {#adversarial-review}
A multi-lens adversarial review of the design and the implementation: the
auto-detect probe, the `--fix` safety boundary, the spine doctrine scope. Findings
recorded in design-review.md; the re-cut staged there.
- verify by: every blocking finding fixed or recorded; the re-cut executed
- depends: #cast-consult

### write-spine-doctrine {#write-spine-doctrine}
The host-template CLAUDE.md gains the per-user memory-store convention, the
append-only asymmetry restated at the per-user level, and the `dream` cadence.
An UPGRADING entry keys the new revision.
- verify by: `host-lifecycle upgrade` lists the entry on a pre-revision host;
  `upgrade --record` clears it
- depends: #adversarial-review

### release-and-re-pin {#release-and-re-pin}
`host-lifecycle release host-lifecycle --change-class adds-flag`, re-pin
`.host-software`, record the release receipt, close #16.
- verify by: `host-lifecycle software --check .` clean at the new pin; #16
  closed
- depends: #write-spine-doctrine

### fen-acceptance {#fen-acceptance}
The real `qwen3.5-4b` runs `dream` on a constructed fixture with a known
supersession and confirms the finding routes (suggested append vs suggested edit
vs MADR route), not just that a finding exists.
- verify by: Fen routes each finding class correctly on the fixture
- depends: #release-and-re-pin

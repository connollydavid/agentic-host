# plan/0073 host-lifecycle-dream: own the per-user memory store, then audit it

Closes [connollydavid/host-lifecycle#16](https://github.com/connollydavid/host-lifecycle/issues/16).

## Why

`host-lifecycle validate` checks room structure and naming; it has no notion of
memory-content staleness. A recalled memory that a later decision silently
superseded is invisible until an agent anchors on it. The motivating failure
(in the issue) was exactly that: a session anchored a megakernel base on a
recalled note that was a one-day-later *workaround* description, and missed the
standing operator decision that locked the base to F16-ssm_out.

The original plan was to audit each vendor's per-user memory store. The
gather-data survey (2026-07-19) showed that path is not worth it: the closed
harnesses are encrypting their stores, opencode has no native store at all, and
fighting encryption is a moving target with no durable win. The clean play is
to **own the store**: ship an optional opencode plugin that implements the
host-* per-user store format, and let `dream` audit *that*. Vendor stores become
explicitly out of scope.

## Scope

Three deliverables, in one milestone:

1. **The host-* per-user memory store** (the format and the storage layer). A
   markdown-per-entry store at `~/.host-memory/<project>/`, with a `MEMORY.md`
   index, `description:` + free-form body per entry, and `[[slug]]` cross-entry
   links. The format is the methodology's own, named in the spine.
2. **Memory tools added to the existing `host-lifecycle mcp` server** (shipped
   in v0.39.0 per plan/0065 with `init` and `adopt`). The plan/0073 work adds
   `memory_list` / `memory_read` / `memory_write` / `memory_consolidate` to
   that server. The reference implementation of the format; the plugin opencode
   already loads gains a per-user memory tier alongside the onboarding tools.
3. **`host-lifecycle dream <dir>`**: the advisory, read-mostly audit over both
   stores (the repo `MEMORY.md` and the host-* per-user store), flagging
   staleness, contradictions, drift, and append-only violations. Read-only by
   default; emits findings, never auto-rewrites.

### Operator rulings (2026-07-19)

1. **Own the store; do not read vendor stores.** The closed harnesses encrypt
   their stores; opencode has none. We ship an optional opencode plugin that
   implements the host-* format. Other harnesses are out of scope; an operator
   on a closed harness uses only the repo `MEMORY.md` tier.
2. **Both stores audited.** The repo `MEMORY.md` (append-only) and the host-*
   per-user store (editable) are both in `dream`'s scope. The asymmetry is
   encoded in what `dream` suggests: an *append* for repo-store findings, an
   in-place edit suggestion for editable-store findings.
3. **Memory tools added to the existing `host-lifecycle mcp` (stdio), not a
   new server.** Plan/0065 shipped `host-lifecycle mcp` (v0.39.0) with `init`
   and `adopt`. plan/0073 extends that server with `memory_list` /
   `memory_read` / `memory_write` / `memory_consolidate`. Same stdio JSON-RPC
   pattern; one server, two concerns (onboarding + memory), each tool
   independently invocable. Matches the existing opencode MCP config (pal is
   configured the same way); portable to any harness that speaks MCP.
4. **One plan, not split.** Doctrine + plugin + dream ship together. The
   plugin and the audit co-evolve against the same format.
5. **Full methodology.** Gather-data (done), cast consultation, adversarial
   review, then build.

### What is descoped (explicitly)

- Reading any closed/encrypted vendor memory store (Codex, Cursor, Pi, etc.).
  Closed harnesses get the repo `MEMORY.md` tier only.
- Reading Claude's or Qwen's native store, even though both are plain
  markdown. Convergent formats are noted empirically in the survey; nothing is
  adopted from them. The host-* store is its own thing.
- Auto-detecting which harness is running. `dream` reads `~/.host-memory/`
  regardless of harness; an operator who installed the plugin gets audited, an
  operator who did not gets only the repo-store findings.

## The two-store asymmetry (load-bearing)

1. **Repo `MEMORY.md`**: append-only (CLAUDE.md §6). `dream`:
   - never proposes an in-place edit;
   - suggests an *append* with the correction text and a forward `[[link]]` from
     the superseded entry;
   - **detects** any edit to an existing entry as an append-only violation (the
     one and only sanctioned §6 escape is the archive-first map-only rename;
     every other in-place edit is a violation).
2. **Host-* per-user store** (editable). `dream`:
   - may propose in-place rewrites, prunes, relinks;
   - reconciles the index one-liner with the corrected entry `description`;
   - keeps durable measured lore even inside a stale entry (mark the state
     superseded, do not delete the facts).

## Detectors (candidate `dream` checks)

Each is grounded in a real failure mode observed in the motivating run. The
gather-data Fen probe (2026-07-19) showed the simpler detectors read clearly at
the weak-agent bar and the methodology-discipline ones do not; the build does
not start until the detector naming is sharpened (three options recorded in
`gather-data.md`: rename, lean on routing, or accept partial coverage at the
4B bar).

- **description-vs-body drift.** An entry's `description:` (what recall keys
  on) contradicts its own self-corrected body. (Fen PASS both temps.)
- **index-vs-file drift.** The `MEMORY.md` index pointer is staler than the
  file it points to.
- **superseded-but-unlinked.** A conclusion that a later memory overturns,
  with no forward `[[link]]` between them. (Fen PASS both temps.)
- **stale STATE markers over durable lore.** A snapshot memory whose state is
  done but whose measured lore is still valid.
- **workaround-vs-plan conflation.** Two entries asserting contradictory
  current facts, neither referencing the other.
- **dangling `[[link]]`** on either store.
- **append-only violations** on the repo store. (Fen conflated with
  stale-state-over-lore; the build sharpens the naming before this detector
  ships.)
- **room-touching findings** routed to MADR. (Fen conflated with
  superseded-but-unlinked; same sharpening.)

## Routing (the cross-harness discipline, now narrower)

`dream` is read-only and routes findings; it never writes.

- **editable-store hygiene**: suggested edits, printed verbatim.
- **repo-store staleness**: suggested **append** with the correction text and
  the forward `[[link]]` to add, printed verbatim.
- a finding that touches a `call/` or `plan/` **room**: route to the MADR path
  (`Status: superseded` on the immutable record + audited commit), **not** a
  memory edit. `dream` names the room and the record; it does not touch them.
- **anti-ouroboros**: `dream` is methodology hygiene, not a software decision.
  It must **not** propose minting a `call/` for the audit itself. The durable
  output is the corrected store plus a `feedback`-type memory capturing the
  lesson.

`dream` also sits at the intersection of:

- **the two memory stores** (different rules),
- **the recall injector** (which per-user descriptions get surfaced into
  context; the MCP server is the recall surface),
- **`host-lint`** (which gates any repo-store commit; the suggested appends must
  be lint-clean),
- **the room discipline** (findings that touch `call/`/`plan/` route to
  `validate`/MADR, not to a memory edit).

## The CLI shape

- `host-lifecycle dream <dir>`: read-mostly. Print findings, do not write.
- `host-lifecycle dream <dir> --fix`: apply **only** the mechanical, safe class
  (index/description reconciliation, dangling-link repair) on the **editable**
  host-* store, never the repo store. Refuses the repo store even with `--fix`.
- `host-lifecycle dream <dir> --json`: machine-readable findings.
- `host-lifecycle mcp`: the stdio MCP server (shipped v0.39.0). Plan/0073
  adds the memory tools (`memory_list`, `memory_read`, `memory_write`,
  `memory_consolidate`) alongside the existing `init` and `adopt`. Loaded by
  opencode (or any MCP-speaking harness) via the standard stdio-MCP config.
- Exit codes follow the host-lint convention: `0` clean, `1` findings, `2`
  cannot-proceed-on-input (no repo, no host-* store found).

The `--fix` set is conservative and grows one class at a time. Anything that
touches meaning (the workaround-vs-plan class, the supersession class) is
report-only forever; only structure (the index one-liner, the dangling link)
is `--fix`-able.

## The store format (the spine names it)

The host-* per-user memory store at `~/.host-memory/<project>/`:

```
~/.host-memory/
  <project>/                   # one dir per project (encoded cwd, claude-style)
    MEMORY.md                  # the index: one bullet per entry
    <slug>.md                  # one markdown file per memory entry
    ...
```

Each entry file:

```markdown
---
description: <one-line summary; what recall keys on>
type: feedback | fact | workaround | state        # the entry's class
created: <YYYY-MM-DD>
---

<free-form markdown body>

<optional [[slug]] cross-references to other entries>
```

The `MEMORY.md` index:

```markdown
- [<Title>](<slug>.md) — <one-line summary, same as the description: line>
```

The format is the methodology's own. The opencode plugin implements it; the
`dream` audit reads it. Convergence with other harnesses' formats is
empirical, not load-bearing.

## Open design questions

The cast pass and adversarial review rule on these:

- **Detector naming.** The gather-data probe showed `append-only-violation`
  and `room-touching` do not read clearly at the 4B bar. Three options on the
  table (rename, lean on routing, accept partial coverage); a fourth is now
  viable since we own the store: **emit the route as the primary finding and
  the class as secondary metadata**, so the operator-facing surface is
  always actionable ("append this", "edit that", "file this MADR") even when
  the class name is fuzzy.
- **The MCP tool surface.** Four new tools (`memory_list` / `memory_read` /
  `memory_write` / `memory_consolidate`) join the existing `init` and `adopt`
  on the `host-lifecycle mcp` server (plan/0065). The cast review confirms
  whether `memory_search` (a semantic query) is needed at MVP or is a
  follow-up.
- **The store's project-encoding.** Claude uses `/`-to-`-` cwd mangling;
  opencode uses a SQLite-keyed project id. The host-* format names its own
  project-encoding (the cwd with `/` to `-`, plus a project-name override
  for the harness-agnostic case), documented in the spine.
- **The Allium spec scope.** Per plan/0014, a stateful feature earns an
  Allium spec. The detector state machine + the MCP tool surface are the
  natural model. The spec lives in the host-lifecycle repo.
- **The cast-consultation frame.** Bly, Fen, Orin each see a different
  failure mode. The cast review shapes the `--fix` set, the MCP tool
  naming, and the report format.

## The spine doctrine (host-template CLAUDE.md)

The spine gains:

- the **host-* per-user memory store convention**: the path
  (`~/.host-memory/<project>/`), the format (markdown per entry, `MEMORY.md`
  index, `description:` + free-form body, `[[slug]]` cross-refs), and the
  editable rule;
- a restatement of the **append-only asymmetry** at the per-user level: the
  repo `MEMORY.md` is append-only; the per-user store is editable; `dream` is
  the gate that holds both;
- a `dream` cadence: when to run it (e.g. at the start of a session that will
  rely on recall, at the end of a session that superseded a decision);
- a note that **the host-* per-user store is the reference tier**; vendor
  stores are not read. An operator on a harness without the MCP plugin gets
  only the repo `MEMORY.md` tier.

An adopter UPGRADING entry keys the new revision and requires the host-lifecycle
release that carries `dream` and `mcp`.

## Verification

- **Unit tests** for every detector: each fires on a constructed fixture and is
  silent on a clean fixture. The append-only-violation detector fires on a
  hand-edited repo `MEMORY.md` and is silent on the append-only one.
- **Integration tests** for the routing: a repo-store finding suggests an append;
  an editable-store finding suggests an edit; a finding that touches a `call/`
  record names the room and does not propose an edit.
- **Integration tests for the MCP server**: `memory_list` returns the index;
  `memory_read` returns an entry; `memory_write` creates a new entry with the
  right frontmatter and updates the index; `memory_consolidate` runs a `dream`
  pass and reports findings. Tool calls exercised over stdio JSON-RPC. The
  existing `init`/`adopt` tools (plan/0065) stay green unchanged.
- **Allium spec** models the detector state machine and the MCP tool surface;
  `allium check` + `analyse` + `plan` exit 0; obligations discharged by tests;
  Kani for the structural invariants (e.g. the `--fix` set never touches the
  repo store).
- **Fen probe** (gather-data.md): the detector phrasing reads as a finding to
  a 4B at both temps for the simpler detectors; the methodology-discipline
  detectors are either sharpened to pass at the 4B bar or surface the route
  as the primary finding.
- **Cast consultation** (cast/*.md): the `--fix` set, the MCP tool naming,
  and the report format clear Bly (overstates-completeness), Fen (weak-agent
  -trap), Orin (fails-unsafe).
- **Adversarial design review** (design-review.md): five independent lenses,
  with the duplication risk (vs. plan/0074's envhash) and the auto-detect
  reversal as named lenses.
- `host-lifecycle software --check .` clean at the new pin; the host-lifecycle
  release receipt recorded; #16 closed.

## Build sequence

The tasks are anchored receipted nodes (plan/0042), built as a forward graph:

### gather-data {#gather-data}
Grounds every conditional in data: the six-harness memory-store survey, the
auto-detect reversal (closed harnesses encrypt; opencode has no native store),
and the Fen probe on detector phrasing and routing legibility.
- verify: every conditional in this README traces to a gather-data.md row
- depends: none

### write-spec {#write-spec}
The `DreamRun` and `MemoryStore` Allium surface with the detector state
machine, the MCP tool surface, the routing rules, and the append-only-violation
invariant. Lives in the host-lifecycle repo.
- verify: `allium check` + `allium analyse` exit 0, zero findings
- depends: #gather-data

### write-obligations {#write-obligations}
Every `allium plan` obligation dispositioned in a `<spec>.obligations` manifest,
discharged by the unit and integration tests.
- verify: `host-lifecycle obligations <spec> --tests tests --strict-discharge`
  clean
- depends: #write-spec

### implement-store {#implement-store}
The storage layer: read/write markdown entries at
`~/.host-memory/<project>/`, the `MEMORY.md` index manager, the `[[slug]]`
link resolver, the project-encoding helper.
- verify: `cargo test` green; a round-trip write-then-read returns the entry;
  the index stays in sync after every write
- depends: #write-obligations

### implement-dream {#implement-dream}
The `dream` subcommand and the detector set, built on the storage layer plus
the repo `MEMORY.md` reader. `--fix` is the conservative structural-only set
on the editable store, refusing the repo store. dream and the MCP
`memory_consolidate` tool share the detector engine. The initial pass
implements the structural detectors precisely (superseded-but-unlinked,
dangling-link, room-touching) and stubs the semantic ones
(stale-state-over-lore, workaround-vs-plan, append-only-violation) with
documented TODOs; the deferred detectors land at #implement-remaining.
- verify: `cargo test` green; `dream <fixture>` emits the expected findings;
  `--fix` refuses a repo-store fixture
- depends: #implement-store

### weed-and-tend {#weed-and-tend}
Run the `weed` skill in check mode to enumerate every spec↔code divergence
(plan/0015: weed catches hand-authored spec drift the implementation passes
clean on; the host-lint spec bug `DetectInternalCodeAsName` flag-vs-warn is
the precedent). Then run the `tend` skill to reconcile each divergence into
one of three buckets: (a) spec over-promises (e.g. the MemoryWrite surface
not needed for dream-only): trim the spec; (b) code under-delivers (e.g.
the deferred detectors): record for #implement-remaining; (c) they agree:
no change. The tended spec is the new baseline; the manifest is rewritten
to match what the post-tend spec + the current Rust surface can discharge.
- verify: the weed check report and the tend reconciliation table are
  recorded in `weed-and-tend.md`; the tended spec parses + analyses clean;
  the trimmed manifest's `--tests src` check passes non-strict with zero
  STALE entries
- depends: #implement-dream

### write-tests {#write-tests}
The test suite against the tended spec. Every `test:` obligation in the
trimmed manifest has a real test fn (no forward refs). Tests for
not-yet-implemented behaviour are marked `#[ignore]` until #implement-remaining
lands them; the ignored set is recorded. The `--fix` safety property has a
Kani harness (the load-bearing pure-function invariants: `route_for`
monotonicity and the `--fix` refusal).
- verify: `cargo test --release` green (modulo the `#[ignore]` set); Kani
  proofs pass; `host-lifecycle obligations <spec> --tests src --strict-discharge`
  clean for the dischargeable subset
- depends: #weed-and-tend

### implement-remaining {#implement-remaining}
Apply the bucket-(b) divergences from #weed-and-tend: the deferred detectors
(stale-state-over-lore, workaround-vs-plan, append-only-violation), the
`MemoryWrite` Rust surface (op/origin/accepted/completed) if tend kept it in
the spec, and any other code-change the reconciliation surfaced. Each
unignored test from #write-tests goes green.
- verify: `cargo test --release` green (no `#[ignore]` remaining); the
  previously-deferred Kani proofs pass
- depends: #write-tests

### extend-mcp {#extend-mcp}
Add `memory_list`, `memory_read`, `memory_write`, `memory_consolidate` tools
to the existing `host-lifecycle mcp` server (shipped v0.39.0 per plan/0065).
Same stdio JSON-RPC pattern; the `tool_defs` registry grows, the dispatch arm
gains the memory tools, the existing `init`/`adopt` tools stay byte-identical.
Built on the implementation that #implement-remaining just landed.
- verify: `cargo test` green; an integration test drives the server over
  stdio and exercises each memory tool; the `init`/`adopt` tools still pass
  their existing tests unchanged
- depends: #implement-remaining

### wire-opencode-plugin {#wire-opencode-plugin}
The opencode configuration entry for the `host-lifecycle mcp` stdio server is
already in place for `init`/`adopt` (plan/0065); plan/0073 confirms it loads
the new memory tools. Verified by listing memories from inside an opencode
session.
- verify: `opencode` lists `memory_list` in the tool registry; a
  `memory_list` call returns the index from inside a session
- depends: #extend-mcp

### write-tests-final {#write-tests-final}
The MCP-touching integration tests: each `memory_*` tool driven over stdio
JSON-RPC, the round-trip `memory_write` -> `memory_list` -> `memory_read`,
and the `memory_consolidate` -> `dream` engine share. This is the final
strict-discharge gate: every `test:` obligation in the manifest, including
the MCP-flavoured ones, points at a real test fn that exercises the cited
entrypoint.
- verify: `cargo test --release` green; `host-lifecycle obligations <spec>
  --tests src --strict-discharge` fully clean; Kani proofs green
- depends: #wire-opencode-plugin

### cast-consult {#cast-consult}
Cast consultation across Mara, Wren, Bly, Orin, Fen on the detector naming,
the `--fix` boundary, the MCP tool surface, and the report format. Recorded
in design-review.md.
- verify: each cast persona's concern addressed or recorded as a follow-up
- depends: #write-tests-final

### adversarial-review {#adversarial-review}
A multi-lens adversarial review with one lens on the duplication risk vs.
plan/0074's envhash, one lens on the auto-detect reversal, and one lens on
the MCP surface. Findings recorded in design-review.md; the re-cut staged
there.
- verify: every blocking finding fixed or recorded; the re-cut executed
- depends: #cast-consult

### write-spine-doctrine {#write-spine-doctrine}
The host-template CLAUDE.md gains the host-* per-user memory store convention,
the append-only asymmetry restated at the per-user level, the `dream` cadence,
and the note that vendor stores are out of scope. An UPGRADING entry keys the
new revision.
- verify: `host-lifecycle upgrade` lists the entry on a pre-revision host;
  `upgrade --record` clears it
- depends: #adversarial-review

### release-and-re-pin {#release-and-re-pin}
`host-lifecycle release host-lifecycle --change-class adds-flag`, re-pin
`.host-software`, record the release receipt, close #16.
- verify: `host-lifecycle software --check .` clean at the new pin; #16
  closed
- depends: #write-spine-doctrine

### fen-acceptance {#fen-acceptance}
The real `qwen3.5-4b` runs `dream` on a constructed fixture with a known
supersession and confirms the finding routes (suggested append vs suggested
edit vs MADR route), not just that a finding exists. Separately, the model
uses the MCP `memory_list` tool through opencode to read memories and confirms
the tool surface is legible at the weak-agent bar.
- verify: Fen routes each finding class correctly; Fen uses the MCP tool
  unaided
- depends: #release-and-re-pin

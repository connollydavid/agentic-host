# plan/0083 lem-memory-recall: long-term memory as vector lookup, with a short map of its territory

- Status: cut 2026-08-21, not started
- Design: [DESIGN-LEM-MEMORY.md](../../DESIGN-LEM-MEMORY.md), the living design document, cast consulted 2026-08-21
- Rulings: the operator adjudications of 2026-08-21 — a new in-tree host-* component; LanceDB embedded; semantic before episodic namespaces; one living design doc; root CLAUDE.md compression descoped to plan/0079

## Why

MEMORY.md has outgrown its founding purpose: the record is past any single read, and a new session can no longer load it to avoid past mistakes. The record is read wholesale or not at all, and the load assumes a strong model and offers no order for the first hour. The design replaces whole-file reading with vector lookup over an embedded store, a knapped territory map as the load order, and Fen-gated acceptance. The append-only log stays the only write authority; every derived surface re-derives from it.

## Build sequence

### The exclusion surface is repaired first {#exclusion-surface}

The scoping task walks through host-lint's exclusion mechanism, and two defects planned in plan/0082 sit on that path. Both land as standalone patches before it: the host-lint#26 fix, where a column-one LEXICON phrase blanks to leading spaces and clears the whole line, and the worktree-hook ignore-list defect, where a relative gitdir strands `.host-lintignore` and the LEXICON outside the tree.

- verify: host-lint#26's own reproduction leaves the surviving match flagging; a worktree hook finds `.host-lintignore` and the LEXICON after `software --materialize`
- depends: none

### Vendor calx-knap {#vendor-calx-knap}

calx-knap enters as a submodule under tools/, external by source after the allium/specula precedent, used as-is and read-only: it is never maintained in this repo, and a change it needs goes upstream, never into the submodule. link-skills.sh gains the shape for its two skill directories; the spec copies to the repo root per the plugin's install contract; the register instruction block lands in CLAUDE.md with this repo's bindings; the calx-knap-gate binary builds in the recorded toolchain.

- verify: both skills link; `calx-knap.md` reads at the root; the gate binary honours the exit contract on the shipped example
- depends: none

### Component scaffold {#component-scaffold}

The new component, named `host-memory` by operator ruling of 2026-08-21, lands under the `.host-software` recipe: bare store, worktree, deps-bundle pin, hermetic musl artifact in the recorded toolchain. The name names the content it serves, not the mechanism. LanceDB's dependency tree is audited against the deps-bundle doctrine before any release.

- verify: `software --check` reads the stanza clean; the artifact re-derives under `software --verify-build`
- depends: vendor-calx-knap

### Embedder boundary {#embedder-boundary}

Qwen3-Embedding-0.6B INT8 ONNX ships pinned behind an arm's-length boundary after the host-reference-ocr pattern, license checked and receipted; last-token pooling runs under the ort crate. Qwen lineage is deliberate: Fen is Qwen-lineage, so the canary and the embedder share a tokenizer family.

- verify: a receipt records the pinned weights and the license check; a fixed probe embeds byte-stable across re-runs
- depends: component-scaffold

### Indexer and query {#indexer-and-query}

`index`, `query`, and `map` commands in the single-command, tool-carried shape Fen demands; hash-gated re-embedding of changed units only; staleness advises, never gates; every hit carries exact pointers back into the log.

- verify: re-indexing an unchanged log embeds nothing; a stale index re-lists rather than falls silent; a garbled query degrades to best-effort hits plus the map
- depends: embedder-boundary

### Semantic pass {#semantic-pass}

MEMORY.md as the first namespace, one unit per entry: the entry format parses cleanly into date, lead, body, line range. Retrieval probes are frozen before compression work, and Fen completes the retrieval loop on the built artifact.

- verify: the frozen probe set passes; Fen finishes a query-to-deep-read loop, single command at a time
- depends: indexer-and-query

### Episodic pass {#episodic-pass}

call/ and plan/ as the second namespace, distinct collection or metadata filter: how the project solved what it solved, so retrieval answers past method alongside static fact.

- verify: a query about a past method returns the milestone record beside the static facts
- depends: semantic-pass

### Territory map {#territory-map}

Generated from the index, longhand first, knapped through the calx-knap corpus loop, gated on Fen, deployed to the session load. The map is the load order and the trigger that says there is something to ask.

- verify: the knapped map passes its probes on Fen; every region slug resolves against the index
- depends: semantic-pass, vendor-calx-knap

### Scope the prose lane {#scope-prose-lane}

host-lint and the prose lane scope off the register, the map, and the index surfaces, using host-lint's own exclusion mechanism; nothing in the register names or configures the tool.

- verify: the prose lane exits zero over the tracked machine-audience surfaces; no human-audience document loses coverage
- depends: exclusion-surface

### Knap the skills {#knap-skills}

The on-demand loaded skills compress into the register, one document at a time, probes frozen first, acceptance measured. Root CLAUDE.md is not in this pass: its compression belongs to plan/0079's render.

- verify: each accepted skill passes its probes on Fen; LOW-YIELD skills keep their originals
- depends: vendor-calx-knap, scope-prose-lane

## Open questions

The map's generation (grown lexicon or index clustering) and its deployed path; distinct collections versus a metadata filter; dream's integration, with index freshness as an audited finding and the per-user tier as a third namespace candidate; the tokenizer lens, since the pinned tiktoken reference over-counts CJK and the embedder and the canary are Qwen-lineage.

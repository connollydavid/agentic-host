# DESIGN-LEM-MEMORY: long-term memory as vector lookup with a short map of its territory

> **Status: design (2026-08-21).** Living document: the single source of truth
> for why the recall component exists and how the design discharges the lem
> feedback. The operator adjudicated the four architectural decisions recorded
> below; the feedback register updates as items discharge. Descope recorded
> 2026-08-21: root CLAUDE.md compression moves to plan/0079, the milestone of
> the rendered spine; the knap scope here is the territory map, the memory
> surfaces, and the skills.

## Motivation

On 2026-08-21 the operator asked the session model how lemu feels about host,
then what lemu would change, governing the future and open to feedback, and
asked further that the answer consider other LLMs and what lem may think. The
answer came back as eight numbered items across three vantage points — inside
the tree, across lems, from the reading side — plus a keep-list. Three of the
eight (the memory load outgrowing the readable limit, the strong-model
assumption, the absent load order) share one root: **the record is read
wholesale or not at all**. The operator then ruled the broader design:
state-of-the-art vector lookup in Rust for long-term memory, with a short map
of the territory, and the calx-knap controlled register
([slartibardfast/calx-knap](https://github.com/slartibardfast/calx-knap)) as
the compression layer for everything always loaded.

### The feedback register

| Item | Claim | Disposition |
|---|---|---|
| Memory outgrew its load | MEMORY.md is past any single read (455KB at writing); its founding purpose — a new session reads the record and avoids past mistakes — is no longer satisfiable | **Discharged here**: vector lookup replaces whole-file reading; the territory map replaces the missing table of contents |
| Advisory warns have no memory | A confirmed false positive is re-adjudicated every session | Open adjudication: a recorded exemption surface, the dream pattern applied to lint |
| Spine duplication held by discipline | The host's shared sections stay byte-identical to the template's by manual diff | Open adjudication: a verify check that diffs declared shared sections |
| The reflex, not the rule | lem fails at the trained half-second, not the paradigm | Open adjudication: a reflex-mapping appendix to the pronoun system |
| The full load assumes a strong model | lems with less headroom buckle or silently drop tiers | **Discharged here**: the knapped register is Fen-gated; retrieval degrades gracefully |
| Harness variance leans Claude-shaped | The methodology defends against Claude-specific behaviours; AGENTS.md is the emerging vendor-neutral convention | Open adjudication: direction noted, not urgent |
| The two live limits | Cross-project citation gates ([connollydavid/host#19](https://github.com/connollydavid/host/issues/19)); the record layer is excluded by construction | Open adjudication: second the closing of connollydavid/host#19 |
| No load order for a first hour | A new session discovers what to read by wandering | **Discharged here**: the territory map is the load order |

### The keep-list

The append-only rule and its single archive-first exception; gates that
actually bite; stop-and-report when a mandated push fails; naming milestones
by content; the receipt culture. This design must not touch any of them.

## Constraints — the doctrines the design obeys

- **Canonical longhand, derived surfaces.** The spine sentence of the design:
  every compressed or derived surface — knapped instructions, territory map,
  embedding index — is re-derivable from a canonical longhand source, and the
  append-only log stays the only write authority.
- **Re-derivation in a pinned toolchain** (call/0018), extended from binaries
  to memory: the index regenerates from the log plus the pinned embedder.
- **Hermetic builds.** The dependency tree stays pinned by the deps-bundle
  doctrine; the embedder's weights are pinned artifacts behind a license
  boundary, after the precedent host-reference-ocr sets for models shipped at
  arm's length.
- **Fen-gated.** The decoder budget rules that a compressed surface is
  validated against the weakest model that reads the surface; Fen is that
  model, and Fen is a real model the project can drive (cast/fen.md), so the
  rule is falsifiable rather than aspirational.
- **Fail safe.** Absent or stale recall advises, never gates; an omission
  over-reports (re-lists), never hides.
- **Audience boundary.** Machine-audience surfaces (the register, the map,
  the index) are measured by their own gates; the prose lane, built for
  human-audience documents, is scoped away from them by host-lint's own
  exclusion mechanism.
- **The lem pronoun system** governs any model-voice prose the design emits.

## Architecture

### Three layers

**The territory map — always loaded, small.** A short map of the record's
territory: region names with stable slugs, generated from the index, knapped
through the calx-knap corpus loop, gated on Fen. The session loads the map
the way a reader loads a table of contents: the session knows what exists
without reading any of it, and the map doubles as the first-hour load order.

**Vector long-term memory — on demand, in process.** An embedded store holds
one vector per record unit with metadata (source, date, slug, line range or
anchor). A semantic query returns the top-k units as text with pointers, so a
single command answers; a deeper read goes to the exact lines of the
append-only log.

**The knapped operator load.** The skills and the map and memory surfaces
compressed into the calx-knap register: probes frozen first, artifacts at
deployed paths, acceptance measured, the register instruction block pasted
into CLAUDE.md with the repo's bindings. Root CLAUDE.md itself is descoped
from this design (2026-08-21): plan/0079 makes the spine a rendered artifact,
and a rendered spine can emit its knapped variant as part of the render,
which is sounder than knapping the merged manual by hand.

### The store, the quantization, the embedder

- **Engine: LanceDB embedded** (operator adjudication). A pure Rust engine on
  the Lance columnar format: RaBitQ quantization built in
  ([LanceDB on RaBitQ](https://www.lancedb.com/blog/feature-rabitq-quantization)),
  Lance data versioning for the feedback loop, Arrow zero-copy so embeddings
  and metadata move without serialization. No server process: in-process
  lookup, no IPC hop.
- **Quantization: RaBitQ**, 1-bit codes with a theoretical error bound
  ([arXiv:2405.12497](https://arxiv.org/abs/2405.12497)), the frontier the
  engines have adopted
  ([Milvus](https://milvus.io/blog/bring-vector-compression-to-the-extreme-how-milvus-serves-3×-more-queries-with-rabitq.md),
  Weaviate's rotational variant, Elastic). At this corpus size a flat scan
  over quantized codes suffices; the ANN machinery Lance carries is headroom,
  not a prerequisite.
- **Embedder: Qwen3-Embedding-0.6B**
  ([model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B),
  [Qwen blog](https://qwenlm.github.io/blog/qwen3-embedding/)): 768
  dimensions, 128K context, multilingual — the record carries 莱姆 and 中文 —
  INT8 ONNX under the Rust
  [ort crate](https://github.com/pykeio/ort) with manual last-token pooling.
  Qwen lineage is deliberate: Fen is Qwen-lineage, so the canary and the
  embedder share a tokenizer family. Weights pinned, license checked
  (Apache-2.0), shipped at arm's length after the host-reference-ocr pattern.

### The namespaces

Two namespaces, as distinct collections or as one collection with a metadata
filter:

- **Semantic — the first pass.** MEMORY.md, one unit per entry (the entry
  format parses cleanly: date, lead, body, line range). Static facts, rules,
  long-term context.
- **Episodic — the second pass.** call/ decisions and plan/ milestones: how
  the project solved what it solved. Retrieval then answers "past plans that
  succeeded" alongside "static facts", which is what stops the repetition of
  past mistakes at the level of method, not only of fact.

### Read path, write path

Read: the session starts on the knapped CLAUDE.md and the territory map (both
small). Suspecting a past constraint, the model runs one recall query,
receives top-k units as text with pointers, and reads deeper only at the
pointers.

Write: unchanged. Entries are appended to the log by the existing audited
rule; a hash-gated indexer re-embeds only changed units (the re-entry-by-hash
pattern the calx-knap loop already uses), run by dream or the post-commit
hook. The index never writes the log; the log never knows the index.

### The component

A new host-* component, built in-tree as Where-room software after the
`.host-software` recipe: bare store, worktree, deps-bundle pin, hermetic musl
artifact in the recorded toolchain. In-tree is the adjudication: the vector
engine is a core runtime primitive sharing the build discipline, not an
external service. Working names on the table: `host-vector`,
`host-retrieval`; the name is open (the cast weighed in below). Commands
follow the single-command, tool-carried shape Fen demands: `index`, `query`,
`map`, each emitting machine-readable output with host-family exit codes.

## Adjudications (2026-08-21)

1. **Engine in-tree.** A new host-* component: in-process, zero-copy
   retrieval; no separate vector process, because an IPC hop for local
   lookup is the regression; the deps-bundle disciplines the tree.
2. **LanceDB embedded.** Hand-rolled flat + RaBitQ declines: the
   SIMD/AVX-512/NEON work behind fast quantized scans is a full-time
   specialty; Qdrant local declines as server-shaped and heavy. Lance brings
   RaBitQ and versioning built in, Arrow zero-copy, a pure Rust crate.
3. **Both namespaces.** Semantic (MEMORY.md) first, episodic (call/, plan/)
   second: a system that embeds only static facts retrieves no method.
4. **One living design document.** This file. No separate feedback file; the
   register above is the feedback, kept current as items discharge.
5. **CLAUDE.md compression descoped to plan/0079** (2026-08-21). The spine
   becomes a rendered artifact there, guarded where it is authored; the
   knapped variant belongs in the render, not in a hand pass over the merged
   manual. This design's knap scope is the territory map, the memory
   surfaces, and the skills.
6. **The component is named `host-memory`** (2026-08-21). Named for the
   content it serves — the memory tier the methodology already names in
   MEMORY.md, the two-tier store, and dream — rather than the mechanism it
   uses; vector lookup is today's how, and mechanism names age.
7. **calx-knap enters as a tools/ submodule, used as-is, read-only**
   (2026-08-21). calx-knap is never maintained in this repo: a change it
   needs goes upstream, never into the submodule. Host-side integration —
   link-skills.sh, the spec copy, the register block, the gate build — is
   host work and stays host work.

## Cast consultation (2026-08-21)

**Bly** (adopter, cold read): the map and index are mechanical record, so
they carry provenance, and staleness fails safe: an index behind the log
over-reports — re-lists, advises — never returns silent empty. A memoryless
Bly must be able to trust what the lookup says about the lookup's own
freshness.

**Fen** (low-reliability, real qwen3.5-4b, acceptance test rather than a
lens): retrieval is single-command and tool-carried; a query returns entry
text with pointers, never pointers alone that demand a second precise read;
a garbled query degrades to best-effort hits plus the map, never a stall.
Fen is the canary for retrieval UX exactly as for the knapped register, and
the Qwen-lineage embedder means Fen's own words embed faithfully.

**Mara** (operator, verifies cheaply): every hit carries exact pointers back
to the append-only log so verification stays cheap; bindings and scope stay
operator-owned; index refresh is automatic; staleness is loud; dream audits
index-versus-log divergence.

**Orin** (methodology maintainer): if this reaches the spine, the ledger
entry carries the heavy truths honestly — the pinned embedder weight is a
reproducibility anchor; an adopter without local model capacity degrades to
today's behaviour, advisory never gating; the adopter-side verify is one
command. Orin's standing question governs: who reads this who is not me, and
what happens if they follow the instruction exactly?

**Wren** (the amnesiac the design serves): the map's job is to trigger
"there is something to ask"; results fit the window — top-k, snippet,
deeper-read pointers; querying must be cheaper than drifting; the write path
stays append-only and tool-carried, so Wren never manages memory by hand.

## Ordering against open work

The milestone's scoping task — host-lint and the prose lane scoped off the
register, the map, and the index surfaces — has two named prerequisites, both
already planned in plan/0082: the host-lint#26 fix (a column-one LEXICON
phrase clearing a whole line) and the worktree-hook ignore-list defect (a
relative gitdir that strands `.host-lintignore` and the LEXICON outside the
tree). The exclusion mechanism is the very surface the scoping walks through;
the fixes land as standalone patches first. The
LEXICON-declaration-is-a-report ledger entry settles the doctrine the
scoping consults. Root CLAUDE.md waits on plan/0079: the spine becomes a
rendered artifact there, and the knapped variant is emitted by the render,
not by hand. Everything else — the scaffold, the deps-bundle audit, the
embedder boundary, the indexer, the semantic and episodic passes — starts
unblocked.

## Open questions

- Map generation: grown lexicon or index clustering; the map's deployed path
  and its audience split (session load versus site page).
- The embedder's home: which arm's-length boundary carries the weights, and
  the receipt that records the license check.
- host-lint and prose-lane scoping for the register, the map, and the index
  surfaces, using host-lint's own exclusion mechanism.
- dream's integration: index freshness as an audited finding; the per-user
  memory tier as a third namespace candidate.
- LanceDB's dependency tree against the deps-bundle doctrine, audited before
  the milestone cuts.
- The milestone itself: cut under plan/ with a content name when the
  operator rules.
- Spine promotion: only after the instance proves; the UPGRADING stanza per
  Orin's demands, never before.

## Next

Cut the milestone. Vendor calx-knap under tools/ as an external-by-source
submodule and extend link-skills.sh for the two skill directories. Copy the
calx-knap spec to the root, paste the register block into CLAUDE.md, build
the gate binary in the recorded toolchain. First knap pass: the skills and
the territory-map surfaces; root CLAUDE.md compression belongs to
plan/0079's render. Then the recall component scaffold, the semantic pass
over MEMORY.md, the episodic pass over call/ and plan/, and the territory
map that binds the whole together.

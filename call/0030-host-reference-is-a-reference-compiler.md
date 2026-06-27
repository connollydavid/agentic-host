# host-reference is a reference compiler: a deterministic normalised layer and a collaborative overlay

- Status: accepted
- Date: 2026-06-27
- Scope: a new instance-only `host-*` component, `host-reference`, embedded as a Where-room
  component (a bare store pinned in `.host-software`). The milestone is `plan/0049`. This is
  instance software and binds no adopter; there is no spine change. Two follow-on decisions are
  carved out: `call/0031` (the untrusted-input threat model) and `call/0032` (the
  engineering-geometry token target).
- Relates: `plan/0049` (the milestone, the open questions, and the weak-agent run in its
  `gather-data.md`); `plan/0039` (the concept-as-URI vocabulary the semantic layer binds to);
  `call/0018` (discharge as re-derivation in a pinned toolchain, which the immutable layer
  reuses); `call/0010` (software as a bare store with worktrees); `plan/0042` (the receipted
  task graph the build runs as).

## Context and Problem Statement

An agentic project applies rigour to what it produces. The build is reproducible, the authored
prose is linted, the specifications are checked. The material it consumes has none of that
treatment. External reference knowledge, the vendor documents and datasheets and schematics an
agent reasons over, enters the context window raw and unpinned. It is heavy in tokens, and
nothing records where it came from. The `reference` memory kind records only a pointer to such material, not its
content. So there is no inbound counterpart to the outbound discipline.

The primary goal is in-context interpretation: let an agent understand external material inside
its context window at low token cost, and act on it and cite it with a provenance trail. The
material arrives in many shapes. The available tools (MarkItDown, Docling, Marker) convert most
shapes to Markdown, but they are best-effort, they are not reproducible, and they carry no
provenance, so their output cannot be attested or traced span by span. They also normalise every
shape to Markdown, which ignores that the token-optimal target depends on the content kind. The
gap that is ours to fill is a normalisation that is reproducible, attested, and provenance-bearing,
the discipline the project already applies to a binary.

## Decision

Adopt `host-reference`, a reference compiler, built on a two-layer model.

- The immutable normalised layer holds the normalised corpus, a semantic skeleton, and a
  content-addressed source map that resolves in both directions. It is re-derived byte for byte
  from the source bytes in a pinned toolchain, so `software --check` and host-prove attest it the
  same way they attest a binary (`call/0018`).
- The mutable overlay layer holds annotations, edits, and agent notes. It is collaborative and
  anchored into the immutable layer by standard selectors, so it survives a re-derivation. It is
  not attested.

Four properties carry the design.

- Semantic normalisation to tokens. Each content kind maps to its token-optimal target, and the
  semantic structure that aids interpretation (headings, reading order, tables, entities, cross
  references) is preserved rather than discarded. The content spine is Markdown, the token-lean
  lingua franca; the semantics ride alongside as a sidecar in JSON-LD, whose `@context` binds to
  the project concept vocabulary of `plan/0039`.
- Deterministic re-derivation and attestation. The immutable layer is a reproducible artifact. Any
  model-based transform is non-reproducible by nature, so it lives in the overlay, behind a single
  provider-agnostic adapter, recorded with its provenance (the source hash, the model identity, the
  prompt). It never enters the attested layer.
- Bidirectional provenance and editing. The source map resolves a span to its origin and an origin
  to its span. Round-trip fidelity is a declared per-kind property, verified as a lens law in the
  property-based lane (full for text and data and markup, approximate for Office and PDF, none for
  the lossy kinds). An editable view writes back where a well-behaved lens exists. A hard-to-edit
  kind such as PDF carries its edits in a standard sidecar (the W3C Web Annotation model, and XFDF
  for PDF) rather than a mutated original.
- Tiered, range-addressable views. A cheap skeleton is always resident; a full slice is fetched on
  demand by page range, section, offset, or token budget, so a large document costs only the slice
  a task needs. Each ingest records the raw token count against the normalised token count, so the saving
  is a measured number.

The format superset is specified once and built one kind at a time, each kind with a conformance
fixture that re-derives byte for byte. The breadth collapses to a small set of shared mechanisms (a
zip reader, a compound-file reader, an XML reader, fixed-layout extraction, optical character
recognition, and the engineering parsers).

Two settled mechanism choices, taken from 2026 practice and the weak-agent run.

- The overlay is a Loro document. It is Rust-native, so a pure-Rust reproducible workspace can use
  it without a second toolchain. Its model is version-controlled by design, and its encoding is compact.
  Automerge is the recorded fallback if a Git-like change-attribution feature is later required.
- Optical character recognition is hybrid. A pinned deterministic engine reads clean scans into the
  immutable layer. The provider-agnostic vision adapter reads diagrams, noisy scans, and handwriting
  into the overlay, recorded with its provenance.

A capability that a normaliser does not declare defaults to the most restrictive setting (no
round-trip, no write-back), so a normaliser that omits a declaration cannot over-claim editability
(the Bly fail-safe rule from the cast review).

## Considered Options

1. **A new instance-only `host-*` component (chosen).** It isolates a genuinely new concern as its
   own bare store, reproducible build, and spec, the same shape as the other components.
2. **A subcommand of `host-lifecycle`.** Rejected: it bolts a large, independent content-transform
   concern onto the generator and gate tool, whose job is generation and gating.
3. **Adopt a state-of-the-art converter as the engine.** Rejected: MarkItDown and Docling are
   best-effort, not reproducible, and carry no provenance, so their output cannot be attested or
   traced, and a single-target-to-Markdown conversion ignores the per-kind token-optimal target.
   They stay useful prior art for the per-kind extractors.
4. **Build model-based semantic compression into the core now.** Rejected: it is not byte
   reproducible, so it would break the one property that lets the corpus be attested. It is kept as
   a later, evolvable overlay layer behind the same provider adapter, recorded with provenance.

## Consequences

- Good: inbound reference material gains the reproducibility and provenance discipline the project
  already applies to its own artifacts; the token saving is measured rather than claimed;
  in-context interpretation is carried by preserved semantic structure; the source map makes a fact
  citable and an edit possible; broad format coverage rides a small set of mechanisms; the
  deterministic line keeps the corpus attestable while the overlay stays free to hold model output
  and collaborative edits.
- Costs: the component is a large Rust workspace, since each format kind is its own normaliser with
  its own fixture; the overlay and the annotation standards add surface; the boundary between the
  deterministic engine and the model adapter must be policed so no model output leaks into the
  attested layer; the parser dependencies must stay licence-compatible with the component licence;
  and two questions are deferred, the untrusted-input threat model (`call/0031`) and the
  engineering-geometry token target (`call/0032`).

## Confirmation

The four agent-facing surfaces (the windowed retrieval selector, the capability declaration, the
content-is-data posture, and the deterministic boundary between the two layers) passed at the
weak-agent bar: the real `qwen3.5-4b` on rope chose the intended option in three of three runs each,
with the option order rotated so the pass reflects content reasoning rather than position
(`plan/0049/gather-data.md`). The cast reviewed the instrument before the run and the results after
it. The component lands as a bare store pinned in `.host-software`, built reproducibly, with its
`.allium` spec, its check, analyse, and plan lanes, and its obligations discharged, its build run as
a receipted task graph (`plan/0042`), and its release carried by `host-lifecycle`. The deferred
decisions `call/0031` and `call/0032` follow.

## Lineage and sources

The per-kind token-target choice rests on the format token-efficiency research: the
[eleven-format table benchmark](https://www.improvingagents.com/blog/best-input-data-format-for-llms/)
(the accuracy-against-tokens trade-off), [TOON](https://arxiv.org/pdf/2603.03306), and
[structured context for file-native agents](https://arxiv.org/pdf/2602.05447). Markdown as the
content spine and JSON-LD as the separated semantic layer follow 2026 practice
([markdown for language models](https://www.searchcans.com/blog/markdown-llm-output-benefits/),
[JSON-LD best practices](https://w3c.github.io/json-ld-bp/)). The overlay choice rests on the
[CRDT comparison](https://www.pkgpulse.com/guides/yjs-vs-automerge-vs-loro-crdt-libraries-2026) and
[Loro](https://github.com/loro-dev/loro). The hybrid recognition posture follows the
[2026 recognition guidance](https://joshua8.ai/ocr-models-vs-vision-llms-vs-tesseract/). The prior
art is [MarkItDown](https://github.com/microsoft/markitdown) and Docling. The bidirectional editing
model is the lens, or bidirectional transformation, tradition, and the sidecar standards are the W3C
Web Annotation model and XFDF.

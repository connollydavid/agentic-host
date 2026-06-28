# plan/0049: external reference corpus

This milestone adds a new component, `host-reference`, that reads external
documentation an agentic project depends on but does not author, and normalises it
into a token-lean form an agent can interpret in context. The material arrives in
many shapes, such as Markdown, HTML, PDF, Office documents, images, structured data,
electronic design files, and mechanical CAD. `host-reference` reads each shape and
produces a normalised representation chosen for low token cost and faithful meaning.

The milestone is in design. This README records the direction and the open questions;
the settled decisions land in `call/0030` and its siblings once the weak-agent probes
and the cast review return. The probe set and its adversarial review live in
`gather-data.md`.

## Why

An agentic project already applies rigour to what it produces. The build is
reproducible, the authored prose is linted, the specifications are checked. The
material it consumes has none of that treatment. External reference knowledge enters
an agent's context raw and unpinned. It is heavy in tokens, and nothing records where it
came from.
The `reference` memory kind records only a pointer to the content. There is no inbound
counterpart to the outbound discipline, and `host-reference` is that counterpart.

The primary goal is in-context interpretation: let an agent understand external
material inside its context window at low token cost, and act on it and cite it with a
provenance trail. Token reduction is the means; correct interpretation is the end. The
impact is measured rather than asserted, since each ingest records the raw token count
against the normalised token count, so the saving is a number a reader can check.

## Direction

`host-reference` is a reference compiler with a two-layer model.

- The immutable normalised layer holds the normalised corpus, a semantic skeleton, and
  a content-addressed source map. It is re-derived from the source bytes in a pinned
  toolchain, so it is reproducible and attestable the same way a binary is.
- The mutable overlay layer holds annotations, edits, and agent notes. It is
  collaborative and anchored into the immutable layer by standard selectors, so it
  survives a re-derivation.

Four properties carry the design:

- Semantic normalisation to tokens. Each content kind maps to its token-optimal
  target, and the semantic structure that aids interpretation (headings, reading
  order, tables, entities, cross references) is preserved rather than discarded.
- Deterministic re-derivation and attestation. The immutable layer is a reproducible
  artifact that `software --check` and host-prove verify.
- Bidirectional provenance and editing. The source map resolves both directions,
  round-trip fidelity is a declared per-kind property, an editable view writes back
  where a well-behaved lens exists, and a hard-to-edit kind such as PDF carries edits
  in a standard sidecar rather than a mutated original.
- Tiered, range-addressable views. A cheap skeleton is always resident; a full slice
  is fetched on demand by page range, section, offset, or token budget, so a large
  document costs only the slice a task needs.

## Format coverage

The specification is closed over the superset of content kinds; the build lands one
kind at a time, each with a conformance fixture that re-derives byte for byte. The
modality families are prose, structured data, office documents, fixed-layout
documents, raster images, vector graphics, electronic mail, electronic design,
engineering geometry, and audio-visual media. Each family holds several kinds. Prose
covers Markdown and HTML and the documentation markups, the TeX family and
reStructuredText and AsciiDoc and Org-mode among them, along with RTF and EPUB and the
manual page. Structured data covers JSON and CSV and YAML and XML, the config and
tabular kinds (TOML, the INI family, JSON Lines, the calendar and contact kinds, the
Jupyter notebook), and the columnar Parquet and Arrow. Electronic design covers the
SPICE netlist alongside KiCad and Gerber and Eagle. Engineering geometry covers
mechanical CAD and the 3D-printing kinds (mesh, the container kinds, the toolpath kind,
and the parametric source kind).

Many kinds share a reader, so the breadth collapses to a small set of mechanisms: a zip
reader for the Office and EPUB and 3D-printing containers, a compound-file reader for
legacy Office and Outlook mail, an XML reader for vector graphics and several design
kinds, fixed-layout extraction, optical character recognition, columnar decoding,
media-container metadata, and the engineering parsers.

Audio-visual media follows the recognition split of `call/0030`. The attested layer
holds what re-derives deterministically, the container metadata such as duration and
codec and stream layout. The transcript and the description are machine-learning
output, so they live in the overlay through the provider-agnostic adapter, the same way
the text inside an image does. The columnar kinds re-derive deterministically and stay
in the attested layer, since a schema and its statistics are a parse rather than an
inference.

The component's remit is external reference material, not code. Source code and the
interface and schema definition kinds, an API description or a protocol schema, are
software; they belong to the *Where* room and the `host-*` tooling rather than to a
reference reader, and they are out of scope here. Archives are out of scope as well,
since a container of arbitrary files is a packaging concern rather than a content kind.
The pluggable model of `call/0033` carries the superset as the menu, and an adopting
project enables the subset its corpus needs.

## Decisions

The design is settled across four records.

- `call/0030` fixes the component shape and these mechanism choices: the overlay is a Loro
  document, recognition is hybrid (a deterministic engine for the attested layer and a
  provider-agnostic vision adapter for the overlay), the semantic layer is a sidecar in JSON-LD
  bound to the `plan/0039` vocabulary, the round-trip law is a per-kind lens law in the
  property-based lane, and an undeclared capability defaults to the most restrictive setting.
- `call/0031` fixes the untrusted-input threat model: ingested material is untrusted, met by
  defensive parsing with hard bounds, a legible untrusted boundary, and a fail-safe recorded
  refusal.
- `call/0032` fixes the engineering-geometry token target, taken to the cast since the summary
  target has no settled industry answer: a deterministic structure-and-metadata summary keyed on
  the model tree, with a parsed-against-computed reproducibility split and an extensible per-format
  default.
- `call/0033` fixes the reader architecture: each format is a pluggable Cargo feature, every reader
  is pure-Rust with no C dependency, the best reader per format is chosen on merit, the dependency
  licences are per plugin with AGPL banned and GPL flagged, and the in-scope set is the adopting
  project's choice.

The canonicalisation rules, the reference tokenizer the token accounting reports against, and the
query surface a running project calls are build-time details settled inside the milestone.

## Readers and dependencies

Each kind binds the best maintained pure-Rust reader, pinned with its version and licence in
[`readers.md`](readers.md), which also carries the licence watch-list and the pure-Rust feature
discipline. Almost every pick is permissive. The GPL `openscad-rs` runs out-of-process under
`call/0033`, which doubles as the first real test of the plugin API, since the OpenSCAD plugin drives
that helper through the same `Normalizer` interface as every in-process reader. The manual page and
TeX and IGES have no pure-Rust library, so they are deferred rather than hand-rolled or bound to a C
library. A `cargo-deny` lane denies AGPL and flags GPL.

## Validation

The agent-facing surfaces are validated at the weak-agent bar before the design locks,
the way plan/0042 and plan/0039 were. The probe set, its adversarial review, and the
recorded run live in `gather-data.md`. A design judgement with no settled answer, such
as the engineering-geometry summary fields, goes to the cast rather than a pass rate.

## Build sequence

The build runs as an anchored task graph (plan/0042): each task carries a receipt in
`.host-task-receipts`, and a downstream task stays pending until its prerequisites carry receipts.
The order lives in the `depends` edges rather than the names. The scaffold and the embed are done.

### Scaffold the workspace {#scaffold-workspace}

Author the Cargo workspace on the pinned toolchain. The `host-reference-core` library carries the
`Normalizer` trait and the two-layer types, and a thin CLI sits over it.

- verify: cd software/host-reference/main && cargo test

### Embed the component {#embed-component}

Create the public repo and push the scaffold. Pin it source-only in `.host-software` and
materialize the bare store and worktree. Record the embed and release receipts.

- depends: #scaffold-workspace
- verify: attested operator

### The text-cheap kinds {#text-cheap-kinds}

Land the text-cheap normalisers that `call/0030` groups under the text and data and XML
mechanisms, each with a conformance fixture that re-derives byte for byte.

- depends: #embed-component
- verify: cd software/host-reference/main && cargo test

### The pluggable foundation {#pluggable-foundation}

Retrofit the text-cheap readers behind Cargo features in the CLI, the text-cheap set on by default
and the heavier readers reserved for their own opt-in features (call/0033). Add the `cargo-deny` lane
that denies AGPL and flags GPL. A build with no features compiles to an empty registry.

- depends: #text-cheap-kinds
- verify: cd software/host-reference/main && cargo test && cargo deny check licenses advisories

### The expanded prose and structured readers {#expand-prose-and-structured-readers}

Land the documentation markups and the extra config and tabular kinds behind their features, each
with a conformance fixture. The prose readers are reStructuredText and AsciiDoc and Org-mode and RTF
and EPUB and BibTeX; the structured readers are TOML and the INI family and JSON Lines and the
calendar and contact kinds and the Jupyter notebook and the columnar Parquet and Arrow. The pins live
in `readers.md`.

- depends: #pluggable-foundation
- verify: cd software/host-reference/main && cargo test

### Office and mail and fixed-layout {#office-mail-fixed-layout}

Land the office and mail normalisers over the shared container readers, and add the born-digital
PDF. Each carries its fixture.

- depends: #pluggable-foundation
- verify: cd software/host-reference/main && cargo test

### Recognition and engineering {#recognition-and-engineering}

Land the recognition path for scanned PDF and image and audio-visual media. Add the EDA layout
normalisers and the engineering geometry of `call/0032`. Each carries its fixture.

- depends: #office-mail-fixed-layout
- verify: cd software/host-reference/main && cargo test

### The overlay {#overlay}

Land the Loro overlay and the write-back path over the W3C Web Annotation selectors, with the
round-trip law proptested per kind.

- depends: #recognition-and-engineering
- verify: cd software/host-reference/main && cargo test

### The spec and the release {#spec-and-release}

Add the `.allium` spec with its lanes and obligations, and wire the CI. Establish the reproducible
build with its deps-bundle, and release through `host-lifecycle`.

- depends: #overlay
- verify: host-lifecycle software --verify-build .

## Status

The design is settled and the build is under way. The scaffold and the embed are done, and so is
the text-cheap-kinds task: its normalisers and conformance fixtures have landed behind the
`host-reference-core` contract and the CLI (prose, structured data, markup, vector, and the SPICE
netlist). The component is pinned source-only in `.host-software`, and `software --check` is green.
The build sequence above is an anchored receipted task graph (plan/0042). The pluggable foundation and
the expanded prose and structured readers have landed, each reader a feature-gated crate, and the
per-kind pins live in `readers.md`; the library-less kinds stay deferred. Office and mail and
fixed-layout have landed (DOCX, PPTX, XLSX over undoc; EML over mail-parser; born-digital PDF over
lopdf and pdf-extract), and so has recognition-and-engineering: the attested deterministic readers of
the recognition split, image and audio-visual container metadata alongside the EDA and
engineering-geometry parsers. The machine-learning half of recognition, OCR and transcription, is
deferred to the overlay node by the `call/0030` split. The ready frontier is now the overlay.

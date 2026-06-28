# plan/0049 reviewer's guide: the external reference corpus

This guide orients a review of the milestone. It says what to read in each repository and what is
worth scrutiny. The milestone's code spans five repositories; review `host-reference` first, since it
is the bulk.

## What the milestone delivers

`host-reference` is a reference compiler. It normalises external documentation that an agentic project
consumes but does not author, turning it into a token-lean, attestable form. It carries a two-layer
model: an immutable attested layer that re-derives deterministically from the source bytes, and a
mutable overlay layer for annotations and edits, anchored into the attested layer by standard
selectors.

The design is settled across the `call/` decisions:

- `call/0030`: the component shape and the immutable-against-overlay split.
- `call/0031`: the untrusted-input threat model (defensive parsing, a recorded refusal).
- `call/0032`: the engineering-geometry token target (a deterministic structure summary).
- `call/0033`: the reader architecture (pluggable by feature, pure-Rust, the licence policy, and the
  out-of-process boundary).
- `call/0034`: OCR as the first out-of-process plugin.

The build ran as an anchored task graph (`README.md` in this folder). Every node carries a receipt in
`.host-task-receipts`, and `readers.md` records the pinned reader for each content kind alongside the
licence watch-list.

## host-reference (released v0.1.1)

The component, a Cargo workspace. `crates/core` holds the contract, `crates/cli` is a thin CLI over the
registered readers, and each reader is its own crate behind a Cargo feature.

The contract lives in `crates/core/src/lib.rs`:

- the `Normalizer` trait, with `modality`, `capabilities`, `detect`, `skeleton`, `view`, and `put`.
- `Caps`, whose `Default` is the most restrictive setting, so an undeclared capability cannot
  over-claim editability.
- the bidirectional `SourceMap`, the `Tier0` skeleton, and the `Tier1` windowed view.

Worth checking here: the fail-safe default, and that `put` refuses unless a reader declares a
well-behaved lens.

The readers are feature-gated crates, each with byte-for-byte conformance fixtures under
`crates/<name>/fixtures/`:

- the text-cheap default set: prose, structured data, config, HTML, vector, and the SPICE netlist.
- opt-in markup and structured kinds: reStructuredText, AsciiDoc, Org, RTF, EPUB, BibTeX, the calendar
  and contact kinds, the Jupyter notebook, Parquet, and Arrow.
- office, mail, and fixed-layout: the office documents through undoc, internet mail through
  mail-parser, and born-digital PDF through lopdf with pdf-extract.
- recognition and engineering: image metadata and EXIF; audio-visual container metadata under a new
  `AudioVisual` modality; the EDA tallies for KiCad, Eagle, and Gerber; and the engineering geometry
  kinds (STL, glTF, DXF, OBJ, PLY, G-code, 3MF, AMF, STEP).
- out-of-process: the `ocr` and `openscad` plugins, which spawn helper binaries reviewed in their own
  repositories.

What to scrutinise:

- Determinism. Each conformance golden is compared byte-for-byte, and the fixtures are static committed
  files, so a golden is independent of the build configuration. Confirm that no reader folds in
  nondeterministic state such as a timestamp, a hash-map iteration order, or a re-encoded container.
- The overlay (`crates/overlay`). It is a Loro CRDT document holding annotations anchored by W3C Web
  Annotation selectors. A `TextQuote` selector re-locates by content, so an annotation survives a
  re-derivation that shifts offsets. The per-kind round-trip lens law (GetPut and PutGet) is proptested
  for the write-back kinds in `crates/overlay/tests/lens_law.rs`.
- The licence lane (`deny.toml`). AGPL is banned and GPL is flagged. Confirm the allow-list matches the
  dependency tree and that no copyleft code reached the permissive crates.
- The specification. `host-reference.allium` distils the Normalizer contract, and
  `host-reference.obligations` dispositions every `allium plan` obligation. The trait rules map to
  named contract tests in `crates/core/tests/contract.rs`; the rules realised outside the trait are
  waived with stated reasons. The CI workflow runs the build, the conformance fixtures, the lens-law
  proptests, clippy, cargo-deny, and the allium lane.

## host-reference-ocr (released v0.1.1)

The out-of-process OCR helper. It carries the `ocrs` engine over the `rten` runtime, with the OCR
models embedded in the binary.

It is a separate program because the models are CC-BY-SA-4.0, a content-copyleft licence. The
permissive `host-reference-ocr` plugin runs this binary at arm's length and reads the recognised text
from stdout, so the plugin and its dependents are an aggregation with the helper rather than a
derivative of it. This is the `call/0033` boundary built for GPL, applied to a content licence, and the
first real exercise of the out-of-process plugin API.

What to scrutinise: the licence confinement (the README states the split upfront and `NOTICE.md`
attributes the models), and that the helper honours the simple contract the plugin expects, an image
path argument in and the recognised text on stdout.

## host-reference-openscad (released v0.1.1)

The out-of-process OpenSCAD helper. It links the GPL-3.0 `openscad-rs` parser, so the binary is GPL. It
prints the kind of each top-level statement, which the permissive `openscad` plugin tallies into the
structure skeleton.

What to scrutinise: that the GPL stays confined, since the helper binary is GPL while `host-reference`
carries no `openscad-rs`, and that the helper repository's `cargo-deny` names `openscad-rs` and the
binary as the flagged GPL exceptions while banning AGPL.

## host-lifecycle (v0.31.2)

Two patches, both to let a workspace component release through the tool-carried sequence, since
host-reference is the first such component:

- `cargo_version` and `set_cargo_version` fall back to `[workspace.package]` when a virtual workspace
  root carries no `[package]` version.
- the lock sync bumps every workspace member that inherits the workspace version, not only the deploy
  crate, so the pinned `--locked` rebuild does not fail on a stale member.

What to scrutinise: the two functions and their unit tests, and that a single-crate component still
releases unchanged, since a root `[package]` wins over `[workspace.package]`.

## agentic-host (the host repository)

The milestone's prose and provenance, rather than code:

- `plan/0049-external-reference-corpus/`: this README task graph, `readers.md`, and `gather-data.md`.
- `call/0034`: the decision that OCR ships out-of-process.
- `.host-software`: the reproducible-build provenance for host-reference and the two helpers, naming
  the toolchain, the build, the artifact digest, and the deps-bundle.
- `.host-task-receipts` and `.host-lifecycle-receipts`: the anchored task receipts and the
  per-component embed and release receipts.

What to scrutinise: that each receipt's evidence matches the work, and that the recorded artifact
digests are the ones `software --verify-build` reproduces.

## Reproducibility and the verification lanes

Every artifact component builds offline in a pinned muslrust container from a vendored deps-bundle, and
re-derives byte-identically. `host-lifecycle software --verify-build` is green across all six artifact
components. The recorded digest is the container build at the `/src` mount path, the reproducibility
anchor; a build at any other path embeds different crate paths and drifts.

## Known deferrals, intentional rather than gaps

- Transcription of audio-visual media: non-deterministic inference, deferred to the overlay's
  provider-agnostic adapter.
- IGES: no pure-Rust reader exists.
- Compressed AMF, the zip variant: the reader refuses it with a clear message, and uncompressed AMF is
  delivered.
- Outlook MSG: skipped, its OLE2 fixture disproportionate for a niche format, and internet mail covers
  the common case.

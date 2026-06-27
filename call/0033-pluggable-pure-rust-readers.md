# host-reference is pluggable and pure-Rust: each format stands up by feature, with the best pure-Rust reader

- Status: accepted
- Date: 2026-06-27
- Scope: the reader architecture and the dependency-licence policy of `host-reference` (`plan/0049`,
  `call/0030`). Instance software, binds no adopter, no spine change. Refines the format-coverage and
  the recognition notes of `call/0030`.
- Relates: `call/0030` (the component and the immutable-against-overlay split); `call/0031`
  (untrusted input and the no-reach-out rule); the reproducible-build production anchor.

## Context and Problem Statement

The format superset spans many readers, and some are heavy (the Office documents, PDF, recognition).
Three constraints shape how they are brought in. The reproducible build is offline and pure-Rust, so
a reader that links a C library (libtesseract through `leptess`, or PDFium) does not fit. A project
rarely needs every format, so the weight of a reader it does not use should not be a cost it pays.
And the dependency licences must stay clear of the strongest copyleft.

A single comprehensive Office reader was evaluated, to avoid the per-format work. `litchi` reads the
whole Office and OpenDocument family in pure Rust, which is attractive. It was deferred for two
reasons. Its embedded objects and images are still in progress, so it cannot extract the images a
slide deck carries, the capability this work needs. And it sits at version 0.0.1, with an API that by
its own note may change without notice. It is worth revisiting once it stabilises and gains
embedded-media extraction.

## Decision

- Pluggable by feature. Each format or family is a normaliser crate, gated by a Cargo feature in the
  consumer. Only the enabled formats compile and register, so a project stands up the readers its
  corpus needs and pays for no others. A heavy reader is an opt-in cost.
- Pure-Rust, with no C dependency. Every reader builds in pure Rust, so the offline reproducible
  build and the no-reach-out rule of `call/0031` hold without a foreign toolchain. The C-linking
  readers are out.
- The best maintained pure-Rust reader per format, chosen on merit rather than weight, since the
  weight is opt-in. The current picks:
  - `calamine` for spreadsheets, both xlsx and the legacy xls.
  - `htmd` for HTML.
  - `mail-parser` for internet mail, with `msg_parser` over `cfb` for Outlook `.msg`.
  - the `zip` and `quick-xml` and `image` crates for the Office documents and their embedded media.
  - `lopdf` with `pdf-extract` for born-digital PDF.
  - `ocrs` over `rten` for optical character recognition.
- Recognition stays in the overlay. A pure-Rust optical-character reader does exist, `ocrs` over the
  `rten` runtime, so recognition need not link C. It is a machine-learning reader, though: it carries
  model weights, vendored for the offline build, and its inference can vary across hosts at the float
  level. So the recognised content (the text inside an image, a description of it) lives in the
  overlay through the provider-agnostic adapter, recorded with its provenance, while the attested
  layer holds only what re-derives deterministically: the image metadata and its alt-text and the
  structure. A pinned model that proves cross-host deterministic could later promote the text into
  the attested layer. This refines the deterministic-recognition note of `call/0030`.
- The in-scope format set is the agent's judgement per project. The methodology carries the superset
  of readers; a project enables the subset it needs.
- Licences are per plugin, and copyleft is bounded. Each plugin's licence is the one its libraries
  carry, so a project reads a plugin's licence before it enables it. AGPL is never allowed, a hard
  rule. GPL is avoided where a permissive reader exists, and any GPL reader is expressly noted, so
  enabling its plugin is a knowing choice. A `cargo-deny` lane enforces the rules: it denies AGPL and
  surfaces GPL. The current readers are all permissive (MIT, Apache-2.0, or Unlicense), so the build
  carries no GPL and no AGPL today; `mail-parser` is Apache-2.0 or MIT, the parser crate rather than
  the AGPL Stalwart server.

## Considered Options

1. **Pluggable, pure-Rust, the best reader per format, permissive licences (chosen).** A project pays
   only for what it stands up, the build stays offline and reproducible, a reader is chosen on merit,
   and the licence stays clear of copyleft.
2. **One comprehensive Office reader, litchi.** Rejected for now: it extracts no embedded media and
   carries a 0.0.1 unstable API. A revisit candidate once it matures.
3. **A fixed, always-compiled reader set.** Rejected: every project would pay the weight of every
   reader, the heavy ones included.
4. **Allow a C-linking reader where it is best (libtesseract, PDFium).** Rejected: it breaks the
   pure-Rust offline reproducible build and the no-reach-out rule.
5. **Allow AGPL or GPL where convenient.** Rejected: AGPL is banned outright, and GPL is avoided and
   flagged, so a plugin's copyleft is never a surprise to the project that enables it.

## Consequences

- Good: a project pays only for the formats it enables; the build stays pure-Rust and reproducible; a
  reader is chosen on merit; recognition stays out of the attested layer; and the licence of each
  plugin is legible and copyleft-bounded.
- Costs: the feature matrix adds build-configuration surface; pptx image extraction is a scoped
  in-house walk (`zip` with the `image` crate), since no pure-Rust library extracts slide media
  today; optical character recognition is machine-learning, so its text is overlay-only until a
  pinned model proves deterministic; and a `cargo-deny` lane has to be carried and kept current.

## Confirmation

The normalisers already built (prose, structured data, HTML, vector, netlist) are retrofitted behind
feature gates, the Office and mail and fixed-layout readers each land behind a feature, and a
`cargo-deny` lane denies AGPL and surfaces GPL. The conformance fixtures and `software --check` stay
green. The operator set the direction this session: pluggable, pure-Rust, the best reader per format,
the agent's judgement on the in-scope set, and copyleft bounded with AGPL banned.

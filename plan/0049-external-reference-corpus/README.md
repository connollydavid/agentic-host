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
an agent's context raw, unpinned, token-heavy, and with no trail back to its source.
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
  document never costs its whole size.

## Format coverage

The specification is closed over the superset of content kinds; the build lands one
kind at a time, each with a conformance fixture that re-derives byte for byte. The
modality families are prose, structured data, office documents, fixed-layout
documents, raster images, vector graphics, electronic mail, electronic design, and
engineering geometry. Many kinds share a reader, so the breadth collapses to a small
set of mechanisms: a zip reader for the Office and 3D-printing containers, a
compound-file reader for legacy Office and Outlook mail, an XML reader for vector
graphics and several design kinds, fixed-layout extraction, optical character
recognition, and the engineering parsers. Engineering geometry covers mechanical CAD
and the 3D-printing kinds (mesh, the container kinds, the toolpath kind, and the
parametric source kind).

## Open questions

The design leaves several questions to settle by data and by the cast before
`call/0030` locks them:

- The overlay data structure for conflict-free collaborative edits.
- The token target for engineering geometry, which has no settled industry answer and
  so leans on the cast.
- The strength of the round-trip law per content kind.
- The boundary for optical character recognition: a deterministic engine for the
  attested layer, with a model-based reader confined to the overlay and recorded with
  its provenance. The model-based reader is provider-agnostic behind one adapter.
- The serialisation of the semantic layer, and how it binds to the concept vocabulary
  of plan/0039.
- The threat model for untrusted input, which is substantial enough to warrant its own
  `call/` decision, since the component's whole job is bringing external material into
  an agent's context.
- The query surface a running project uses to pull a skeleton or a windowed view.
- The canonicalisation rules and the reference tokenizer the token accounting reports
  against.
- The licence compatibility of the parser dependencies with the component's own
  licence.

## Validation

The agent-facing surfaces are validated at the weak-agent bar before the design locks,
the way plan/0042 and plan/0039 were. The probe set, its adversarial review, and the
recorded run live in `gather-data.md`. A design judgement with no settled answer, such
as the engineering-geometry summary fields, goes to the cast rather than a pass rate.

## Status

In design. The probe set is drafted and adversarially reviewed; the recorded run and
the cast review are pending, and the settled decisions follow in `call/0030` and its
siblings.

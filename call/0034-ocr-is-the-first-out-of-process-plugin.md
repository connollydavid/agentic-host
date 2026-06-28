# OCR ships now as the first out-of-process plugin, attested behind an arms-length boundary

- Status: accepted
- Date: 2026-06-28
- Scope: the OCR reader of `host-reference` (`plan/0049`, `call/0030`, `call/0033`). Instance
  software, binds no adopter, no spine change. Refines the recognition-stays-in-overlay clause of
  `call/0033` and the recognition split of `call/0030`.
- Relates: `call/0030` (the immutable-against-overlay split and "a deterministic engine for the
  attested layer"); `call/0033` (pluggable pure-Rust readers, the out-of-process rule, the
  recognition-in-overlay clause, and the pinned-model promotion path); `call/0031` (untrusted input
  and the no-reach-out rule).

## Context and Problem Statement

The recognition-and-engineering wave was directed to deliver image and OCR together. `call/0033` had
parked the recognised text of an image in the overlay until a pinned model proved cross-host
deterministic, and it named the GPL OpenSCAD helper as the first use of the out-of-process rule. Two
facts reshaped the choice for OCR.

The only pure-Rust OCR engine, `ocrs` over the `rten` runtime, carries its model weights as a pair of
`.rten` files licensed CC-BY-SA-4.0. That is a copyleft content licence. The `host-reference`
component is otherwise permissive (Unlicense code, permissive dependencies), and it must not absorb a
ShareAlike obligation into its own distribution as a derivative of the weights.

The engine is also run-to-run deterministic on a host: the helper run twice over the same image with
the same pinned models returns byte-identical text. So the recognised text of a fixed engine over
fixed bytes behaves as a parse, not as the open-ended inference the overlay was built for.

The out-of-process rule of `call/0033`, designed to keep the GPL OpenSCAD code out of the permissive
build, fits the CC-BY-SA models exactly. A separate helper program carries the licence-encumbered
engine and weights, and the permissive plugin runs it at arm's length.

## Decision

- OCR ships now as an attested reader, rather than deferring to the overlay. The recognised text of a
  fixed engine over fixed bytes is the deterministic parse that `call/0030` placed in the attested
  layer, and the vendored pinned models are the pinned model that `call/0033` named as the promotion
  path.
- It is the first out-of-process plugin, ahead of OpenSCAD. The `host-reference-ocr-helper` binary
  embeds `ocrs`, `rten`, and the CC-BY-SA-4.0 ocrs models. The permissive `host-reference-ocr` plugin
  writes the image to a temporary file, runs the helper as a separate process, and reads the
  recognised text from its stdout. The two are an aggregation, not a linkage, so the plugin and its
  dependents stay permissive and the copyleft weights never enter their distribution as a derivative.
  This is the same arms-length boundary `call/0033` specified for GPL, applied to a content licence.
- The plugin implements the same `Normalizer` interface as every in-process reader, which proves the
  interface drives an out-of-process helper with no special case. That is the interface test
  `call/0033` wanted from the OpenSCAD route.
- The helper must be installed. The plugin finds it through `HOST_REFERENCE_OCR_HELPER` or the binary
  name on `PATH`, and returns a recorded refusal when it is absent, which is the cost the `call/0033`
  out-of-process consequence already named.
- Conformance is a byte-for-byte golden over a synthetic text image, the same contract the in-process
  readers carry. Cross-host bit-determinism is not yet proven, so the reproducible-build attestation
  of the recognised text is the open edge, carried by the verification ladder when the
  spec-and-release task lands.

## Consequences

- The CC-BY-SA-4.0 models are confined to the helper and attributed in its `NOTICE.md`. The licence
  watch-list in `readers.md` records the first content-copyleft dependency and its confinement behind
  the boundary.
- A consumer that enables the `ocr` feature must install the helper binary. The default text build
  pays nothing for OCR.
- OpenSCAD remains the planned GPL out-of-process plugin. OCR is the first instance of the pattern and
  validates it before OpenSCAD arrives.

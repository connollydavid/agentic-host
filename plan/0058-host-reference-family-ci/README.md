# plan/0058 host-reference-family-ci: complete the reference family's continuous integration

The host-reference family's CI is incomplete. host-reference itself is red, and its two helpers carry
no CI at all, so a third of the family is unverified by any per-repo lane. This is the only red in the
whole suite, so it is the first of the open-bug milestones.

## The defects

- **host-reference CI is red**
  ([connollydavid/host-reference#2](https://github.com/connollydavid/host-reference/issues/2)): the
  `lint` and `features` jobs fail because the pinned `1.95.0` toolchain is installed without the
  `rustfmt`/`clippy` components (`'cargo-fmt' is not installed`). The `release` job, gated on them, is
  skipped, so a tagged release publishes no binaries. `test`, `allium`, and every `build` job pass, so
  the code is sound and this is a CI-config defect. It predates plan/0057 (v0.1.3 failed the same way).
- **host-reference-ocr and host-reference-openscad carry no CI workflow.** Their reproducibility is
  anchored by agentic-host's `software --verify-build`, yet neither has a per-repo test or build lane,
  so a regression in a helper is caught only downstream.

## Decided direction

- Install the components on the pinned toolchain (`components = ["rustfmt", "clippy"]` in
  `rust-toolchain.toml`, or `rustup component add rustfmt clippy` before the lint and features steps),
  so `lint`, `features`, and `release` go green and the release binaries publish.
- Add a CI workflow to each helper that covers its test and build lanes, in the host-reference shape
  scaled to a single-crate helper.

## Verification

All three repos' CI green on a fresh push, host-reference's release job publishing its artifacts, and
agentic-host's whole-suite verify still green. A host-reference CI-only change carries no binary
change, so it re-pins by the artifact-preserving pin-advance reserved for a pure CI fix (no version
bump); a helper that gains a workflow does the same.

## As-built (complete)

host-reference's toolchain now declares the rustfmt and clippy components, which turned `lint` and
`features` green and un-masked three advisories cargo-deny had never reached under the earlier fmt
failure:

- **quick-xml RUSTSEC-2026-0194 and 0195** (real DoS advisories) are accepted as a scoped, tracked
  ignore in `deny.toml`. They reach the workspace only through the opt-in office and geometry readers
  (`undoc`, `threemf`), never the deployed default-features binary, and the upgrade is blocked upstream
  (`threemf` 0.8.0 is unpatched; bumping `undoc` drags in a still-vulnerable 0.40.1; forcing 0.41
  breaks the API). Tracked in
  [connollydavid/host-reference#3](https://github.com/connollydavid/host-reference/issues/3) until
  upstream lands quick-xml >= 0.41.0 (operator ruling: scoped ignore over a breaking dependency surgery).
- **ttf-parser RUSTSEC-2026-0192** (unmaintained only, no vulnerability, under the opt-in pdf reader) is
  accepted on the same footing as the existing unmaintained advisories.

ocr and openscad each gained a test, lint, and build workflow plus a pinned toolchain; openscad's new
fmt lane fixed one pre-existing formatting diff. All three re-pinned artifact-preserving (openscad's fmt
re-derives byte-identically, verified). The three repos' CI and `software --check` are green.

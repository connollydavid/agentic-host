# call/0044: release immutability on the host family's release repos

- Status: accepted
- Scope: host-lint, host-lifecycle, host-prove, host-reference, host-reference-ocr, host-reference-openscad
- Date: 2026-07-07

## Context and problem

plan/0065's install trust chain single-sources each binary's canonical hash from the public per-component
release receipts. A mutable release host is a moving target: a compromised token (or a maintainer under
pressure) could re-publish a release with a different binary and rewrite the recorded hash to match; the
leaf hash-check then passes against a substitute. The reproducible-build root (call/0018, plan/0005) lets an adopter rebuild
and confirm a hash independent of the host, but the publication channel is only trustworthy if a published
artifact and its receipt cannot be silently swapped after the fact.

## Decision

Enable GitHub release immutability (prevent edit and delete of releases) on the six release-bearing host-*
repos: host-lint, host-lifecycle, host-prove, host-reference, host-reference-ocr, and
host-reference-openscad. The published assets and receipts are frozen at publication; a defective release
is corrected by cutting a new version (host-lint v0.14.0 to v0.14.1, host-reference v0.1.5 to v0.1.6),
never by editing the tag or the release in place. This is the release-host mirror of the methodology's
"the tag is the release" and "history is immutable" discipline, and it covers the deps-bundle releases
(vendor-vN) as well as the binaries.

## Consequences

Good: the install trust chain's single-sourcing is anchored at stable, non-mutable targets, so the
reproducible-build root is defended against a moving-target attack on the publication channel; release
fixes follow the existing new-version discipline; the deps-bundle hashes are frozen too. Bad: a release
cannot be edited in place even when convenient, so every fix is a new version and tag.

This is a project-local decision for the host-* family's GitHub release repos; the methodology itself
stays host-agnostic. Its root is the reproducible build (which an adopter can verify anywhere), and it
leaves the choice of release host and its features to each project. An adopter on a different host uses
that host's immutability if it offers one, or relies on the reproducible-build root alone.

## Relates

plan/0065 (the install trust chain whose single-sourcing this anchors); call/0018 and plan/0005
(reproducible-build re-derivation, the host-agnostic root); the host-lint v0.14.1 and host-reference
v0.1.6 re-releases (the new-version discipline this decision makes mandatory).

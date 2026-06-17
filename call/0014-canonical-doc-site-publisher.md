# The canonical doc-site publisher is `host-lifecycle book`

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-17
- Refines: `call/0011` (worktree-absence coherence; the `src = "."` hazard).

## Context and Problem Statement

The methodology mandates five rooms (Who/What/When/Where/Why/How) and two spec
formats, but shipped **no canonical way to publish them**. `host-template` carried
only a one-line note ("scope `src` to `docs/`"); every adopter therefore hand-rolled
an mdBook generator, and each got the same things wrong. A complete case-(b)
adoption reported it (the `agentic-host` repo issue on doc-site gaps), and four of
its findings reproduce on **this repository's own published site**:

- The Software/Where room — the action the project exists to produce — has no page,
  though `.host-software` carries the data to render a stub.
- Spec bodies (`.allium`/`.tla`) are never published.
- The sidebar is in source-call order, not the five-rooms lifecycle order (Cast,
  the Who, sits near the bottom).
- Nothing asserts a page per room, so a half-room site ships green.

The root cause is singular: a missing, maintained publisher. Worse, this
repository's own `book.toml` set `src = "."` — the exact hazard `call/0011` warned
against — surviving only because CI prunes dangling symlinks and the worktrees are
absent in checkout.

## Decision

Ship one canonical publisher, **`host-lifecycle book`**, and route every adopter
(this repository included) through it instead of a hand-rolled generator.

1. **`src = "docs"`, never `"."`.** `book` writes `book.toml` scoped to a generated
   `docs/`, encapsulating the `call/0011` rule once, centrally — so no adopter
   re-derives it wrong.
2. **Lifecycle order.** `SUMMARY.md` is emitted Cast (Who) → Plan + specs
   (What/When) → Software/Where → Call (Why) → Reference/CLAUDE (How) → Memory.
3. **The Where stub is read from `.host-software`.** Component, url, pin, worktrees,
   and the materialize command — from the committed recipe only, so it is safe in an
   un-materialized checkout (the worktrees themselves are never walked; `call/0011`).
4. **Specs render.** Each spec becomes a fenced code page, navigable from its
   milestone — the What contract is published, not listed as bare filenames.
5. **A coverage gate.** `host-lifecycle book --check` fails the build naming any room
   that has source material but renders no page with content; a room with no source
   (a fresh `call/`, a project with no software yet) is legitimately empty and
   skipped.

`book.toml` and `docs/` are generated output (gitignored), regenerated in CI before
`mdbook build`. The publisher lives in `host-lifecycle` (the token-free generator),
the reference Site workflow and the canonical-order documentation live in
`host-template`, and the upgrade is recorded in the template's `UPGRADING.md` ledger
(requires `host-lifecycle v0.6.1`).

## Consequences

- Good: the four findings stop reproducing on this repository's site, and every
  future adopter inherits one maintained, tested artifact instead of a footgun.
- Good: the `src = "."` contradiction with the template's own guidance is resolved —
  this repository now obeys the rule it published.
- Neutral: the doc site is now a build-time generation step (run the publisher, then
  mdBook) rather than a hand-maintained `SUMMARY.md`.
- Limit: prose pulled in by copy keeps its own relative links; cross-room links
  resolve because `docs/` mirrors the room layout, but a generator change that moves
  a room would need the links revisited. The coverage gate guards room presence, not
  link correctness.

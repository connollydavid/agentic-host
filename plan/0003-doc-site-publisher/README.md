# Canonical doc-site publisher

Status: **built** (`host-lifecycle v0.6.1`, `5738808`; `book` + `book --check`,
tests green, smoke-built on this repo with mdBook). Decision: `call/0014`. Ships the
one canonical mdBook publisher for the five rooms, fixing the doc-site gaps a
case-(b) adoption reported (the `agentic-host` doc-site issue), four of which
reproduced on this repository's own site. Builds on `host-lifecycle` (the token-free
generator, `call/0003`) and the bare-store software model (`call/0010`/`call/0011`).

## Goal

A token-free `host-lifecycle book` that publishes all five rooms in one maintained
artifact, so no adopter hand-rolls a generator that drops a room or sets `src = "."`
(the `call/0011` hazard). Concretely it must: scope `src` to a generated `docs/`;
emit `SUMMARY.md` in lifecycle order (Who, What/When, Where, Why, How, Memory);
render every spec as a fenced page; emit a Where stub parsed from `.host-software`;
and gate room coverage so a half-room site cannot ship green.

## What was built

- **`host-lifecycle book <dir> [--dry-run]`**: writes `book.toml` (`src = "docs"`),
  rebuilds `docs/` (copying room prose, generating spec pages and the Where stub),
  and writes `docs/SUMMARY.md` in lifecycle order.
- **`host-lifecycle book --check <dir>`**: fails (exit 1) naming any room with
  source material that renders no page with content; skips a room with no source.
- The Where stub reads `.host-software` only (name, url, pin, worktrees, materialize
  command), so it renders with no worktree on disk, safe in an un-materialized
  checkout.

Two host-lifecycle tooling fixes filed in the same report rode along in `v0.6.0`:
the explicit `worktree = <dir> <branch> <pin>` recipe form (a parallel line is
reproduced on its own branch at its own pin, not the canonical one), and a
spec-aware `remap` (declared substitutions now reach `.allium`/`.tla`/`.cfg`).

## Invariants (verification lane)

- `SUMMARY.md` part order is exactly Cast, Plan, Software, Call, Reference,
  Memory (unit test).
- `--check` fails when a room with source renders nothing, passes when every such
  room renders a content page, and skips a source-less room (unit test).
- `book.toml` is `src = "docs"`, never `"."` (unit test); `additional-css` only when
  the repo ships `custom.css`.
- A spec body is rendered as a fenced code page whose fence outgrows any backtick run
  in the body (unit test).
- `--dry-run` writes nothing.

## Dogfood

This repository (adopter zero): replace the hand-maintained `SUMMARY.md` and the
`src = "."` `book.toml` with `host-lifecycle book`, re-pin `tools/host-lifecycle` to
`v0.6.1`, re-stamp `.host` to the template revision that introduced the publisher,
and run `book` + `book --check` in the Site workflow before `mdbook build`. Verify
gh-pages redeploys with a Where section and lifecycle-ordered nav.

## Out of scope

- Making the bare-store embedding optional for single-line components (case-study
  friction rather than a filed defect); would need its own decision. **Not pursued**:
  no filed defect, dormant unless a case study forces it.
- Link-correctness checking across rooms (the gate guards room presence, not links).
- Rewriting the reporter's own generator; that is the adopter's, not ours.

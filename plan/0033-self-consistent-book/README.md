# plan/0033: the generated book is correct and obeys the prose-hygiene rule

> **Goal:** close `connollydavid/host#15`. The methodology's own published book has two
> defects. First, `host-lifecycle book` emits a generated home-page link to a room landing
> whose source is `README.md`, and mdBook serves that page at `index.html` while rewriting the
> in-content link to `README.html`, so the link is a 404. Second, the rendered book carries
> em-dashes that the prose-hygiene rule (`plan/0030`) forbids in authored docs: the five
> generated room separators and roughly 113 em-dashes in the spine
> (`host-template/CLAUDE.md` and `STRUCTURE.md`) that every adopter renders in the Reference
> section. Operator ruling: clean fully, so the book obeys the rule the methodology preaches.

## Context

`host#15` was observed building the mdBook for an adopted project. Two findings:

1. **Dead room-landing link.** `host-lifecycle book` generates the home page (`docs/index.md`)
   with a bullet per room linking the room's first page. For a room whose landing file is
   `README.md` (the Cast room is the example), the emitted link is `cast/README.md`. mdBook
   applies its README-to-index rule and serves that page at `cast/index.html`, but it rewrites
   the in-content link to `cast/README.html`, which is never generated. The home page (and the
   aggregated `print.html`) therefore carry a 404. The sidebar nav link works, because mdBook
   maps `SUMMARY` chapter links through the README-to-index rule; only the generated in-content
   link breaks.

2. **The methodology breaks its own prose-hygiene rule.** `plan/0030` shipped a rule: authored
   docs carry zero prose tropes, and a decoration em-dash is a flagged trope. The rendered book
   shows em-dashes anyway, from two tool-controlled sources: the generated nav separators that
   `host-lifecycle book` writes for the five room part-titles, and the spine prose
   (`host-template/CLAUDE.md` and `STRUCTURE.md`) that renders verbatim in every adopter's
   Reference section. `host-lint --prose` flags roughly 96 em-dashes in the spine `CLAUDE.md`
   and 17 in `STRUCTURE.md`, plus a few other tropes (negative parallelism, a false range, a
   decoration arrow, an anaphora run).

## Decision (operator ruling, 2026-06-22)

**Clean fully.** Both tool-generated sources move off the em-dash, and the spine prose is
reworded to `host-lint --prose` clean with meaning preserved. The alternative (an explicit
exemption for the spine and the generated nav) was weighed and rejected: the methodology should
obey the rule it asks every adopter to obey, and the issue itself notes that cleaning is the
fix that makes the methodology consistent.

## Part A: the `host-lifecycle book` generator

Two changes in the `book` generator, with unit tests:

- **Home-page room links resolve.** When the generated home overview links a room landing whose
  destination basename is `README.md`, link the page mdBook actually serves (`<dir>/index.md`,
  which mdBook rewrites to `<dir>/index.html`) rather than `<dir>/README.md`. The `SUMMARY` nav
  links already resolve through mdBook's README-to-index rule and stay as they are.
- **Nav separators carry no em-dash.** The five room part-titles (Cast, Plan, Software, Call,
  Reference) use a colon separator ("Cast: who") in place of the em-dash, so the generated
  sidebar and home overview obey the prose-hygiene rule on every page.

The change alters the generated book output, so it ships as a `host-lifecycle` release (a fix to
the generator). The recorded musl artifact moves, so `.host-software` re-pins and the release
receipt is back-filled.

## Part B: the spine prose

`host-template/CLAUDE.md` and `STRUCTURE.md` are reworded so `host-lint --prose` reports zero on
both. Em-dashes become commas, colons, parentheses, or sentence breaks; the few other flagged
tropes are reworded in place. Meaning is preserved exactly: only flagged punctuation and phrasing
change, and every identifier, version string, citation, and rule stays byte-for-byte. The spine
commit is pushed in `host-template`, then the agentic-host submodule pointer is bumped to it so
the rendered Reference section is clean. This is a prose-only spine revision with no new adopter
action, so it carries no `UPGRADING.md` ledger entry.

## Lifecycle run (software-first)

1. Implement Part A in the `host-lifecycle` worktree, with unit tests; `cargo test` and clippy
   clean.
2. Implement Part B in the `host-template` worktree; verify `host-lint --prose` is zero on both
   files; commit and push `host-template`.
3. `host-lifecycle release host-lifecycle --change-class neither` (a generator fix), run its
   printed commit, push, and tag steps, and collect the new pin and musl artifact hash.
4. One atomic agentic-host commit: re-pin `.host-software` `host-lifecycle`, back-fill the
   release receipt, and bump the `host-template` submodule pointer.
5. Reinstall the gate driver from the released commit.
6. Gate with the released binary: `software --check`, `software --verify-build` (the artifact
   reproduces), `book` then `book --check`, and a direct check that the generated `docs/index.md`
   no longer links a `README.md`, that the generated nav carries no em-dash, and that the
   rendered spine pages are prose-clean.
7. CI rewire: move the agentic-host workflow `host-lifecycle` install pins to the released
   commit.
8. Records: this plan, the `PLAN.md` row, `MEMORY.md`, and a close comment on `host#15`.

## Verification (whole-suite green)

- A `cargo test` case proves the home overview links the served page for a `README.md` landing,
  and a case proves the generated nav part-titles carry no em-dash.
- `host-lint --prose` is zero on `host-template/CLAUDE.md` and `STRUCTURE.md`.
- The regenerated `docs/index.md` contains no `](`-link ending in `README.md`, and the generated
  `docs/SUMMARY.md` part-titles carry no em-dash.
- `software --check`, `software --verify-build`, and `book --check` are green; the producer and
  agentic-host CI runs are green across every repo.

## Records

This plan, the `PLAN.md` row, `MEMORY.md`, and the `host#15` close comment. No `call/` decision is
needed: Part A is a tool bugfix and Part B is a prose-clean of the spine, neither a methodology
decision.

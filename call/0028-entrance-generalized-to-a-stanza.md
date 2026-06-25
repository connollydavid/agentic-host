# The entrance check generalizes to a declared `[entrance]` stanza

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (the `entrance` check: the `[entrance]` stanza parse, the routed
  concept set, the document resolution, the legacy shim) and host-template (the entrance
  doctrine and the adopter `UPGRADING` entry). Adopter-facing. The software change of
  `plan/0043`.
- Relates: `plan/0043` (the milestone, its design review and code review); `call/0026` and
  `call/0027` (the front-door check and the rename this generalizes and completes); `plan/0039`
  (the reconcile arm the entrance is the standalone sibling of); `plan/0040` (the front-door
  check, now generalized).

## Context and Problem Statement

The front-door check (`call/0026`, `plan/0040`) was agentic-host-local and hardwired to one
member's `README.md` marked `entrance = true`. The same self-blindness recurs for any
self-contained document that restates the spine and cannot link to it: a published front door,
a standalone `SKILL.md`, an operator-and-agent landing page. Each restates, and the restatement
stales when the spine moves, with no in-context link to give. The capability had no way for
another document, or another project, to opt in.

## Decision

A project declares one entrance, a global singleton, in an `[entrance]` stanza in
`.host-software`: `member` (the `[software]` member it belongs to, set apart from
`components`), `document` (the file within that member's worktree, default `README.md`, so a
`SKILL.md` or a landing page is reached by path), and `restates` (`true` for every concept, or
a named subset of the closed vocabulary `phases`, `tools`, and the `.host` stamp).
`host-lifecycle entrance --check` then holds the document complete against the declared
concepts: it generates the stamp and covers the rest. The entrance is the standalone sibling of
reconcile, which holds a linkable document with pointers; the entrance holds a self-contained
one with coverage and generation, because it cannot link.

The declaration is a stanza rather than a per-member value, so the marker that sets the entrance
member apart from `components` stays unambiguous and no richer value can demote the front door
into the component set. The spine carries the doctrine and an adopter `UPGRADING` entry
(host-template `ba86125`). The legacy per-member marker (`front-door = true` or `entrance =
true`) is accepted by a deprecation shim, warned, until a later revision retires it (the named
follow-up, the `plan/0039` deprecate-then-retire path).

## Considered Options

1. **Keep the front-door check agentic-host-local (`plan/0040`).** Superseded: the same
   self-blindness recurs for any project with a self-contained document.
2. **A per-member value form (`entrance = phases tools`).** Rejected by the code review: it
   breaks the marker that defines `components` and silently demotes the front door, the
   `call/0027` failure reintroduced.
3. **A dedicated singleton `[entrance]` stanza reaching any document by path (chosen).** The
   marker is unambiguous, the document is not hardwired to `README.md`, and the entrance stays
   the one set-apart entry point.

## Consequences

- Good: any project may declare an entrance and have it held to the spine; the front door is no
  longer hardwired to one `README.md`; the marker-break is designed out; the scope is honest,
  since a document that restates only home-less doctrine declares no checkable concept.
- Costs: the legacy per-member marker is debt, owed a retirement a release later (the named
  follow-up); a partial entrance declared on a real component member is a misuse outside the
  model (the entrance is the single set-apart entry point), a recorded boundary.

## Confirmation

`entrance --check .` is clean on agentic-host's stanza-declared entrance with no deprecation
warning; `reconcile` and `software --check` are green; a malformed stanza is loud in every
consumer (`reconcile` exits `2` on a typo'd member, the entrance exits `2` on an empty
`restates`). The form was settled by a three-reviewer adversarial design review (re-scope
verdict, operator re-cut to expand), a Qwen-3.5-4B run on the declaration form and the stanza
ergonomics, and a three-reviewer adversarial code review that fixed two blocking defects before
release. `cargo test` is green and `cargo clippy` clean. Released as host-lifecycle v0.29.0;
host-template `ba86125` carries the doctrine and the `UPGRADING` entry; agentic-host adopted it.

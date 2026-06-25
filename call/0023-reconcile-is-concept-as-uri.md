# Reconcile is concept-as-URI: project-local facts and three checks

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (`reconcile`, the `.host-software` schema additions, and the
  `manifest --check` hardening). The software implementation of the spine's concept-as-URI
  reconcile doctrine.
- Relates: the spine doctrine in `host-template` (`7be692f`, the reconcile arm; `e4f6207`,
  the `UPGRADING` entry); `plan/0039` (which authored the doctrine and this decision);
  `call/0020` (the host family as Where-room software) and the earlier inline-annotation
  reconcile (`plan/0036`).

## Context and Problem Statement

`plan/0036` shipped the reconcile arm as an inline `<!-- host-reconcile: KIND -->`
annotation: a restatement that had to stay carried a comment the tool checked against the
spine manifest's `[components]`/`[verification]` data. The operator rejected every inline
annotation form on aesthetic grounds (any inline annotation is checker machinery in the
prose), and the manifest data was an agentic-host overfit living in the shared spine.
`plan/0039` evolved the arm to concept-as-URI. This records the software implementation and
its limits.

## Decision

A project's own facts source from its `.host-software`, never the shared spine. The
`components` are the `[software]` members minus a single-file front door (a member marked
`front-door = true`); the `verifiers` are a `[verification] drivers = ...` stanza. The
lifecycle manifest is hardened to phases only: `manifest --check` rejects any stanza that is
not a `[phase "..."]`, so no adopter inherits another project's facts and no overfit creeps
back into the spine.

Each methodology concept (`components`, `verifiers`, `software-root`, `spec-home`) is defined
once at a `{#id}` anchor on a heading (its home) and pointed at with a `[text](FILE#id)`
link. `reconcile` runs three checks over the tracked docs: link-integrity (every concept
link resolves to its home), declared-anchor (the link names a real concept), and coverage
(each project-local home names its full `.host-software` set, so a dropped tool fails by
absence). A home is a heading ending in `{#id}` (mdBook honors no other placement) and its
section runs to the next heading of the same or higher level.

The inline annotation is deprecated: it keeps checking during the transition and is warned,
and the form retires a spine revision later. The cutover is fail-safe, since a surviving
annotation is never silently inert.

## Considered Options

1. **Keep the inline annotation, renamed.** Rejected: every inline form is checker
   machinery sitting in the prose, which the operator rejected on aesthetic grounds.
2. **Generate a `concepts.md` aggregating the definitions.** Rejected: with every definition
   in one authored doc, a page of links back to them is redundant; the tool carries the
   concept vocabulary and the homes are found by their anchors.
3. **Concept-as-URI with project-local facts (chosen).** One canonical definition per
   concept, pointed at; the facts live with the project; the spine stays phases only.

## Consequences

- Good: single-source definitions a weak agent reads through correctly; the spine carries no
  project overfit; project facts are project-local and tool-enforced; validated on stock
  mdBook and the real Qwen-3.5-4B, which authored a home, a stanza, and a pointer migration.
- Costs: coverage guards the home, so an enumeration left un-pointed elsewhere can drift
  unguarded (the author's choice); the weak agent needs the home and stanza forms shown, so
  the doctrine shows them; the inline form lingers one spine revision under
  deprecate-then-retire.

## Confirmation

The host-lifecycle suite passes; `reconcile`, `prose`, and `software --check` are green on
this repository with the released v0.25.0; the real Qwen-3.5-4B authors a concept home (with
the anchor at the heading end), the `[verification]` stanza, and an annotation-to-pointer
migration; adversarial review closed the heading-placement and coverage-section holes before
release.

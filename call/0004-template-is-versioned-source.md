# The template is the canonical, versioned source of the methodology

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-14

## Context and Problem Statement

The methodology is stated in two places: the host's own `CLAUDE.md` (which
governs this meta-repo) and the template's `CLAUDE.md` (the canonical manual
shipped to projects built from the template). They share a spine — the four
working principles, audited plans, append-only memory — and will drift as the
methodology moves. The host also *builds* the template whose methodology it
follows, which makes "where is the single source?" awkward: a template's
`CLAUDE.md` is addressed to an agent working in an *instantiated* project, not in
this host, and an existing exemption already forbids treating the nested template
`CLAUDE.md` as live governance here.

## Considered Options

1. **Diverge** — declare them not-duplicates; sync the shared spine by a
   documented checklist when it changes.
2. **Template canonical, host live-references it** — shrink the host `CLAUDE.md`
   to a pointer at the template's.
3. **Extract a shared spine** both files import.
4. **Copy-at-version** — the template is the source; every project holds a copy
   of the spine at the revision it adopted, recorded in a stamp; upgrading re-runs
   a migration.

## Decision Outcome

Chosen option 4: **the template is the canonical, versioned source; each project
(the host included) holds a copy of the spine at the revision it adopted.**

- **The template authors the spine.** Changes to the methodology land in the
  template `CLAUDE.md` first.
- **Every project carries a copy, pinned to a revision.** A `.host` stamp
  at the repo root records the template revision adopted. The copy is inline and
  acted-on (not a fragile pointer), so governance stays strong locally.
- **The host is adopter zero, not a special case.** It is migrated by the same
  protocol any project uses (decision 0005); the self-referential "compiler
  compiling itself" loop dissolves into ordinary adoption.
- **The exemption stays true.** A project never *obeys* the nested template
  `CLAUDE.md` as live governance; it *copies from it* during a migration event.
  Copy-at-version is single-sourced (the template authors the revision) yet
  drift-managed (re-run the migration to upgrade).

## Consequences

- Good: one source of truth for the spine; upgrades are a defined, mechanical
  diff between two template revisions, not a hand merge.
- Good: the host's existing template-CLAUDE.md exemption is now principled and
  permanent, not a stopgap.
- Cost: the spine text is duplicated into each adopter at adoption time; staleness
  is bounded by whether a project re-runs the upgrade migration, and made visible
  by the recorded revision.
- Deferred: fully reconciling the host's own `CLAUDE.md` wording with the template
  beyond the spine refresh — the broader duplication — is out of scope here.

# The front-door check: cover the spine's structured facts, generate the stamp

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (the `front-door` and `front-door --check` subcommands: phase
  and tool coverage, and `.host` stamp generation). The software change of `plan/0040`.
- Relates: `plan/0040` (the milestone and its two-lens design review); `plan/0039`
  and `call/0023` (the reconcile coverage pattern this reuses for a link-free doc);
  `plan/0038` (the meta-repo precedent: no adopter obligation).

## Context and Problem Statement

The single-file front door (the `.host-software` member marked `front-door = true`)
is a published README in its own repo, outside any host's verify gate. It must stay
self-contained, so it cannot point at the spine with a link the way an in-host doc
does (the reconcile arm); it restates. Every spine move stales the restatement
silently, and the front-door phase list had already dropped the `release` phase.

## Decision

`host-lifecycle front-door [--check]` holds the front door to the spine's structured
facts:

- Coverage of the lifecycle phases against the manifest (each phase named, checked as
  a backtick token, since a bare word like "release" recurs in prose), and of the
  wired tools against the `.host-software` `[verification]` drivers plus the lifecycle
  engine.
- Generation of the `.host` stamp block from the tool's canonical format, checked
  byte-exact.

The check is wired as a step in agentic-host's CI (the reproducible-build job), where
the spine sources are materialized. It is agentic-host-local: a separate step, not the
shared spine recheck, so no adopter without a front door runs it, and no `UPGRADING`
entry is owed.

A two-lens adversarial review rejected the original mechanism (the template carries a
hand-authored fragment per section): a fragment is a second source of truth, so the
check would prove the README matches the fragment and never that the fragment matches
the spine. Generation draws only from the structured data the tool already reads. The
version pins, the lanes rule, and the tool descriptions have no structured home and
stay authored; a structured pin home is a named follow-up.

## Considered Options

1. **Hand-authored template fragments, stitched (the original proposal).** Rejected:
   a second source of truth that relocates the drift rather than removing it.
2. **A drift gate only, with no generation.** Declined by the operator earlier (it
   leaves the restatements in place, against the front-door principle).
3. **Generate from structured data, coverage for the fact-sets, pins de-scoped
   (chosen).** Drift-proof for every fact with a home, and honest about the rest.

## Consequences

- Good: a phase or wired tool dropped from the spine fails the front door by absence,
  and the stamp block cannot be restated wrong; the teaching prose stays authored, so
  the front door still reads as written.
- Costs: the version pins are not drift-proof yet (no structured home); the check runs
  in agentic-host's CI rather than the front-door repo, an asymmetry the design review
  records.

## Confirmation

`front-door --check` is clean on the front door once the `release` phase is named, and
a deliberately staled front door fails it (a drifted stamp block, or a phase named
nowhere). Unit tests cover the coverage and stamp logic. `cargo test` and `cargo
clippy` are green, and the released binary gates green.

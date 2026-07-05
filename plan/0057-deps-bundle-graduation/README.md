# plan/0057 deps-bundle-graduation: a tool-carried ramp out of onboarding, so the drift guard is never dormant behind a green check

This milestone continues the recipe-and-materialisation-hardening lineage (plan/0056): the tool
should fail safe on a degenerate state and present a state that neither git nor a cold reader can
misread. Here the degenerate state is a bundled component that records a `deps-bundle` pin with no
committed producer `deps-bundle.lock`. The tool tolerates it as a green `note`
`(onboarding)` forever, with no action that ever drives it to closure, so the pin-versus-lock drift
guard the methodology advertises sits dormant behind a passing check.

The cast's Fen (the real `qwen3.5-4b`) is the acceptance test.

## Where it came from

The `host` upgrade flow left agentic-host up to date, but `software --check` carried three standing
`(onboarding)` notes: `host-reference`, `host-reference-ocr`, and `host-reference-openscad` declare a
`deps-bundle` yet commit no lock. The operator asked whether to commit those locks. Consulting the
cast reframed the question: the missing locks are the symptom; the defect is that host-lifecycle
ships no way out of onboarding, and reports the owed work as green.

Filed as [connollydavid/host-lifecycle#10](https://github.com/connollydavid/host-lifecycle/issues/10).

## The defect (two facets)

1. **No graduation path.** `embed` names the entry (record the pin) but nothing names the exit
   (commit the lock, arm the guard). Followed literally, `embed` then `software --check` then a green
   result leaves an adopter believing the component is finished while the advertised guarantee is off.
   A later re-point of that component's bundle hash in `.host-software` then passes `--check` clean,
   the exact drift the lock exists to catch.
2. **Verdict-layer under-report.** The onboarding line re-prints every run (over-reports at stdout,
   which is correct), but the exit code is `0`. A cold-read auditor or a CI gate reads the verdict,
   not the prose, so at the verdict layer the owed lock under-reports: the gate says up to date while a
   graduation is owed, and the word `(onboarding)` frames a debt as a stable resting state.

The never-tracked lock staying green is not the defect; plan/0051 decided that correctly, and a
tracked-then-deleted lock is already a HAZARD. The defect is the absent exit and the green verdict
over an owed transition.

## Why it is universal

The shape is a property of the lifecycle contract, not of any component: record a bundle pin, tolerate
the missing lock as green, name no next action, and a bundled component sits in onboarding
indefinitely with the guard dormant. Any adopter who brings a reproducibly-built component under the
methodology in the natural order lands there. The fix belongs in host-lifecycle and the shared docs,
not in a downstream cleanup. The operator's universality call stands (cast unanimous).

## Decided direction (operator ruling: a steady-state ramp, not a migration bolt-on)

The exit is a standing lifecycle operation reachable at any time, not a step wired onto the migration
or upgrade flow. The fix must:

- **Ship a standalone, tool-carried, receipted graduation** (the `software --lock <name>` verb the
  operator later ruled): write the `deps-bundle.lock` from the recorded pin, drive the producer commit
  and the re-pin, and record a receipt. One command a weak agent can run, never a manual git dance.
- **Be reachable late and independently**: order-free, with no unrelated migration or full release
  cascade replayed to reach it. Onboarding is entered at arbitrary times, so its exit is a standing
  operation.
- **Surface onboarding as a distinct, enumerable, owed third state** (the no-hollow-green three-state
  model, plan/0052): a countable owed-list a cold read sees as owed graduations, queryable apart from
  clean, held in the tool's mechanical record rather than a prose note.
- **Be idempotent and self-re-listing**: derive the owed-set from repo state each run (declares a
  `deps-bundle` and has no committed lock), so a truncated partial graduation re-lists the remainder and
  never buries it.
- **Fail loud on mismatch**: one green terminal (lock committed and equal to the pin); refuse a lock
  that disagrees with the pin.

The fix must not: re-color the note into a HAZARD before the graduation ships; couple graduation to an
unrelated migration; silence the note; or mutate state inside `--check` (graduation is a separate,
explicit, receipted action).

## The cast's throughline

Fen is the acceptance test, not a lens: the design is validated by driving the real 4B to graduate a
bundled component in one command, and confirming it fumbles the manual multi-step git form. Four seats
returned the same verdict and shaped the requirements:

- **Orin** (maintainer): the graduation must be a standalone, late-reachable action, not a
  version-keyed migration step; the spine already states the drift guard as if automatic while the tool
  leaves it un-armed. The tool lands first; the three onboarding components are its first customer.
- **Bly** (writes now, reads cold; its own auditor): the exit-code `0` under-reports the owed lock;
  onboarding must read as owed and enumerable, and each graduation must drop a receipt a cold session
  can trust.
- **Mara** (operator, final say): universal and worth a small milestone; the defect is a steady-state
  lifecycle gap that merely surfaces during migration, so build the general ramp. A release-grade path
  would mint no-op version bumps for a byte-identical re-derivation.
- **Wren** (amnesiac executor): the done predicate exists (the `ok` branch) but nothing asserts a
  bundled component must reach it, so there is no goal to loop against; the graduation must be
  idempotent and self-re-listing across a truncated window.

Because this touches tool behaviour the spine relies on, the milestone is gated on a cast review
(`cast/applying-personas.md`) and the Fen probe.

## Open questions

- **Which authority the graduation commit answers to.** Committing the lock advances the producer HEAD,
  and `.host-software` pins a released commit with its re-derived artifact hash (dual-release-authority).
  A release-grade graduation mints a no-op version bump for a byte-identical re-derivation; a lighter
  graduation that re-pins to an untagged commit breaks dual-release-authority. The milestone must decide
  which holds, or whether a bundled-lock commit is a sanctioned exception.
- **Whether the owed third state reuses `next` or extends `software --check`.** The owed-list could
  surface through the existing `next` action or as a new disposition in `--check`; both must avoid the
  gate mutating state.
- **The first-customer cleanup.** agentic-host's three `host-reference*` components graduate through the
  new tool once it ships, not by a hand-rolled release cascade. That cleanup is downstream of the tool,
  not a substitute for it.

## Verification

Ships as one host-lifecycle release, then re-vendor and propagate to consumers, with the whole-suite
verify gate green across host-lifecycle and every consumer and the Fen probe passing on the graduation
flow. The cheap-verification bar (Mara): every bundle-declaring component reads `ok pin matches
deps-bundle.lock`, zero onboarding notes, and a recorded receipt per graduated component, so nothing is
silently owed after the fix.

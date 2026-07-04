# Releasing a tool updates the template's pin of that tool

- Status: accepted
- Date: 2026-07-04
- Scope: the release process for any `host-*` tool that `host-template` pins (today
  host-lifecycle, in the template's `prose.yml` CI install). A durable rule binding this
  project's release sequence: a tool release is incomplete until the template's pin of that
  tool equals the released version. Surfaced as connollydavid/host-lifecycle#9 and folded into
  `plan/0056`. This governs how a release propagates, so it rides with the existing propagate
  rule and is not a spine change.
- Relates: `plan/0056` (the robustness superset that surfaced it); `call/0021` and `plan/0032`
  (re-vendor and propagate to consumers on a tool release); `call/0010` (software as a bare
  store pinned in `.host-software`); the dual-release-authority rule (the producer tag is the
  release, and `.host-software` pins it).

## Context and Problem Statement

`host-template` is the scaffold for new agentic projects and the source of the methodology
spine. Its CI pins the tools it depends on: `prose.yml` installs host-lifecycle at a fixed
revision (`46d481cd`, v0.30.1) so the spine's prose verdict matches every adopter's verify
audit. host-lifecycle has since released through v0.35.1, yet the template's pin was never
bumped. So the template gates its own prose, and hands new adopters, an outdated
host-lifecycle, and the "same host-lifecycle the host gates on" invariant the pin comment
asserts is already false.

The release sequence re-pins `.host-software` and propagates to the consumer components
(`call/0021`), but the template sits outside that consumer set, so its tool pins drift
silently on every release.

## Decision

On every release of a `host-*` tool, updating the template's pin of that tool is part of the
release, carried by the tool so a weak operator never has to remember it:

- The release sequence for a tool the template pins includes a bump of the template's pin
  (the `prose.yml` revision today) to the released version, committed and pushed inside the
  template, then the submodule pointer bumped in the host.
- `host-lifecycle release` prints this as an explicit outward instruction, beside the re-pin
  and re-vendor instructions it already emits.
- A release gate fails when the template still pins an older version of the released tool, so
  the drift is loud rather than silent.
- The invariant is stated positively: the template's pinned tool versions equal the latest
  release of each pinned tool.

## Consequences

- New projects scaffold with current tools, and the template's own gates match what it
  publishes.
- One more instruction per release, mechanized and gated by the release command, so the
  burden lands on the tool and not on the operator.
- The template joins the set of surfaces a release must reconcile, alongside `.host-software`
  and the vendored-dependency bundle.

# plan/0069 release-gate-discharges-obligations: the release discharges the component it releases and prompts every carried pin

## Scope, and what this plan does not fix

This plan closes two release-flow gaps that surfaced when host-lint v0.14.0 shipped with stale obligation
digests: the release gate does not discharge the component it releases, and the release tool prompts the
carried-template pin bump only for host-lifecycle.

It does not guarantee a release ships green. A sibling incident, host-reference v0.1.5 (unformatted code,
`cargo fmt --check` red), is a different lane this plan leaves to a follow-up. And component release-CI
triggers on the tag, so lanes that only run in CI (the multi-platform build matrix, GitHub-hosted kani,
`cargo test`) remain the final gate; a local pre-flight can only catch the lanes it can reproduce locally.

## The incident and root cause

host-lint v0.14.0 shipped with its own CI red on the tag: its release commit bundled feature code that
changed `src/lib.rs` without re-recording the two `DetectReviewCodeAsName` obligation digests, so the
`--strict-discharge` lane failed on the tag. The verify gate's discharge reported STALE, but only after the
release had tagged and pushed. This is the recurring born-red-tag class (plan/0045, plan/0048).

Two gaps in `run_release`:

**Gap 1: the release gate does not discharge the component it releases.** Step 1 runs the manifest verify
phase's `recheck =` (host-template `lifecycle.manifest`), which is `validate plan/ call/ && prose . &&
reconcile .`, a project-level prose-and-drift check. It does not run the obligations check against the
released component's `<spec>.obligations` ledger, so a stale digest or an undispositioned obligation in
that component is invisible at release time. The discharge runs only in the component's own CI, after the
tag.

**Gap 2: the release tool prompts the carried-template pin bump only for host-lifecycle.**
`template_pin_bump_lines` returns the host-template pin-bump steps only when the released component is
host-lifecycle. host-lint is also carried as `host-template/tools/host-lint`, so releasing it leaves the
template pin behind; `software --check`'s call/0038 HAZARD catches it after the fact, but the release flow
does not prompt the operator. The call/0038 rule is spine-resident (host-template `CLAUDE.md`); only the
tool prompt is missing.

## Decided direction

Both gaps close in one host-lifecycle release; both live in `run_release`.

- **Gap 1**: `run_release` gains a component-scoped obligations check as a gate step, after the manifest
  recheck and before the version bump. It runs `host-lifecycle obligations <spec>` (no `--tests`, no
  `--rederive`) for each `.allium` the released component carries; a component with no spec is skipped, the
  way `software --check` already detects lanes. The offline check catches MISSING and STALE dispositions
  and STALE input digests (`staleness_problems` runs whenever `--rederive` is absent, independent of
  `--tests`), which is exactly the born-red class. Test-name resolution and proof re-derivation stay in
  component CI, where the test sources and heavy verifiers live. A non-zero check blocks the release the
  way a red verify recheck already does.
- **Gap 2**: `template_pin_bump_lines` generalizes to every component the carried template pins. It reads
  the template's `.gitmodules` against the recorded pointer (so a partially-initialized submodule is
  handled, not silently skipped) and emits the bump steps for any released component that appears there,
  not only host-lifecycle. No spine change (the rule is spine-resident); the tool catches up to the rule.

## Open design questions

1. **allium-cli dependency.** `obligations` shells out to `allium plan` to derive the obligation set, so
   allium-cli must be on PATH at release time. It is on this host; a fresh-clone release environment must
   install it. host-prove is not needed (the gate runs no `--rederive`). Flag, don't hide.
2. **Hard gate vs staged warn-then-retire.** A release-time gate is not the same as reddening an adopter's
   `software --check`: a release that ships its own component red should block. Proposal: hard gate at
   release, no staging. Operator confirm.

## Build sequence

### Add the component-scoped obligations gate {#add-discharge-gate}
- verify: a fixture whose digest ledger is staled blocks `host-lifecycle release` before the version bump
- inputs: src/main.rs

### Generalize the carried-pin prompt {#generalize-pin-bump}
- verify: releasing a component carried in host-template/tools prints the template bump steps; releasing
  one not carried prints none
- inputs: src/main.rs

### Release and re-pin {#release-and-repin}
- depends: #add-discharge-gate, #generalize-pin-bump
- verify: host-lifecycle released, re-pinned, software --check green, and a stale-digest worktree
  reproduibly blocks release
- attested: operator

## Follow-ups (not this plan)

- **The general release pre-flight.** Step 3 runs only `cargo build --release`; the component's other CI
  lanes (fmt, clippy, test, allium, kani, deny) do not run locally before tagging. `cargo fmt --check` is
  the cheapest and would have caught host-reference v0.1.5; a follow-up could add the cheap local lanes
  (fmt, and clippy where CI runs it) to the release container step. The heavier lanes and the
  multi-platform matrix stay in tag-CI by necessity.

## Verification

A constructed stale-digest worktree blocks `host-lifecycle release <component>` with the same STALE line the
verify gate surfaces, before any version bump or tag. Releasing host-lint prints the host-template
`tools/host-lint` bump steps; releasing host-reference prints none (it is not carried). clippy clean, the
inline suite passes, and the whole-suite verify gate is green.

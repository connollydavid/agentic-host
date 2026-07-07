# plan/0069 release-gate-discharges-obligations: a release must not ship its own component red

## The incident

host-lint v0.14.0 and host-reference v0.1.5 each shipped with their own CI red on the tag they just
pushed. host-lint's release commit bundled feature code that changed `src/lib.rs` without re-recording the
two `DetectReviewCodeAsName` obligation digests, so the `--strict-discharge` lane in host-lint's CI failed
on the tag. host-reference's threemf2 port (plan/0068) shipped unformatted, so its `cargo fmt --check` lane
failed. Each was caught by the `verify` gate's obligations discharge / fmt lane after the release had
already tagged and pushed, not by the release flow itself. host-lint was re-released as v0.14.1 and
host-reference as v0.1.6 to clear them.

This is the recurring born-red-tag class (plan/0045, plan/0048). The verify gate can see the defect; the
release flow cannot.

## Root cause: two gaps in the release flow

**Gap 1: the release gate does not discharge the component it releases.** `run_release` step 1
(host-lifecycle `src/main.rs`) runs the manifest verify phase's `recheck =`
(host-template `lifecycle.manifest`), which is `validate plan/ call/ && prose . && reconcile .`, a
project-level prose-and-drift check. It does not run the obligations discharge against the released
component's `<spec>.obligations` ledger, so a stale digest or an undispositioned obligation in that
component is invisible at release time. The discharge runs only in the component's own CI, after the tag.

**Gap 2: the release tool prompts the carried-template pin bump only for host-lifecycle.**
`template_pin_bump_lines` returns the host-template pin-bump steps only when the released component is
host-lifecycle. host-lint is also carried as `host-template/tools/host-lint`, so releasing it leaves the
template pin behind; `software --check`'s call/0038 HAZARD catches it after the fact, but the release flow
does not prompt the operator. The call/0038 rule is already spine-resident (host-template `CLAUDE.md`,
"the producer re-pins the carried template when it releases the tool"); only the tool prompt is missing.

## Decided direction

Both gaps close in one host-lifecycle release; both live in `run_release`.

- **Gap 1**: `run_release` gains a component-scoped obligations discharge as a gate step, after the
  manifest recheck and before the version bump. It runs the obligations check for each `.allium` the
  released component carries (conditional: a component with no spec is skipped, the way `software --check`
  already detects lanes). A non-zero discharge blocks the release the way a red verify recheck already
  does. The cheap offline signal (staleness + undispositioned) is the right level for a release-time gate;
  the full proof re-derivation (`--rederive`) stays in component CI, where the heavy verifiers live.
- **Gap 2**: `template_pin_bump_lines` generalizes to every component the carried template pins. It reads
  `host-template/.gitmodules` (materialized at release time) and emits the bump steps for any released
  component that appears there, not only host-lifecycle. No spine change (the rule is spine-resident); the
  tool catches up to the rule.

## Open design questions

1. **Test-dir location.** The discharge's `--tests <dir>` resolves `test:` dispositions against a
   directory that is recorded in each component's CI workflow today, not in `.host-software`. The gate
   must locate it per component: a declared field, a convention probe, or a discharge mode that checks
   staleness without test-name resolution. Settle by data before building.
2. **`--tests` vs `--rederive` at release time.** `--tests` catches staleness and undispositioned
   obligations cheaply; `--rederive` re-runs the proofs and needs host-prove plus each verifier on PATH.
   Proposal: the release gate runs the cheap check; `--rederive` stays the component-CI job. Operator call.
3. **allium-cli dependency.** `obligations` shells out to `allium plan`, so allium-cli must be on PATH at
   release time. It is on this host; a fresh-clone release environment must install it. Flag, don't hide.
4. **Hard gate vs staged warn-then-retire.** A release-time gate is not the same as reddening an adopter's
   `software --check`: a release that ships its own component red should block. Proposal: hard gate at
   release, no staging. Operator confirm.

## Build sequence

### Settle the test-dir question by data {#settle-test-dir}
- verify: the chosen mechanism locates each component's test dir across all five specced components
- attested: operator

### Add the component-scoped discharge gate {#add-discharge-gate}
- depends: #settle-test-dir
- verify: a fixture whose digest ledger is staled blocks `host-lifecycle release` before the version bump
- inputs: src/main.rs

### Generalize the carried-pin prompt {#generalize-pin-bump}
- depends: #add-discharge-gate
- verify: releasing a component carried in host-template/tools prints the template bump steps; releasing
  one not carried prints none
- inputs: src/main.rs

### Release and re-pin {#release-and-repin}
- depends: #generalize-pin-bump
- verify: host-lifecycle released, re-pinned, software --check green, and a v0.14.0-style stale-digest
  worktree reproduibly blocks release
- attested: operator

## Verification

A constructed stale-digest worktree blocks `host-lifecycle release <component>` with the same STALE line
the verify gate surfaces, before any version bump or tag. Releasing host-lint prints the host-template
`tools/host-lint` bump steps; releasing host-reference prints none (it is not carried). clippy clean, the
inline suite passes, the whole-suite verify gate is green, and the two incident classes (stale digest,
unprompted carried pin) are reproducibly blocked.

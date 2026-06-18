# Enforcement gate: a spec without its lane is a HAZARD

## Why

`plan/0014` made the verification lanes a conditional MUST in prose; nothing
mechanically failed when a spec shipped without its lane. This gives the MUST
teeth, so it is enforced, not only reviewed.

## What shipped (host-lifecycle v0.10.0)

`software --check` now enforces the lane per materialized component:

- Walk the component worktree (skipping `.git`/`target`/`node_modules`) for
  `.allium` / `.tla` specs.
- A present `.allium` requires a CI workflow (under the worktree's
  `.github/workflows/`) running **`allium check` + `allium analyse`**; a present
  `.tla` requires a **TLC** lane (`tlc2.TLC` / `tla2tools`).
- A present spec with no matching lane is a **HAZARD** (exit 1), alongside the
  existing worktree-symlink hazards. An un-materialized worktree is skipped (the
  specs cannot be seen), like every other `--check` gate.

`find_specs` + `read_workflows` back the check; `spec_lane_problems` reports the
HAZARD count. One test (`spec_lane_gate_requires_a_lane_when_a_spec_is_present`):
no workflow → HAZARD, `check`+`analyse` → clean, add a `.tla` → HAZARD, add TLC →
clean, absent worktree → skipped.

## Verification

- 36 host-lifecycle tests pass; clippy clean.
- Live on this host: `software --check` prints `ok host-lint allium lane present
  (check + analyse)` — host-lint carries `host-lint.allium` and its CI runs the
  lane. `host` carries no spec, so it is silent.

## Scope

The gate enforces lane **presence** (the workflow runs the commands), not that
every `allium plan` obligation is discharged by a named test — that deeper check
(`propagate` coverage) remains review-driven. Presence is the decisive, mechanical
floor that stops a spec shipping as undecorated reference.

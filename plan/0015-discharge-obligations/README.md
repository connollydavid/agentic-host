# Close the obligation loop — use the skills, discharge `allium plan`

## Why

`plan/0014` made the lane a MUST: a `.allium` spec's `allium plan` obligations
**MUST** be discharged by the software's tests, and specs are authored/maintained
**through the skills** (`weed`, `propagate`), not by hand. Neither is true yet —
the specs were hand-written and the proptest suites were never checked against the
derived obligations. This milestone closes that loop, finally using the wired
skills as intended.

## Work (per software component, using the skills)

1. **`allium plan`** each spec to enumerate its obligations (config defaults,
   entity fields, enum comparability, invariants, rule pre/post, transitions).
2. **`weed`** — run the alignment skill to find where the `.allium` spec and the
   implementation have diverged; resolve each divergence (fix the spec via `tend`,
   or note a real code gap).
3. **`propagate`** — generate / map the tests that discharge the `plan`
   obligations; reconcile with the existing `proptest` suite so every obligation
   is covered.
4. **CI** — add an `allium plan` step to each software repo's allium lane so the
   obligations are emitted on every run (the discharge itself is carried by the
   test job).

## Components

- **host-grammar** (`host-grammar.allium` ↔ the `tells` engine + `prose_properties.rs`).
- **host-lint** (`host-lint.allium` ↔ the checker + its verdict lifecycle).

## Verification

- `weed` reports alignment (no unresolved divergence) for each spec.
- Every `allium plan` obligation maps to a test in the component's suite.
- CI runs `check` + `analyse` + `plan`; the test job stays green.

## Note

This is the first milestone authored with the allium skills live (`plan/0014`
wired them). Spec edits go through `tend`, not hand-editing.

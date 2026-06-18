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

## Outcome

- **`weed` ran for real** (first use of the wired skills) and caught a genuine
  spec bug: `host-lint.allium` modelled `DetectInternalCodeAsName` as `flag`, but
  the code (`check_code_label_prefix`) is Tier-3 **Warn** — fixed the spec
  (host-lint `6f94916`). For host-grammar, `weed` confirmed the five modelled
  weights all align with `tells.rs` but the spec was a **partial model**; added
  the missing structural equations `countdown`/`ing-tail`/`false-range`
  (host-grammar `068f3eb`). The lexical-phrase corpus stays an intentional
  abstraction.
- **`allium plan`** wired into both software CI lanes (`check` + `analyse` +
  `plan`), so obligations are emitted on every run.

## Deferred

Full `propagate` test-generation — mechanically mapping every one of the 44+
`allium plan` obligations to a named test — is deferred. The proptest +
integration suites already exercise the behaviour (tell types, severities, exit
codes); a dedicated obligation→test manifest is a follow-on, and the host-lifecycle
enforcement gate (`plan/0016`) is the mechanism that will require it.

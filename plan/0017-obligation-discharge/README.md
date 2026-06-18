# Total obligation discharge, per component

## Why

`plan/0016` enforced lane *presence*; it did not check that `allium plan`'s test
obligations are actually discharged. This closes that — every obligation gets an
explicit disposition, mechanically checked, per component — using the method's own
remap-dictionary discipline.

## What shipped

**host-lifecycle v0.11.x** — `host-lifecycle obligations <spec.allium> [--tests
<dir>]`: runs `allium plan`, then requires a sibling `<spec>.obligations` manifest
to disposition **every** derived obligation:

- `test:<name>` — a named test discharges it (with `--tests`, the name must exist
  in the test sources).
- `structural` — the spec's own `check`/`analyse` lane covers it (field presence,
  enum comparability, surface shape, declared transition graph).
- `waived: <reason>` — an honest, recorded gap.

Fails on any undispositioned obligation, any stale disposition, any absent test.
And `software --check` now HAZARDs a `.allium` with no `.obligations` manifest
(v0.11.1) — discharge is required at the host gate, not just in CI.

**Manifests, per component:**

- `host-lint.obligations` — all **44** obligations: spec-integrity → `structural`;
  the five detection rules and the verdict-lifecycle transitions → named property
  tests in `property_tests.rs` (e.g. `flag_wins_over_warn_on_the_same_line`);
  `StartScan` waived.
- `host-grammar.obligations` — all **39**: structural-equation rules → named PBTs
  in `prose_properties.rs`; `ing-tail`/`false-range` and two negative cases waived
  honestly (no dedicated PBT yet — a follow-on).

**CI:** both software lanes run `host-lifecycle obligations --tests tests`.

## Verification

- `host-lifecycle obligations` exits clean on both specs (44 / 39 dispositioned,
  every `test:` name real).
- `software --check`: `ok host-lint obligations manifest present`.
- 37 host-lifecycle tests pass (`obligation_gaps` unit-tested); clippy clean.

## Honest gap

The waived entries (`ing-tail`, `false-range`, and two negative cases in
host-grammar) are real coverage holes the manifest now makes visible — a dedicated
PBT for each is a follow-on. Waiving with a reason is a valid disposition (like a
`.host-lint-allow` entry); the discipline is that nothing is silently uncovered.

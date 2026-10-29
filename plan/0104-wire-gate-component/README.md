# plan/0104 the wire gate becomes a component: host-voice

**Status: cut 2026-10-29, queued** (operator ruling 2026-10-29, the plan/0089 carries
ruled: the promotion begins as its own milestone, and the lem lane's flag tier is
confirmed in the same breath)

## Why

The wire gate (plan/0091's `lemgate.py`, certified at occurrence below 0.005 with
gate v3) still lives inside plan/0091's directory. A certified instrument that
gates deployments belongs in the component family with a release, a recorded
recipe, and receipts, not in a plan artifact that future sessions must
rediscover. The same ruling confirms the lem lane's tier: **flag, permanently**
(months of commits have run under it; the soak is the evidence, and no review is
scheduled).

## Scope

- The component (proposed name `host-voice`, the alternative `host-gate`
  rejected for colliding with the commit-gate vocabulary): the OpenAI-compatible
  reverse proxy, its scorer and nudge, the DPMO chart, and the probe battery
  harness. Rust is not required by doctrine; the recipe records whatever
  toolchain reproduces it. The name is the operator's to change at the cut
  review.
- The `.host-software` stanza, the release cascade, and the vendored-deps
  question resolved the way host-lifecycle's was.
- The chart's standing surface: the bounded residual plan/0100 owed (no
  credentialed channel exists; nothing simulated) rides the component's own
  records.
- The tier confirmation is recorded here, not built: the lem lane ships as
  flag, no escalation ladder, no scheduled review.

## Build sequence

1. **Port** {#port}: the gate's scorer, nudge, and retry protocol extracted
   verbatim from plan/0091 with the conformance suite green against the
   recorded transcripts.
2. **Recipe and release** {#release}: the `.host-software` stanza, the first
   release cascade, the publish receipt (the lc#30 discipline from day one).
3. **Records** {#records}: PLAN.md row complete, MEMORY entry, plan/0091's
   README points at the component, plan/0089's held-rulings note closed.

## Constraints

Terse writing; credentials never committed (the edge token stays in the
gitignored `.env`); the certification claim is not re-run without a channel; an
unpushed pin halts with a report.

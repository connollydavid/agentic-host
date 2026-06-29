# host-lifecycle's discharge check verifies an `exercises=` link, and verify-build reports only what it checked

- Status: accepted
- Date: 2026-06-30
- Scope: the `host-lifecycle` component (its obligation-discharge check and `software --verify-build`).
  Instance software. The methodology doctrine this realises ("a verification lane that cannot perform
  its check must not report clean") is a separate `host-template` spine change recorded under
  `plan/0052` with an `UPGRADING` entry; this decision binds no adopter except through the tool they
  already run.
- Relates: `plan/0051` (the host-lifecycle review that found the gap), `plan/0052` (the no-hollow-green
  doctrine and this realisation), `call/0018` (discharge is re-derivation in a pinned toolchain, the
  pattern reused here), `call/0042` (the receipted task graph the gate guards).

## Context and Problem Statement

The plan/0051 review found, and the plan/0050 review of `host-reference` had found independently, that
a verification lane can report clean without performing its check. The `obligations` check confirmed
only that a `test:<name>` disposition named a test that exists (a substring match), never that the
named test exercised the rule it discharges. Seven hazarded-verdict obligations in host-lifecycle's own
manifest were dispositioned to `host_root_escape_is_detected`, a pure helper test that never called the
gate, and the ladder stayed green. Separately, `software --verify-build` printed "every non-exempt build
reproduces its recorded artifact" and exited 0 even when no container runtime was present, attesting a
guarantee it never checked. The same two findings are one shape: a lane that does not perform its check
must not report clean.

The deep rungs (`kani`, `apalache`, `tlaps`) already discharge correctly through `--rederive`, which
re-runs the verifier via host-prove and requires a PASS, and which returns `UNPROVEN` when the
re-deriver cannot run. So the fix finishes an uneven application of a pattern the codebase already
trusts rather than inventing one.

## Decision

The obligation-discharge check and the reproducible-build lane are strengthened in host-lifecycle:

- A `test:` disposition gains an optional `exercises=<symbol>` link. The check resolves the named test
  to exactly one `fn <name>` definition (`AMBIGUOUS` otherwise, not a loose substring) and confirms the
  declared symbol appears in that test's body (`HOLLOW` otherwise). A `test:` with no link is
  `UNLINKED`, and an `#[ignore]`'d discharging test is flagged. These are advisory by default and
  HAZARD under `--strict-discharge`, so tightening a shared gate reaches adopters warn-then-retire
  rather than reddening a green ladder on a tool bump (the cast's propagation rule).
- The two relabel escapes are closed in the same change: a behavioural obligation dispositioned
  `structural` is `RELABEL` (the analyse lane does not discharge it), and a `waived:` with no reason is
  `UNWAIVED`. Hardening `test:` without these would only move the hole.
- `software --verify-build` becomes three-state: VERIFIED (rebuilt and matched), DEFERRED or EXEMPT (a
  foreign attest-host or a cited repro-exempt, an honest neutral skip), and UNVERIFIABLE (an in-scope
  build the lane could not run). It prints its clean line only when a build was actually verified and
  none was UNVERIFIABLE, and exits non-zero on an UNVERIFIABLE, with the remedy inline.
- The deeper "the test truly drives the rule" claim is left as an opt-in check; the always-on lane is a
  static link, the test's PASS is established by the project's own suite, and an automatic
  rule-neutralisation flip is deliberately not built because there is no mechanical map from an
  obligation to the code lines that realise it.

## Consequences

- host-lifecycle's own manifest was re-dispositioned: the off-pin and verdict obligations now point at
  `off_pin_worktree_hazards_the_check` (which `software_check` returns its hazard count to make
  testable), and `DetectUnreproducedArtifact` at a new `artifact_reproduces` verdict helper.
  `software --check` runs clean; under `--strict-discharge` the manifest is honest where it was hollow.
- Honest limitation: the link is a token-PRESENCE heuristic, gameable in principle by naming any symbol
  the chosen test happens to contain. It was validated against the real `qwen3.5-4b` (Fen, the
  weak-agent acceptance test): the model authored the correct link unaided and, on a HOLLOW, re-pointed
  honestly and rejected the link-gaming dodge on semantic-mismatch grounds. So the design holds at the
  weak-agent bar, but its robustness rests on the author naming the rule's true observable, plus the
  opt-in exercise check and review, not on a tamper-proof mechanism. This limitation is stated, not
  hidden.

## Alternatives Considered

- Mutation testing or per-rule coverage instrumentation to prove a test drives a rule. Rejected: heavy,
  runtime-dependent, and flaky, which trains a reader to ignore red, the inverse of the hole it would
  close.
- Requiring every `waived:` to cite a `call/` decision. Rejected: a software repo running `obligations`
  has no `call/` directory to cite, and a legitimate no-observable waiver (the lifecycle-entry rule)
  would break. Whether `waived:` needs stronger teeth is left to the probe-informed doctrine.

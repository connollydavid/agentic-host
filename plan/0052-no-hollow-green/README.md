# plan/0052 no-hollow-green: a lane that cannot check must not report clean

This milestone states one doctrine and realises it: **a verification lane that cannot perform its
check must not report clean.** A gate that reports clean without having run its check is worse than
no gate, because it lies to the reader who cannot catch the lie: the cold auditor with no memory of
intent, and the executor that reads the green as a signal to stop.

## Where it came from

The plan/0051 review of host-lifecycle found the doctrine violated in two lanes, and the plan/0050
review of host-reference found the same shape independently. Two independent components showing the
same gap make it methodology-level, not a single component's bug.

- **The obligation-discharge lane.** `host-lifecycle obligations` confirms only that a `test:<name>`
  disposition names a test that exists (a substring check), never that the named test exercises the
  rule it discharges. Seven hazarded-verdict obligations in host-lifecycle's own manifest are
  dispositioned to a test that asserts a pure helper and never drives the gate, and the ladder stays
  green. The same pattern appeared in host-reference, where a hostile-input obligation was waived but
  unrealised with green CI.
- **The reproducible-build lane.** `software --verify-build` skips every build when no container
  runtime is present and then prints "every non-exempt build reproduces its recorded artifact" and
  exits 0, attesting a guarantee it never checked.

The deep rungs (`kani`, `apalache`, `tlaps`) already discharge correctly: the `--rederive` path runs
the verifier through host-prove and requires a PASS, and a missing re-deriver returns UNPROVEN and
exits non-zero (plan/0048). So this milestone finishes an uneven application of a pattern the codebase
already trusts; it does not invent one.

## The cast review

A spine change is gated on a cast review (cast/applying-personas.md). All five personas reviewed both
realisations. The converged verdict:

- **Reuse the rung lane.** Strengthen the `test:` disposition the way the deep rungs already work, not
  with mutation rigs or coverage instrumentation (Mara, Wren: a flaky gate trains the reader to ignore
  red, which is hollow green wearing the opposite mask).
- **Auditable link, not proven behaviour** (Orin). The always-on check verifies a static link: the
  named test resolves to exactly one test and names the rule's observable (its Finding kind or verdict
  transition). The heavier claim, that the test truly drives the rule, is an opt-in tool-applied check,
  and the residue the machine cannot prove is labelled *attested*, never written as if the machine
  proved it. A doctrine sentence the adopter cannot mechanically obey recreates hollow green one level
  up.
- **Three states, not two** (all five). A lane distinguishes verified, legitimately-not-checked-here
  (a declared attest-host or a cited repro-exempt, an honest neutral skip), and could-not-check (a
  HAZARD). Only the third may never be rendered as the first. The verb is "report exactly what you
  established", not "HAZARD whenever you cannot check", so legitimate by-design skips do not turn
  adopter suites into hollow red.
- **Shut the escapes in the same change** (Fen). Hardening `test:` without hardening the `waived:` and
  `structural` dispositions only moves the hole: a weak agent under a hard gate routes around it by
  relabelling. So `waived:` must cite a real `call/` decision (reusing the existing
  `cited_decision_exists` check, which today gates repro-exempt but not waived), and `structural` is
  cross-checked against the analyse lane.
- **Propagation is a breaking change** (Orin, Bly). Tightening a shared gate turns every adopter's
  green `test:` dispositions red the instant they bump the tool, often as a transitive install
  decoupled from the upgrade ledger. So the tightening ships warn-then-retire, keyed at a revision,
  and the reject line self-references its own UPGRADING entry by revision key, with the entry marked
  `independent = true` so it can be applied alone.

The weak agent (Fen, the real qwen3.5-4b) is the acceptance test for the discharge change, not a lens:
the design's weak-agent claim is falsifiable and is to be falsified before the doctrine ships.

## Build sequence

- **#strengthen-discharge.** Replace the substring check with: resolve to exactly one test (else
  AMBIGUOUS) and a static linkage check that the test names the rule's observable. Crisp HOLLOW reject
  that self-references its UPGRADING revision key. Harden the `waived:` and `structural` escapes in the
  same change. Ship as a warning first (deprecate-then-retire).
- **#three-state-verify-build.** Never print the clean guarantee unless at least one in-scope build
  was actually rebuilt and matched. An in-scope build that could not run (no runtime, no pin) is
  UNVERIFIABLE, a distinct token from a real drift, exits non-zero, and carries its remedy inline.
  The declared attest-host and cited repro-exempt skips stay neutral.
- **#exercise-check.** Extend `--rederive` to the `test:` rung: run the named test and require a PASS,
  and as an opt-in heavy check neutralise the rule and require the verdict to flip to FAIL, with the
  neutralisation applied by the tool, never authored by the weak agent.
- **#dogfood-redisposition.** Re-disposition host-lifecycle's own manifest so the strengthened check
  turns its hollow green honest (the plan/0051 findings 3, 4, 5, 10, 17), proving the check bites on
  the dogfood.
- **#probe.** Drive the real qwen3.5-4b against the strengthened gate: can it author passing
  dispositions unaided, and on a red does it author an exercising test or route to mass-waive. This
  gates the doctrine and the release.
- **#spine-doctrine.** Author the doctrine in host-template (the discharge link and the three-state
  reporting rule), with an UPGRADING entry staged warn-then-retire and marked `independent = true`,
  then adopt it into agentic-host through the revision-keyed upgrade ledger (copy-at-version).

## Status

In design. The tool changes land in host-lifecycle and the doctrine lands in host-template; both are
gated on the qwen probe. The plan/0051 component remediation proceeds independently and is not gated
on this milestone.

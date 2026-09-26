# plan/0093 suite-bug-remediation-pattern: seven open bugs, triaged to four classes

Operator-directed: consider the bugs on `connollydavid/host` and the `host-*` suite,
and assemble the triage-to-remediation pattern. This milestone cuts that pattern and
works the live queue through it; the standing zero-open-bugs effort is plan/0082's,
and this plan is its 2026-09-26 recut against the census below.

## The census (2026-09-26)

Seven open issues across the nine-repo suite; none on `connollydavid/host` itself.
`host-prove`, `host-grammar`, and the three `host-reference` repos are clean (the
reference repos restrict issue creation, so their defects ride the family tracker,
which is empty).

| Issue | Filed | Names | Class |
|---|---|---|---|
| [host-lint#29](https://github.com/connollydavid/host-lint/issues/29) | 09-23 | entry-point mode-gate misfires on `..`-prefixed script paths (the regex reads the `./` inside them) | R2, live detection defect, small |
| [host-lint#28](https://github.com/connollydavid/host-lint/issues/28) | 09-23 | skill census double-counts a tool that is both a referenced submodule and an embedded component | R2, live defect, small |
| [host-lifecycle#23](https://github.com/connollydavid/host-lifecycle/issues/23) | 09-22 | a recorded claim's verify runs raw against ambient PATH, so four applied claims HAZARD wherever the tool is not on PATH | R3, lifecycle defect |
| [host-lifecycle#22](https://github.com/connollydavid/host-lifecycle/issues/22) | 09-22 | two ledger verifies grep `CLAUDE.md` for text the spine moved to `AGENTS.md`, so four entries can never be recorded | R3, lifecycle + spine text |
| [host-lifecycle#21](https://github.com/connollydavid/host-lifecycle/issues/21) | 09-19 | a CI lane's outcome is outside every receipt, so a lane can be red from birth and every gate stays green | R4, design (receipt-CI coupling) |
| [host-lint#23](https://github.com/connollydavid/host-lint/issues/23) | July | room-touching precision: cross-check cited records against the applied-receipts set, the owed mechanical half | R4, owed work, deferred by plan/0082 |
| [host-lifecycle#18](https://github.com/connollydavid/host-lifecycle/issues/18) | 07-19 | host-reconcile design handover | R4, deferred to plan/0075 |

Corrections and cross-checks against the plan records:

- plan/0082's census misattributed the room-touching issue to `host-lifecycle#23`;
  it lives on `host-lint#23`. Recorded here, not rewritten into plan/0082 (the
  record layer is append-only).
- The census was taken over the web (`gh` and `curl` were sandbox-blocked at the
  time) and cross-checked three ways: the HTML issue pages, the search API, and the
  plan records' close stories. The cross-check caught the fetch layer serving stale
  cached endpoints that contradicted the live pages (host-lint#29 appeared both
  closed with its pronoun-era title and open with the mode-gate title); the HTML
  pages, the live titles, and the numeric-monotonicity of each repo's issue numbers
  settle the open set as listed. Execution step 0 re-takes the census with `gh` and
  reconciles before any queue work.

## The pattern (triage to close)

- **R1, fixed-but-open**: re-run the repro on the pinned binary; quote the
  evidence; close only after the final push (the close-resolved ritual;
  host-lint#26's pattern, plan/0086).
- **R2, live defect at the detection layer**: pinned-binary repro as a failing
  case; fix at the lowest layer it lives (grammar, then host-lint); spec
  obligations with mutation-killed tests and a corpus regression; the tool-carried
  release sequence (verify gate, bump, recorded-toolchain artifact); re-pin the
  embeds and record the receipts; a ledger entry only if spine-visible; close with
  the transcript.
- **R3, lifecycle or records defect**: reproduce adopter-shaped, never only
  in-tree (a fresh clone, a legacy stamp, a drifted PATH); fix in host-lifecycle,
  spine text through the template; the same release, re-pin, and receipt cascade;
  `software --check` and `software --verify-setup` re-run before closure; close
  with the transcript.
- **R4, design or owed work**: the issue stays open; the remediation is a design
  record reviewed adversarially, and a build milestone is cut only if the design
  survives (plan/0075's precedent). Deferred with a recorded reason.

Invariants across the classes: spine-first where doctrine moves; every release
rebuilds in the recorded toolchain; never push a host commit whose software pin or
submodule pointer is unpushed; nothing closes without quoted, pinned evidence.

## The queue

1. host-lint#29 (R2), then host-lint#28 (R2): the small live defects.
2. host-lifecycle#23 (R3), then host-lifecycle#22 (R3): the adopter-facing
   lifecycle defects.
3. A status check of plan/0082's four carried no-issue findings (call/0057 settled
   the LEXICON-publishes one; the red test suite at the v0.18.1 pin, the worktree
   ignore-list loss, and the release-poisoning residue are verified against their
   claimed fixes).
4. R4 stays open with its reasons restated: #21's receipt-CI design is the natural
   next cut after the live queue drains; lint#23 waits on it (the cross-check
   consumes the receipts set #21 hardens); lifecycle#18 waits on plan/0075.

## Results

Recorded as the queue drains.

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

- The web census below was taken over the network fetch layer (`gh` and `curl`
  were sandbox-blocked at the time) and it is wrong about repository attribution;
  the `gh` census in the next section supersedes it entirely. It is kept as taken,
  because the episode is the lesson: the fetch layer attributed issues to the wrong
  repositories and aged them wrongly, and only the numeric-monotonicity cross-check
  exposed the fabrication.
- Execution step 0 re-took the census with `gh` before any queue work, as this
  section required.

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

## Census corrected (step 0, gh)

The `gh` census supersedes the web table above. Eight open issues across the suite:

| Issue | Filed | Names | Class |
|---|---|---|---|
| [host-lifecycle#29](https://github.com/connollydavid/host-lifecycle/issues/29) | 09-23 | entry-point mode-gate misfires on `..`-prefixed script paths (the regex reads the `./` inside them) | R2, live defect, small |
| [host-lifecycle#28](https://github.com/connollydavid/host-lifecycle/issues/28) | 09-23 | skill census double-counts a tool that is both a referenced submodule and an embedded component | R2, live defect, small |
| [connollydavid/host#23](https://github.com/connollydavid/host/issues/23) | 09-22 | a recorded claim's verify runs raw against ambient PATH, so four applied claims HAZARD wherever the tool is absent from PATH | R3, lifecycle defect |
| [connollydavid/host#22](https://github.com/connollydavid/host/issues/22) | 09-22 | two ledger verifies grep `CLAUDE.md` for text the spine moved to `AGENTS.md`, so four entries can never be recorded | R3, lifecycle + spine text |
| [connollydavid/host#24](https://github.com/connollydavid/host/issues/24) | 09-26 | the worker's front foot: cfg-gated code, comment-only diffs, a typed inventory and a shared index sit outside every lane, so harm lands and a human finds it | triage at queue time (body unread) |
| [connollydavid/host#21](https://github.com/connollydavid/host/issues/21) | 09-19 | a CI lane's outcome is outside every receipt, so a lane can be red from birth and every gate stays green | R4, design (receipt-CI coupling) |
| [connollydavid/host#18](https://github.com/connollydavid/host/issues/18) | 07-19 | host-reconcile design handover | R4, deferred to plan/0075 |
| [host-lifecycle#23](https://github.com/connollydavid/host-lifecycle/issues/23) | 07-22 | room-touching precision: cross-check cited records against the applied-receipts set, the owed mechanical half | R4, owed work, deferred by plan/0082 |

host-lint's tracker is clean. The component defects ride the family tracker
`connollydavid/host`, which is plan/0082's standing condition; plan/0082's original
attribution of the room-touching issue to `host-lifecycle#23` was correct, and this
plan's web-borne correction of it is withdrawn.

## The queue

1. host-lifecycle#29 (R2), then host-lifecycle#28 (R2): the small live defects.
2. connollydavid/host#23 (R3), then connollydavid/host#22 (R3): the adopter-facing
   lifecycle defects.
3. Triage connollydavid/host#24 from its body; a same-day filing carries no plan
   context, so class and disposition settle there.
4. A status check of plan/0082's four carried no-issue findings (call/0057 settled
   the LEXICON-publishes one; the red test suite at the v0.18.1 pin, the worktree
   ignore-list loss, and the release-poisoning residue are verified against their
   claimed fixes).
5. R4 stays open with its reasons restated: #21's receipt-CI design is the natural
   next cut after the live queue drains; lifecycle#23 waits on it (the cross-check
   consumes the receipts set #21 hardens); #18 waits on plan/0075.

## Results

Recorded 2026-09-26, one session. Two releases (v0.54.3, v0.54.4) landed through the
full cascade (verified musl build, tags, re-pin, template `--rev` and submodule pins,
receipts); this host's PATH copy refreshed per the 2026-09-05 lesson.

- **host-lifecycle#29 closed** (dd54db5, v0.54.3): the mode-gate's grep anchors the
  `./` on line start or one non-path character, so a parent-relative invocation
  (`python3 ../scripts/x.py`) and a redundant-member path (`a/./x`) stop reading as
  in-place calls. Regression test
  `entry_point_mode_gate_never_reads_a_parent_relative_path_as_in_place`.
- **host-lifecycle#28 closed** (c41e436, v0.54.3): `skill_sources_checked` keys
  offers by skill name with the embedded copy winning, and the bootstrap linker
  consumes the same list, so link and gate agree by construction. Regression test
  `a_tool_both_submodule_and_embed_offers_its_skills_once`.
- **connollydavid/host#23 closed** (9828c18, v0.54.4): `run_verify` resolves a bare
  `host-lifecycle` token to the running binary, the manifest recheck's rule.
  Measured green under the issue's own stripped-PATH shape; the only remaining
  HAZARDs under it are true ones (the declared rungs' re-deriver genuinely absent
  from that PATH).
- **connollydavid/host#22 closed** (9828c18, v0.54.4, plus host-template 21693d8
  and 88c7319): the record path now applies the rename translation the claim
  recheck applies, which was the defect one site deeper than the proposed remedy;
  `REFS-a-number-resolves`' verify is reworded to `host-template/AGENTS.md`, while
  `LEM-pronoun-system`'s keeps `CLAUDE.md` by design, an adopter meeting that entry
  before the rename entry and the translation covering the renamed tree. Both
  adopter shapes measured recording on v0.54.4 against the tip ledger.

**connollydavid/host#24 triaged R4.** Filed the same day from a bench worker's
seat: five placements where the check exists at a boundary the worker never stands
at (a shared index under fan-out, `#[cfg(kani)]` code no lane compiles, a
comment-only diff that is not byte-neutral, a hand-typed module inventory, and
lanes a worker cannot run, the naming sweep among them). The issue is the design
record and the build is not gated here. Recommended next cut, cheapest contract
first: `software --verify-setup` requiring the commit gate it documents installing;
the naming sweep joining the host's CI lane set; then the cfg-declaration rule, the
`software --artifact-delta` proposal, and the derived inventory; the shared-index
rule is a manual clause before it is a gate.

**plan/0082's carried findings, status-checked.** call/0057 settled
LEXICON-publishes. The v0.18.1 red-suite finding: the named property is unchanged
since introduction, the current pin's suite is held green by the v0.22.0 release
gate, and the draw-dependence stays a watch-item. The worktree ignore-list loss:
fixed at host-lint `e4e03f3` and held live by today's worktree commits gating
correctly. The release-poisoning residue: not reproduced across today's two
releases, both of which staged deps-bundles with `.cargo/config.toml` clean after;
still carried without an issue by operator direction.

**R4 deferrals restated.** connollydavid/host#21 (receipt-CI coupling design) is
the next cut; host-lifecycle#23 (room-touching cross-check) waits on it;
connollydavid/host#18 waits on plan/0075; connollydavid/host#24 joins them as the
freshest design record.

**Process lessons with teeth.** A cross-tracker census is a local-tool job: the web
fetch layer attributed issues to the wrong repositories and aged them wrongly, and
only `gh` settled it, so plan/0093's cut-time census was superseded by step 0
before any queue work. And a submodule checkout can sit detached, where a plain
`git push` refuses and a piped `-q` push hid the refusal: the template's four
commits rode an orphaned head until `rev-parse origin/main` caught it, and the
cascade's push step now ends with that read-back.

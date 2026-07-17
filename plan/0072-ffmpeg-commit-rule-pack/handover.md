# plan/0072 handover — adversarial-review outcome and the staged re-cut

Written 2026-07-17, after the adversarial review of this milestone's README completed and
before the re-cut it mandates. This document is the transferable session state: a fresh
session on any host, given this folder and the linked GitHub records, can execute the
re-cut without the originating machine. It is superseded once `design-review.md` and the
re-cut README land; it is then history, not instruction.

## Committed state

- `2a6a93eb` — cut plan/0072-ffmpeg-commit-rule-pack (README + PLAN.md row). Pushed.
- `929aaacf` — MEMORY.md entry (the cut; the fork-SHA pin lesson; the Anubis
  user-agent-gating lesson). Pushed.
- The public-signals addendum is posted on the design record:
  <https://github.com/connollydavid/host-lint/issues/22#issuecomment-5004216593>.
- `signals-digest.md` (this folder) is the verified research digest backing that addendum.
- `review-findings.json` (this folder) is the adversarial review's full result:
  `{held, survivors, refuted, critic}`. 29 survivors — 2 blocker, 8 major, 13 minor,
  6 advisory — and 1 refuted finding. Each survivor carries id, severity, verdict
  (`confirmed` | `partly-wrong`), kind, lenses, claim / corrected_claim, remedy, and an
  optional severity_adjust. Use `corrected_claim` where present; respect the
  severity_adjust demotions (`bare-issue-refs-after-first-link` and
  `long-lead-operator-provisioning-sequenced-last` both demote to advisory). The
  `critic` slot is null — the workflow's critic agent returned nothing — and the inline
  critique below replaces it.

Review shape, for the record: six attack lenses (graph-soundness,
design-record-completeness, tier-honesty-and-verifiability, factual-grounding,
methodology-conformance, consumer-adoption) plus six author-flagged candidates, merged
and deduplicated, one adversarial skeptic per finding, ~38 agents. All six author
candidates were confirmed in some form (two escalated to blocker); 23 of the 29
survivors were independently discovered.

## The two blockers

1. `core-fix-release-seam-breached-and-landed-state-unrecorded` — host-lint main already
   carries the core fail-closed fix plus engine-surface, pack-dispatch, workspace-split,
   and fixture-licensing past v0.14.2 (cited: commits e46880c1 and 3faa4c0b after the
   pin commit 241a870b; main head cited as 28b1fd59). The skeptic reports this
   API-confirmed, but it has NOT been independently re-verified in-session — verify
   first (compare 241a870b...main on connollydavid/host-lint) before folding. If true,
   it changes core-fix-release's shape (change-class `neither` becomes wrong for a
   main-head release; either release main as a feature or cut a fix-only release from a
   branch at the fix commit) and forecloses open decision one (the workspace is already
   split, so pack residence is decided).
2. `tier-freeze-precedes-most-mechanical-rules` — corpus-calibration freezes tiers
   before the series, mail, forge, and cosmetic mechanical rules exist. Remedy: move or
   duplicate the calibration gate after series-lane, add cosmetic-separation to its
   depends, give mail/forge rules explicit uncalibratable-tier annotations, and bind
   the freeze test to a digest of the calibrated rule set. Composition hazard: series-lane
   currently depends ON corpus-calibration, so the remedy inverts an edge — re-derive
   the whole graph (critic gap one below).

## Inline coverage critic

Replaces the null critic slot; must be recorded in `design-review.md`.

1. **Remedy composition unverified.** The skeptics verified the 29 findings
   individually; nobody verified the remedies compose. Applying them all reshapes the
   graph: calibration moves after series-lane while series-lane's stated depends include
   corpus-calibration (edge inversion, cycle risk); hook-installer gains pack-dispatch;
   checklist-reporter and spec-obligations gain mail-lane and forge-lane;
   docs-and-release's "everything above" becomes an enumerated list. After folding,
   re-derive the dependency graph and re-check acyclicity, reachability, and that every
   verify is executable at its position; record that re-check in `design-review.md`.
2. **Blocker one's repo-state evidence is second-hand.** One direct compare call
   settles it; run it before the re-cut.
3. **The re-cut's new material ships unreviewed.** The review ran against the committed
   README; the delegated tier, the Fairies pinned-submodule sourcing, and the
   delegated-llm-review task were never attacked by any lens. Unexamined surfaces:
   prompt-injection and gaming of a delegated model reviewing hostile diff content;
   non-reproducible model verdicts versus the receipt discipline (both mitigated by
   advisory-only framing, which the re-cut must state explicitly); the GPL-2 gitlink
   boundary mechanics. Either run a targeted skeptic pass over just those sections after
   folding, or mark them review-pending in `design-review.md`.
4. **Digest-layering residual risk (note only).** Several lenses verified README claims
   against the digest rather than primary sources. The layering caught one divergence
   (the security-page change count); thin-sample facts (verbatim landings verified over
   three pull requests) carry residual risk. No action beyond the survivors filed.
5. **The review's own receipt was hollow.** The workflow critic returned null; this
   inline critique replaces it, and `design-review.md` must say so — no-hollow-green
   applies to the review record itself.
6. **Bounded non-gaps.** Held claims are unaudited by design, with false-negative risk
   bounded by six-lens overlap; author-candidate anchoring is bounded by the 23
   independently discovered survivors. No action.

## Next actions, in order

The operator approved proceeding. One re-cut commit, then a separate MEMORY commit.

1. Verify blocker one's repo-state claim directly against connollydavid/host-lint.
2. Re-cut this folder's README in one pass, folding: (a) all 29 survivors' remedies,
   (b) the four-tier delegation doctrine and rule moves below, (c) the Fairies
   pinned-submodule sourcing below. Then re-derive and re-check the task graph.
3. Write `design-review.md` (the house pattern of the review issue): method, survivors
   table by severity with dispositions, the refuted finding
   (`corpus-freshness-verify-not-offline-runnable`), and the inline critic above.
4. Update the PLAN.md row status if its wording changes.
5. Lint every changed file (`host-lint <file>`; hooks may be absent on a fresh clone,
   so lint manually; a warn is advisory — confirm the token is a genuine
   version/identifier, then proceed). Commit README + design-review.md (+ PLAN.md if
   touched) together and push immediately (the audited-plans rule).
6. Post one addendum comment on the design record
   ([host-lint#22](https://github.com/connollydavid/host-lint/issues/22)): the
   delegation doctrine, the Fairies submodule decision, and the review outcome with a
   pointer to `design-review.md`. Lint the body.
7. MEMORY.md entry (separate commit, push): review outcome, the seam-breach lesson once
   verified, the tier-freeze-ordering lesson, and the critic-null note.

## The delegation doctrine to fold (operator directive)

Maximize model delegation; encode as tools anything black-and-white or without
variability. The tier rule: if two competent runs must agree, it is a tool (mechanical
or expensive); if they may reasonably differ, it is `delegated` — a new tier: a model
call with a rubric, a structured verdict, a receipt, advisory-only, unrun never passed;
if it certifies responsibility, it is human-attested — a model may assist, never
discharge.

- The tier enum becomes `mechanical | expensive | delegated | attested`. Delegated
  registry entries carry a rubric (prompt fragment), an output schema, and receipt
  requirements. Calibration extends to delegated rules (rubric refinement before the
  freeze). Checklist verdict kinds: checked, receipted, model-advised, attested.
- Moves to delegated: why-present quality; the vague close-variants judgment (killed at
  mechanical tier by the review — this is its right home); atomic-scope and the
  backport-fix split; resubmit discipline (comparing versions and the review thread);
  doc-updated adequacy; the security classification (the model proposes
  exploitable / non-exploitable-UB / normal, the human decides, the routing is then
  mechanical — this also discharges the survivor
  `security-routing-classifier-untiered-and-unenforceable`); the AI-verbosity
  pre-screen (assist only).
- Hardened to tools from pinned Fairy facts: sample minimality (the documented size
  thresholds), the tests/ref no-hardcoded-expected rule with its CMP=grep exception,
  and the AVOption name-equals-value tell (already mechanical).
- Human-only, never delegated: DCO sign-off; the entire security path; the final
  line-by-line review of agent-drafted code; list subscription; benchmark
  responsibility; post-land FATE monitoring.
- Delegated-lane infrastructure: a new task `delegated-llm-review` (depends:
  build-receipts, project-pack-config — re-derive with the new graph). Harness seams:
  `claude -p --output-format json --json-schema <schema>` and
  `opencode run -m <provider/model> --format json --agent <name>`; both verified on the
  originating dev host — re-verify availability on a new host. Batch a commit's
  delegated rules into one call. The receipt records harness, model id, rules-pin
  digest, series head SHA, config digest, and verdict. Fairy's own REVIEW_SCHEMA, for
  reference: classification enum, markdown message, head-vs-branch diff-evidence flag.

## The Fairies sourcing to fold (operator directive, firm)

The Fairies repository (Michael Niedermayer's Forgejo Fairy reviewer; GPL-2 with a
personal relicense permission reserved) is included ONLY as a pinned git submodule —
never vendored text, never fetch-at-pin. Upstream master was
`cffd25ca7b0f28184d189c3b9c462a64eee7e377` at check time;
`git ls-remote https://code.ffmpeg.org/michaelni/Fairies` passes Anubis (git
user-agents pass; the anonymous API answers plain curl).

- host-lint carries the submodule for sync tests and fixtures, test-time only: GPL text
  never enters the tree, artifacts, or binary — the gitlink alone is tracked.
- pgs-release carries its own pinned submodule for runtime; the project config names the
  path; the delegated leg verifies the checkout against the acknowledged pin, warns on
  skew, records the Fairies SHA in the receipt, and reports unrun with an install hint
  when the checkout is absent.
- Sync tests bind every Fairy-derived registry value to pinned submodule text (the
  vocabulary-term-lists-match-the-code pattern): pin bump → sync red → deliberate
  re-encode → recalibrate → freeze.
- The drift lane compares the pinned SHA against upstream master via ls-remote and
  discriminates rule-bearing paths (project_facts/, llm_prompt.py) from engine
  internals, which acknowledge trivially.
- The Fairy rule source encoded from: project_facts/ffmpeg.md — FATE portability, the
  per-new-component fate test, the samples-request procedure, the size thresholds, the
  tests/ref rule, side-data constraints, get_buffer2 alignment.

## Open operator decisions

As in the README, amended by the review: pack residence (likely foreclosed by blocker
one — verify); the pgs branch grammar; patcheck depth; the sign-off default; the
calibration threshold, which now needs an explicit operator-gated node (report
committed → a call/ decision records the rate → the tier-freeze gate), per the survivor
`operator-decisions-lack-gate-nodes`.

## Host notes

- The originating session ran on a WSL2 dev host; its workflow transcripts and raw
  fetches were session-local and are not needed — this folder plus the GitHub records
  (host-lint#22, host-lint#23) are the complete inputs to the re-cut.
- On a fresh clone, the software worktrees are absent until materialized (see the root
  CLAUDE.md fresh-clone sequence); host-lint can be worked via
  `gh --repo connollydavid/host-lint` without materializing.
- The design-record comment order on host-lint#22: opening post → pgs9 addendum →
  consolidated revision → public-signals addendum → (pending) the
  delegation/Fairies/review addendum from next-actions item six.
- Commit style here: lowercase content-named subjects; plan-doc commits push
  immediately; MEMORY.md entries are separate commits.

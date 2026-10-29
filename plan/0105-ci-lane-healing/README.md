# plan/0105: the red CI lanes heal

**Status: complete 2026-10-29. All three repos green on main and at their tags; both offline judges read zero findings. The releases landed as host-lint v0.24.0 plus the v0.24.1 patch and host-lifecycle v0.62.0 plus the v0.62.1 patch (the tool computes a minor from `adds-flag`); the results section carries the actuals.**

## Why

The operator: "let's replan around healing CI gates that fail in github. these make me sad because i get email about them." The live sweep on 2026-10-29 found three repos red on main, and every push to any of them emails another failure.

## The diagnosis

| repo | red lanes | cause |
| --- | --- | --- |
| agentic-host | Check, Reproducible build (six runs on 2026-10-29) | the three recorded-state hazards: host-lint's Cargo.toml embeds grammar `2ebf3e9` against the pin `435960c`; host-lifecycle's embeds lint `90a0d71` against the pin `cb58793`; host-lint's publish lane builds its asset without the recorded deps-bundle. The ci judge adds a recorded failure on `host/check` at HEAD and unreceipted lanes: lint `ci` at `cb58793`, the four grammar lanes at `435960c`, and `software/host/main` `install`+`prose` at `423d152` |
| host-lint | CI on main and on tag v0.23.1 (fifteen straight runs) | the six `scan_line_never_panics_n1..n6` matrix rows run to GitHub's six-hour ceiling and die cancelled. The job sets no `timeout-minutes`. The other twenty rows conclude in seconds to forty minutes |
| host-template | Prose, Site (six runs on 2026-10-29) | Prose: the version-derived-artifacts sentence in the template AGENTS.md trips the `negative-parallelism` rule under the lint that v0.61.8 embeds. Site: the v0.61.8 every-tracked-doc book gate finds the template's `plan/PLAN.md` unpublished |

Older failures elsewhere (host-lifecycle Clippy at v0.61.5, host-grammar Clippy on 2026-10-28, prove and allium in June) are superseded by green runs at tip. Only receipts are owed there.

The host tree sweeps clean under the v0.61.8 prose gate, verified at cut, so the regen sentence needs its reword only in the template.

## The chain, in dependency order

1. This record, pushed now. A few more red-run emails arrive during the healing window; the end state is green.
2. The framing retest: the six harnesses run against the checked-slicing fix, in parallel, ninety minutes each. A row that concludes green stays in the matrix. A row that hangs comes out. The admission rule lands in the workflow comment and in plan/0102: a harness row enters the CI matrix only after one concluding local run.
3. The template AGENTS.md reword, with its push held until step 7 so one push heals both template lanes.
4. `vendor-v21`, the new lint deps-bundle for the grammar move to `435960c` (the lint series stands at `vendor-v19`; `vendor-v20` was born with a misnamed asset on an immutable release and was replaced the same hour).
5. host-lint v0.24.x: the anchor-divergence rule with its allium and obligations updates, grammar `435960c`, the checked-slicing fix, and the ci.yml edits. The matrix follows the retest, the kani job gains `timeout-minutes: 100`, and the publish lane stages and verifies the recorded bundle. The green tag run is the acceptance moment.
6. host-lifecycle v0.62.x: the lint embed moves to the lint release sha, and the book generator publishes `plan/PLAN.md` in the template shape, with a fixture test.
7. One host-template push: the tools/host-lifecycle submodule at v0.61.9, the pin commits, and the reword. Prose and Site heal. Then the host pointer bump.
8. The host heals: `.host-software` re-pins lint v0.24.1 (`db4a0d2`, artifact `65b0eee7`) and lifecycle v0.62.1 (`e6d43a3`, artifact `a57a1342`) with bundle v21 for lint and v19 for lifecycle, and every receipt the judge names records at the healed revisions.

## The results

- **agentic-host**: Check and Reproducible build green at the healed HEAD; both offline judges (`software --check`, `ci --gate`) read zero findings.
- **host-lint**: v0.24.0 carried the rule set, the bounded matrix, and the deploy lane; its tag run failed on a duplicated ambient build step the lane edit left behind (a runner-side cargo build after the container left a root-owned `target/`), and v0.24.1 removed the duplicate. The v0.24.1 tag run concluded green in twenty-eight minutes on the twenty-row matrix, and the published asset hashes `65b0eee7`, byte-identical to the anchored artifact.
- **host-lifecycle**: v0.62.0 carried the lint embed and the book landing (the template's `plan/PLAN.md` becomes the room's landing page, pinned by a fixture test); v0.62.1 followed the lint patch so the embed stays equal to the pin. The published assets hash equal to their anchors (`dedc814d` at v0.62.0, `a57a1342` at v0.62.1).
- **host-template**: the single push carried both pins and the reword; Prose and Site green, with Check and Reproducible build green beside them.
- **The framing retest**: all six harnesses capped at ninety minutes against the checked-slicing rework (`rc=124` each), so the rows came out under the admission rule; plan/0102 records the halt, and the framing route pick (the contract route, a heap-free LemHit, a TLA+ lateral lane, or the test downgrade) returns to the operator as the lacuna survey's deliverable.
- **The goal-mutator fix rode the same day**: the parked close's composed gate caught the goal suffix writer decorating the milestone README (an em-dash marker, and an append that spliced wrapped statuses mid-paragraph), fixed upstream as host-lifecycle v0.62.2 under the [host-lifecycle#36](https://github.com/connollydavid/host-lifecycle/issues/36) authorization with the tag run green and the published asset equal to the anchor `38470c15`; one wrong claim in that issue's closing evidence (a GOAL.md frontier line it never carried) is corrected by a follow-up comment on the issue.
9. Close: both local judges green, the GitHub sweep green across the eight repos, this README completed with the results, MEMORY entries, and plan/0103's queue resumes behind (the [host#27](https://github.com/connollydavid/host/issues/27) lifecycle and MCP tail, plan/0104 host-voice, the receipt coupling from plan/0103, plan/0075 last).

## Rules the healing installs

- A kani row enters the CI matrix only after one concluding local run.
- `timeout-minutes` on every kani row.
- The lane's own gate runs locally before every push: `software --check`, `ci --gate`, `prose`, `book --check`.

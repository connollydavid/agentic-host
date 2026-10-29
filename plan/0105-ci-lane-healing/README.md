# plan/0105: the red CI lanes heal

**Status: cut 2026-10-29, in build.**

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
4. `vendor-v18`, the new lint deps-bundle for the grammar move to `435960c`.
5. host-lint v0.23.2: the anchor-divergence rule with its allium and obligations updates, grammar `435960c`, the checked-slicing fix, and the ci.yml edits. The matrix follows the retest, the kani job gains `timeout-minutes: 100`, and the publish lane stages and verifies the recorded bundle with the build-id flag. The v0.23.2 tag run green is the acceptance moment. A receipt records at the new pin.
6. host-lifecycle v0.61.9: the lint embed moves to the v0.23.2 sha, and the book generator publishes `plan/PLAN.md` in the template shape, with a fixture test.
7. One host-template push: the tools/host-lifecycle submodule at v0.61.9, the pin commits, and the reword. Prose and Site heal. Then the host pointer bump.
8. The host heals: `.host-software` re-pins lint v0.23.2 and lifecycle v0.61.9 with fresh artifact hashes and bundle v18, and every receipt the judge names records at the healed revisions.
9. Close: both local judges green, the GitHub sweep green across the eight repos, this README completed with the results, MEMORY entries, and plan/0103's queue resumes behind (the [host#27](https://github.com/connollydavid/host/issues/27) lifecycle and MCP tail, plan/0104 host-voice, the receipt coupling from plan/0103, plan/0075 last).

## Rules the healing installs

- A kani row enters the CI matrix only after one concluding local run.
- `timeout-minutes` on every kani row.
- The lane's own gate runs locally before every push: `software --check`, `ci --gate`, `prose`, `book --check`.

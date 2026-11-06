# plan/0112: the suite debt queue

**Status: cut 2026-11-06, queued** (operator direction: "complete #remediate
phase now" on plan/0111; the rows that outgrow a lane disposition here by
plan/0111's own rule). One queue, ascending effort where known, one release
cascade per component it touches.

## Why

plan/0111's audit measured the suite and remediated what fit a lane; these
are the rows it dispositioned to this queue by name. Nothing here is new
work discovered after the audit: every row cites its findings-register entry
or its tracker ticket.

## The queue

1. **lc#43** (trivial): the usage summary line gains the `ci` verb its own
   detail line documents (plan/0111 D-lane finding; the A/B round's measured
   cost).
2. **lc#37** (small): the closure-pair check accepts the marker the v0.62.2
   writer actually writes; a completed closure stops reading unresolved.
3. **F3/F4, the dream re-point mechanism** (medium): dream's room-touching
   remedy is unactionable under the append-only store (the detector reads the
   entry's first room reference; old bodies cannot change; the only printed
   path is retirement via an audited MADR). Either the detector reads a
   appended correction as a re-point, or the retirement path gets its
   governed template. The 19 re-points and 34 prompts stand disclosed in
   MEMORY and the register until then.
4. **lc#38** (medium): dream's Status-line reading and the task gate's
   Status-section reading unify into one convention.
5. **host#31** (medium): the install door's description stops hardcoding the
   reference host's plan/0101.
6. **host#30** (medium): `book --check` gains a placement for a nested
   evidence archive beyond the flat `reference/` form.
7. **host#29** (medium): the template's AGENTS.md task-graph example stops
   self-flagging under its own pinned host-lint (the anchor rule postdates
   the example); the fix rides the template front door (commit inside
   host-template, then the pointer bump).
8. **D1-D4, the dependency cascade** (medium): the pulldown-cmark bump in
   host-grammar (waived this cycle on the no-wikilinks path evidence;
   `Parser::new` compiles no extensions) cascades through the lint and
   lifecycle embeds; crossbeam-epoch bumps past RUSTSEC-2026-0204 in
   host-reference-ocr (waived this cycle: the fmt::Display-on-null path is
   never exercised); the host-reference unmaintained set gets bumps or
   configured ignores; lint, lifecycle, prove, and grammar declare their
   advisory scanners or record standing waivers.
9. **lc#41** (medium-large): the ci judge's sanctioned local-lane discharge
   form.
10. **lc#42** (medium-large): the goal gate's plan-row path covers template
    adopters' `plan/PLAN.md`.
11. **lc#39** (large): the anchor-rename path that does not orphan task
    receipts.
12. **host#27** (large): the authored-tokens encoding, carried from
    plan/0103: name minting and comment rulings in the grammar, the judgment
    half through a tight MCP side.

## Constraints

One release cascade per touched component. An unpushed pin halts the queue
with a report. Every ticket closes with a comment citing its release and run
URLs. host#18 stays plan/0075's, last by standing order, outside this queue.

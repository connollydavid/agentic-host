# plan/0103 open-issue sweep: the superset, eleven issues, simplest first

**Status: cut 2026-10-28, in build** (operator-directed: "please examine the superset of
open issues. let's fix them in order of complexity")

## Why

The census (2026-10-28, GitHub API over every connollydavid repository and the vendored
upstreams) counts eleven open issues across three trackers, and nothing else:

| Repo | Issues |
|---|---|
| connollydavid/host | [#18](https://github.com/connollydavid/host/issues/18) [#25](https://github.com/connollydavid/host/issues/25) [#26](https://github.com/connollydavid/host/issues/26) [#27](https://github.com/connollydavid/host/issues/27) [#28](https://github.com/connollydavid/host/issues/28) |
| host-lifecycle | [#30](https://github.com/connollydavid/host-lifecycle/issues/30) [#31](https://github.com/connollydavid/host-lifecycle/issues/31) [#32](https://github.com/connollydavid/host-lifecycle/issues/32) [#33](https://github.com/connollydavid/host-lifecycle/issues/33) [#34](https://github.com/connollydavid/host-lifecycle/issues/34) |
| host-lint | [#32](https://github.com/connollydavid/host-lint/issues/32) |

Clean: agentic-host, host-template, host-grammar, host-prove, host-reference,
host-reference-ocr, weco-cli, weco-skill, slartibardfast/calx-knap.

Existing assignments stand, not re-cut: lint#32 is [plan/0102](../0102-kani-lane-concludes/README.md)
(cut, in build, whose landing also unparks plan/0101's parked goal close); host#18 is
[plan/0075](../0075-host-reconcile/README.md) (design-only; the standing order places it
last); the /goal vacuum half of host#26 is answered by
[plan/0101](../0101-goal-and-loop-subsystem/README.md) (v0.61.0). Two operator rulings
taken at cut: lc#30 fixes by **receipt digest + static scan** (both directions); host#26
**closes the /goal half and defers the plugin** to its own future milestone.

A live instance of host#25 sits in this very tree: SUMMARY.md's plan index stops at
plan/0092, so plans 0093 through 0102 render nowhere while `book --check` passes green.

## The queue (ascending complexity; one lifecycle release per lifecycle issue)

1. **host#28 (trivial)**: `--locked` on the front-door README's allium install line.
2. **lc#34 (small)**: `resolve_ledger_id` resolves the exact stanza id and prefix before
   the ordinal parse; rejection only when both readings fail.
3. **lc#32 (small-medium)**: `hooks` scripts resolve across bases: component worktree,
   host root, initialized submodules.
4. **lc#31 (medium)**: `regen = <command>` stanza key, run between the version bump and
   the release commit.
5. **host#25 (medium)**: `book --check` reconciles every tracked markdown document
   against SUMMARY.md; the generator emits milestone siblings.
6. **lint#32 (medium-large)**: plan/0102 executes: pure per-word classifier and word-run
   extraction, word-level proofs at n at most 10, unwind bounds everywhere, v0.23.1.
7. **lc#33 (medium-large)**: an `--inapplicable` recorded claim; the check reports a named
   disclosure, never a permanent HAZARD; the spine calls Actions a reference lane.
8. **lc#30 (large)**: a release-asset receipt digest, reconciled offline by `software
   --check`, plus the static workflow scan (no staged bundle, or a CARGO_HOME override).
9. **host#27 (large)**: `tasks --new` title validation, a measured STE-style subset in
   host-grammar, `mint_name`/`rule_comment` MCP tools in host-lint.
10. **host#26 (ruled)**: close the /goal half citing plan/0101; the OpenCode plugin is
    its own future milestone, recorded here as deferred, not cut. (Resolution
    2026-10-30: cut as [plan/0106](../0106-opencode-goal-plugin/README.md), built and
    accepted on real qwen3.5-4b; the promotion ruling proposes the `host-loop`
    component.)
11. **host#18 (largest, last)**: plan/0075 executes: the reviewed host-reconcile design,
    go/no-go, build ungated.

## Status (2026-10-28, end of the first working session)

Done and closed: #28, lc#34 (v0.61.1), lc#32 (v0.61.2), lc#31 (v0.61.3 plus the
9a0f7d0 ledger entry), host#25 (v0.61.4), lc#33 (v0.61.5 plus 7ef379e), and
host#26 (closed citing plan/0101, the plugin deferred by ruling). Built and
ruled: lc#30 (v0.61.6/v0.61.7: the publish receipt and the lane scan, which
caught real divergence on first dogfood; the issue stays open on the residual
byte-matching, the comment carries the evidence). Released and awaiting its
verdict: lint#32 (v0.23.1, cb58793, the 22-row kani matrix; the tag run is the
moment of truth). Halfway: host#27 (host-grammar v0.8.0 released with the slug
derivation and the measured verb register; the lint divergence rule
implemented and tested, its release riding the lane fix; the lifecycle mint
and comment tools pending). Not started: host#18 (plan/0075, last by standing
order). Found on the way and filed: host-lifecycle#35 (the release gate's
clippy blind spot). The embed-equality and publish debts the gates now hazard
are exactly the next two releases' cargo.

## Constraints

One release cascade per lifecycle issue (six). An unpushed pin halts the sweep with a
report. Credentials never committed. Every issue closes with a comment citing its release
and run URLs. The sweep ends with `software --check` and the ci receipts green,
plan/0103 completed, MEMORY appended.

# plan/0111: the full-sweep component audit and the public-ticket sweep

**Status: cut 2026-11-05, queued behind plan/0110's ship verdict** (operator
direction: audit all software under development with this host and plan its
complete remediation, with the publicly open GitHub tickets part of the
sweep; the nine `.host-software` components sit in remediation scope, the
vendored upstreams are audited as pins and filings only and their fixes go
upstream). The queue is plan/0110's until its `#ship` verdict lands; this
plan cuts now and waits.

## The design

The audit invents nothing. The host already owns the judges, so the sweep
runs them and banks what they refuse. The matrix runs every offline judge
over the host root and each component; the ticket lane re-censuses the
public trackers; the reproducibility, dependency, and quality lanes run
what the judges do not cover. Every non-green exit and every open ticket
banks as one row in a findings register (`findings.md` in this folder)
carrying the tracker or component, the lane, the evidence, and the remedy.
Remediation closes every row by fix or by receipted waiver: a changed
component releases through the tool-carried sequence (`host-lifecycle
release <component> --change-class <class>`, tag and push inside the
worktree, re-pin, receipt), and a ticket closes with a comment citing its
release and run URLs.

The ticket census at cut (2026-11-05, read from the public pages because
`gh` was unavailable in the cutting session; the lane re-censuses with
`gh` at execution):

| Tracker | Open | Notes |
|---|---|---|
| [connollydavid/host](https://github.com/connollydavid/host) | [#18](https://github.com/connollydavid/host/issues/18) [#27](https://github.com/connollydavid/host/issues/27) [#29](https://github.com/connollydavid/host/issues/29) [#30](https://github.com/connollydavid/host/issues/30) [#31](https://github.com/connollydavid/host/issues/31) | #18 stays plan/0075's, last by standing order; #27 is plan/0103's halfway remainder, carried here; #29 through #31 are unassigned, newer than plan/0103's census |
| [connollydavid/host-lifecycle](https://github.com/connollydavid/host-lifecycle) | [#37](https://github.com/connollydavid/host-lifecycle/issues/37) [#38](https://github.com/connollydavid/host-lifecycle/issues/38) [#39](https://github.com/connollydavid/host-lifecycle/issues/39) | all three unassigned |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | [#61676](https://github.com/anomalyco/opencode/issues/61676) | our upstream filing, tracked, not ours to close |

Clean everywhere else in the tree's orbit: agentic-host, host-lint,
host-loop, host-grammar, host-prove, host-reference, host-reference-ocr,
host-reference-openscad, host-template, weco-cli, weco-skill.
[host-lifecycle#30](https://github.com/connollydavid/host-lifecycle/issues/30)
has closed since plan/0103's census, which drains that queue: plan/0103
closes at this cut with its remainder carried (#27 arrives here, #18 stays
plan/0075's).

Four openings the sweep must confirm and disposition, observed at cut:
plan/0102's PLAN.md row still reads in build though its lane greened via
plan/0105; the host#25 under-rendering class (`book --check` green while
plan documents go unrendered, host#30 the nested-archive instance of the
same surface); MEMORY.md's two newest entries sit above the `# MEMORY.md`
title; and `.calx-knap/overrides.md` is named by the manual but absent in
this clone, which may be an unmaterialized binding surface or a hole.

## Build sequence

### The audit matrix {#matrix}

- verify: every judge below runs over the host root and each component
  with its exit code recorded; `findings.md` holds a row for every
  non-green exit, and a judge that could not run is itself a row that
  names its blocker
- judges: `host-lifecycle ci .`, `software --check .`,
  `software --verify-setup .`, `env --check .` (advisory; act only on the
  lines that say to), `refs --check .`, `refs --gate .`,
  `validate plan/ call/`, `dream .`, `book --check .` with the page-count
  measure (rendered pages against tracked plan markdown, the host#25
  class), `entrance --check .`, `install --check .`, and
  `obligations <spec>.allium --strict-discharge` per declared spec
- note: nothing banks green on a judge that did not run; a missing
  container or verifier is a row, not a skip

### The public-ticket lane {#tickets}

- verify: the re-census (`gh issue list -R <repo> --state open` over the
  connollydavid repos in this tree's orbit, plus our own open filings
  upstream) matches the cut census or the delta is itself a row; every
  open ticket carries exactly one disposition row in `findings.md`
  (remediated here, closed with evidence, assigned to an existing
  milestone, or upstream tracking); every closure comment cites its
  evidence; every `gh` create or edit title lints clean first
- depends: #matrix
- note: #27's pending lifecycle mint and comment tools absorb from
  plan/0103; #29 rides the template front door (commit inside
  host-template first, then the pointer bump; nothing lands here but the
  pointer and any recorded upgrade action); #18 stays plan/0075's;
  host-lifecycle #37, #38, and #39 remediate as the sweep's own gates
  trip them

### The reproducibility lane {#repro}

- verify: `software --verify-build .` reports VERIFIED for each of the
  six container-built components, or the DEFERRED or repro-exempt
  verdict is a row in `findings.md`
- depends: #matrix

### The dependency and security lane {#deps}

- verify: each Rust component runs `cargo deny` or `cargo audit` clean
  (a component declaring no advisory scanner is itself a row whose
  remedy follows the change-class rules), host-loop runs `npm audit`
  clean, and every deps-bundle lock agrees with its pin
- depends: #matrix

### The quality lane {#quality}

- verify: `cargo clippy --all-targets -- -D warnings` clean inside each
  Rust worktree (the runner's clippy is not the box's, the v0.60.7
  lesson), `node --test` green for host-loop, host-lint clean over each
  component tree, and `lint-skill.sh` green for host-lint itself; each
  failure is a row
- depends: #matrix

### Remediation and re-release {#remediate}

- verify: `software --check .` green at the new pins, `ci . --gate` exit
  0 with a receipt citing a run URL for every re-run lane,
  `obligations --strict-discharge` green per declared spec,
  `refs --gate .` green, and every `findings.md` row closed as fixed,
  waived with a receipt, or dispositioned to a named owner
- depends: #matrix, #tickets, #repro, #deps, #quality
- note: one release cascade per changed component; an unpushed pin halts
  the sweep with a report; credentials never committed

### Records {#records}

- verify: the PLAN.md row, MEMORY, the gate
- depends: #remediate

## Named risks

[host-lifecycle#37](https://github.com/connollydavid/host-lifecycle/issues/37)
can make this plan's own completed closure read unresolved; if the sweep
trips it, it is fixed in lane as a finding, never worked around in
silence. [host-lifecycle#39](https://github.com/connollydavid/host-lifecycle/issues/39)
forbids renaming any task anchor mid-flight, because the receipts orphan.
Every re-pin stales its publish receipt until the new asset re-records,
one red Check window per release, by design. A missing container runtime
blocks the reproducibility lane, and the DEFERRED verdict is a row, not a
skip. The queue belongs to plan/0110 until its `#ship` verdict lands.

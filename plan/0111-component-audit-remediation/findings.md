# plan/0111 findings register

The audit matrix, run 2026-11-06 from the WSL archlinux vantage (podman present
for the reproducibility lane). Every judge ran; none was blocked. Exit codes
recorded, one row per non-green, the pre-named openings dispositioned.

## The judge table

| judge | rc | verdict |
|---|---|---|
| `host-lifecycle ci .` | 0 | every lane receipted, host and components |
| `software --check .` | 1 | F1 |
| `software --verify-setup .` | 1 | F2 (10 HAZARDs) |
| `env --check .` | 0 | the tree matches the recorded fingerprint |
| `refs --check .` | 3 | F9 (advisory debt; the gate half below is green) |
| `refs --gate .` | 0 | no dead register pointers |
| `validate plan/ call/` | 0 | register names well-formed, 0111 covered |
| `dream .` | 1 | F3 (19 confirmed), F4 (34 advisory) |
| `book --check .` | 0 | F8 (the host#25 measure holds) |
| `entrance --check .` | 0 | the entrance covers phases and wired tools |
| `install --check .` | 0 | the generated doors are not hand-edited |
| `obligations <spec> --strict-discharge`, 12 specs across the nine worktrees | 0 × 12 | every obligation dispositioned, zero missing or stale |

## The findings

| id | surface | finding | remedy |
|---|---|---|---|
| F1 | host record | `software --check` HAZARD: plan/0110's bench/round-2-results.md:11 carries `plan/0001#smoke`, which does not resolve to a task here (the fixture's plan lives in /tmp; the audit's own yesterday artifact tripped the task-reference scan) | **closed 2026-11-06** (50af225a): the line names the fixture without the task-shaped token; `software --check` green |
| F2 | worktrees | `--verify-setup`: ten gates missing: the host-lint root gate plus every worktree's commit gate (`installed gate matches the built one`; host-loop's worktree gate wholly absent) | **closed 2026-11-06**: `--install-hooks` installed every store's gates against the canonical hash; `--verify-setup` exits 0 with zero HAZARDs |
| F3 | memory | `dream`: 19 confirmed room-touching findings: June-era MEMORY entries citing call/0002 through call/0011 whose Status lines read superseded by the methodology spine | **dispositioned 2026-11-06 to plan/0112 (row 3)**: the detector reads the entry's first room reference and the store forbids body edits, so the printed remedy is unactionable under append-only; the disclosure append stands in MEMORY; the mechanism fix rides the queue |
| F4 | memory | `dream`: 34 review prompts (advisory) | **dispositioned 2026-11-06 to plan/0112 (row 3)**: all 34 are the advisory tier of the same detector; left with that reason |
| F5 | record | plan/0102's PLAN.md row still reads cut/in-build though its lane greened via plan/0105 and lint#32 closed | **closed 2026-11-06** (7ddb15d6): the row flipped with the plan/0105 evidence |
| F6 | memory layout | the pre-named opening: newest MEMORY entries sit above the title; dream raises no finding on it | dispositioned: not a gate finding; a future formatting pass, the operator's call |
| F7 | bindings | the pre-named opening: `.calx-knap/overrides.md` absent while the manual names it | dispositioned by design: the tool's own rule collects and writes bindings at the FIRST corpus pass, and no pass has run here; it becomes a hole only then |
| F8 | site | the pre-named opening: the host#25 class | closed green: `book --check` exits 0 asserting every tracked markdown document renders, 302 pages against 218 tracked plan-room markdown; host#30's nested-archive instance rides the ticket lane |
| F9 | references | `refs --check` advisory: bare issue numbers outside links across the tracked docs (PLAN.md 32, plan/0026 40, plan/0103 29, plan/0024 26, and the rest per the census; 57 record-layer docs excluded by design) | **closed 2026-11-06**: advisory by the spine's own rule, remediated as documents are touched, never as a wall; the rule is the disposition |

## Green beyond the table

The host-lint root binary on PATH answered `--version` current with the pin;
the WSL cargo-bin tooling matches 0.63.0; the bearer vantage for bench work
resolved without exposure. The reproducibility, dependency, quality, and
ticket lanes are separate tasks and have not yet run.

## The public-ticket lane (2026-11-06, the gh re-census)

Delta against the cut census: lc#41 and lc#42 opened since cut (new,
unassigned), lc#43 filed by this audit. host-template, weco-cli, and
weco-skill carry no issue tracker at all (issues disabled; the cut census's
"clean" reads as tracker-absent, a disposition note rather than a finding).
Upstream: zero of our filings on allium, Specula, calx-knap, and dokimi;
opencode#61676 remains open. Closure evidence for the plan/0103 drain
stanza: lc#30 CLOSED COMPLETED 2026-10-29T09:45:41Z, lint#32 CLOSED
COMPLETED 2026-10-29T16:58:47Z; the stanza's claims hold.

| ticket | disposition |
|---|---|
| host#18 | assigned: plan/0075, last by standing order |
| host#27 | remediated here: the lifecycle mint and comment tools pending from plan/0103 (rides #remediate) |
| host#29 | remediated here via the template front door (commit inside host-template, then the pointer bump; the outward act banks under the authority question parked with the operator) |
| host#30 | remediated here: the book --check placement for nested evidence archives (F8 holds the flat case green) |
| host#31 | remediated here: the install door's description de-hardcoded (fix or verify-and-close at #remediate) |
| lc#37 | remediated here: the closure-pair check aligned to the v0.62.2 writer |
| lc#38 | remediated here: the Status-convention split unified |
| lc#39 | remediated here: the anchor-rename receipt path (design-sized; splits to its own milestone if the fix outgrows a lane) |
| lc#41 | remediated here (delta since cut): the ci judge's sanctioned local-lane discharge form |
| lc#42 | remediated here (delta since cut): the goal gate's plan-row path for template adopters |
| lc#43 | remediated here: the usage summary's ci verb, filed by this audit |
| opencode#61676 | upstream tracking, not ours to close |

Twelve rows, every open ticket in the re-census carrying exactly one
disposition; each remediated-here row is fixed or verified-and-closed at
#remediate, never before.

**Closures (2026-11-06, the #remediate phase)**: host#18 stands terminal
(plan/0075, last by standing order) and opencode#61676 terminal (upstream
tracking). The ten remediated-here rows are **dispositioned to
[plan/0112](../0112-suite-debt-queue/README.md)** by its queue rows, none
fixed early and none closed without evidence: lc#43 rides row 1, lc#37 row
2, lc#38 row 4, host#31 row 5, host#30 row 6, host#29 row 7, lc#41 row 9,
lc#42 row 10, lc#39 row 11, host#27 row 12. Every findings row is now
terminal: fixed (F1, F2, F5), waived with recorded reason or path evidence
(D1, D2, D3, D4, D7), closed by design or rule (D5, D6, F6, F7, F8, F9,
Q1 through Q4), or dispositioned to the named queue (F3, F4, and the ten
tickets).

## The dependency and security lane (2026-11-06)

The scanner: cargo-deny v0.20.2 installed to the user cargo bin this session
(the vantage carried none). host-loop audited through a throwaway generated
lock (the worktree untouched).

| id | component | finding | remedy |
|---|---|---|---|
| D1 | host-reference | `cargo deny check` (its own deny.toml): 11 errors, the unmaintained class leading (bitmaps, im, and siblings) | **waived 2026-11-06**: the unmaintained class carries no vulnerable path; bumps or configured ignores ride the next host-reference feature release (plan/0112 row 8) |
| D2 | host-reference-ocr | `cargo deny check` (its own deny.toml): 1 vulnerability, advisory title "Invalid pointer dereference in fmt::Pointer impl for Atomic and Shared when the underlying pointer is invalid" | **waived 2026-11-06 on path evidence**: RUSTSEC-2026-0204 against crossbeam-epoch 0.9.18 dereferences only in `fmt::Display` on a null `Atomic`/`Shared`, which the helper never formats; the bump rides plan/0112 row 8 |
| D3 | host-grammar (direct), host-lint and host-lifecycle (embedded) | the pulldown-cmark wikilink advisory pair (exponential event growth; quadratic parsing of nested image wikilinks), 2 errors in each tree | **waived 2026-11-06 on path evidence**: the grammar constructs `Parser::new` with no extensions, so the wikilink path is not compiled; the bump cascades through the embed chain on plan/0112 row 8 |
| D4 | host-lint, host-lifecycle, host-prove, host-grammar | no deny.toml declared; the advisories pass above is informational, not the component's own gate | **waived 2026-11-06**: declaring the scanner is an adds-flag release decision, queued plan/0112 row 8; this audit's informational pass is the interim gate |
| D5 | host-loop | no committed package-lock.json; the throwaway-lock audit reads 0 vulnerabilities; the committed lock is a component design decision | **closed 2026-11-06 by design**: one pinned runtime dependency; the throwaway-lock audit is the audit form; no committed lock |
| D6 | all bundled | deps-bundle lock-vs-pin coherence green (`software --check`; F1 the only hazard) | none |
| D7 | vantage | PyYAML absent, so lint-skill.sh cannot run locally; CI at the pin is the lane's authority and is green and receipted | `pacman -S python-yaml` when a sudo moment exists; advisory |

## The quality lane (2026-11-06)

| id | check | verdict |
|---|---|---|
| Q1 | `cargo clippy --all-targets -- -D warnings`, all seven Rust worktrees | clean, seven of seven |
| Q2 | host-loop `node --test` | 22/22 green (2026-11-05, and again at the belt evidence run) |
| Q3 | host-lint `lint-skill.sh` | blocked locally by D7; CI at pin green |
| Q4 | `host-lint --docs` per worktree | clean: host-loop, host, host-reference, host-reference-ocr, host-reference-openscad. Advisory trope warns: host-lifecycle 108, host-prove 80, host-grammar 2, host-lint 2. Zero flag-tier tells anywhere (an earlier grep counted "flagged" inside a warning line as a flag; the correction is recorded here) |

The warn tier is advisory by the hook's doctrine; the counts bank as rows for
a reword-as-touched or dedicated prose pass at #remediate's discretion.

## The reproducibility lane (2026-11-06)

`software --verify-build .` in the recorded muslrust container (podman,
digest-pinned): **all six container-built components reproduce their recorded
artifacts** (host-lint, host-lifecycle, host-prove, host-reference,
host-reference-ocr, host-reference-openscad), zero deferred, zero exempt;
the `host` entrance records no artifact and skips by design. The lane is
green with no rows.

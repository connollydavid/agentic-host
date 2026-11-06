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
| F1 | host record | `software --check` HAZARD: plan/0110's bench/round-2-results.md:11 carries `plan/0001#smoke`, which does not resolve to a task here (the fixture's plan lives in /tmp; the audit's own yesterday artifact tripped the task-reference scan) | reword the line to name the fixture without the resolvable-looking token; milestone-doc edit, own commit |
| F2 | worktrees | `--verify-setup`: ten gates missing: the host-lint root gate plus every worktree's commit gate (`installed gate matches the built one`; host-loop's worktree gate wholly absent) | `host-lifecycle software --install-hooks .`, then re-run the gate |
| F3 | memory | `dream`: 19 confirmed room-touching findings: June-era MEMORY entries citing call/0002 through call/0011 whose Status lines read superseded by the methodology spine | 19 appended re-points (dream's route=append), never in-place edits |
| F4 | memory | `dream`: 34 review prompts (advisory) | read at remediation; each dispositioned or left with reason |
| F5 | record | plan/0102's PLAN.md row still reads cut/in-build though its lane greened via plan/0105 and lint#32 closed | flip the row with the evidence |
| F6 | memory layout | the pre-named opening: newest MEMORY entries sit above the title; dream raises no finding on it | dispositioned: not a gate finding; a future formatting pass, the operator's call |
| F7 | bindings | the pre-named opening: `.calx-knap/overrides.md` absent while the manual names it | dispositioned by design: the tool's own rule collects and writes bindings at the FIRST corpus pass, and no pass has run here; it becomes a hole only then |
| F8 | site | the pre-named opening: the host#25 class | closed green: `book --check` exits 0 asserting every tracked markdown document renders, 302 pages against 218 tracked plan-room markdown; host#30's nested-archive instance rides the ticket lane |
| F9 | references | `refs --check` advisory: bare issue numbers outside links across the tracked docs (PLAN.md 32, plan/0026 40, plan/0103 29, plan/0024 26, and the rest per the census; 57 record-layer docs excluded by design) | advisory by the spine's rule: remediated as documents are touched, never as a wall |

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

## The dependency and security lane (2026-11-06)

The scanner: cargo-deny v0.20.2 installed to the user cargo bin this session
(the vantage carried none). host-loop audited through a throwaway generated
lock (the worktree untouched).

| id | component | finding | remedy |
|---|---|---|---|
| D1 | host-reference | `cargo deny check` (its own deny.toml): 11 errors, the unmaintained class leading (bitmaps, im, and siblings) | bump or waiver per the config's own rules at #remediate |
| D2 | host-reference-ocr | `cargo deny check` (its own deny.toml): 1 vulnerability, advisory title "Invalid pointer dereference in fmt::Pointer impl for Atomic and Shared when the underlying pointer is invalid" | bump the crate at #remediate |
| D3 | host-grammar (direct), host-lint and host-lifecycle (embedded) | the pulldown-cmark wikilink advisory pair (exponential event growth; quadratic parsing of nested image wikilinks), 2 errors in each tree | a grammar-side bump cascading through the embed-equality chain |
| D4 | host-lint, host-lifecycle, host-prove, host-grammar | no deny.toml declared; the advisories pass above is informational, not the component's own gate | declare the scanner or record the waiver, per change-class rules |
| D5 | host-loop | no committed package-lock.json; the throwaway-lock audit reads 0 vulnerabilities; the committed lock is a component design decision | decide at #remediate |
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

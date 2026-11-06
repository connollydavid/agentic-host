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

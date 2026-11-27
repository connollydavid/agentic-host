# plan/0113 selection: the frozen 30-draw round

**Status: complete 2026-11-27.** The 30 draws are recorded. Only
`null/house-host-lint-docs` produced the contract; the other 29 hit the
1800-second cap without a `sources.json`. The lock is `weizhena` by the frozen
tie-break; the confirmation is next.

## The frozen protocol

One selection round, frozen at the cast review: five arms (null plus the four
candidates) on six selection tasks, one draw per arm and task, interleaved by
task, 30 draws. The band is 1.0 point of the 16-point applicable maximum; the
lock is the highest suite-fit among the candidate arms within the band, then
fewer tokens, then name order.

## The arm setup

Each draw ran the pinned OpenCode v2.4.2 binary in its own scratch `HOME` and
XDG roots, outside the repository, with the model
`api.d07yx58.net/qwen3.8-flash-next` and Exa enabled. The per-arm config:

| Arm | Setup |
|---|---|
| `null` | no skill or plugin; the frozen prompt in `../contract/prompts/null.md` |
| `weizhena` | the five research skills and the `web-search` agent, the agent's model and write permission overridden |
| `hffmnnj` | the plugin from the snapshot at its pin |
| `kanatami` | the `web-search-deep` skill and the `web-search-worker` agent, the agent's model overridden |
| `samber` | the `deep-research` skill |

Every draw got the same contract: `report.md`, `sources.json`,
`fetch-log.jsonl`, the page snapshots and the harness's receipt. A draw whose
contract or rubric failed is void and scores zero.

## The draws

The round ran in six task waves, five arms concurrent within each wave. The
first draw (`null` on `house-host-lint-docs`) had already run alone; the waves
carried the other 29.

| Task | null | weizhena | hffmnnj | kanatami | samber |
|---|---|---|---|---|---|
| `simpleqa-0000` | 0 | 0 | 0 | 0 | 0 |
| `simpleqa-0002` | 0 | 0 | 0 | 0 | 0 |
| `simpleqa-1000` | 0 | 0 | 0 | 0 | 0 |
| `house-path-crates` | 0 | 0 | 0 | 0 | 0 |
| `house-rg-ast-grep` | 0 | 0 | 0 | 0 | 0 |
| `house-host-lint-docs` | **13** | 0 | 0 | 0 | 0 |

| Arm | Pooled | Valid draws | Tokens | Suite-fit |
|---|---|---|---|---|
| `null` | 2.17 | 1 of 6 | 308926 | 4 |
| `weizhena` | 0.00 | 0 of 6 | 182098 | 4 |
| `hffmnnj` | 0.00 | 0 of 6 | 228028 | 4 |
| `kanatami` | 0.00 | 0 of 6 | 496827 | 4 |
| `samber` | 0.00 | 0 of 6 | 482686 | 4 |

The valid draw: citation support 6/6 (17 cited sentences, all in the fetched
snapshots), must-cover 4/4 (`0.8.0`, `--docs`, `VOCABULARY.md`), numerals 3/3,
prose 0/3 (the host-lint prose lane flagged the report's style), total 13/16.
The report cites the host-lint `v0.8.0` release, the `--docs` commit and
`VOCABULARY.md` §6. Its receipt, report, ledger, fetch log and snapshots are in
`draws/null/house-host-lint-docs/`.

The other 29 draws hit the 1800-second cap before writing `sources.json`; their
reports, fetch logs and snapshots are recorded, but the contract fails on the
missing ledger. The five-way waves starved the reference model's provider; the
one draw that ran alone produced the contract at the cap.

## The suite-fit

| Arm | Model | Ledger | Snapshots | Artifacts | One command | Vendored | Score |
|---|---|---|---|---|---|---|---|
| `weizhena` | yes | no | no | yes | yes | yes | 4 |
| `hffmnnj` | yes | no | no | yes | yes | yes | 4 |
| `kanatami` | yes | no | no | yes | yes | yes | 4 |
| `samber` | yes | no | no | yes | yes | yes | 4 |

The model column is the per-arm override to
`api.d07yx58.net/qwen3.8-flash-next`; the ledger and snapshot columns are the
contract's valid draws; the artifacts are under the draw directory; one
command is `run.py`; the vendored column is the arm snapshot's pin and license
([arms/README.md](../arms/README.md)). Every candidate scores four and clears
the model and vendored criteria.

## The lock

The best candidate pooled score is 0.00; all four candidates are within the
1.0-point band. The suite-fit is 4 for each, so the tie goes to fewer tokens:
`weizhena` 182098, `hffmnnj` 228028, `samber` 482686, `kanatami` 496827. The
lock is **`weizhena`**.

The lock follows the frozen rule on the recorded scores. The data is a harness
finding as much as an arm finding: the 1800-second cap and the five-way waves
leave the reference model unable to finish the ledger, and the null's one
valid draw is the only contract-valid output. The confirmation against `null`
on the held-out set is the guard; the selection does not declare a winner.

## The driver

- `run.py`: one draw or the full round; the waves; it writes
  `draws/<arm>/<task>/` with the report, ledger, fetch log, snapshots, receipt
  and `score.json`.
- `round.py`: reads the 30 draws, pools each arm's score, computes the band,
  fills the suite-fit table and writes `round.json`.

`round.json` carries the draws, the pooled scores, the suite-fit and the lock.
The draw directories are the audit surface; `.host-lintignore` excludes them
from the prose and reference walks as verbatim draw evidence.

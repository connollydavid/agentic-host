# plan/0113 selection: the frozen 30-draw round

**Status: in progress.** The driver is built and the first draw is running; the
round report lands when all 30 draws are in.

## The frozen protocol

One selection round, frozen at the cast review: five arms (null plus the four
candidates) on six selection tasks, one draw per arm and task, interleaved by
task — 30 draws. The band is 1.0 point of the 16-point applicable maximum; the
lock is the highest suite-fit among the candidate arms within the band, then
fewer tokens, then name order.

## The arm setup

Each draw runs the pinned OpenCode v2.4.2 binary in its own scratch `HOME` and
XDG roots, outside the repository, with the model
`api.d07yx58.net/qwen3.8-flash-next` and Exa enabled. The per-arm config:

| Arm | Setup |
|---|---|
| `null` | no skill or plugin; the frozen prompt in `../contract/prompts/null.md` |
| `weizhena` | the five research skills and the `web-search` agent, the agent's model and write permission overridden |
| `hffmnnj` | the plugin from the snapshot at its pin |
| `kanatami` | the `web-search-deep` skill and the `web-search-worker` agent, the agent's model overridden |
| `samber` | the `deep-research` skill |

Every draw gets the same contract: `report.md`, `sources.json`,
`fetch-log.jsonl`, the page snapshots, and the harness's receipt. A draw whose
contract or rubric fails is void and scores zero.

## The driver

- `run.py` — one draw or the full round; it writes `draws/<arm>/<task>/` with
  the report, ledger, fetch log, snapshots, receipt and `score.json`.
- `round.py` — reads the 30 draws, pools each arm's score, computes the band,
  fills the suite-fit table and writes `round.json`.

## The result

To fill when the 30 draws are in: the per-draw table, the pooled scores, the
suite-fit evidence and the locked arm.

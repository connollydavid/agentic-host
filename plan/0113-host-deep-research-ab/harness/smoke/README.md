# plan/0113 smoke gate: one draw per arm before any scored draw

**Status: the corrected machinery passes on the recorded live draws; the fresh
all-arm run is the `#selection-redo` record.** The gate is the last check before
the redo selection. It runs one draw per arm on a dedicated task, through the
full pipeline: the native prompt, the adapter, the measured search provider,
the fetch log, the receipt, the rubric and the isolation probe.

The review found that the first record read the wrong OpenCode tables: replies
came from a `message` table that does not exist in the v2.4.2 schema, and
fetches read `state.output` while the scratch database stores the page as
`state.content`. The corrected reader uses `session_message` for replies and
`session_part` for fetches (including subagent sessions), and the report's
prose is no longer a fetch fallback. The recorded live draws now yield:

| Arm | Outcome | Evidence |
|---|---|---|
| `null` | valid, 4.0/16 | provider `exa`, 22 replies, 4 fetched pages |
| `hffmnnj` | valid, 16.0/16 | 10 replies, 1 fetched page, no websearch; the fresh run turns embedding off |
| `kanatami` | budget | 1,264,094 prompt tokens, 72 tools, wall 10,800s; native route `html.duckduckgo.com` recorded |
| `weizhena` | excluded | 26 result URLs, report cites no quote or locator |
| `samber` | excluded | 49 report citations, 2 fetched; the ledger cannot carry the rest |

The fresh record supersedes this table. The isolation probe is 11/11. A valid
draw has a live receipt with the 300000/100000/60/10800 caps, a fetch log, a
reply ledger and a scored rubric. The record is `smoke/smoke.json`; its
`records` list is append-only.

## The task

`smoke/house-capital`: "What is the capital of France, and which river runs
through it?" with `Paris` and `Seine` as must-cover. It is deliberately simple:
the smoke tests the pipeline, not the arms' research depth. It is not in the
selection or held-out sets.

## The gate

- The null arm must produce the contract; a null void is a harness failure.
- Every mapped arm must produce the contract, a recorded exclusion, or a
  recorded budget result. A budget result is a terminal arm result: it is not
  re-run under the same cap. A harness break is a void and re-runs once.
- An exclusion is suspect when the native notes, workers or report already
  carry a source record that the run's fetch log supports; the smoke fails it
  and the draw is re-run after the adapter fix. A report that cites pages the
  run never fetched is a phantom source, not a recoverable record.
- A pseudo-tool-call transcript (`<tool_call>` or `<function=`) is a void, not
  an exclusion; the plugin tools were not invoked, so the draw is re-run.
- The non-null prompt must not carry the wrapper postscript; it must carry the
  arm's native line, and the task file is in the working directory.
- The null's search provider must be `exa` or `none`, and the null may not
  fetch a search engine. Each research arm's native search route is recorded,
  not judged against the null's provider.
- A valid draw must have a live receipt with the frozen caps, a fetch log, a
  passing `replies.jsonl` and a scored rubric; an excluded draw must have
  `exclusion.json` and a reason.
- The isolation probe (`../probe.py`) must pass; it proves the pinned binary,
  the arm loads and the planted skill/manual controls.

## Run

```sh
cd plan/0113-host-deep-research-ab/harness
python3 smoke/run.py --only null --skip-probe   # one arm, record unchanged
python3 smoke/run.py --force --parallel 2       # all arms, two-way
python3 smoke/run.py --record-only              # consolidate existing draws
```

A partial `--only` run writes its draw but never the all-arm record. The
record is `smoke/smoke.json`; the draws are under `smoke/draws/`, and a forced
re-run keeps the prior attempt under `attempts/` with `rerun.json`.

## The smoke is not a scored draw

The smoke scores are not used in the selection. It proves the pipeline and the
controls; the redo selection runs separately with the frozen budget.

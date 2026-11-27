# plan/0113 smoke gate: one draw per arm before any scored draw

**Status: the first record passed, then the five-seat review invalidated the
kanatami and samber results; the corrected all-arm smoke is the
`#selection-redo` run.** The gate is the last check before the redo selection.
It runs one draw per arm on a dedicated task, through the full pipeline: the
native prompt, the adapter, the measured search provider, the fetch log, the
receipt, the rubric and the isolation probe.

## The result

| Arm | Outcome | Wall |
|---|---|---|
| `null` | valid, 9.615/16, provider `exa` | 5021.9s |
| `hffmnnj` | valid, 5.09/16, recorded-draw reuse | 928.8s |
| `kanatami` | valid, 9.818/16, recorded-draw reuse | 8231.4s |
| `weizhena` | excluded, structured field JSON/report | 7204.8s |
| `samber` | excluded, claim notes without quote/locator | 6514.2s |

The isolation probe is 11/11. Every valid draw has a live receipt with the
200000/50000/60/10800 caps, a fetch log and a scored rubric. The
suspect-exclusion and pseudo-tool-call gates pass. The record is
`smoke/smoke.json`.

## The task

`smoke/house-capital`: "What is the capital of France, and which river runs
through it?" with `Paris` and `Seine` as must-cover. It is deliberately simple:
the smoke tests the pipeline, not the arms' research depth. It is not in the
selection or held-out sets.

## The gate

- The null arm must produce the contract; a null void is a harness failure.
- Every mapped arm must produce the contract or a recorded exclusion. A void
  fails.
- An exclusion is suspect when the native notes or workers already carry a
  source record; the smoke fails it and the draw is re-run after the adapter
  fix.
- A pseudo-tool-call transcript (`<tool_call>` or `<function=`) is a void, not
  an exclusion; the plugin tools were not invoked, so the draw is re-run.
- The non-null prompt must not carry the wrapper postscript; it must carry the
  arm's native line.
- The search provider must be `exa` or `none`, and no draw may fetch a search
  engine.
- A valid draw must have a live receipt with the frozen caps, a fetch log and a
  scored rubric; an excluded draw must have `exclusion.json` and a reason.
- A valid draw must have a passing `replies.jsonl`: the model pre-flight checks
  every assistant reply against the pinned route.
- The isolation probe (`../probe.py`) must pass; it proves the pinned binary,
  the arm loads and the planted skill/manual controls.

## Run

```sh
cd plan/0113-host-deep-research-ab/harness
python3 smoke/run.py --only null --skip-probe   # one arm
python3 smoke/run.py --force                    # all arms, serial
python3 smoke/run.py --record-only              # consolidate existing draws
```

The record is `smoke/smoke.json`; the draws are under `smoke/draws/`. The
record carries the task, the isolation result, each draw's summary and the
findings.

## The smoke is not a scored draw

The smoke scores are not used in the selection. It proves the pipeline and the
controls; the redo selection runs separately with the frozen budget.

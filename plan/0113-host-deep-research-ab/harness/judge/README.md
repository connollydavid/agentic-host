# plan/0113 judge: Opus 5.5, blind, with a validity gate

**Status: landed 2026-11-27.** The judge is `claude-agent/opus` through the
host's `claude` CLI, which resolves to `claude-opus-5-5`. It scores the blind
report and ledger for completeness (0-4) and creativity (0-4). The validity
gate passed on the clean and broken samples; a malformed reply is rejected.

## The route

```
claude -p --model opus --output-format json
```

The CLI's `modelUsage` records `claude-opus-5-5` (context 1,000,000, output
128,000). The judge is a model other than the reference, as the plan requires.
The route and the resolved model are recorded in every `judge.json`.

## The prompt

The judge sees the question, the must-cover entities, the report and the
source ledger. It never sees the arm, the task key or the run's token count.
It is told not to reward length, token count or confident tone. It returns
only:

```json
{"completeness": 0, "creativity": 0, "rationale": "..."}
```

The judge's score is the sum, 0-8. The selection's pooled score is the
mechanical rubric (0-16) plus the judge (0-24). The lock uses a 1.5-point band,
then the suite-fit, then the judge score, then name order. The token count is
recorded, never a tie-break.

## The validity gate

The gate is the dokimi shape: a clean sample must outrank a broken one, and a
malformed reply must be rejected. The samples are in `validity/`:

- `clean.report.md` names `v2.4.2`, `523b1502` and `64e4a374`, cites two
  sources and closes with a synthesis.
- `broken.report.md` names none of the entities and cites nothing.
- The malformed control is `{"completeness": 5, "creativity": "high"}`.

The recorded run:

```
PASS validity clean: ... "model": "claude-opus-5-5", "completeness": 4, "creativity": 2, "score": 6
PASS validity broken: ... "completeness": 0, "creativity": 0, "score": 0
PASS validity malformed reply is rejected
judge validity: passed
```

The result is in `validity.json`. When the gate fails, the judge is not used:
`judge.json` carries `valid: false`, and the mechanical score stands alone.

## Per draw

```sh
python3 judge/judge.py --draw <selection/draws/arm/task> \
  --task <selection/draws/arm/task/task.json> --question "<question>"
```

The output is `judge.json` beside the draw. `round.py` reads it; a draw with no
judge or an invalid judge contributes 0. The cost is in `cost_usd`, recorded
and never scored.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/judge
python3 judge.py --validity
python3 -m json.tool validity.json
```

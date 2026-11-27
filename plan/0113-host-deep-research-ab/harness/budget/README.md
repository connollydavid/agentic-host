# plan/0113 budget: two-way draws, 3600 seconds, 60 tools

**Status: landed 2026-11-27.** The corrected budget is fixed before the redo
selection and the smoke gate. The cost is recorded in every receipt; no lock,
tie-break or judge reads it.

## The first round's budget failure

The first selection ran five arms concurrently in each task wave, with a
1800-second wall cap and 40 tool calls. Twenty-nine of thirty draws hit the
cap without a ledger; the one valid draw used 103k prompt tokens, 47 tools and
the full 1800 seconds. The waves starved the reference model's provider, so the
round measured the wave width, not the arms. The confirmation then ran four
concurrent draws and produced one valid draw and three voids before the
operator paused it.

## The corrected constants

| Constant | Value |
|---|---|
| Prompt tokens | 200000 |
| Completion tokens | 50000 |
| Tool calls | 60 |
| Wall seconds | 3600 |
| Wave width | 2 |
| Draw order | two-way, interleaved by task; serial when the provider is under load |

The caps live in `contract.CAPS`. `run.py` reads the wall cap from it, and its
default wave width is 2. `confirm.py` uses the same two-way default. A draw
whose budget is exhausted is a void, not a zero-cost success; the receipt's
used counts and the exit status are the evidence.

## What reads the budget

- The receipt: `budget.caps` and `budget.used` (prompt tokens, completion
  tokens, tool calls, wall seconds).
- The driver: the `opencode run` timeout is `contract.CAPS["wall_seconds"]`.
- The selection and confirmation: `--parallel` defaults to 2.

The lock rule in `round.py` and the judge do not read the budget. The first
round's 1800/40 receipts remain historical; the redo draws carry the values
above.

## Reproduce

```sh
python3 - <<'PY'
import sys
sys.path.insert(0, "plan/0113-host-deep-research-ab/harness/contract")
import contract
print(contract.CAPS)
PY
```

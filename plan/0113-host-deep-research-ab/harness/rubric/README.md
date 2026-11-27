# plan/0113 rubric: the mechanical checker and its controls

- Landed 2026-11-27. The rubric scores a draw's report against its source
  ledger, the run's fetch log and the frozen task. The hard gate is a count:
  one cited URL the run did not fetch voids the draw.
- The citation threshold is frozen at **5 of 6** before any draw. A draw whose
  cited-quote support falls below 5 fails the citation component even when it
  scores elsewhere.

## The gates

- **Foreign model.** The receipt's model must equal the pinned
  `api.d07yx58.net/qwen3.6-27b` record: provider, route, deployment id, backend
  and limits. A different model voids the draw. The reply-level check remains
  `model-preflight.py --replies`.
- **Foreign harness.** The receipt's harness must equal the pinned OpenCode
  `v2.4.2` tag and binary digest.
- **Phantom source.** Every URL in the report and every URL in the ledger must
  appear in the run's `fetch-log.jsonl`. One unlogged URL voids the draw.
- **Ledger coverage.** Every URL in the report must have a ledger entry; the
  contract's report check already requires every ledger entry to be cited.

## The components

| Component | Points | Rule |
|---|---|---|
| Cited-quote support | 6 | `6 × supported cited sentences / cited sentences`; a cited sentence is supported when every matching ledger entry's quote appears in its page snapshot after whitespace and Unicode normalisation. Threshold: 5. |
| Known-answer correctness | 4 | Normalised match against the SimpleQA key; known-answer tasks only. |
| Must-cover recall | 4 | `4 × matched entities / entities`; an entity matches its aliases; house tasks with a must-cover list. |
| Numerals | 3 | One point lost per numeral in the report that appears in no cited snapshot; floor 0. |
| Prose | 3 | One point lost per `host-lint --prose` match; floor 0. |

Known-answer and must-cover are alternatives by task kind, so a task's
applicable maximum is 16: 6 + 4 + (the other 4 is not applicable) + 3 + 3. The
plan's 20 points are the union of the two task kinds, not one task's maximum.
Cost is recorded in the receipt, not scored.

## The controls

```
PASS clean house draw scores full: 16.0/16
PASS planted phantom citation voids: phantom source: https://invented.example/claim
PASS foreign-model draw is refused: receipt model is foreign to the pinned route
PASS planted wrong answer misses its key: known_answer=0, score 12.0/16
PASS planted unsupported quote misses the frozen threshold: citation_support=0, score 10.0/16
rubric-probe: 5 checks passed
```

- **Clean draw.** The house task `selection/house-path-crates` in a fixture with
  one fetched source and a snapshot: citation 6, must-cover 4, numerals 3,
  prose 3, total 16/16.
- **Phantom citation.** The clean draw plus a cited URL absent from the fetch
  log: void.
- **Foreign model.** The clean draw's receipt on `qwen3.8-27b`: void.
- **Wrong answer.** The known-answer task `selection/simpleqa-0000` with
  SimpleQA row 1's answer where row 0's key belongs: the known-answer
  component is 0 and the total is 12/16.
- **Unsupported quote.** The clean draw's ledger quote replaced by a sentence
  absent from the snapshot: citation support 0, below the frozen threshold,
  10/16.

## The fixtures

`fixtures/clean-house/` carries the report, ledger, fetch log and one snapshot;
`fixtures/wrong-known-answer/` carries the wrong-answer report and its fetched
snapshot. The probe builds each draw's receipt from the pinned harness, model
and null-arm config, so the receipt digests are the contract's own.

The known-answer key is SimpleQA row 0 (`selection/simpleqa-0000`); the wrong
fixture uses row 1's answer, `Annick Bricaud`, against the key `Michio Sugeno`.
The dataset is the frozen SimpleQA CSV, checked against
`feee3f7e7db3617e94e8fcf1977b756ec420ef8568f4e0fcbbe0e92e9d5fc032`.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/rubric
python3 probe.py
```

The probe fetches the frozen SimpleQA CSV to `/tmp/opencode/simpleqa.csv` when
the cache is absent, then writes the four draws under
`/tmp/opencode/plan0113/probes/rubric/`. `rubric.py` is the checker the
selection and confirmation rounds call; it prints one JSON verdict per draw.

# plan/0113 run contract: one task in; a report, a ledger and a receipt out

- Landed 2026-11-27. The contract is the interface every arm's adapter targets;
  the dry runs use fixtures shaped by each arm's documented output, so they
  prove the adapter and the contract, not a live draw. The live draws land at
  the selection round.

## The task file

```json
{
  "key": "dry-run/contract",
  "question": "Does each arm's output satisfy the report, source-ledger and receipt contract?",
  "must_cover": [{ "entity": "source ledger", "aliases": ["ledger"] }]
}
```

`contract.py` requires `key`, `question` and a list `must_cover`; each item
carries a non-empty `entity`. The task sets freeze their own keys and
must-cover lists later.

## The output

| File | Shape |
|---|---|
| `report.md` | Markdown. Every cited source's URL or ledger id appears in the text. |
| `sources.json` | `{"sources": [{"id"?: "...", "url": "https://...", "quote": "verbatim passage", "locator": "section or paragraph"}]}` |
| `receipt.json` | The task, arm, status, harness, model, search provider, budget and config digests. |

The ledger entry's optional `id` is the arm's own citation key, for an arm that
cites notes by id rather than URL (hffmnnj's `[rn_…]`). The report check accepts
the id or the URL. The quote and locator are required; a paraphrase record does
not satisfy the contract.

The receipt carries:

- `harness`: `tag` and `binary_sha256` from the harness pin.
- `model`: provider, route, deployment id, backend and limits from the model
  pin.
- `search_provider`: the provider the draw used; the dry run records `exa`.
- `budget`: the caps (200000 prompt tokens, 50000 completion tokens, 40 tool
  calls, 1800 wall seconds) and the used counts. The dry run's used counts are
  zero.
- `config_digests`: the task, harness pin, model pin, arm config, and (for the
  null arm) the frozen prompt.

An arm that cannot satisfy the ledger writes `exclusion.json` instead:

```json
{"arm": "...", "task": "...", "status": "excluded", "reason": "...", "evidence": "..."}
```

## The adapters

| Arm | Adapter | Dry-run result |
|---|---|---|
| `null` | `adapters/null.py` | valid: the frozen prompt returns the report and ledger directly |
| `hffmnnj` | `adapters/hffmnnj.py` | valid: the report cites `[rn_…]`; the finding note carries `url` and `quote`, and the body carries `locator:` |
| `kanatami` | `adapters/kanatami.py` | valid: the report cites the worker result URL; the first sentence of `full_text` is the quote and the worker/paragraph is the locator |
| `weizhena` | `adapters/weizhena.py` | excluded: field JSON and a generated report carry no source URL, quote or locator |
| `samber` | `adapters/samber.py` | excluded: the claim record carries URL, access date and confidence, not a quote or locator |

The optional `verify` arm stays out (no license at its pin), and `gptr-mcp` is
an optional MCP server whose admission is the selection round's. Neither has an
adapter in the roster dry run.

## The dry-run output

```
PASS null: valid output and receipt (report 209 chars, sources 1, digests 5)
PASS hffmnnj: valid output and receipt (report 97 chars, sources 1, digests 4)
PASS kanatami: valid output and receipt (report 88 chars, sources 1, digests 4)
PASS weizhena: excluded — The arm outputs structured field JSON against fields.yaml and a report generated from those fields; it carries no source URL, verbatim quote or locator, so the source ledger cannot be populated.
PASS samber: excluded — The researcher's claim record carries the source URL, access date and confidence, but no verbatim quote or locator; the report cites the URL only, so the ledger's quote and locator cannot be populated.
PASS control: an empty quote is rejected
PASS control: a foreign model receipt is rejected
PASS control: a report that cites no ledger source is rejected
contract-dryrun: 8 checks passed
```

## What the checks prove

- **The valid arms** produce a report that cites the ledger, a ledger with a
  URL, quote and locator per source, and a receipt whose harness, model, budget
  and config digests match the pins.
- **The excluded arms** record why their output cannot populate the ledger; the
  reason and the evidence are checked, and a fixture that later grows a source
  record fails the dry run rather than silently passing.
- **The controls** reject an empty quote, a foreign model receipt and a report
  that cites no ledger source. The validator is not a rubber stamp.

## The limits

The dry-run fixtures are representative, not fetched pages. The contract checks
the shape; the rubric checks whether the quote is in the run's fetched snapshot,
whether the URL was fetched and whether the report's claims are supported. The
dry run does not replace a live draw, and the selection round records the
draw's real receipt and fetch log.

The `hffmnnj` note body's `locator:` label is a house convention over the arm's
evidence contract; the run prompt asks the agent to keep it. A note without the
label fails the adapter, and the draw is invalid, not excluded.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/contract
python3 dryrun.py
```

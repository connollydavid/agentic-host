# plan/0113 search provider: Exa, selected and measured

**Status: landed 2026-11-27.** One provider, Exa, is selected in the per-draw
config and measured from the `websearch` tool's own metadata. A live probe
returned eight results and recorded `provider: exa`; the driver writes that
measured value into the receipt and voids a draw whose search provider is
foreign or whose only search is a search-engine fetch.

## The defect the first round carried

The selection driver set `OPENCODE_ENABLE_EXA=1` and wrote `search_provider:
"exa"` into every receipt, but its per-draw config never selected a provider.
A non-interactive draw has nobody to answer the provider form, so the form was
cancelled after a minute and the model fell back to `webfetch`:

```
"tool":"websearch" ... "status":"error" ... "error":"Web search cancelled"
"tool":"webfetch"  ... "url":"https://html.duckduckgo.com/html/?q=%22host-lint%22+VOCABULARY.md+docs+lane"
```

That is the whole mismatch: the receipt said Exa, the tool called nobody, and
the fetches went to DuckDuckGo. The evidence is in the null's selection draw
under `/tmp/opencode/plan0113/selection/null-house-host-lint-docs/events.jsonl`.

## The fix

The per-draw config selects the provider:

```json
"websearch": { "provider": "exa" }
```

with `OPENCODE_ENABLE_EXA=1` in the draw environment. The `websearch` tool then
runs without a form. Its event carries the provider it actually used:

```json
"metadata": { "metadata": { "provider": "exa" }, "content": [ ... ] }
```

The driver reads that value; it never invents it. The receipt's
`search_provider` is the measured provider, `"none"` when the draw made no
`websearch` call.

## The probe

```sh
cd plan/0113-host-deep-research-ab/harness/search-provider
python3 probe.py
```

The probe starts the pinned OpenCode v2.4.2 binary in a scratch `HOME`, asks
for one `websearch` call on the reference model, parses the event, and writes
`probe.json` plus `evidence/`. The recorded run:

```
PASS search-provider: exa returned 8 result(s) for 'OpenCode web search provider Exa' in 62.2s
```

`probe.json` records the harness pin (`v2.4.2`, binary `523b1502`), the model
pin (`qwen3.8-flash-next`, deployment `64e4a374`), the config digest, the
query, the measured provider, the result count, the first URL, the event-log
digest and the controls. `evidence/websearch-event.json` is the tool event
itself; `evidence/events.jsonl` is the full run.

## The controls

- A receipt that names another provider while the tool called `exa` is void:
  `provider_of({"search_provider": "parallel"}, "exa")` raises.
- A fetch to a search engine (`duckduckgo.com`, `google.com`, `bing.com`,
  `search.yahoo.com`) is a foreign provider: the driver voids a draw whose
  only search is that fetch, and the probe's `is_search_engine` control covers
  the DuckDuckGo URL from the defect above.
- A receipt that names the measured provider passes.

## The driver change

`harness/selection/run.py` now:

- writes `"websearch": {"provider": "exa"}` into `arm_config`;
- parses completed `websearch` tool events and takes the provider from
  `state.metadata.metadata.provider`;
- writes that measured provider into the receipt, and records
  `websearch_calls`, `search_provider` and `search_engine_fetches` in
  `score.json`;
- voids a draw whose measured provider is neither `exa` nor `none`, and a draw
  that reaches a search engine without a `websearch` call.

The confirmation driver imports the same `run` module, so the confirmation
draws inherit the fix.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/search-provider
python3 probe.py          # live: needs ROPE_BEARER and the pinned binary
python3 -m json.tool probe.json
```

# plan/0113 model pin: the named `qwen3.6-27b` route

- Pinned 2026-11-27 from the router's `/v1/model/info` record.
- The reference model is `Qwen3.8-Flash-Next` on strata, reached through the
  exact named entry `qwen3.6-27b`; the name `qwen3.8-flash-next` has no named
  entry and resolves through the `qwen*` and `*` wildcards, whose deployment
  ids are different.

## The pin

| Field | Value |
|---|---|
| Provider | `api.d07yx58.net` |
| Named route | `qwen3.6-27b` |
| Deployment id | `159fb72cfac7e532d0c04cd4b32d65eec500fcff4e1d724cc5eef434b5b24969` |
| Backend model | `openai/qwen3.8-flash-next` |
| Max input tokens | 500000 |
| Max output tokens | 524288 |
| Route record | `https://api.d07yx58.net/v1/model/info` |

The run contract sets the session model to `api.d07yx58.net/qwen3.6-27b` for
every role. The router's `/v1/models` list is empty; `/v1/model/info` is the
deployment authority.

## The drift the pin defends against

The `qwen3.6-27b` name survived; its deployment did not. The cut's record at
2026-11-26 21:26 was:

| Field | Cut record | Pinned record |
|---|---|---|
| Deployment id | `2f8863340f6db4763ff3bf04b236dde977d79042b87385862a462a4d6564d2ff` | `159fb72cfac7e532d0c04cd4b32d65eec500fcff4e1d724cc5eef434b5b24969` |
| Backend model | `openai/qwen3.8-27b` | `openai/qwen3.8-flash-next` |
| Max input tokens | 262144 | 500000 |
| Max output tokens | 32768 | 524288 |

A pin on the name alone would have drawn the old 27B deployment after the
name moved. The pin is the deployment id and the backend, and the pre-flight
voids the cut's record as foreign. The wildcard entries carry their own ids
(`qwen*` `64e4a374…`, `*` `74f7315a…`), so the default spelling is not a
substitute for the named entry.

## The reply ledger

The run contract records one JSON object per assistant reply, one line per
reply:

```json
{"provider": "api.d07yx58.net", "model": "qwen3.6-27b"}
```

`model-preflight.py --replies <file>` passes only when at least one reply is
present and every reply carries the pinned provider and route. One foreign
model id, one foreign provider, or an empty ledger voids the draw.

## The probe output

```
PASS model-preflight: ok route=qwen3.6-27b deployment=159fb72cfac7e532d0c04cd4b32d65eec500fcff4e1d724cc5eef434b5b24969 backend=openai/qwen3.8-flash-next limits=500000/524288
PASS replies: two pinned replies passes
PASS replies: one foreign model id is void
PASS replies: one foreign provider is void
PASS replies: an empty ledger is void
PASS route: the cut's old deployment record is void
PASS route: a missing named entry is void
model-probe: 7 checks passed
```

## What each check proves

- **The live route.** The router's named entry still resolves to the pinned
  deployment id, backend and limits. A missing `ROPE_BEARER`, a missing entry,
  or any of the four fields moving is a void.
- **The clean ledger.** Two pinned replies pass.
- **One foreign model id.** `qwen3.8-27b` beside a pinned reply voids the draw.
- **One foreign provider.** The pinned model name under another provider voids
  the draw.
- **An empty ledger.** No reply is not a clean draw.
- **The cut's old deployment record.** The record the cut saw is void under
  this pin.
- **A missing named entry.** An empty record is void.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/model-pin
export ROPE_BEARER=...   # the router bearer, never committed
python3 probe.py
```

The pin is in `model-pin.json`; `model-preflight.py` reads it for both the
route check and the reply check.

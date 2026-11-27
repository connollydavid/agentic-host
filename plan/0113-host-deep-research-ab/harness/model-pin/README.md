# plan/0113 model pin: strata's `qwen3.8-flash-next`

- Pinned 2026-11-27 from the router's `/v1/model/info` record, on the
  operator's correction: the reference route is strata's `qwen3.8-flash-next`,
  not the legacy `qwen3.6-27b` name.
- The router carries no exact named `qwen3.8-flash-next` entry. The name
  resolves through the `qwen*` entry; the pin is that entry's deployment id,
  backend and limits.

## The pin

| Field | Value |
|---|---|
| Provider | `api.d07yx58.net` |
| Route the engine sends | `qwen3.8-flash-next` |
| Router entry | `qwen*` (wildcard) |
| Deployment id | `64e4a3742445b5bf58b5e6b75f83b9a84b87cfe19b47692b7984419f71804bf6` |
| Backend model | `openai/qwen3.8-flash-next` |
| Max input tokens | 500000 |
| Max output tokens | 524288 |
| Route record | `https://api.d07yx58.net/v1/model/info` |

The run contract sets the session model to
`api.d07yx58.net/qwen3.8-flash-next` for every role, and the per-arm config
overrides every arm agent's model to that route. The router's `/v1/models` list
is empty; `/v1/model/info` is the deployment authority.

## The wildcard is the route, the id is the pin

The `qwen3.8-flash-next` name matches the `qwen*` entry first. A second
wildcard, `*`, has its own deployment id
(`74f7315a44e446ca4413e24acc607c0912141b23a2d456975ed1b52407d7285d`) and the
same backend. The engine's name is not an exact named entry, so the pin is the
`qwen*` entry's deployment id; the `*` entry is a different deployment and the
pre-flight voids a record that carries it.

The legacy `qwen3.6-27b` entry also routes to `openai/qwen3.8-flash-next` now,
with deployment `159fb72cfac7e532d0c04cd4b32d65eec500fcff4e1d724cc5eef434b5b24969`.
It is a legacy name for the same backend, not the reference route; a draw whose
receipt says `qwen3.6-27b` is foreign under this pin. At the cut that entry
pointed at `openai/qwen3.8-27b` with deployment `2f886334…` and 262144/32768
tokens; the name moved under the cut, which is why the deployment id, not the
name, is the anchor.

## The reply ledger

The run contract records one JSON object per assistant reply, one line per
reply:

```json
{"provider": "api.d07yx58.net", "model": "qwen3.8-flash-next"}
```

`model-preflight.py --replies <file>` passes only when at least one reply is
present and every reply carries the pinned provider and route. One foreign
model id, one foreign provider, or an empty ledger voids the draw. A live
completion through the same edge echoes `qwen3.8-flash-next` in the response's
`model` field, so the ledger records the route the draw sent.

## The route and reply probes

`model-preflight.py` with no arguments fetches `/v1/model/info`, finds the
`qwen*` entry and checks its deployment id, backend and limits.
`--record PATH` reads a saved record for the drift controls. `--replies PATH`
checks a draw's reply ledger.

## The probe output

```
PASS model-preflight: ok route=qwen3.8-flash-next via=qwen* deployment=64e4a3742445b5bf58b5e6b75f83b9a84b87cfe19b47692b7984419f71804bf6 backend=openai/qwen3.8-flash-next limits=500000/524288
PASS replies: two pinned replies passes
PASS replies: one foreign model id is void
PASS replies: one foreign provider is void
PASS replies: an empty ledger is void
PASS route: a drifted wildcard deployment is void
PASS route: a missing wildcard entry is void
model-probe: 7 checks passed
```

## What each check proves

- **The live route.** The router's `qwen*` entry still resolves to the pinned
  deployment id, backend and limits. A missing `ROPE_BEARER`, a missing
  wildcard entry, or any of the four fields moving is a void.
- **The clean ledger.** Two pinned replies pass.
- **One foreign model id.** `qwen3.8-27b` beside a pinned reply voids the draw.
- **One foreign provider.** The pinned model name under another provider voids
  the draw.
- **An empty ledger.** No reply is not a clean draw.
- **A drifted wildcard deployment.** The `*` entry's id is void under this pin.
- **A missing wildcard entry.** A record that carries only the legacy
  `qwen3.6-27b` entry is void.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness/model-pin
export ROPE_BEARER=...   # the router bearer, never committed
python3 probe.py
```

The pin is in `model-pin.json`; `model-preflight.py` reads it for both the
route check and the reply check.

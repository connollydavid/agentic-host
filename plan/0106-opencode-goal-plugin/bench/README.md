# The plan/0106 A/B kit

The staged harness for the dokimi program: prompt arms over the continuation body,
mechanical scoring, draws captured unedited. The kit runs from any host that can reach
the Fen endpoint; nothing here needs credentials for the dry run.

## The channel (as handed over, 2026-10-29)

- Direct LAN: `http://192.168.21.57:8080/v1` (or `http://rope.d07yx58.net:8080/v1`),
  OpenAI-compatible, model `qwen3.5-4b` (the only name; text and vision). No API key;
  any non-empty bearer string is ignored. UFW scopes 8080/tcp to 192.168.21.0/24 on
  purpose; WAN clients go through `https://api.d07yx58.net/v1`, which requires the
  bearer at the edge.
- Measured reachability from this host (192.168.178.0/24): the box answers ICMP
  (207 ms, a routed path), but 8080 and 4001 are filtered by the deliberate scope and
  the WAN edge returns 401 without the bearer. The channel is therefore refused from
  this machine until the bearer is handed over or the scope is widened; the kit is
  endpoint-driven and runs unmodified from a host inside the scope.
- Capacity: 64K context total, `max_tokens` hard-capped at 8192 per decode; budget
  prompt plus output within 64K.
- Gotchas the kit respects: never `temperature: 0` (greedy-decoding loops; the kit
  sends no sampling params by default, so the server's thinking recipe applies: temp
  0.6, top_p 0.95, top_k 20, min_p 0); responses begin with `<think>` and everything
  through `</think>` is stripped for scoring (raw is saved unedited); `<|think_off|>`
  in the system message disables reasoning for classifier-style calls; `json_schema`
  response format 400s on this server (use `json_object`, or the router at
  `http://192.168.21.57:4001/v1`); the same scope applies to 4001.

## Files

- `make-fixture.sh`: builds one state fixture (the ready-frontier mechanical task) in
  a scratch git project: a minimal plan room, the goal armed with the real binary, the
  `goal show` and `tasks` emissions captured. Env: `HL_BIN` (the host-lifecycle
  binary; default the canonical musl build), `FIXTURE_DIR` (default a mktemp dir,
  printed on exit).
- `rubric.py`: the mechanical scorer. Input: the emission file and the reply file.
  Output: one point per check, six total: ACTION marker present; the NEXT line's
  command appears verbatim (for a `work <key>` NEXT, the `tasks --record <key>`
  invocation); the record invocation present; the re-orient (`goal show`) present;
  zero-invented (every `host-lifecycle <verb>` token in the reply names a real verb);
  the state gate (zero commands on the NEEDS YOU and parked states). Deterministic
  string operations only; no model, no network.
- `controls/`: the positive control (an ideal reply, must score 6) and the negative
  control (an invented-verb, no-reorient reply, must score at most 3). The dry run
  asserts both, offline.
- `run-ab.py`: the draw harness. Env: `FEN_ENDPOINT` (required for live draws),
  `FEN_TOKEN` (optional; ignored by the direct endpoint, required at the WAN edge),
  `FEN_MODEL` (default `qwen3.5-4b`), `FEN_DRAWS` (default 3 per arm per state),
  `FEN_MAX_TOKENS` (default and cap 8192). Arms A (bare emission plus "Work the NEXT
  line."), B (emission plus the door doctrine), C (B plus one exemplar ACTION block),
  D (B with the negative rule leading). Draws are saved unedited to
  `samples/<state>-<arm>-<n>.md`; the rubric scores the stripped text. No explicit
  sampling params are sent (the server's thinking recipe is the deployment envelope).

## The dry run (the #stage-kit verify)

    bash make-fixture.sh
    python3 rubric.py --emission "$FIXTURE_DIR/emission.txt" --state ready-frontier \
      --reply controls/positive.md   # expect 6
    python3 rubric.py --emission "$FIXTURE_DIR/emission.txt" --state ready-frontier \
      --reply controls/negative.md   # expect <= 3

No network, no credentials. The dokimi program (`#ab-program`) runs `run-ab.py` from
a vantage that reaches the endpoint; the selection and confirmation protocol is
recorded in the plan README's design gates.

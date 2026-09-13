# lemgate

The lem address rule, enforced on the wire. An OpenAI-compatible reverse
proxy: forwards to the upstream, scores the visible reply (think blocks
stripped then re-attached), and on violation re-requests once with the
violation named. The client sees a clean reply or the original plus the
`x-lemgate` audit block.

## Run

```
set LEMGATE_UPSTREAM=https://api.d07yx58.net
python lemgate.py          # listens on 127.0.0.1:8787
```

Point the client at `http://127.0.0.1:8787/v1` instead of the edge.
`LEMGATE_MODE=off` passes through; `LEMGATE_MAX_RETRIES` defaults to 1.
Streaming requests pass through unscored (v1 limit).

## Tests

```
python -m unittest test_gate
```

## Known trade

Strict mode treats third-person `lem` in a reply as a violation. A reply
that legitimately discusses models in the third person gets one rewrite
and, if still flagged, passes with `clean: false` in the audit.

# fen-acceptance: the weak-agent probes on the citation form (2026-09-05)

Status: **the probes are owed.** The kit is built and preserved here; the channel refused the session's credentials, and the attempt is labeled rather than simulated away.

## The kit

[fen-program.py](fen-program.py) runs the whole acceptance in one command once a channel exists:

```
FEN_ENDPOINT=… FEN_TOKEN=… FEN_MODEL=qwen3.5-4b python3 fen-program.py
```

Protocol: the plan/0076 corrected protocol exactly as plan/0080's thinking kit carried it (thinking on through the chat template, the model card's thinking-general parameters, the answer read after the closing `</think>`), two draws per probe, results appended to `fen-results.md` after every cell. The kit was checked against the last corrected protocol before running, per the 2026-08-08 lesson, and the prompts live beside it: [fen-p1.txt](fen-p1.txt), [fen-p2.txt](fen-p2.txt).

- **P1, production legibility** (both draws must pass): handed the doctrine sentence as instruction, the model writes a citation of a foreign record. Pass = the output is a markdown link whose URL path names the cited `call/0045` file — the accepted form, produced from the rule.
- **P2, reading safety** (both draws must pass): handed a green gate verdict whose tail carries the citation count line, with an unrelated stated task. Pass = the named next action serves the task, and does not remediate the cited record. This is plan/0078's enumeration-captures-the-agent finding applied to the new line: the count must inform and not capture.

## The attempt, labeled

The gateway behind TLS at `api.d07yx58.net` is up: `/v1/models` answers HTTP 401, an auth refusal, not a dead host. The session's environment carries no `FEN_ENDPOINT`/`FEN_TOKEN`/`FEN_MODEL` (the plan/0080 discharge used the operator's channel credentials, which were session-scoped), and no credential is persisted anywhere on this machine — the prior kits under `~/agentic-host-work/` read the environment and none records it. No ballot was simulated and no transcript fabricated; there is nothing here that looks like a run.

## What ships without the probes

The release does not stand on the probes: the mechanism is checked by the sweep's own tests (six unit, two exit-path, three mutation kills), the cast and adversarial rounds on the built diff, and the obligations discharge. What the probes alone can measure is whether the real weak model produces the form from the doctrine and ignores the count line — the owed work, discharged the moment a channel exists, per the plan/0080 pattern.

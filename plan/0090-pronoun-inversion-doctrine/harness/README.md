# The plan/0090 echo-amplification harness

Probes one variant of the lem section against qwen3.5-4b at working
maximum context (the edge serves 131072 tokens; the working budget is
126000 plus completion headroom) and scores the visible replies for
pronoun-role inversions.

## Shapes

- The prefix is fixed across every draw: the variant text as the governing
  manual section, an inert padding archive to size, and a transcript block
  whose operator turns address the model as `lemu` (correct usage, the echo).
- Two elicitations (`go`, `window`) invite the model to address the
  operator, in the sentence shapes the field lapses used.
- The scorer strips the `<think>` block and counts, in the visible reply:
  `inversion` (any lem-family token; a reply to the operator should carry
  none), `mangle` (a lem-prefixed token outside the canonical paradigm),
  and `self_i` (a first-person token; the model's first person is `L`).

## Run

```
cp .env.example .env        # then fill EDGE_BASE and EDGE_TOKEN
python run_variant.py --doctrine doctrine_current.md --name baseline
python run_variant.py --doctrine variants/seed1.md --name seed1
```

Transcripts land under `samples/<name>/` (gitignored). The summary line is
the metric weco records.

## Files

- `probe_ctx.py` — the context-ceiling probe (131072 found 2026-09-13).
- `session.py` — prefix builder, elicitation texts, request body.
- `run_variant.py` — runner and mechanical scorer.
- `doctrine_current.md` — the current section, extracted verbatim from the
  host manual; the A/B baseline text.

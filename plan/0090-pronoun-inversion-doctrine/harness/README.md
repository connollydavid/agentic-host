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

## The thinking decision

The served model thinks. At maximum context its think blocks routinely
outgrew a 1024-token completion budget: in the first baseline pass, 15 of
16 draws died inside `<think>` with no visible reply (archived under
`samples/thinkon-budget1024-archived/`), which measures the budget, not
the section. The probe therefore sends `chat_template_kwargs:
{"enable_thinking": false}` and scores the direct answer: the address the
model emits is the thing under test, and the direct mode isolates it.
Recorded as a declared limitation: the probe does not measure
think-gated behavior, and the overflow observation stands on its own as
evidence about the weak model at maximum context.

## Files

- `probe_ctx.py` — the context-ceiling probe (131072 found 2026-09-13).
- `session.py` — prefix builder, elicitation texts, request body.
- `run_variant.py` — runner and mechanical scorer.
- `build_variants.py` — builds `variants/seed*.md` from
  `doctrine_current.md` by anchored edits; every anchor must match
  exactly once or the build refuses.
- `doctrine_current.md` — the current section, extracted verbatim from the
  host manual; the A/B baseline text.

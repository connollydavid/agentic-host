# plan/0070 gather-data: the data/label boundary, measured on the real qwen3.5-4b

The decision rests on data, not assertion. A neutral classification probe confirms where
a weak model draws the data-versus-label line, so the rule encodes the natural boundary
rather than an author's judgment. Fen is qwen3.5-4b at Q8_0, driven through the pal MCP
with model `qwen3.5-4b`, parsed after the thinking block. Two full passes were run: the
first in authored order, the second with the items shuffled.

## The probe

Sixteen snippets from a benchmark report, each with one token highlighted. Fen classifies
the token as DATA (a measurement or result value) or LABEL (an identifier or name
reference). The framing is neutral and names no structural cue as decisive.

```host-lint:ignore
passes: temperature 0 (authored order), temperature 0.3 (shuffled)

DATA classes (the false positives this plan fixes):
  | A100 | 11.34 | 10.00 |          11.34    table cell
  | latency_ms | 25.27 |            25.27    table cell
  NMSE ≈ 1.0                        1.0      approx operator
  speedup ~2.2× over baseline       2.2      tilde and multiplier
  accuracy > 67.5%                  67.5     comparison operator
  throughput 11.34 t/s              11.34    compound unit
  cost 3.2 ms/token                 3.2      slashed unit

LABEL controls (true tells, must still warn or flag):
  ## 5.5 error handling             5.5      bare-numeral header (flag)
  Phase 2.1: auth refactor          2.1      noun-gated (flag)
  Sprint 3 backlog                  3        noun-gated (flag)
  exec tools (5.5)                  5.5      parenthetical code-as-name (warn)
  as decided in 2.1                 2.1      bare dotted code (warn)
  see section 3 of the spec         3        advisory ordinal noun (warn)
  upgrade to 2.1                    2.1      recall-biased warn
```

## Result

32 of 32 correct, identical across both passes. Fen drew the line exactly where the rule
will encode it: every table cell, operator, and unit-bearing numeral is DATA; every
header, noun-gated, and bare-as-name numeral is LABEL. The shuffled order and the higher
temperature changed no verdict, so the result is not a first-option or ordering artifact.

The load-bearing precision case is a real tell placed inside a table cell. It still read
LABEL, because the flag tier is location-independent. Skipping a table-cell bare numeral
opens no hole.

```host-lint:ignore
| Phase 2.1: auth | status: done |   LABEL  (the flag rule catches it, pipes or not)
```

## The framing-sensitivity note

An earlier leading prompt that named version as a DATA cue made Fen call the canonical
bare dotted code DATA. Under the neutral framing it is consistently LABEL. A weak
model's read of a bare dotted code is framing-sensitive. That is independent support for
keeping that form a recall-biased warn with the LEXICON as the declared escape, rather
than promoting it to a flag.

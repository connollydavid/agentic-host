# The word-effectiveness sweep (2026-10-20)

Six teaching-line variants, one word dimension each, sixteen draws per
variant on the real qwen3.5-4b at deployment sampling, strict ACTION-line
scoring with the zero-invented invariant (the mechanical rubric: the
scoring layer that stands, per the judge-tier verdict the same day).

| variant | strict | empty | invented |
|---|---|---|---|
| V0 current | 14/16 | 0 | 0 |
| V1 terse (half the words) | 8/16 | 7 | 0 |
| V2 do-verb (`do` for `work`) | 13/16 | 0 | 0 |
| V3 format-first (reply rule first) | 6/16 | 10 | 0 |
| V4 no-frame (drop the host-loop sentence) | 13/16 | 0 | 0 |
| V5 ste-strict (simplified words, full sentences) | 14/16 | 0 | 0 |

## What the words are worth (the standing table)

- **The if-then scaffolding is load-bearing.** Compressing the conditionals
  away (V1) or reordering them after the reply rule (V3) collapses adherence
  and breeds empty replies (7 and 10 of 16: a confused model thinks longer
  and exhausts the reply budget). Terseness past the structure is
  destruction, not economy.
- **The register is free.** V5 simplifies every word to the STE-approved
  register, keeps full sentences, and holds V0's full effect at about 40
  percent fewer words. Simplification wins whenever the structure survives.
- **The verb is indifferent.** `work <key>` versus `do <key>` measures no
  difference; keep `work` (already shipped, already measured).
- **The frame sentence earns nothing.** "governed by the host loop" drops
  without measurable cost; it stays only if the spine wants the naming.
- **V0's earlier 16/16 was favorable sampling**: the fresh re-baseline reads
  14/16, the honest reference for future comparisons at this n.

## The ruling

V5 ships as the teaching-line text: equal measured effect, fewer words, the
STE register the spine already mandates. The staged terse variant (V1) is
refused by its own measurement and retires.

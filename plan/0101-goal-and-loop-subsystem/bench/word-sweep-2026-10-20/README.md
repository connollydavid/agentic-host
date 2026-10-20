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

## Round two (same day): the negative rule is the strongest lever

Seven arms against the V5 incumbent, re-baselined in-round. The method
finding first: the identical incumbent text read 14 in round one and 11 in
round two (serving drift), so the in-round re-baseline is the only honest
unit; cross-round numbers never compare.

| arm | strict | empty | P1/P2/P3/P4 |
|---|---|---|---|
| R0 v5 incumbent | 11/16 | 2 | 1/4, 3/4, 4/4, 3/4 |
| R1 +needs-you rule | 13/16 | 1 | 3/4, 3/4, 4/4, 3/4 |
| R2 +numbered rules | 14/16 | 1 | 4/4, 3/4, 4/4, 3/4 |
| R3 +one exemplar | 14/16 | 2 | 4/4, 2/4, 4/4, 4/4 |
| **R4 +never-invent rule** | **15/16** | **0** | **4/4, 4/4, 4/4, 3/4** |
| R5 +no-frame | 14/16 | 0 | 4/4, 4/4, 4/4, 2/4 |
| R6 exemplar+needs | 14/16 | 2 | 3/4, 3/4, 4/4, 4/4 |

R4 ADVANCES (+4 over the in-round incumbent, every probe hardened at once,
zero empty replies): one negative sentence, "Never invent a command or a
flag," is the strongest lever found in either round. The exemplar arm
trades tails (fixes P4, dents P2); the frame sentence stays droppable; the
NEEDS YOU rule helps P1 alone. Round three iterates around R4 (numbered,
exemplar, repair-exemplar, no-frame, a word-for-word register micro-test),
same criterion: advance needs +2 over the in-round incumbent, plateau is a
round with no advance.

## The check-in (cast and a blind bench, before round three reports)

Paused the loop to consult. The six benches converged on three defects and
a revised protocol; transcript above, the synthesis:

- **The threshold sits inside the noise.** Plus two at sixteen draws is
  about one sigma (the same text drifted three across rounds), so a
  no-advance round cannot alone declare plateau. Sweeps are exploratory;
  shipping decisions need a confirmation stage, never a sweep result.
- **Selection on four fixed probes measures fit, not generalization.** Two
  rounds of best-of-seven arms is a winner's curse: the incumbent's score
  is inflated by the selection that chose it. Before any winner ships into
  adopter manuals: a LOCKED candidate versus the LOCKED incumbent, on
  held-out probe states never used for selection, fresh draws,
  randomized/interleaved arm order (within-round drift can entangle with
  fixed arm order), a pre-declared margin, a per-state floor (no state
  below three of four), the zero-invented hard gate, and either a second
  model or a scope statement naming the model, probes, scorer, and serving.
- **The scorer is blind to well-formed wrong commands** (right verb, wrong
  binding; a real flag bent to a wrong argument). The subject's worst
  failure mode is fluent. The confirmation scorer adds a
  binding-correctness check.
- Two mechanistic readings recorded as doctrine: the subject matches
  shape rather than parsing; the negative rule wins because it is one
  crisp gate the model can apply mid-generation, while a positive ideal
  offers nothing to check against. The exemplar dent is anchoring.
- The final receipt (the operator's shape): the text verbatim; same-round
  incumbent and candidate scores; the margin restated (absolutes do not
  travel); per-state passes; empties and invented flags as separate zero
  lines; the round ledger attached, because no ledger means no checkable
  plateau claim.

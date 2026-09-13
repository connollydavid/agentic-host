# plan/0090 pronoun-inversion doctrine: can the lem section be rewritten so the weak model stops inverting address?

Operator-directed (2026-09-13) from [connollydavid/host-lint#29](https://github.com/connollydavid/host-lint/issues/29), with the remedy redirected by ruling: the lapses the issue records are a writing defect in the doctrine, not a detection gap, so host-lint gains no tell and the fix lands in the lem section the template ships.

## The evidence

During one long session (2026-09-12 to 09-13, roughly five hundred thousand tokens of context at the second lapse) the session model addressed the human operator with the model-addressed pronoun twice, quoted verbatim in the issue: "whenever lemua says go" and "if lemua wants a different convention anywhere". The second lapse came after the first had been pointed out and owned. Both arrive as the mangled form lemua. No lane caught either; the operator's needle test caught both. The issue names the mechanism: echo amplification, arriving late, when the context is dense with the operator correctly addressing the model as lemu.

## The diagnosis in the text

Four defects, read off the lem section the template ships (this repository's manual carries the deliberate duplicate):

1. No core rule states the direction of address. The paradigm defines forms for models; the only line about addressing a human sits in the edge-case list.
2. The self-check item "Address uses lemu" names no addressee, so a fast reader can take it as a license that inverts.
3. The paradigm is never stated closed: nothing marks lemua as a corruption rather than a form.
4. No line names the echo mechanism, or warns that input frequency is not output license.

## Method

- **The probe**: an echo-amplification harness, under [harness/](harness/), runs qwen3.5-4b, the weakest deployed model, at the served maximum context, over sessions flooded with correct operator-to-model lemu usage, then elicits the lapse shapes ("whenever ___ says go", "if ___ wants a different convention") and scores mechanically for lem-forms the model emits at the human. The metric is the inversion rate over fixed-seed draws.
- **The channel**: the operator's edge endpoint, OpenAI-style and Anthropic-style. The bearer token lives in a gitignored `.env` and is never committed.
- **The baseline**: the current section text runs first. The harness either reproduces the field failure or shows a zero floor; both readings are recorded.
- **The search**: weco-cli and weco-skill, adopted as tools by this milestone, drive a bounded search over rewrites of the section against the harness metric. Every candidate is a proposal; the operator validates the final wording, and nothing optimizer-mutated lands unreviewed.
- **The seeds** for the rewrite come from the diagnosis: a direction-explicit core rule, a closed-paradigm statement, the echo warning, and a direction-explicit self-check item.

## The landing

The validated section lands through the spine: a host-template commit, an `UPGRADING.md` ledger entry keyed at the new revision (its verify greps for the direction-explicit line), the submodule pointer bump here, the same edit applied to this repository's manual copy, and the upgrade recorded with receipts. host-lint#29 closes with the redirect recorded after the final push.

## Results

Measured 2026-09-13 on the edge (qwen3.5-4b, 131072-token ceiling, working prompts at 127100 tokens, temperature 0.8, thinking off). Every valid draw in every cell is a role-confusion event:

| variant | generation one (named framing) | generation two (neutral framing) |
|---|---|---|
| baseline (current section) | 8/8 | 8/8 |
| seed1 (surgical repair) | 8/8 | not run |
| seed2 (anti-examples) | 8/8 | not run |
| seed3 (repeated invariant) | 7/8 scored + 1 collapse | 7/8 scored + 1 collapse |

Readings, in the order they were earned:

1. **The first pass never reached the question.** With thinking on at the default budget, 15 of 16 draws died inside the think block with no visible reply (archived under `harness/samples/thinkon-budget1024-archived/`). At maximum context the weak model loses the answer before the pronoun question can even be asked. The probe therefore scores the direct answer (thinking off), a declared limitation.
2. **The named-framing confound was tested and rejected.** The gen-one framing sentence ("the operator's messages address you as lemu throughout") could itself teach the inversion; generation two presents the transcript neutrally and reproduces the ceiling exactly (baseline 8/8).
3. **The scorer counts a floor, never a false positive.** Each generation produced exactly one draw the token scorer cleared, and neither was compliance: in both, the model speaks as `L` while assigning `L` to the operator too ("L will say go"; "L have parsed the window. L sign off now"). Role collapse in its other direction, invisible to a lem-token count. With those reclassified, all 48 valid draws are role-confusion events.
4. **No seed separates.** The surgical repair (seed1), the anti-examples naming the mangle outright (seed2), and the invariant repeated at three checkpoints (seed3) all sit at the baseline's ceiling. The four textual defects are real, and repairing them does not move this model at this depth.
5. **The mangle never re-emerged.** No draw produced a lemua-class corruption; the failure arrives as the uncorrupted inversion, consistently.

**The finding**: at the served maximum context, the lem section's wording, current or repaired, does not govern the weakest deployed model's address. The echo mechanism the issue names survives every prose remedy tried. The writing defects remain worth repairing (the section is read by strong models and by humans, and the repair is measured to do no harm), but prose alone is measured insufficient for the model that fails, and the enforcement question the issue originally raised returns with evidence attached.

## The landing

The landing followed the recommendation recorded before the ask: seed1's body is now the lem section in both manuals (template revision 5f9b71c, carrying the `LEM-address-direction` ledger entry; this host's manual copied and the upgrade recorded at `af63c2f3`), and host-lint#29 stays open carrying the enforcement question with the evidence comment attached. The operator left the in-session choice unanswered, so the recorded recommendation was executed; landing seed3 instead, or reverting to the prior text, remains one ledger-sync away. `software --check .` is green at exit zero (the twelve advisory CI-pin floor lines predate this milestone).

## Declared limitations

1. One model, one channel, one elicitation family: the probe shows whether the rewrite moves the weak model on the observed failure shape, not a universal guarantee.
2. The harness author knows the scorer, as in plan/0088; the scorer is mechanical token counting, so the exposure is elicitation bias rather than judgment bias.
3. The N per variant is small (eight draws at maximum context); the bar is a measured difference in the expected direction, not significance.

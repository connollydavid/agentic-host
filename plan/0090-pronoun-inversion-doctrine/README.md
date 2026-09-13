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

Recorded as runs complete; the baseline row lands first.

## Declared limitations

1. One model, one channel, one elicitation family: the probe shows whether the rewrite moves the weak model on the observed failure shape, not a universal guarantee.
2. The harness author knows the scorer, as in plan/0088; the scorer is mechanical token counting, so the exposure is elicitation bias rather than judgment bias.
3. The N per variant is small (eight draws at maximum context); the bar is a measured difference in the expected direction, not significance.

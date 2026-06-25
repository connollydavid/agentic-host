# gather-data: the prose-lane LEXICON approach at the weak-agent bar

The `#settle-by-data` task. The questions were whether extending the LEXICON mask to the
prose lane is the least-surprising reading, whether the mask should be surgical at the word
boundary, and whether reusing the allowlist opens an abuse surface. The run went direct
against the rope HTTPS endpoint (the OpenAI-compatible front-end to Fen, `qwen3.5-4b`) with a
real system prompt, the sampler at the Qwen thinking-precise values (`temperature` 0.6,
`top_p` 0.95, `top_k` 20, `min_p` 0). The model thinks before it answers, so the judgement is
read off the converged reasoning, the way Fen is always read.

## The system prompt

A senior-engineer reviewer of host-lint, asked to judge a self-contained multiple-choice
design question and answer with the single best option and a short justification.

## Probe one: lane consistency

Given that the naming lane masks a LEXICON phrase and the prose lane does not, what is the
least-surprising prose-lane behaviour for a declared `rehost harness`? The model chose **(A)**,
the prose lane consults the same LEXICON, and rejected the blanket-mute option as
over-permissive and inconsistent with the naming lane's scope logic. So the model expects both
lane consistency and the surgical word boundary.

## Probe two: the abuse guard, and a contamination correction

The first abuse-guard probe offered an option that asserted LEXICON requires multi-word
phrases. The real `validate_lexicon_entry` enforces no such rule: a single legitimate word is
a valid entry, and the guards are a letter requirement, a refusal to launder a flag-tier tell,
and a URL for a tracker reference. The model accepted that false premise, so that pass was
discarded as contaminated.

The re-run offered honest options: two sound "adequately bounded" rationales (the sentence-count
denominator; the provenance guards plus naming-lane symmetry) and one genuine dissent (hold for
a separate stricter prose allowlist). With the dissent on the table, the model chose **(b)**:
the prose lane reuses the same provenance-gated entries the naming lane already masks with, so
it grants no muting power the naming lane lacked. It reconfirmed the surgical semantics, **(ii)**:
after the declared phrase is blanked, only a standalone occurrence of the word still flags.

## Verdict

The direction and the surgical semantics are confirmed, and the dissent option was available
and not chosen. The abuse concern is real and bounded by two facts the model and the code
agree on: the provenance guards make a declaration a visible, enumerated act, and the density
denominator is the sentence count, so a mask removes only its own weight and cannot dilute the
other tells. The recorded rope responses are the evidence trail.

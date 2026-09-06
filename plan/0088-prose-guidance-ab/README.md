# plan/0088 prose-guidance A/B: does naming the banned words help, or do positive exemplars work better?

An auto-research experiment, operator-directed (2026-09-06): invert how the word-choice topic is discussed: instead of prohibition lists, give positive examples: and measure whether it works before changing any doctrine.

## The hypothesis

Prohibition lists have two failure modes with language models. The known one: the model finds synonyms the list does not know, so the slop survives the ban. The suspected one, demonstrated four times in this session: **the detector fires on its own documentation**: a document that names the banned words in order to ban them trips the rule that bans them. The inversion states the target as exemplars: "write like this" names nothing that needs banning.

## Design

- **Writer**: the session model (a strong model that has internalized this session's house style: a declared limitation, below). Each sample is a first draft, generated straight through, never revised.
- **Conditions**, identical except for the guidance sentence appended to the same task prompt:
  - **A (control)**: the bare task.
  - **B (negative list)**: the task plus the current `ai-diction`/`grandiose-noun`/`house-diction` terms and the decoration family, as prohibitions.
  - **C (positive exemplars)**: the task plus two clean exemplar sentences, naming nothing banned.
- **Tasks**: two, both slop-inducing genres: a capability description for a README (T1) and a milestone summary paragraph (T2).
- **Draws**: three per task per condition: 18 samples.
- **Scorer**: `host-lint --prose <file>` per sample; the score is the count of warning lines. The tool is the whole judge; no human reads the samples before scoring.
- The prompts are preserved verbatim in [prompts.md](prompts.md); the samples in [samples/](samples/), unedited.

## Declared limitations

1. The writer knows the scorer: unavoidable, and equally true of every condition, so the *differences* remain informative while the absolute counts do not transfer to an unaware writer.
2. One writer, one session. This is a pilot for the harness; the population the doctrine cares about is the weak model, and the harness reruns with the real qwen3.5-4b the moment a channel exists (the standing owed probe, now with a reusable kit).
3. N = 18 is a pilot's N. The result is directional evidence, not a verdict.

## Result

See [results.md](results.md): the per-sample scores, the condition means, and the reading.

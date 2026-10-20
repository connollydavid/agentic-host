# The dokimi arms run (2026-10-20): the teaching lines measured

Adopted [intel/dokimi](https://github.com/intel/dokimi) at `691c007` as the
standing paired-arms instrument (submodule `tools/dokimi`), and used it
idiomatically on this milestone's own question: do the three teaching lines
help the weak model operate the emission?

- Subject `qwen3.5-4b` on the router (openai provider, `OPENAI_API_BASE`);
  judge `qwen3.6-27b`, a different model per the instrument's own anti-self-
  judge rule. Reply budget 1024 (the serving lesson from the freeze battery).
- Arms: `baseline` (the question carries the ACTION-format ask only) versus
  `profile:teaching-profile.md` (the three teaching lines as the system
  prompt). The four probes are the freeze battery's real tool outputs, with
  the sanctioned move as each question's expected topic.
- Result: baseline 30.8, profile 89.0, paired delta +58.2, 95 percent CI
  [+28.7, +87.8], Cohen's d_z +3.14. Per probe: the composed refusal stays
  hardest even taught (56), the other three score 100 taught. The taught arm
  is also cheaper and faster: 902 completion tokens at 28s against 4096 at
  38s untaught (the untaught model spends its budget flailing).
- This independently replicates the freeze battery's taught-context finding
  (9/16 minimal-context against 16/16 taught) through industrialized paired
  arms with a judge that is not the subject.
- The instrument's free first step also ran on this tree: `dokimi repo scan`
  reported three FAILs, all judged as reads, not defects (two are the
  manual's `NNNN` numbering placeholders, one is the bootstrap's gitignored
  `.claude/skills` symlink layer, machine state by the volatility split).
- One serving artifact recurred: a draw hit the 1024-token ceiling (the
  think-leak again); raise the budget on future runs.

Lab files: `teaching-profile.md` (the profile arm), `goal-loop_golden.json`
(the question set), `arms.md`/`arms.json` (the instrument's own report).

## The judge role, done properly (2026-10-20, same day)

The instrument's own docs are emphatic that a verdict under one judge is a
property of that judge, and prescribe the panel, the validity gate, and the
per-model rule. All three ran.

- **The cross-judge panel** (`cross-judge.json`, `cross-judge.md`): the same
  stored answers re-scored by every judge. Direction unanimous: the stored
  qwen3.6-27b scored +58.2, a fresh qwen3.6-27b pass +73.0, and glm-5.3
  +87.8, each with four wins and zero losses. The sign test stays at
  p 0.125 because n is four; that is sample size, not disagreement.
- **The validity gate** (`validity-qwen3.6-27b.json`): the stored judge
  FAILED its own gate, ordering 61 percent of known-order pairs against the
  80 percent bar (tie rate 22 percent). Under the discipline, its measures
  are shown but do not vote. glm-5.3's validity run and a sequential retry
  for the 27B are in flight; the voting judge is whichever passes.
- **The per-model half** (glm-5.3 as subject, taught versus untaught) is
  queued behind a validated judge, per the same discipline.
- **An upstream wart, recorded for filing**: `eval cross-judge` splits
  `provider/model` but passes the bare model to LiteLLM without the
  provider, which refuses it ("Provider NOT provided"); the working form is
  the double prefix (`openai/openai/glm-5.3`), which is also why the stored
  judge's name carries it. The serving on this endpoint is ollama-backed
  and real, and glm-5.3 answers take a thinking budget (442 completion
  tokens for a one-line reply): size judge calls generously.

## Correction (operator, 2026-10-20)

The model this endpoint serves under the id `qwen3.6-27b` is **Qwen3.8-27B**.
The artifacts retain the id as called (the runs used it verbatim); read
every `qwen3.6-27b` below as Qwen3.8-27B, the mid tier of this endpoint's
judge pool beside the frontier-tier glm-5.3.

## The terse variant, staged not shipped

The audit pass tightened every free text; the teaching profile is measured
text (+58.2 under the stored judge) and is not edited blind. The terse
variant is staged as `teaching-profile.terse.md` (same meaning, half the
words). It ships only if it measures: a three-arm run (baseline, the current
profile, the terse profile) before the spine freezes, judged by whichever
judge passes the validity gate.

## The judge tier verdict: no gated LLM judge on this endpoint (2026-10-20)

The validity chain finished and both candidates failed
(`validity-glm-5.3.json`, `validity-qwen3.6-27b-seq.json`). glm-5.3 scored
31 percent accuracy with a 61 percent tie rate, and scored DAMAGED copies
above originals on three variants (mismatched answer, padding, shuffled
sentences: negative mean drops). The sequential 27B retry scored 61 percent
with every tie decided, failing the same 80 percent bar. Under the
instrument's discipline, no measure on this endpoint votes.

What stands instead is the instrument the house already trusted for exactly
this reason: the mechanical rubric scorer of the freeze battery (strict
ACTION-line matching, zero-invented-commands invariant) is deterministic by
construction and needs no calibration. dokimi's own gate just measured the
house thesis on the judge tier: open-ended LLM judgment at the weak and mid
tier is not reliable enough to score with, while a rubric-bound mechanical
scorer is. dokimi stays adopted: its arms structure, paired design, and
answer capture carry the experiments; the scoring layer is the house rubric.
The word-effectiveness sweep runs on exactly that basis.

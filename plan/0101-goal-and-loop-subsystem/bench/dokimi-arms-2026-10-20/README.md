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

# Treatment-arm comparison — goal-loop

- Model: `openai/openai/qwen3.5-4b`
- Harness: `arms-runner`
- Plugin set: `none` (`sha256:e3b0c44298fc1c149afbf4c8996fb924`)
- Arms: `baseline`, `profile:teaching-profile`
- Baseline arm: `baseline`
- Questions: 4

## Summary (avg aggregate score, 0–100)

| Arm | Avg | Δ vs baseline | n |
| --- | ---: | ---: | ---: |
| `baseline` | 30.8 | (baseline) | 4 |
| `profile:teaching-profile` | 89.0 | +58.2 | 4 |

## Paired significance vs baseline

_Each arm is paired per question against `baseline`. p-values are Holm-Bonferroni-adjusted across the 1 treatment arm(s); **Sig.** uses the adjusted value._

| Arm | Δ (paired) | 95% CI | Cohen's d_z | Effect | p | p (adj) | Sig. | n |
| --- | ---: | :---: | ---: | --- | ---: | ---: | :---: | ---: |
| `profile:teaching-profile` | +58.2 | [+28.7, +87.8] | +3.14 | large | — | — | — | 4 |

## Cost & latency

| Arm | Cost (USD) | Prompt tok | Completion tok | Mean latency (s) | Mean TTFT (s) | Cache hit | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | — | 882 | 4096 | 38.278 | — | 0.0% | 4 |
| `profile:teaching-profile` | — | 1258 | 902 | 28.464 | — | 0.0% | 4 |

## Per-question scores

| Question | `baseline` | `profile:teaching-profile` |
| --- | ---: | ---: |
| Below is the verbatim output of a host-loop tool. Read it an… | 16 | 100 |
| Below is the verbatim output of a host-loop tool. Read it an… | 8 | 56 |
| Below is the verbatim output of a host-loop tool. Read it an… | 41 | 100 |
| Below is the verbatim output of a host-loop tool. Read it an… | 58 | 100 |

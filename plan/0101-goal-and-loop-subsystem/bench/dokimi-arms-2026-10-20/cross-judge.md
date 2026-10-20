## Verdict robustness

Every arm against `baseline`, under each judge and axis. A verdict that holds under one judge only is a property of that judge. Gate: the judge's own `judge-validity` result; a measure whose judge failed it (✗) is shown but does not vote.

| Arm | Verdict | Measure | Gate | Δ | 95% CI | W/L/T | p (sign) | p (Holm) |
| --- | --- | --- | :---: | ---: | ---: | ---: | ---: | ---: |
| `profile:teaching-profile` | **NO DETECTABLE EFFECT** | aggregate · qwen3.6-27b (stored) | — | +58.2 | [+28.7, +87.8] | 4/0/0 | 0.125 | 0.375 |
|  |  | aggregate · qwen3.6-27b | — | +73.0 | [+41.1, +104.9] | 4/0/0 | 0.125 | 0.375 |
|  |  | aggregate · glm-5.3 | — | +87.8 | [+48.8, +126.7] | 4/0/0 | 0.125 | 0.375 |

\* p < 0.05 after Holm over the measures that vote on the arm; two-sided sign test over questions.

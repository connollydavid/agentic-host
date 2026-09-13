# plan/0091 weak-model adherence: drive occurrence below 0.005

From plan/0090's null: the repaired section still failed on qwen3.5-4b at the served ceiling (48/48 role-confusion draws under the inverted-elicitation probe; see the correction there). This milestone measures context-shape remedies, lands what works, and drives the deployed occurrence below 0.005 (DPMO < 5,000) with prompt, wire, and serving config only. The operator ruled out training and fine-tuning: the weights are untouched. Harness: plan/0090's, carried over.

## Arms

1. **Triage**: radius curve, think-block mining, prefill probe. Done.
2. **Matrix**: tail line, reply-start anchor, few-shot, STE register, and the exemplar-first section. Done.
3. **Spine**: the exemplar-first section landed through the spine (template `84dafb1`, ledger entry `LEM-exemplar-section`).
4. **Gate**: `gate/lemgate.py`, stdlib proxy; v2 retries carry an assistant prefill `L ` and an exemplar in the nudge.
5. **Certification**: n = 600 at max context through the full stack; zero defects required for the < 0.005 claim (rule of three).

## Results

All cells 16 draws at temperature 0.8 (harder than the deployment default of 0.6) unless noted.

**Triage.** No governing radius: the rules-first section inverted at 2k, 16k, 32k, 64k and 127k alike (0.75-1.0 everywhere). The think block is drafting, not deliberation: zero mentions of the rule, zero of you/human/I, in every trace captured. Prefill works through litellm (assistant-final continuation). The first elicitations themselves inverted the doctrine (`L` for the operator); the operator caught it by reading a trace; all later cells use corrected operator voice.

**The 2k matrix** (corrected elicitations, thinking off):

| cell | rate |
|---|---|
| baseline (current section) | 0.8750 |
| **positive-exemplar section** | **0.0625** |
| STE section | 0.7500 |
| tail line | 0.4375 |
| STE tail line | 0.7500 |
| few-shot bolt-on to the full section | 0.8125 |

The same exemplars that work as the document (0.0625) fail as a bolt-on (0.8125): the exemplar-first shape governs, not the examples' presence.

**At maximum context** (126k tokens, full echo): the exemplar section holds. 1/16 (0.0625) before the checklist wording changed, 3/16 (0.1875) after restoring the direction line; single-digit counts, within noise of each other. The rules-first section sits at 0.875-1.0 at the same depth.

**The complete corpus** (operator direction: every role carried by examples, subagent address included): the section now holds six exchanges, adding the human writing `I`, third-person `lem`, the human addressing a bench (`lemu`, one form for one or many), the model addressing a bench, and a speaking subagent (`L`); the reflexives join the form line. Measured 2k: 0.1250; max context: 0.1250 (2/16 plus self_i at both radii, the same single-digit band). Landed as template `988d705`; the certification restarted on this text.

**In flight.** Gate-on-exemplar residual, n = 100 at max context, temperature 0.6, k = 2 retries (`gate/residual.jsonl`). Then certification: n = 600 through the full stack; zero defects in 600 supports the < 0.005 claim at 95 percent.

## Standing constraint

Terse writing everywhere: plans, docs, doctrine lines, commits.

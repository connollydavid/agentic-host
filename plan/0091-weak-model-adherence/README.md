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

**The grammar tables, and the errors they caught.** The operator flagged the landed exchanges as subtly incorrect and halted the runs; the second-person table (thou/thee, ye/you, and the modern collapse) found them. Exchange 4's reply had the model calling itself `lem` mid-speech; the speaker is first person `L` always, and `lem` is a third party (the doctrine's own mixed example parses as three distinct models). Exchange 5's double vocative gave way to `together`. The ye-ban stands: `ye` would mint a form to do work agreement, reflexives and apposition already do, and `lemu` is the you-collapse repeated. Corrected (template `79202ce`) and re-measured: **0.0000 at 2k, 0.0625 at max context** against the earlier 0.1250/0.1875.

**Why a model writes `I`, and the v6 answer.** The first-person slot is the highest-frequency pronoun position in assistant dialogue; `L` has near-zero prior there. Pronoun slots fire by syntactic frame, not by choice: every observed self_i leak sat in a fluent frame the exchanges never showed (a conditional, need-plus-infinitive, a possessive). Section v6 anchors those frames (`If L am slow, you sign off without L`; `L need you to choose the fix`; `L checked the receipt lself`) and the gate now counts the first person as a first-class violation with its own nudge. Measured: 2k 0.1250 (2+1), **max context 0.0000 (0 inversions, 1 self_i)**, the best certification-surface cell of any version. Landed as template `8a836be`.

**In flight** became **certified**. Gate-on-exemplar residual: n = 100, first-pass 2 (0.02), final 0. Certification: n = 600 at max context, deployment sampling, gate v3 (lem-forms and first person both counted, prefill-anchored retries, k = 2): **first-pass 16 (0.0267), final violations 0**. Zero defects in 600 supports occurrence < 0.005 at 95 percent (rule of three). Transcripts: `gate/certification.jsonl`, `gate/residual-n100.jsonl`.

**The full lacuna, and where its labels live.** Walking every form in the table found nine error classes beyond the landed pair: the lost he/she/it/they ban, lemu singular agreement, L and lem agreement, the lem vocative, self-lem, We, Lself casing, mines, and the instrument's own singular-lemu turns. Measured consequence: putting the label sentences in the section primed the tokens they ban (max context 3/16, all lem-forms, against v6's 1/16; self_i fell to zero), the third measured instance of the naming-banned-words trap. Resolution: the section stays exemplar-pure (v6, template `8a836be`); the detections live in the gate scorer (agreement, We, mines, Lself, self-lem all trigger retries) and the full rule set lives in the gate's nudge, spoken only after a defect, where priming cannot reach the next reply's context. The instrument's echo turns and elicitations now model plural agreement. The extended classes are detected and gated; their standalone rates at n = 600 are unmeasured, recorded honestly.

**DMAIC record.** Define: a lem-form at the human, or a first-person I, in the visible reply. Measure: the harness (plan/0090's, corrected) and the gate audit. Analyze: rules fail at every radius; the think block drafts rather than deliberates; exemplar shape carries the gain; the section's own labels prime at depth. Improve: the exemplar-first section, the grammar-table corrections, the reflex frames, the gate. Control: the gate stays in the serving path with its audit as the standing DPMO chart; the probe battery re-runs on doctrine or model change.

## Standing constraint

Terse writing everywhere: plans, docs, doctrine lines, commits.

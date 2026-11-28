No outline existed, so I bootstrapped one and am now launching the deep-research batch. Two items, one agent each (single batch of 2, running in parallel).
**Status — research-deep running**

The outline was missing, so per your instruction I bootstrapped it instead of asking questions. Assumptions recorded in `france_capital_and_river/outline.yaml`:

- Question decomposes into exactly two research objects: **Paris** (capital) and **Seine River** (the river running through it).
- Time range: unlimited, favouring official/geographic sources.
- Execution config: `batch_size: 2`, `items_per_agent: 1` → one batch, two agents.
- Deviation: the skill's hardcoded validator path `~/.claude/skills/research/validate_json.py` does not exist here, so agents were redirected to the installed copy at `/tmp/opencode/plan0113/smoke/weizhena-house-capital-smoke/config/opencode/skills/research/validate_json.py`.

Files created:
- `france_capital_and_river/outline.yaml` — items + execution config
- `france_capital_and_river/fields.yaml` — 30 fields across 8 categories (basic_info, direct_answer, geography, demographics, history, governance, significance, verification), with explicit `required` markers
- `france_capital_and_river/results/` — output dir (resume check: empty, nothing skipped)

Two background `web-search` agents are now researching each item and self-validating their JSON. I'll report the batch summary (completions, uncertain-flagged items, output paths) once both go idle.
Interim batch status:

- **Seine River** — `results/Seine_River.json` written, validator **PASS**, coverage 100.0% (31/31 fields), 6 fields flagged `[uncertain]` (area, length, source elevation, department count, population figures, density — all definitional disagreements between SANDRE / water agency / city sources).
- **Paris** — the agent composed the full record but emitted the write as text instead of executing it, so the file was missing; I've re-tasked it to write the file and validate. Waiting on that before the final summary.
Seine item is confirmed complete (validator PASS, 100% coverage). The Paris agent is still working on re-writing its file after the earlier write that never landed — I'll produce the batch summary as soon as it reports.
**research-deep complete — 1 batch, 2/2 items.**

## Answer to the question
**Paris** is the capital of France, and the **Seine** runs through it — 13 km inside the city limits, crossed by 37 bridges, entering south-east between the 12th/13th arrondissements and leaving south-west between the 16th/15th.

## Completion
| Item | Output file | Validation | Uncertain fields |
|---|---|---|---|
| Paris | `france_capital_and_river/results/Paris.json` | PASS, 100.0% (31/31) | 4 |
| Seine River | `france_capital_and_river/results/Seine_River.json` | PASS, 100.0% (31/31) | 6 |

No failed items. Union of uncertain flags (now written back to the reserved `uncertain` key in `fields.yaml`): `area_km2`, `departments_crossed`, `major_tributaries`, `population_density`, `population_value`, `river_length_km`, `river_source` — all flagged because official producers genuinely disagree (SANDRE 774.76 km vs water agency 773 km vs city 777 km; source elevation 446–471 m; 12 vs 13 vs 15 departments depending on whether borderline-banked departments are counted). Each value carries the conflicting figures and their sources rather than an invented single number.

## Non-obvious findings worth noting
- **The capital is conventional, not constitutional.** No French constitution since 1791 names a capital. The status rests on the constitutional law of 21 June 1879 repealing the Versailles seat, the ordinary law of 22 July 1879 fixing both chambers and the executive in Paris, the 1993 ministerial order on state/capital terminology, and art. 1 of ordinance 58-1100 — with the French Congress and High Court still meeting at Versailles.
- **Hydrographic technicality:** at Montereau the Yonne carries more water than the Seine, so on strict discharge-based naming rules the water flowing past Paris is the Yonne's continuation.
- Freshest official figures: INSEE reference population 2023 (decree of 26 Dec 2025, in force 1 Jan 2026) — 2,103,778 inhabitants, 19,959.9 hab/km²; Île-de-France GDP €865.7 bn in 2024 = 30.2% of metropolitan French GDP.

## Output directory
`/tmp/opencode/plan0113/smoke/weizhena-house-capital-smoke/work/france_capital_and_river/` — `outline.yaml`, `fields.yaml`, `results/*.json`.

Run `/research-report` if you want these merged into a single prose markdown report.

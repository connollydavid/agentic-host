# plan/0113 adapter layer: native prompts, adapter-written contracts

**Status: landed 2026-11-27; the five-seat review re-opened the smoke, and the
corrected fresh all-arm smoke passed 2026-11-28.** The live driver sends each
arm its own workflow prompt and lets the arm's adapter write the contract. The
wrapper postscript is gone. The null arm keeps the frozen contract prompt,
because it is the control, not an arm with a native output shape.

## The flow

1. `run.py` prepares the arm's scratch tree and writes the native prompt.
2. `opencode run` executes the arm in the work directory.
3. `prepare_native` copies the arm's documented output into `draw/native/`:
   the hffmnnj library notes, the kanatami workers, the weizhena result JSON,
   the samber research notes, or the final report text.
4. The arm's adapter (`contract/adapters/<arm>.py`) reads `draw/native/` and
   writes `report.md`, `sources.json` and the receipt, or `exclusion.json`.
5. The driver reads every `webfetch` call from the scratch OpenCode database,
   including subagent sessions, into `fetch-log.jsonl` and `snapshots/`, then
   validates the contract or the exclusion and writes `score.json`.

The prompt carries no `report.md`/`sources.json` postscript for a non-null arm.
The arm runs its own workflow; the adapter maps the result.

## The arm mapping

| Arm | Native output | Adapter |
|---|---|---|
| `null` | the frozen prompt's `report.md` and `sources.json` | copies and validates |
| `hffmnnj` | the library notes under `$XDG_DATA_HOME/opencode-deep-research/library/notes` (or `~/.local/share/...`), the report note | resolves `[rn_...]` citations to source records; a direct answer with no note id is an exclusion |
| `kanatami` | the final report and the worker results; `workers.json` if the arm wrote one, otherwise the run's fetch log | maps each cited URL to its worker result; first sentence is the quote, the worker/paragraph is the locator |
| `weizhena` | the structured result JSON and the generated report | builds the ledger from report inline citations; excludes when the report cites no quote/locator; the result URLs are the evidence |
| `samber` | the report's inline citations and the claim notes | builds the ledger from the report's inline `[passage](url)` citations only when every cited URL is in the fetch log; otherwise excludes with the missing count |

The hffmnnj exclusion is live, not a dry-run assumption: the plugin's effort
router sends a narrow question to the Quick tier, where the coordinator may
answer without saving notes. The smoke records that outcome instead of
pretending the note ledger exists. A report that contains `<tool_call>` or
`<function=` is a pseudo-tool-call transcript, not a direct answer: the plugin
tools were not invoked, the adapter raises a void, and the draw is re-run.

## The null control

The null arm's frozen prompt asks for the contract directly, so its adapter is
a shape check and a copy. It must be valid in the smoke; a null void means the
harness, not the arm, failed.

## Verification

- The contract dry run: `python3 contract/dryrun.py` returns 8 checks passed (three
  valid, two exclusions, three controls).
- The live smoke: `python3 smoke/run.py` runs one draw per arm on
  `smoke/house-capital` and checks the native prompt, the adapter, the measured
  provider, the fetch log, the receipt, the rubric and the isolation probe.
- The smoke record is `smoke/smoke.json`; a mapped arm passes on the contract
  or a recorded exclusion, and the null must be valid.

## Reproduce

```sh
cd plan/0113-host-deep-research-ab/harness
python3 contract/dryrun.py
python3 smoke/run.py --only null --skip-probe
python3 smoke/run.py --record-only
```

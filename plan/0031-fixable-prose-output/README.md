# plan/0031 — Fixable prose output: one record per occurrence, a column, a mechanical fix, advisory tiers

> Spun out of `plan/0030`'s D2 (operator: "this needs a plan"). `plan/0030` made the prose lane real
> and walkable (`host-lint --docs`, shipped); this milestone makes its **output weak-agent-fixable** —
> the precondition for `plan/0030`'s triggered clean (D5). The fix-site fork (engine vs host-lint) that
> this plan was opened to settle is **now resolved by investigation**: the defect is a `host-lint`
> localization bug, not an engine over-emission, so the whole milestone is **host-lint-side**
> (see *Diagnosis*). No `host_grammar` change.

## Context

`plan/0030` shipped `host-lint --docs` — the repo-wide prose audit walks authored markdown. But the
prose **output** defeats a weak agent doing the clean (`plan/0030` D5), in three ways:

- **Mislocalization (the headline defect).** `call/0019` has **ten** em-dashes (lines 12, 15, 23, 24,
  34, 38, 41, 42, 56), and the engine correctly emits **one** `decoration` tell per em-dash — but
  `host-lint`'s `locate_line(input, excerpt)` returns the **first** line containing the excerpt, so all
  ten records collapse onto `line 12`. A weak agent sees ten identical `line 12: —` and cannot tell
  which dash is where, that there are ten distinct ones, or when it is done. There is also no **column**.
- **Span-less tropes.** `tell-density` (a whole-document score), `bold-first-bullets` ("21/23 bullets
  open with bold lead-ins"), `anaphora`/`punchy-fragments` (cross-sentence patterns) report a synthetic
  diagnosis whose text does not appear literally in the source. A clean-to-**zero** bar over these is an
  unterminating loop — there is nothing to edit.
- **Volume.** ~1,100+ `--docs` warning-lines across the authored docs; a long mechanical campaign needs
  reliable, located output or a weak agent drifts.

## Diagnosis (resolves the fork)

The fork was "fix the over-emission in the engine vs work around it in host-lint." Investigation showed
there **is no over-emission**: for `call/0019`, em-dashes in the file = 10, `decoration` tells emitted =
10 (one-to-one). The engine is the source of truth and it is correct. host-lint's `locate_line` is the
bug — it maps every tell to the *first* occurrence of its excerpt. So:

- The fix is **host-lint-side and exact**, not heuristic: there are exactly as many tells of a given
  `(id, excerpt)` as there are occurrences of that excerpt, so mapping the *k*-th tell to the *k*-th
  occurrence assigns each a distinct, correct position. No phantom duplicates to drop, no smearing.
- **No `host_grammar` change**, no rev-bump, no touching its allium/property lanes.
- The **density-score concern is moot** — `tell_score` counts correctly because the engine emits the
  right number of tells.

## Deliverables (all host-lint)

- **E1 + E2 — locate each occurrence with a column.** Replace `locate_line`'s first-occurrence search
  with **occurrence-mapping**: group tells by `(id, excerpt)`; for each group, walk the successive
  positions of the excerpt in the source and assign tell *k* → occurrence *k*, yielding `file:line:col`.
  Ten em-dashes → ten records at their real `line:col`; one em-dash → one record. Output becomes
  `path:line:col: …`.
- **E3 — a mechanical fix-hint** keyed on the trope `id` (e.g. `decoration` → "drop it, or replace with
  a comma/period"; `arrow` → "use a word"), in the text line and as a `fix` field in `--json`. Only
  mechanically-rewritable tropes carry a `fix`.
- **E4 — advisory tiers.** A tell whose excerpt does **not** appear literally in the source (the
  synthetic whole-document diagnoses: `tell-density`, `bold-first-bullets`, `anaphora`,
  `punchy-fragments`, a span-less self-answered-question) is **advisory** — emitted once for awareness
  but **not** part of the clean-to-zero gate. Locatable tropes drive the exit code; advisory ones do not.
  So "zero" is achievable and terminating. (The locatable-vs-advisory split is *derived* — found in
  source → locatable, not found → advisory — so no hardcoded id list to maintain.)

## Verification

- **Golden tests** (host-lint): the `call/0019` regression — ten `decoration` records at the ten real
  em-dash lines (not ten at line 12), each with a column; one em-dash → one record; a mechanical trope
  carries a `fix`; a synthetic-diagnosis trope is advisory (present in output, does **not** make `--docs`
  exit non-zero on its own).
- **4B acceptance — PASSED (atomic).** Qwen-3.5-4B (`unsloth/Qwen3.5-4B-MTP-GGUF`) applied the located +
  fix-hinted output correctly **one fix at a time**: a mechanical decoration fix (`robust — it … — and` →
  commas) and a no-fix reword (`delve` → `look at`), and it **correctly ignored the advisory `note`**. It
  could *not* do the six mixed edits in one shot (it echoed the doc, though it still parsed which to
  ignore). Finding: the format is weak-agent-usable at the **per-occurrence** granularity the clean uses;
  the compound-in-one-shot failure **confirms** `plan/0030` D5's one-doc / one-fix cadence and STOP rule
  (drive a weak agent atomically, never hand it the whole doc). No engine offset needed. A 27B sanity run
  agreed. (Golden tests prove the mechanics deterministically; the 4B proves the goal.)
- Whole-suite green (66 unit + integration + clippy); new host-lint release re-pinned in `.host-software`
  with `software --verify-build` green. **Bundled with `plan/0030`'s D1 (`--docs`) as one host-lint
  release** — `--docs` only pays off with fixable output, so they ship together.

## Push order

host-lint-only: **host-lint** (E1–E4 + golden tests, on top of the already-built D1) → `cargo test` +
clippy + integration green → 4B acceptance → bump version → re-pin `.host-software` → `--verify-build` →
CI. No upstream repo.

## Relationship to plan/0030

`plan/0030` owns the **lane** (`--docs`, built), the re-derivable **classification** (`STATUS:` +
`Status:`), and the **gate wiring** (D4). This milestone owns the **fixable output**, and its host-lint
work ships in the **same release** as `plan/0030`'s D1. `plan/0030`'s D5 (the triggered repo-wide clean)
depends on this — the clean is not weak-agent-executable until the output is located, columned, fix-hinted,
and tiered.

## Risks / honesty

- Occurrence-mapping matches by excerpt string. It is exact when tell-count == occurrence-count (the
  confirmed reality). If a future detector ever emits a tell whose excerpt is a non-literal normalization
  (curly→straight quotes, collapsed whitespace), that tell would not be found and would fall to the
  advisory tier (a conservative under-gate, not a wrong location). Worth a property test.
- Advisory-tiering changes the prose exit model slightly: a doc with *only* synthetic-diagnosis tropes
  now exits 0 under `--docs` (gate passes) instead of warn. That is the intended "zero is achievable"
  behavior; the existing `--stdin`/`--prose` tests assert on locatable tropes, which still warn.
- The 4B acceptance gate is the real check; golden tests prove the mechanics, the 4B proves the goal.

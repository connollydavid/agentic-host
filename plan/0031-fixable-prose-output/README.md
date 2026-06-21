# plan/0031 — Fixable prose output: one record per occurrence, a column, a mechanical fix, advisory tiers

> Spun out of `plan/0030`'s D2 (operator: "this needs a plan"). `plan/0030` made the prose lane real
> and walkable (`host-lint --docs`, shipped); this milestone makes its **output weak-agent-fixable**,
> which is the precondition for `plan/0030`'s triggered clean (D5). The one open design decision — where
> the over-emission + column fix lives (the `host_grammar` engine vs `host-lint`) — is laid out below
> for the same 4B + adversarial-review rigor `plan/0030` got, **not yet settled**.

## Context

`plan/0030` shipped `host-lint --docs` — the repo-wide prose audit walks authored markdown. But the
prose **output** defeats a weak agent doing the clean (`plan/0030` D5), in four concrete ways, all
verified against the live tool:

- **Over-emission.** `call/0019` line 12 has **one** em-dash and **one** period, yet the engine emits
  **ten** byte-identical `decoration` records (all `line 12`, `text "—"`). A weak agent cannot count
  occurrences, pick a span, or know when it is done — it loops or strips every dash. (A clean
  single-em-dash line emits exactly one record, so the defect is specific to the markdown scan path.)
- **No column.** `host-lint` derives `Match.line` by re-locating the excerpt's *first* line
  (`locate_line`); there is no column, and `host_grammar`'s `Tell` struct carries **no byte offset**.
  A trope on a busy line has no locatable fix point.
- **Span-less tropes.** `bold-first-bullets` reports "21/23 bullets open with bold lead-ins";
  `tell-density` reports a whole-document score; a self-answered-question can report with no single
  span. A clean-to-**zero** bar over these is an unterminating loop — there is nothing to edit.
- **Volume.** ~1,100+ `--docs` warning-lines across the authored docs; a long mechanical campaign needs
  reliable per-occurrence output or a weak agent drifts.

## Deliverables

- **E1 — one record per real occurrence** (kill the over-emission). One em-dash → one record; N em-dashes
  → N records. *(Site: see Decision.)*
- **E2 — a column per occurrence** (`file:line:col`), so every locatable trope names an exact fix point.
  *(Site: see Decision.)*
- **E3 — a mechanical fix-hint** keyed on the trope `id` (e.g. `decoration` → "drop it, or replace with
  a comma/period"; `arrow` → "use a word"), emitted in the text line and as a `fix` field in `--json`.
  Only mechanically-rewritable tropes carry a `fix`. *(host-lint.)*
- **E4 — advisory tiers.** Structural / density tropes (`tell-density`, `bold-first-bullets`, a span-less
  self-answered-question) are **advisory** — printed for awareness but **not** part of the clean-to-zero
  gate; the `--docs` exit code is driven by **locatable** tropes only. So "zero" is achievable and
  terminating. *(host-lint.)*

## Decision — where E1 + E2 live (the fork, to settle with 4B + review)

The column and the over-emission can be fixed in the engine (the source of truth for tropes) or worked
around in `host-lint`. Three options, with the tradeoff named:

- **A — host-lint-side (recommended for the output).** `host-lint` occurrence-maps each tell to the
  successive positions of its excerpt in the content: surplus phantom tells (10 tells, 1 occurrence) are
  dropped → one record; the position yields `line:col`; N real occurrences → N distinct columns. E3/E4
  are host-lint-side regardless. **No `host_grammar` change**, contained and fast; the cost is that it is
  heuristic (matches by excerpt string) and the engine stays over-emitting for any other caller.
- **B — fix the over-emission at the source** (`host_grammar`'s `scan_prose_markdown`) so it emits one
  tell per occurrence, and keep columns host-lint-side. Smaller engine change than C (a markdown-scan
  bug fix, no `Tell` API change), more correct than A; opens the remote `host-grammar` repo (its tests +
  allium spec + a push + a rev-bump).
- **C — full engine offset API.** Add a byte offset to `Tell` and thread it through every detector, so
  each tell carries an exact span from the source; `host-lint` just renders it. Most precise, biggest
  blast radius (all detectors + the allium spec + property tests).

**Recommendation:** do the **output** host-lint-side (A) — it is contained and the clean (the actual
goal) only needs locatable output — **and** separately verify whether the over-emission also inflates
the engine's **density score** (`tell_score`/`tell_score_markdown` are computed independently of the
tell list); if it does, that is a genuine `host_grammar` correctness bug worth fixing at the source
(option B), independent of the output. Settle A-vs-B with a 4B clean-one-doc run and an adversarial
review, as `plan/0030` was.

## Verification

- **Golden tests** (host-lint): one em-dash → exactly one record with a column; N em-dashes → N records
  with distinct columns; the `call/0019` line-12 regression → exactly one `decoration` record; a
  mechanical trope carries a `fix`; a structural trope is advisory (present in output, does **not** make
  `--docs` exit non-zero on its own).
- **Density-score check:** confirm whether the markdown over-emission inflates `tell_score_markdown`; if
  so, fix in `host_grammar` and add a property test.
- **4B (the executability proof):** drive Qwen-3.5-4B through cleaning one real doc using the new output;
  confirm it locates and fixes each trope without looping (the bar `plan/0030` D5 needs).
- Whole-suite green; if `host_grammar` is touched, its allium + property lanes green and the rev bumped
  in host-lint's `Cargo.toml`; new host-lint release re-pinned in `.host-software`, `--verify-build`
  green.

## Push order

If host-lint-only (A): **host-lint** (E1–E4 + tests) → re-pin → release. If the source fix (B/C) is
taken: **host-grammar** (fix + tests + spec, push, tag) → **host-lint** (rev-bump + E2–E4) → re-pin →
release.

## Relationship to plan/0030

`plan/0030` owns the **lane** (`--docs`, shipped), the re-derivable **classification** (`STATUS:` +
`Status:`), and the **gate wiring** (D4). This milestone owns the **fixable output**. `plan/0030`'s D5
(the triggered repo-wide clean) **depends on this** — the clean is not weak-agent-executable until the
output is one-record-per-occurrence, columned, and tiered. `plan/0030`'s D4 gate can wire `--docs` now,
but the gate only goes green after D5, which waits on this milestone and on the operator's front-door
sentence.

## Risks / honesty

- The host-lint occurrence-mapping (A) is heuristic: it matches by excerpt string and assumes the engine
  emits ≥ the real occurrence count (true for the over-emission, the case that matters). A trope whose
  excerpt does not appear literally in the source (the synthetic `tell-density` message) is special-cased
  to the advisory tier (E4), line 1, no column.
- Advisory-tiering (E4) is a severity-model change: `--docs` must distinguish "locatable trope → gate"
  from "structural trope → advisory". Kept simple — a fixed list of advisory trope ids — to stay
  weak-agent-legible.
- If the density score is inflated (open question above), that is a pre-existing `host_grammar` bug this
  milestone surfaces; fixing it is option B's territory and may move the rev.

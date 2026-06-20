# Literal tell-citations live in a `host-lint:ignore` fenced block, never `--no-verify`

- Status: accepted
- Date: 2026-06-20
- Relates to: `call/0006` (the sanctioned-vocabulary allowlist), `call/0009` (exclude the generated record from the audit), `CLAUDE.md` §0 (host-lint is the hygiene lane).

## Context and Problem Statement

The host *develops* host-lint, so its own authored content legitimately cites tell-shaped
tokens: decision records explain detection by naming the token classes they handle, and
`PLAN.md` carries a mandated retired-ordinal dictionary (old name to content name, kept for
reading history). `call/` is intentionally linted — and that caught a *real* ordinal tell that
had hidden in a decision record. But the recurring legitimate citations were being committed
with `git commit --no-verify`, a blanket bypass that defeats the lane: it is exactly how the
real tell slipped in unnoticed. Excluding whole files via `.host-lintignore` is no safer — it
mutes any *future* real tell in those files. We need an exclusion that is line-precise, explicit,
visible in the source, and that cannot silently hide a real tell.

## Decision Outcome

A tell-shaped token in linted host content is legitimate only if it is a real tracker reference
(the `closes`/`fixes` traceability allowlist) or a declared LEXICON entry; anything else is a
violation and is reworded out. For the residual case — literal *reference* content that must
reproduce old tokens for history (the retired-ordinal dictionary, an archived citation) — that
content goes in a fenced code block whose info string is **`host-lint:ignore`**:

    ```host-lint:ignore
    <literal reference content, reproduced verbatim>
    ```

host-lint's naming scan skips such a block; its prose scan already skips every fenced block.
Why this form:

- **Idiomatic markdown.** It is the mermaid / PlantUML info-string pattern — a plain fenced
  block to a renderer, and a meaningful "this is excluded literal reference data" to a reader.
  No bolted-on HTML-comment pragma, no out-of-band config.
- **Explicit, never blanket.** Only a block *tagged* `host-lint:ignore` is skipped; a regular
  code block and all prose stay linted. The exemption is always a deliberate, reviewable act —
  the "excluded, not bypassed, validated" rule, now self-documenting at the point of use.
- **Inline stays linted.** Only fenced *blocks* are skipped, never inline backticks, so a tell
  cannot be laundered by inline-quoting it — it must be reworded.
- **Region-precise, drift-proof.** It bounds exactly the fenced lines — no line numbers to rot.

`git commit --no-verify` is retired for record-layer commits: the legitimate cases are now
handled (a tracker reference, a LEXICON entry, or a `host-lint:ignore` block), and everything
else is a real tell to fix. The lane is never bypassed.

## Consequences

- Good: the host's own docs self-audit clean with no bypass; the gate is honest.
- Good: a future real tell in prose still flags; a tell moved into a `host-lint:ignore` block is
  a visible, reviewable change in the diff, not a silent mute.
- Cost: a small host-lint feature (the naming scan learns the info string) and a one-time cleanup
  (wrap the dictionary, reword the violations, retire the `--no-verify` rule).
- Builds on `call/0006` (an allowlist for legitimate vocabulary) and `call/0009` (exclude the
  generated record): this is the third escape — literal reference *citations* — and the
  strictest, because it is per-block and visible.

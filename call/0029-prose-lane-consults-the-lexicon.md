# The prose lane consults the per-project LEXICON

- Status: accepted
- Date: 2026-06-25
- Scope: host-lint (the `scan_prose_text` mask, the `--prose` and `--docs` lanes, the README
  masked-modes wording). The software change of `plan/0044`. No spine change, since the
  existing doctrine is met rather than changed, so it is adopter-facing only as fixed
  behaviour on the next host-lint bump.
- Relates: `plan/0044` (the milestone and its `gather-data.md`); host-lint issue #13 (the
  LEXICON) and host-lint issue #16 (the divergence this closes); `plan/0039` (the
  living-grammar doctrine the LEXICON is the home for).

## Context and Problem Statement

The LEXICON allowlist masks a sanctioned phrase before the naming lane classifies a line, so
a legitimate tell-shaped token a project declares stops flagging. The prose lane, the
host-grammar density engine behind `--prose` and `--docs`, never consulted that allowlist. A
legitimate domain word the prose grammar reads as an ai-diction trope had no sanctioned
escape: the only inline-source escape is the block-level `host-lint:ignore` fence, and there
is no per-project prose allowlist. The living-grammar doctrine names the LEXICON as the home
for such a token, so the doctrine was unmet for the prose lane. host-lint issue #16 reports
this.

## Decision

The prose lane consults the same LEXICON. `scan_prose_text` masks the whole document with
`mask_allowed`, the naming lane's pre-detection blank-out, before both the per-tell scan and
the document density score, so a declared phrase contributes to neither. The mask is surgical
at the word boundary: a declared `rehost harness` clears the trope on `harness` within that
phrase and leaves a standalone occurrence reported. One declaration serves both lanes. The
README masked-modes wording adds `--prose` and `--docs`, so its "in any mode" claim holds. The
spine is unchanged, since the doctrine is met rather than changed, so host-template carries no
UPGRADING entry.

## Considered Options

1. **Extend the existing mask to the prose lane (chosen).** One declaration, the same
   provenance-gated entries, the same word-boundary specificity. Reuses `mask_allowed`, so the
   prose lane grants no muting power the naming lane lacked.
2. **A separate prose-vocabulary allowlist.** Rejected: a second list to maintain and a second
   provenance model, for a need the existing LEXICON already meets.
3. **Document the gap as intentional.** Rejected: it would leave the living-grammar doctrine's
   promised home absent for the prose lane, and force reword-or-tolerate on a legitimate domain
   word.

## Consequences

- Good: the doctrine's home now exists for the prose lane; one declaration serves both lanes;
  the README claim becomes true; no new abuse surface, since the entries are the naming lane's
  own and the density denominator is the sentence count.
- Costs: the mask now feeds the density engine, so a mis-scoped entry could hide a real trope;
  the provenance guards and the per-occurrence word boundary keep it specific. The change
  removes prose findings when a phrase is declared, so it ships under the removes-findings
  change class.

## Confirmation

A Qwen-3.5-4B run, direct against rope with a real system prompt and non-contaminated options,
confirmed the lane-consistency reading and the surgical word boundary, and judged the reuse
adequately bounded with the dissent option available and not chosen (`gather-data.md`).
Regression tests pin the behaviour: a declared phrase clears the trope within the phrase, a
standalone occurrence still flags, an empty allowlist leaves the scan unchanged, and the
density score drops by the masked phrase alone. Released as host-lint v0.10.0 (`f1474e8`,
artifact `5106ee7a`), with `.host-software` re-pinned, the release receipt recorded, host-lint
issue #16 closed, and the whole suite green.

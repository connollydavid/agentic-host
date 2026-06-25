# plan/0044: LEXICON masking reaches the prose lane

The LEXICON allowlist (host-lint issue #13) masks a sanctioned phrase before the
naming lane classifies a line, so a legitimate tell-shaped token a project declares
stops flagging. The prose lane, the host-grammar density engine behind `--prose` and
`--docs`, never consulted that allowlist, so a legitimate domain word the prose grammar
reads as an ai-diction trope had no sanctioned escape. host-lint issue #16 reports the
divergence. This milestone extends the existing pre-detection mask to the prose lane, so
one declaration serves both lanes.

## Problem

The two lanes take different paths. The naming lane masks each line with the sanctioned
phrases before it classifies; the prose lane hands the raw document to the host-grammar
engine and never sees the allowlist. So a project that legitimately uses a domain noun
the grammar over-reads (the reporter's case is the noun `harness`, the name of a
`rehost harness` used identically across its codebase) is left with two options, rename
the term or carry the warning, while the naming lane would have honoured a declaration.

This contradicts the living-grammar doctrine, which names the per-project LEXICON as the
home for a token the shared grammar flags but the project judges legitimate. For a prose
trope that home did not exist: the only inline-source escape is the block-level
`host-lint:ignore` fence, and there is no per-project prose allowlist. The README also
overclaims. It says a declared phrase never flags "in any mode", though the enumerated
modes are the naming modes alone.

## Decision (operator)

Of the three options the issue lists, the operator chose the first, extend the mask, and
set aside a separate prose allowlist and documenting the gap as intentional. One
declaration in the existing LEXICON serves both lanes; the prose lane reuses the same
pre-detection blank-out the naming lane already performs. The decision and its alternatives
are recorded in `call/0029`, validated at the weak-agent bar in `gather-data.md`.

## The design

### The mask, before both the per-tell scan and the density score

`scan_prose_text` masks the whole document with `mask_allowed`, the naming lane's
blank-out (byte-length-preserving, word-boundaried, case-insensitive), before the
host-grammar pass. The masked text feeds both the per-tell scan and the document density
score, so a declared phrase contributes to neither. Because the mask preserves byte
length, the offsets that locate each surviving tell still index the original document, and
the reported excerpt stays the author's own text.

### Surgical, not blanket

A declared multi-word phrase clears the trope only within that phrase; a standalone
occurrence of the same word still flags. Declaring `rehost harness` clears `harness`
inside that phrase and leaves a later standalone `harness` reported, the same
word-boundary specificity the naming lane already carries.

### No new abuse surface

The prose lane reuses the same provenance-gated entries the naming lane masks with: an
entry must hold a letter, may not launder a flag-tier tell, and a tracker reference must
carry a URL. So the prose lane grants no muting power the naming lane lacked. The density
gate divides the weighted tell count by the sentence count, so masking a phrase removes
only its own weight from the numerator and cannot inflate the denominator to push other,
undeclared tells under the threshold. A weak-agent run confirmed this reading: handed
honest options, including holding for a separate stricter allowlist, the model judged the
reuse adequately bounded on the no-new-power argument.

### The README reconciliation

The masked-modes wording adds `--prose` and `--docs`, so the "in any mode" claim becomes
true rather than narrowed to the naming modes.

### No spine change

Extending the mask makes the existing doctrine, that a legitimate tell-shaped token stays
in the per-project LEXICON, hold for the prose lane. The doctrine is met, not changed, so
host-template carries no new UPGRADING entry; an adopter reads the corrected behaviour on
the next host-lint bump.

## Build sequence

### Settle the approach with data {#settle-by-data}

Settle the lane-consistency reading, the surgical word-boundary semantics, and the abuse
question with a recorded Qwen-3.5-4B run, in `gather-data.md`, run direct against rope with
a real system prompt and non-contaminated options.

- verify: attested operator

### Extend the mask to the prose lane {#extend-mask}

Thread the sanctioned phrases into `scan_prose_text` and `run_docs`, mask the document
before the per-tell scan and the density score, and report each surviving tell from the
original text. Regression tests pin the behaviour: a declared phrase clears the trope
within the phrase, a standalone occurrence of the same word still flags, an empty allowlist
leaves the scan unchanged, and the density score drops by the masked phrase alone.

- depends: #settle-by-data
- verify: cd software/host-lint/main && cargo test

### Reconcile the README claim {#readme-claim}

Add `--prose` and `--docs` to the masked-modes wording so the "in any mode" claim holds.
host-lint prose stays clean.

- depends: #extend-mask
- verify: attested operator

### Release, re-pin, and close {#release-and-close}

Release host-lint with the change class that removes findings, re-pin `.host-software`,
bump the CI install revisions, and close issue #16. The released binary gates green and the
whole suite is green.

- depends: #readme-claim
- verify: attested operator

## Risks

- The mask now feeds the density engine, so a mis-scoped entry could hide a real trope. The
  provenance guards and the per-occurrence word boundary keep the mask specific, and the
  sentence-count denominator stops a mask from diluting the other tells.
- The change removes prose findings when a phrase is declared, so it ships under the
  removes-findings change class, and an adopter reads the masked-modes wording to learn the
  new reach.

## Status

in progress.

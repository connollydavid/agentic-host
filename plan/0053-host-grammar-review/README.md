# plan/0053 host-grammar review: findings and remediation

This milestone records a maximum-effort review of `host-grammar`, the shared grammar both
`host-lint` (the checker) and `host-lifecycle` (the generator) depend on as a git dependency, and
remediates its findings. It is the next review in the campaign after `host-lifecycle` (plan/0051,
plan/0052). The operator ordered it ahead of `host-lint` and `host-prove` because it is the shared
base: fixing the dependency before its consumers means the consumer reviews build on a corrected
foundation.

## What was reviewed

- Component: `host-grammar` at its pinned release (`9d51468`, v0.3.0): the naming and number grammar
  (`src/lib.rs`, about 102 lines), the token-free agentic-tell prose engine (`src/tells.rs`, about
  792 lines), the `host-grammar.allium` spec and its `host-grammar.obligations` manifest, the
  property tests (`tests/prose_properties.rs`), the three `spec/*.tla` deep-verification specs and
  their `spec/ParallelScan.obligations`, and the four CI workflows.
- Method: six independent reviewers, one per functional surface (the naming grammar and the
  generator-equals-checker symmetry; the lexical and per-sentence tells; the cross-sentence run
  equations and the parallel chunked scan; the markdown-aware path; the density scoring and the
  allium spec fidelity; the obligation-discharge honesty and CI integrity under the no-hollow-green
  doctrine). Each reviewer probed its own claims empirically against the built crate, marked every
  finding confirmed or speculative, and defaulted to speculative on doubt. Cross-reviewer duplicates
  were merged and the load-bearing findings were independently reproduced before remediation.
- Result: 34 findings raised, deduped to 31 (three were found by two reviewers each: the markdown
  heading-diction density inflation, the anaphora-plus-listicle double count, and the stale triad
  comment). Every finding was confirmed by an empirical probe; none survived as speculative only.
  Zero critical, zero high in the sense of a memory-safety or data-loss defect: the prose engine has
  no panics and the parallel scan is correct. The headline class is verification integrity (a
  fabricated test-coverage waiver, two invariants discharged by tests that do not exercise them) and
  detection precision (false positives a documentation gate would raise on clean prose).

## The contract the findings test against

- **Generator equals checker.** `host-grammar` exists so that what `host-lifecycle` emits is exactly
  what `host-lint` accepts. Any divergence between `format_number`, `is_valid_name`, `is_valid_slug`,
  and `is_numeral` and the producible set is the cardinal-invariant class.
- **The prose engine is advisory by density.** An individual tell is advisory; the per-document
  density gate is what escalates. The engine must not panic (it gates commits and docs), must not
  raise a false positive on clean prose, and must not silently miss what it claims to catch.
- **Parallel equals sequential.** `scan_chunked(text, k)` must equal `scan_prose(text)` for every
  chunk count, the property the allium and property-based lanes check and the three `.tla` specs
  model across worker interleavings.
- **No hollow green (plan/0052).** A verification lane that cannot perform its check must not report
  clean. An obligation discharged by a test whose name resolves but which does not exercise the rule
  is the canonical violation; a waiver is the sanctioned escape only when it carries a real
  structural reason, never deferred backlog dressed as discharge.

## The operator decision

The operator ruled **fix everything toward precision** and **propagate now**. The verification
integrity, CI, and spec fidelity findings change no detection output and are fixed outright. The
detection-behavior findings are tuned toward precision: every false positive a clean document would
raise is pruned, and the clear bugs are engineered. After release, the new `host-grammar` is adopted
by both consumers in this same session (each pins it by exact git rev), with the whole suite green
across all three components.

## Findings: verification integrity, CI, and spec fidelity

These change no detection output. They are fixed in this milestone.

1. **The ing-tail and false-range waivers claim coverage that does not exist.**
   `host-grammar.obligations:39-44` waives all six `DetectIngTail` and `DetectFalseRange` obligations
   as "covered by the tells.rs scan unit tests." No test in the crate exercises `ing_tail` or
   `false_ranges`; the only references are the implementation sites. The justification is false and
   the two rules ship with zero coverage. This is the canonical no-hollow-green violation, the same
   class plan/0052 was cut for. Fix: add real positive and negative property tests for both rules and
   remap the six obligations to them. (confirmed)
2. **`DensityIsWeightedOverSentences` is mapped to a test that never asserts the density formula.**
   `host-grammar.obligations:48` points at `density_gate_requires_both`, which asserts the gate
   conjunction (the sibling invariant), never `density = weighted / sentences`. Fix: add a property
   asserting the formula and remap. (confirmed)
3. **`RunTellsAreSuperlinear` is verified for anaphora but not listicle.** The invariant quantifies
   over both ids; the mapped test (`host-grammar.obligations:50`) filters only anaphora, and the sole
   listicle test asserts firing, not weight. Fix: assert the listicle weight too. (confirmed)
4. **The countdown negative-case waiver cites a test with no negated run.**
   `host-grammar.obligations:35` waives the unclosed-run negative as covered by
   `clean_technical_prose_is_silent`, whose fixture contains no negated sentence at all. Fix: add a
   real negative test (a negated run with no closer raises no countdown) and remap. (confirmed)
5. **The listicle negative-case waiver points at the wrong discriminator.**
   `host-grammar.obligations:32` waives the non-ordinal-run negative as covered by
   `anaphora_pair_is_free`, which tests a run-length floor, not the ordinal discriminator. Fix: add a
   negative test (a long non-ordinal run raises no listicle) and remap. (confirmed)
6. **CI runs `cargo test` only; the pinned code fails clippy.** `test.yml` has no clippy or
   format lane, unlike the sibling components, and the pinned code fails `cargo clippy --all-targets
   -- -D warnings` on the recorded 1.95.0 toolchain with six lints (`manual_range_contains` at
   `tells.rs:193`, `manual_div_ceil` at `:476`, three `collapsible_match` at `:554`, `:559`, `:571`,
   and a `manual_repeat_n` in the tests). Fix: clear the six lints and add clippy and format-check CI
   lanes. (confirmed)
7. **A stale `host-lifecycle` pin runs the obligations gate from an old checker.** `allium.yml`
   installs `host-lifecycle --rev d91dae3` while `.host-software` pins a newer release. Fix: bump the
   workflow pin to the recorded release. (confirmed)
8. **The Apalache obligation claims a scope wider than it checks.** `spec/ParallelScan.obligations`
   and `ParallelScanSymbolic.tla` say the reconstruction holds for every `(N,K)` with `1<=K<=N`, but
   `CInit` admits only `N` in `2..8`. Fix: reword the obligation and spec comments to the bound that
   is actually discharged. (confirmed)
9. **The TLAPS gate does not bind to the named theorem.** `host-prove.yml` greps the generic proof
   status, so a rename or deletion of `WorkerIndexInBounds` would pass vacuously. Fix: add a static
   check that the declared theorem is present in the spec file before the proof runs. (confirmed)
10. **The allium spec omits every lexical-corpus and shape tell the engine emits.** The spec models
    only the eight per-sentence and run rules; the seven corpus diction tells and the two shape tells
    (`punchy-fragments`, `bold-first-bullets`) have no rule, so the spec reasons about a smaller score
    than ships, and the `lexical` enum variant is declared but never produced. Fix: add rules for the
    two shape tells with their weights and tests, and an explicit scope statement declaring the
    corpus a data-driven phrase layer modeled as the `lexical` kind rather than enumerated as rules.
    (confirmed)
11. **Listicle emits one aggregate tell summing all runs; the spec emits one per run.** `listicle`
    sums `(L-2)^2` across every ordinal run and `run_tells` emits a single tell, so the tell count
    undercounts and the single weight matches no run when two or more runs exist. Fix: emit one
    listicle tell per run, mirroring `anaphora_runs`. (confirmed)
12. **The cite strings diverge between spec and code for all eight rules.** The spec uses a path form
    and the anaphora cite uses a different prefix entirely; the code uses a prose form. Fix: align the
    spec cites to the shipped strings. (confirmed)
13. **Spec fidelity nits.** The spec types weights and gates as exact `Decimal` while the
    implementation uses `f32`; the `max(1, sentences)` clamp is in the code and README but not the
    spec; the `is_triad` doc comment says four words while the code and spec say five; the TLA model
    spawns exactly `K` workers (with empty trailing chunks) while the implementation spawns at most
    `K` non-empty chunks. Fix: a Decimal-abstracts-f32 note, the clamp in the spec, the corrected
    comment, and a worker-count fidelity note. (confirmed)

## Findings: detection behavior, tuned toward precision

These change what the engine flags. They ripple to `host-lint`'s prose lane (the gate on every
repository's commits and documents) and are tuned toward fewer false positives.

14. **`is_numeral` accepts plain English words as Roman numerals.** The Roman arm is a bare
    charset-and-length gate, so `is_numeral` returns true for `lid`, `mid`, `mild`, and for
    non-canonical forms such as `IIII` and `VV`; the result contradicts its own doc comment. Fix:
    validate a canonical Roman numeral (a value round-trip) so only real numerals qualify. (confirmed)
15. **`format_number` can emit a number `is_valid_name` rejects.** The pad width is a minimum, so a
    register at or past ten thousand formats to more than four digits while the checker enforces
    exactly four, a silent generator-checker divergence. Fix: accept the natural overflow form (four
    digits, or more than four with no leading zero) so the checker accepts exactly what the generator
    produces, while still rejecting an over-padded number. (confirmed)
16. **`is_triad` flags four-or-more-item lists as a tricolon.** The gate accepts three or more
    comma-spans with no upper bound, so an ordinary enumeration is mislabeled a tricolon and adds
    weight. A tricolon is three. Fix: require exactly three spans. (confirmed)
17. **The em-dash pivot in the negative-parallelism config is dead code.** The word tokenizer drops
    punctuation, so the dash entry in the pivot set can never match. Fix: remove the dead entry and
    note that punctuation pivots are outside the word-based equation, the precision-preserving
    resolution (the alternative, detecting it on the raw text, would add a false-positive-prone path,
    and the dash already earns a decoration tell). (confirmed)
18. **Negative parallelism fires on comparatives.** The `than` pivot makes a comparison such as `no
    faster than light` register as antithesis. Fix: drop `than` from the pivot set; the genuine `not
    X but Y` form keeps its pivot. (confirmed)
19. **Countdown fires on a plain sentence-initial negation.** The countdown opener set includes the
    bare `no`, so an ordinary clause opening with `No ...` is read as a countdown fragment. Fix:
    require the `not` opener only. (confirmed)
20. **A repeated-ordinal run is counted as both an anaphora and a listicle.** The spec models a run
    as classified by `ordinal_led` into one of the two, with anaphora requiring `not ordinal_led`;
    the code computes them in independent passes and double-counts a same-ordinal run. Fix: suppress
    the anaphora run when its opener is an ordinal, matching the spec. (confirmed)
21. **The markdown density numerator counts heading diction while the denominator excludes headings.**
    `scan_prose_markdown` scans heading diction (by design, headings can read as a pedagogical hook),
    but `tell_score_markdown` divides the resulting weight by a heading-excluded sentence count, so a
    clean-body document with buzzword headings crosses the gate, and the doc comment falsely claims
    headings are excluded. Fix: score the density over body blocks only so heading diction stays
    advisory and does not escalate the gate, and correct the doc comment. (confirmed)
22. **Loose multi-paragraph list items fuse word boundaries.** A list item with two paragraphs
    concatenates their text with no separator, so the last word of one paragraph and the first of the
    next merge into one token; a word-boundaried tell is then destroyed or fabricated. Fix: insert a
    separator when a paragraph continues a list item. (confirmed)
23. **Blockquote content is scanned as the author's own prose.** A quoted block (commonly an external
    citation, the very text that is trope-dense) is run through every tell as if authored. Fix:
    exclude blockquote text from the scan, mirroring the code-block exclusion. (confirmed)
24. **Image alt text is scanned for diction.** Descriptive alt text naturally uses words such as
    `landscape` and `harness`, so good accessibility text raises diction tells. Fix: suppress text
    capture inside an image, matching the URLs-are-not-prose intent. (confirmed)
25. **The lexical word-boundary test uses ASCII bytes.** A corpus stem adjacent to a non-ASCII letter
    reads as a boundary and fires, an unsound general boundary test. Fix: decide boundaries on
    character classification, not raw ASCII bytes. (confirmed)

## Findings recorded as intended (no clean-text false positive)

These are double-attributions on genuinely trope-dense text, not false positives a clean document
would raise, and the documented behavior is to count adjacencies. They are recorded as intended
rather than coordinated away, which would add stateful complexity and risk missing a real tell.

- **A negated countdown run is also an anaphora.** A run of negated sentences closed by a `Just`
  fragment earns both the countdown and the anaphora tell. The text is genuinely heavy; the
  anaphora is real (a repeated opener) and the countdown is real (the closed run).
- **A chain of terse questions overcounts self-answered adjacencies.** The engine counts adjacencies
  by design; a chain such as a question followed by a one-word question followed by a one-word answer
  is a self-answered-question-dense passage, and each adjacency is a real instance.

## What was checked and cleared

The negatives bound the work. The parallel chunked scan is correct: `scan_chunked` equals
`scan_prose` for every chunk count (verified for a wide range including the degenerate counts), the
merge folds partials in chunk order, run detection runs once over the concatenated metadata so a
boundary-straddling run rejoins, and the float sum is computed in identical order so the gate is
bit-deterministic across worker counts. No function on any surface panics: every slice and unwrap is
guarded. The naming grammar round-trips for every register inside the pad width, the slug validity
is byte-safe, and the decimal arm of `is_numeral` rejects its edge cases. The gate constants match
the spec, the both-gates logic is exact, and all eight structural weights and ids agree between code
and spec. The three deep-verification lanes (the bounded TLC model, the Apalache symbolic check, and
the TLAPS proof) genuinely run and gate, and the anaphora obligations, the positive cases, and the
structural spec-shape dispositions are honestly discharged.

## Status

Complete. host-grammar shipped as **v0.4.0** (commit `9470b81`), a pin-only component with no
artifact. The change is a minor bump because the detection output moves: `is_numeral` now validates
canonical Roman numerals, the prose engine is tuned toward precision, and the markdown density score
covers the body alone. The local gate is green (25 unit tests, 25 property tests, clippy under `-D
warnings`, the three `allium` lanes, and the obligations discharge); a new clippy CI lane plus the
corrected obligation mappings guard against regression.

Two findings carry a recorded judgment rather than the literal fix. The fmt CI lane of finding 6 is
deliberately not added: host-grammar's detection tables are hand-formatted compactly, so a `cargo fmt
--check` gate would force a sweeping reformat out of proportion to this review. The plan/0052
`exercises=` strict-discharge links are not added either: host-grammar's property tests are black-box
over the public API by design, so a white-box containment link does not fit, and the substantive
no-hollow-green fix is already in place (every obligation maps to a test that genuinely exercises its
rule, which the discharge check confirms).

Propagation (operator ruling: propagate now): both consumers adopted the new host-grammar this
session. host-lint shipped as **v0.11.0** (commit `cefc9376`, artifact `136cd7ce`) with its deps-bundle
re-vendored to `vendor-v4`, and its one affected property test moved to the corrected canonical-Roman
contract. host-lifecycle shipped as **v0.34.0** (commit `d4ce47e`, artifact `7f9c2833`) with its
deps-bundle re-vendored to `vendor-v5`; it bumped both its host-grammar and its host-lint dependency so
the tree unifies on a single host-grammar v0.4.0 and its prose lane runs the fixed engine. Both
re-derive byte identically, the release receipts are recorded, and `software --check` is clean at the
new pins. This milestone records no new `call/` decision.

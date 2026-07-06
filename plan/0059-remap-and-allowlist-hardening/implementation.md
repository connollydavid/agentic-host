# plan/0059 implementation (audit of record)

The per-bug audit against host-lifecycle v0.37.0 source, with the code paths located, so the fix work
starts grounded.

## Issue 11: remap --check on an absent or comment-only .host-remap (resolved)

`load_remap` (src/main.rs:750) is already fail-safe: an absent file (NotFound) returns an empty rule
set, and a comment-only file skips every line to the same empty set, with no error. Verified against
v0.37.0: `remap --check` reports clean at exit 0 on both states, and the manifest recheck is exactly
`host-lifecycle remap --check .`, so the recheck and the standalone agree. Neither error string from the
report (`cannot read .host-remap`, `no usable entries`) exists in the current source; the report was
against a pre-fail-safe build. Closed on the tracker; no code change owed.

## Issue 12: remap --apply rewrites inside host-lint:ignore fenced blocks

`apply_text` (src/main.rs:850) substitutes line by line with no fence awareness, so `remap --apply`
corrupts a `host-lint:ignore` boxed block, the very record the box preserves verbatim. The scan side is
already correct: `remap --check` calls `host_lint::scan_text_with_allow`, which skips the fence. The fix
teaches `apply_text` the same rule: track a `host-lint:ignore` fenced region and emit its lines
untouched, while a regular code block stays substituted (the spine skips only the tagged fence). A small
self-contained fence tracker in host-lifecycle keeps M2 independent of a host-lint change.

## Issue 13: the sanctioned-token allowlist is split

`load_allow` (src/main.rs:787) reads `.host-lint-allow`; host-lint and the hooks read `LEXICON`.
`remap --check` uses `load_allow`, so a token declared in `LEXICON` is unknown to remap, and one in
`.host-lint-allow` is unknown to host-lint. Operator ruling: full unification on `LEXICON`, which needs
no host-lint change. `host_lint::load_lexicon` is already public and returns `Lexicon { phrases_lc, .. }`
(the lowercased masking phrases the `--all` and `--docs` lanes use), and its doc names an embedder as a
caller. So `remap --check` calls `host_lint::load_lexicon(root).phrases_lc` and passes it to
`scan_text_with_allow` in place of `load_allow(.host-lint-allow)`, honouring the phrases host-lint
honours. `.host-lint-allow` is read as a legacy alias merged into the phrase list, with a deprecation
note, so an existing adopter file keeps working while `LEXICON` becomes canonical.

## Coupling correction

An earlier draft assumed issue 13 needed a new host-lint LEXICON-scan API, which would have coupled M2
to a host-lint release. That was wrong: `load_lexicon` is already public. So M2 (issues 12, 13, 14) is
host-lifecycle-only, and M3 (issue 18, the hook script in host-lint's `main.rs`) is host-lint-only. The
two milestones are independent, as originally cut.

## Issue 14: software --materialize clones full history every time

`software --materialize` does a full-history bare clone, paid on every CI leg for a large-history
component. Fix: a `--filter=blob:none` partial-clone option (or a documented cache contract) that still
lands the pinned commit's tree, so the pin stays the reproducibility anchor. An enhancement folded in by
operator ruling (bugs plus the coverage gaps).

## Cascade

The spec (`host-lifecycle.allium`) and obligations are updated for any new behaviour, with a Rust
regression test per bug (issue 12 asserts the fence is preserved, issue 13 the single-source property).
Ships as one host-lifecycle release, re-vendored and propagated to consumers, with the whole-suite verify
gate green and the Fen probe passing on the tool-carried behaviours.

## As-built

All three landed in host-lifecycle's source, each with a regression test. `apply_text` gained a
self-contained `host-lint:ignore` fence tracker that replicates host-lint's `fence_info` (a regular code
fence stays substituted, matching the scan side, so a tell cannot be laundered by inline-quoting).
`remap_allow` unifies host-lint's LEXICON as the canonical vocabulary with the legacy `.host-lint-allow`
merged in as a deprecated alias, noted when present. `software --materialize` gained an opt-in
`--partial` flag that clones with `--filter=blob:none`, so the pin still round-trips while the
whole-history blob download defers to worktree checkout. The full inline suite passes and clippy is
clean. No allium or obligations change is owed: the manifest records that the remap and materialize git
mechanics are out of the spec's scope, so the regression tests carry the specification. The code ships
with the host-lifecycle release for this batch.

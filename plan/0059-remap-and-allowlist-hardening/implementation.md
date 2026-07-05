# plan/0059 implementation (audit of record)

The per-bug audit against host-lifecycle v0.37.0 source, with the code paths located, so the fix work
starts grounded.

## #11 — remap --check recheck errors on an absent or comment-only `.host-remap`

`load_remap` (src/main.rs:750) is already fail-safe: an absent file (NotFound) returns an empty rule
set, and a comment-only file skips every line to the same empty set, with no error. So the standalone
`host-lifecycle remap --check .` already reports clean on both states (issue #7's fix). Yet #11 reports
that the **recheck** run inside `software --check` still errors (`cannot read .host-remap`, or `no
usable entries`) and re-opens the phase, disagreeing with the standalone.

So the erroring path is not `load_remap`; it is whatever the manifest's `remap` phase `recheck =`
resolves to inside the receipt gate. First step: reproduce the recheck error (declare the remap phase,
remove `.host-remap`, run `software --check`) and locate the path (the recheck command, or a separate
loader), then unify it with the fail-safe `load_remap`, so the recheck treats an absent or entry-less
dictionary as "map fully applied, audit against an empty map" and matches the standalone. Confirm
whether the current binary already resolves this (the #7 fix may cover it) before writing new code.

## #12 — remap --apply rewrites inside `host-lint:ignore` fenced blocks

`apply_text` (src/main.rs:850) substitutes line by line with no fence awareness, so `remap --apply`
rewrites old names inside a `host-lint:ignore` boxed block, corrupting the durable record the box
exists to preserve. The lint scan already skips fenced blocks via `mask_fenced_lines` (src/main.rs:2289).
Fix: make `remap_apply` skip substitution inside a `host-lint:ignore` fenced block specifically (a
regular code block stays substituted, matching the spine's rule that only the tagged fence is skipped),
reusing the scan's fence detection rather than a second implementation.

## #13 — the sanctioned-token allowlist is split

`load_allow` (src/main.rs:787) reads `.host-lint-allow`; host-lint (and the hooks) read `LEXICON`.
`remap --check` uses `load_allow`, so a token declared in `LEXICON` is unknown to remap and one in
`.host-lint-allow` is unknown to host-lint.

Operator ruling: full unification on `LEXICON`. This needs **no host-lint change**: `host_lint::load_lexicon`
is already `pub` and returns `Lexicon { phrases_lc, .. }` (the lowercased masking phrases the `--all` and
`--docs` lanes use), and its doc names "an embedder" as a caller. So `remap --check` calls
`host_lint::load_lexicon(root).phrases_lc` and passes it to `scan_text_with_allow` in place of
`load_allow(.host-lint-allow)`, honouring the same declared phrases host-lint does. `.host-lint-allow` is
retired (read as a legacy alias, merged into the phrase list, with a deprecation note) so an existing
adopter file keeps working while `LEXICON` becomes canonical. Host-lifecycle-only.

## Coupling correction

An earlier draft assumed #13 needed a new host-lint LEXICON-scan API, coupling M2 to the host-lint
release. That was wrong: `load_lexicon` is already public, so **M2 (#12, #13, #14) is host-lifecycle-only**
and **M3 (#18, the hook script in host-lint's `main.rs`) is host-lint-only** — the two milestones are
independent, as originally cut. #12 replicates a small `host-lint:ignore` fence tracker in `apply_text`
(the scan already skips the fence via host-lint; apply must too) rather than taking a host-lint helper,
keeping M2 self-contained.

## #14 — `software --materialize` clones full history every time

`software --materialize` does a full-history bare clone, paid on every CI leg for a large-history
component. Fix: a `--filter=blob:none` partial-clone option (or a documented cache contract) that still
lands the pinned commit's tree, so the pin stays the reproducibility anchor. An enhancement folded in
by operator ruling (bugs plus coverage gaps).

## Cascade

Spec (`host-lifecycle.allium`) and obligations updated for any new behaviour; Rust regression tests per
bug (#12 asserts the fence is preserved, #13 the single-source property, #11 the absent/empty recheck
is clean). Ships as one host-lifecycle release, re-vendored and propagated to consumers, with the
whole-suite verify gate green and the Fen probe passing on the tool-carried behaviours.

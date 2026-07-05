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
`.host-lint-allow` is unknown to host-lint. Fix: one canonical allowlist read by every lane. Open
sub-decision (the format reconciliation): `LEXICON` holds contextual phrases masked before detection,
while `.host-lint-allow` holds plain lowercased tokens. Candidate: `remap --check` reads `LEXICON`
(the tool-owned, spine-documented surface) through the same masking host-lint uses, and `.host-lint-allow`
is retired or read as a legacy alias by both. Decide the canonical surface and the migration for an
existing `.host-lint-allow` before coding.

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

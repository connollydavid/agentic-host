# plan/0027, `host-lint:ignore` fenced blocks: idiomatic literal-citation exclusion (call/0019)

> **STATUS: COMPLETE (2026-06-20).** Shipped through host-lint's own lifecycle: the
> block (host-lint v0.7.0) skips a fenced block tagged `host-lint:ignore`; specced,
> tested (regression `bbd0687` pins the boundary, an ignore region, a still-scanned
> code block, then a second ignore region), released, applied repo-wide. The Apply
> phase settled into a **three-way rule**: reword a pedagogical example or a doc's
> own ordinal label; box an irreducible literal citation (the PLAN.md retired-ordinal
> dictionary, the frozen plan/0022 + plan/0025 design-reviews); path-exclude only the
> append-only `MEMORY.md`. That corrected an interim blanket `plan/*/*.md` exclusion
> and retired call/0009's plan exclusion (`call/0019`). Spine landed: host-template
> `da000aa` box clause + UPGRADING `97ddf52`; agentic-host recorded da000aa (`.host`
> 0 pending). `host-lint --all` is flag-clean repo-wide; `--no-verify` retired. The
> decision rule was validated down to the local weak-agent bar (Qwen-3.5-4B @ Q8_0).

The host develops host-lint, so its own docs cite tell-shaped tokens; `call/` is linted on
purpose, and `--no-verify` was the wrong escape (it hid a real tell). This milestone ships the
idiomatic fix recorded in `call/0019` (host-lint skips a fenced block tagged `host-lint:ignore`)
and applies it, run through host-lint's **own lifecycle** rather than as a tactical edit to
`--all`.

## Phases (each verified before the next)

1. **Decide**: `call/0019` records the mechanism (an info-string fenced block; skip blocks, not
   inline; the only legitimate citations are a tracker reference, a LEXICON entry, or a
   `host-lint:ignore` block, everything else is reworked). Then committed.
2. **Spec**: model the exclusion in `host-lint.allium` through the allium skills: a
   `host-lint:ignore` block masks its lines before classification, so no `Match` is created
   inside it. Disposition the new obligations. Then verify: `allium check` + `allium analyse`
   clean; `obligations` complete.
3. **Implement**: host-lint's markdown naming scan skips a fenced block whose info string is
   `host-lint:ignore`; the prose scan already skips fenced blocks. Unit + integration tests.
   Then verify: a tell inside a `host-lint:ignore` block does not flag; the same tell in prose, in
   a *regular* code block, and inline still flags; `cargo test` + the integration suite green.
4. **Verify**: the full lane: `allium check/analyse`, `cargo test`, `./test-integration.sh`,
   and `obligations --rederive` on the kani rungs. Then verify: whole host-lint suite green.
5. **Document**: `VOCABULARY.md` (the rule) + host-lint `README.md` (how to use the block).
6. **Release**: host-lint minor bump, regenerate the lock, re-hash + re-pin `.host-software`
   (the version bump moves the artifact hash), tag, CI green.
7. **Apply**: wrap the `PLAN.md` retired-ordinal dictionary in a `host-lint:ignore` block;
   reword the residual prose violations (`Stage`/`step`/`Pass:` ordinals); retire the
   `--no-verify` standing rule (the hook is already refreshed to the pinned host-lint).
   Then verify: `host-lint --all` is clean repo-wide, with no `--no-verify` anywhere.
8. **Spine**: host-template `CLAUDE.md` gains the principle (literal tell-citations go in a
   `host-lint:ignore` block; violations are reworded; the lane is never bypassed) + an UPGRADING
   entry; agentic-host re-records.
9. **Records**: `PLAN.md` row + MEMORY.

## Done

`host-lint --all` clean across the whole host, the dictionary preserved verbatim inside a visible
`host-lint:ignore` block, every prose violation reworded, `--no-verify` retired, and the mechanism
specced, tested, and released through host-lint's own lifecycle, not bolted on.

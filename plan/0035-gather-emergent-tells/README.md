# plan/0035: gather emergent tells

Mechanizes the candidate-tell discovery the plan/0034 doctrine defines (the named
follow-up).

## Context

plan/0034 authored the reflective grammar-growth doctrine: the shared tell corpus is
incomplete and grows by reflective practice, with discovery mechanical-first (sweep the
history and recent work for a recurring shape the lane does not catch), operator-validated,
prompted at the verify gate and at adoption. That sweep is currently run by hand, as it was
over a downstream adopter and at the gate. This milestone gives the doctrine a tool rather
than only a description.

## Where it lives

host-lint owns the gather: it already holds the grammar (`FLAG_TERMS`) and the legitimacy
allowlists (`PREV_SKIP` for version and figure contexts, `UNITS` for quantities) that
separate a real candidate from noise, and it already dispatches subcommands (`lexicon`).
host-lifecycle owns the `verify`, `adopt`, and `classify` skills, where the reflection
prompt is wired.

## The gather subcommand (host-lint)

`host-lint gather [<paths>]` runs `git log` over the repository and scans the tracked docs
and comments itself, one command and parse-free for a weak agent. It extracts a word
followed by a numeral, a numeric range, or a glued numeral; drops every word already in
`FLAG_TERMS` (the lane catches it) and every legitimate context the allowlists name; and
reports the recurring residue: the candidate word, its count, and example lines, ranked by
count. It is advisory and exits zero, so it never gates. A candidate must recur (default at
least twice) to surface, so a one-off is not treated as noise.

Verify by: a synthetic corpus where a novel recurring word-plus-numeral shape is surfaced,
a one-off is not, and a legitimate `figure 3` or `v2.1` is not; `cargo test` and the
integration suite green; released through the lifecycle and re-pinned.

## Reflection wiring (host-lifecycle skills)

The `verify` skill gains a step: run `host-lint gather`, then the operator triages each
candidate (propose it upstream, declare it in the `LEXICON`, or leave it). The `adopt`
skill gains the same at the migration moment, where a project's whole prior history is in
view (the richest sweep). The step is advisory; it prompts reflection and does not block
the gate.

Verify by: the `verify` and `adopt` skills name the gather step; a dogfood run of
`host-lint gather` on this repository surfaces a sensible candidate set (the lane already
catches our own tells, so the residue is small).

## The deferred decision

The software `call/` deferred in plan/0034 is written here, scoped to host-lint and
host-lifecycle: the gather surfaces candidates mechanically, the operator validates, and
the tool never auto-graduates a tell nor auto-bans one. It cites the spine doctrine by
revision.

## Scope boundaries

- No project-local ban surface (still YAGNI; every tell seen so far is universal).
- The gather is advisory and never gates; graduation stays a manual upstream proposal, per
  the doctrine.
- The gather surfaces; it does not decide. The operator triages.

## Verification

host-lint gather unit and integration fixtures pass; a dogfood run on this repository is
sensible; the weak-agent (Qwen-3.5-4B) correctly triages a gather candidate; `software
--check` and `--verify-build` clean; whole-suite CI green.

## Records

PLAN.md row, this doc, a MEMORY entry, and the software `call/`.

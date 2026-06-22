# Enforced remap dictionary

Status: **done** (`host-lifecycle` 0.2.0, `3e55417`; `remap --check`/`--apply`,
8 tests + scratch integration green, CI green). External dogfood satisfied by the
`yarn-agentic` case-(b) adoption (issue #6); see "Dogfood, closed" below.
Decision: `call/0008`. Builds on `host-lifecycle`
(the token-free migrator, `call/0003`), `host-lint` (the policy-free detector), and
`.host-lint-allow` (`call/0006`).

## Goal

A token-free `host-lifecycle` facility that applies an adoption rename map
**deterministically**, guarantees map-only (no fabrication, no spatial drift),
forces every detected tell to be explicitly dispositioned, and leaves **no**
permanent old-vocabulary artifact. `host-lint` stays a pure detector that faults on
tells and never consults the dictionary (`call/0008`: fault, policy-free).

## Dictionary format (proposed)

A plain transient file at the repo root, e.g. `.host-remap`: one `old<TAB>new` per
line; `#` comments and blank lines ignored. `old` is a literal concept token/phrase
(an ordinal tell in any spelling, spaced, concatenated, or decimal-suffixed); `new`
is the human-supplied canonical content-name. Matched case-insensitively and
**word-bounded**, reusing the allow-list masking discipline so a short tell cannot
clip a longer one that contains it as a prefix. Same hand-rolled,
dependency-free parse style as `.host` / `.host-lint-allow`.

## Verbs (`host-lifecycle`, matching the existing `match args.get(1)` style)

- **`remap --check <dir>`**: completeness. Run `host-lint`, enumerate every flagged
  token, and classify each as **map** (a `.host-remap` entry exists), **allow** (a
  `.host-lint-allow` entry exists), or **UNDISPOSITIONED**. Exit non-zero while any
  token is undispositioned. Token-free; the human reads the list and supplies names.
- **`remap --apply <dir>`**: archive originals first (copy each touched file to a
  preserved archive, or assert a clean tree + tag), then substitute **only**
  declared entries, word-bounded, across tracked text files; never touch an unmapped
  token. Print changed-vs-skipped. Deterministic.
- Teardown is an ordinary `git rm .host-remap` + commit; the durable map is embedded
  in the migration `call/` decision, not left in the tree.

## Invariants (verification lane)

- The applied diff contains **only** declared substitutions (golden-file test).
- An undispositioned flagged token makes `--check` fail (no silent residue).
- `--apply` is idempotent and deterministic, same inputs yield same output, no
  `Date`/random (host-lifecycle stays replayable).
- Originals are recoverable: the archive exists before any substitution.
- `host-lint` is unchanged; it gains no dictionary awareness (policy-free).

## Dogfood, closed

`remap` was exercised end-to-end by the **`yarn-agentic`** case-(b) adoption (issue
#6): a 131-milestone corpus renamed to `NNNN-slug`, cross-references rewritten in
scannable files, the durable map captured in that project's migration `call/`. That
run also surfaced the `remap` spec-blind spot: declared substitutions did not reach
`.allium`/`.tla`/`.cfg`, now fixed (spec-aware `remap`, host-lifecycle v0.6.0,
`plan/0003`). The originally-planned **Agentic-MCP-Win32s** dogfood is **descoped**
(its earlier attempt was rejected; superseded by `yarn-agentic` as the live `remap`
exercise).

## Out of scope

- An ongoing drift gate (`call/0008`: redundant with `host-lint` and a per-commit
  token cost; fault, policy-free instead).
- Rewriting git history (tier 3 is acknowledged, not rewritten; `call/0007`).
- Inventing any new name: every `new` value is human-supplied.

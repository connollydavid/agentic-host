# Enforced remap dictionary

Status: **built** (`host-lifecycle` 0.2.0, `3e55417`; `remap --check`/`--apply`,
8 tests + scratch integration green, CI green). Dogfood on Win32s pending.
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
(`Phase 4`, `PHASE4`, `Phase 5.0`); `new` is the human-supplied canonical
content-name. Matched case-insensitively and **word-bounded**, reusing the
allow-list masking discipline so `Phase 1` cannot clip `Phase 12`. Same hand-rolled,
dependency-free parse style as `.agentic-host` / `.host-lint-allow`.

## Verbs (`host-lifecycle`, matching the existing `match args.get(1)` style)

- **`remap --check <dir>`** — completeness. Run `host-lint`, enumerate every flagged
  token, and classify each as **map** (a `.host-remap` entry exists), **allow** (a
  `.host-lint-allow` entry exists), or **UNDISPOSITIONED**. Exit non-zero while any
  token is undispositioned. Token-free; the human reads the list and supplies names.
- **`remap --apply <dir>`** — archive originals first (copy each touched file to a
  preserved archive, or assert a clean tree + tag), then substitute **only**
  declared entries, word-bounded, across tracked text files; never touch an unmapped
  token. Print changed-vs-skipped. Deterministic.
- Stage 2 is an ordinary `git rm .host-remap` + commit; the durable map is embedded
  in the migration `call/` decision, not left in the tree.

## Invariants (verification lane)

- The applied diff contains **only** declared substitutions (golden-file test).
- An undispositioned flagged token makes `--check` fail (no silent residue).
- `--apply` is idempotent and deterministic — same inputs → same output, no
  `Date`/random (host-lifecycle stays replayable).
- Originals are recoverable: the archive exists before any substitution.
- `host-lint` is unchanged — it gains no dictionary awareness (policy-free).

## Dogfood

The Agentic-MCP-Win32s adoption: author `.host-remap` (the milestone names plus any
sub-codes chosen for denumbering), run `--check` until every tell is
map/allow/acknowledged, `--apply`, confirm the diff is only-substitutions and the
archive is present, then remove the scaffold — durable map captured in the migration
`call/`.

## Out of scope

- An ongoing drift gate (`call/0008`: redundant with `host-lint` and a per-commit
  token cost; fault, policy-free instead).
- Rewriting git history (tier 3 is acknowledged, not rewritten — `call/0007`).
- Inventing any new name — every `new` value is human-supplied.

# plan/0059 remap-and-allowlist-hardening: the migration tooling withstands the process it prescribes

This milestone continues the plan/0056 recipe-and-materialisation-hardening lineage. Where plan/0056
hardened the recipe parser and the bare-store layout, this one hardens the migration tooling: `remap`
and the allowlist surface both mishandle states the methodology's own documented process produces. All
four issues were surfaced by the pgs-release adopter exercising a real migration.

## The defects

- **[#11](https://github.com/connollydavid/host-lifecycle/issues/11)** `remap --check` (run inside
  `software --check`) errors on the retired or absent `.host-remap` that the host process itself
  prescribes: the documented remap phase ends by committing the substitutions and removing
  `.host-remap`, and the recheck then fails on exactly that end state. The tool contradicts its own
  flow. (Sibling of plan/0056's #7, which fixed the empty-dictionary case; this is the absent case.)
- **[#12](https://github.com/connollydavid/host-lifecycle/issues/12)** `remap --apply` rewrites inside
  `host-lint:ignore` fenced blocks, corrupting the boxed durable records whose whole purpose is to
  preserve old names verbatim. In pgs-release it rewrote the rename dictionary inside a migration
  decision's boxed block and had to be restored from an archive commit.
- **[#13](https://github.com/connollydavid/host-lifecycle/issues/13)** the sanctioned-token allowlist
  is split: the hooks and `host-lint --all` read `LEXICON`, while `remap --check` reads a different
  surface, so a token declared in one is unknown to the other. One concept, two disagreeing sources.
- **[#14](https://github.com/connollydavid/host-lifecycle/issues/14)** `software --materialize` always
  does a full-history bare clone, with no shallow or filtered option, so a large-history component pays
  the full cost on every CI leg. An enhancement folded in here (operator ruling: bugs plus the coverage
  gaps).

## Decided direction

- `remap --check` treats the retired or absent `.host-remap` as a fail-safe no-op the same way #7 made
  the empty dictionary one, so the documented end state reads clean rather than error.
- `remap --apply` honours the `host-lint:ignore` fence, skipping substitution inside a boxed block the
  way the naming scan already skips it, so a durable record is never corrupted.
- The allowlist reads one source, so every code path honours the same declared tokens.
- `--materialize` gains a filtered or shallow option (or a documented cache contract) that still lands
  the pinned commit's tree, so the pin stays the reproducibility anchor.

The cast's Fen (the real `qwen3.5-4b`) is the acceptance test for the tool-carried behaviours.

## Verification

Each defect carries a regression test; #12 and #13 additionally assert the anti-corruption and
single-source properties. Ships as one host-lifecycle release, re-vendored and propagated, with the
whole-suite verify gate green and the Fen probe passing.

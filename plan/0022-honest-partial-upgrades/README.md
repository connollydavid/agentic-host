# Honest partial upgrades: an applied-set stamp the tool carries

## Why

The `.host` stamp records a **single** `revision`; `host-lifecycle upgrade` lists
UPGRADING ledger entries newer than it (by git ancestry) as pending. That encodes
one assumption — **entries are applied in ancestry order, contiguously**. A real
adopter several revisions behind may need a *late, independent* entry (a worktree
bugfix, `7de7cb1`) without an *earlier, large, unrelated* one (the specs-to-
software migration, `b6232a5 … 821a216`). The single revision cannot express
"applied the late one, skipped the early ones". The only workaround today — jump
the watermark and note the debt in prose `MEMORY` — **fails unsafe**: `upgrade`
then reports "up to date" while the migration is still owed, and the debt
disappears from the tooling.

This was found in the field (a stuck adopter), and the root cause is that the
upgrade model was designed only from the maintainer's seat — always at HEAD,
applying entries in order. So the design here was worked from four added
stakeholder personas instead (`cast/`): **Orin** (maintainer), **Bly** (adopter
behind), **Sable** (cold-start auditor), **Fen** (low-reliability agent whose tool
calls cannot be trusted). All four independently chose the same stamp model, and
Fen + Bly added the tool-assist requirements that turn "expressible" into
"tool-carried and fumble-proof".

## The design

### Stamp model — watermark + applied set (fail-safe)

`.host` keeps `revision` as a **contiguous baseline** (every ledger entry
ancestor-or-equal to it is applied) and gains an optional `applied = <id> …`
listing entries *above* the watermark applied out of order.

```
template = "…/host-template"
revision = "699db99"            # contiguous baseline
applied  = "7de7cb1 ae1e688"   # cherry-applied above it, out of order
adopted  = "YYYY-MM-DD"
name     = "…"
```

An entry is **applied** ⇔ `ancestor-or-equal(revision)` **or** its id ∈ `applied`.
`upgrade` reports the complement. **Fail-safe property:** a forgotten id re-lists
(over-reports pending) — it can never hide owed work. The dangerous "advance the
watermark past unapplied work" operation is removed entirely (see guard).

Back-compat: an existing `.host` with no `applied` line behaves exactly as today.

### Dependency hints on ledger entries

UPGRADING entries gain optional `independent = true` or `depends = <id> [<id> …]`.
`upgrade` uses them to (a) advise which pending entries are safe to apply alone,
and (b) **fail loud** when the stamp records an entry applied whose declared
`depends` is *not* applied (an inconsistent record). Back-fill the existing
ledger: `7de7cb1` (worktrees) and `ae1e688` (adopt-in-place) are `independent`;
the spec lane chain is `c771d60 depends b6232a5`, `b8c54fc depends c771d60`,
`821a216 depends b6232a5 c771d60`. Absent annotation = independence undeclared
(the tool says so; it does not assume safe).

### The tool carries the process (Fen + Bly)

- **`host-lifecycle upgrade --record <id>`** — records an applied entry by writing
  `.host` itself (idempotent; re-record is a no-op). An agent **never hand-edits
  the stamp**.
- **Machine-readable `upgrade` output** — one line per entry:
  `<id>  <title>  [independent | depends: <id>…]  PENDING|APPLIED`, ordered by
  ancestry, so the agent reads status without parsing prose.
- **Watermark-advance guard** — advancing `revision` to `<rev>` is refused (exit
  non-zero) if any entry ancestor-or-equal `<rev>` is neither in range nor in
  `applied`. Debt cannot be buried by stamping early. This is the structural
  teeth, in the spirit of the worktree-escape HAZARD.
- **Consistency check** — `upgrade` (and `software --check` where cheap) errors
  loud on an applied entry with an unapplied `depends`.

## Build (software-first; each step with its check)

1. **host-lifecycle stamp parse** → read `applied` from `.host`; helper
   `is_applied(entry, revision, applied)` (ancestry OR membership).
   *verify:* unit tests for in-range, in-applied, neither.
2. **Ledger parse** → read `independent`/`depends` per `[upgrade]` entry.
   *verify:* parse test incl. multi-id `depends` and absent (undeclared).
3. **`upgrade` rewrite** → compute applied set, machine-readable listing,
   dependency advice + loud consistency error.
   *verify:* fixture ledger + stamp → expected pending/applied lines; an applied
   entry with an unapplied dep → non-zero.
4. **`upgrade --record <id>`** → idempotent stamp write.
   *verify:* record adds id; re-record no-ops; bad id rejected.
5. **Watermark-advance guard** → refuse advancing `revision` past an unapplied
   entry. *verify:* guard test (advance blocked with a gap; allowed when
   contiguous).
6. **Back-fill ledger annotations** in host-template UPGRADING.
   *verify:* `upgrade` marks `7de7cb1` independent; lane chain shows `depends`.
7. **Spine** → host-template CLAUDE.md upgrade-model section + README *Upgrading*
   rewrite (applied-set, `--record`, the guard); UPGRADING entry for this change.
   *verify:* docs describe the model; `validate` clean.
8. **Bundle the two pending `host=` corrections** (the `host=windows`→omit
   example and the `host=` vs `attest-host` materialize-OS-vs-build-OS wording);
   correct the issue #2 comment.
9. **Apply here** → version bump + tag, re-pin `tools/host-lifecycle`, re-stamp
   `.host` (it gains no `applied` line — agentic-host is contiguous at HEAD), bump
   CI rev; MEMORY entry. *verify:* `upgrade .` up to date; `software --check .`
   clean; tests + clippy green.

## Persona acceptance (the design serves each seat)

- **Orin:** the stamp is the contract, readable without prose; sparse annotations.
- **Bly:** takes the late fix now; the deferred rest stays tooling-visible — and a
  later *cold* read of the stamp (Bly with no memory, or a CI gate) cannot be
  deceived into "up to date" while work is owed; the record fails safe.
- **Fen:** `--record` + machine output + the guard mean the tool carries every
  state change; a fumble re-lists, never buries. **Fen is a real model**
  (`qwen3.5-4b`, Q8_0, local via the `pal` MCP), so this is tested empirically,
  not asserted — see the acceptance gate below.

## Verification (milestone done)

`cargo test` + clippy green; the five build-step checks pass; `upgrade` on a
fixture adopter behind HEAD correctly reports a cherry-applied late entry as
APPLIED and the skipped earlier ones as PENDING; the guard blocks a debt-burying
re-stamp; version tagged; applied here with `upgrade .` up to date and
`software --check .` clean.

**Fen acceptance gate (real model, A/B).** Drive the actual `qwen3.5-4b` (Q8_0,
via the `pal` MCP) through the upgrade loop on a fixture adopter behind HEAD:
given the machine-readable `upgrade` output and the `--record` command, the 4B
must complete a correct cherry-apply (apply the independent late entry, record it,
leave the earlier ones PENDING) without hand-editing `.host`. Baseline: the same
model given the *prose / hand-edit* flow is expected to fumble (mis-edit the stamp
or bury the debt). The gate passes when the tool-carried flow succeeds where the
prose flow fails — proving the design serves Fen, not a simulation of Fen.

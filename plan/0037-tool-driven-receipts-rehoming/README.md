# Re-home the receipts family, entirely tool-driven

## Context

`plan/0030` settled the receipts ontology with the operator but deferred the move to
its own milestone, because the shipped binary reads the applied-set only from `.host`
(`applied_ids`) and the lifecycle receipts only from a single `.host-receipts`. Moving
or splitting those files by hand would silently un-apply every recorded upgrade and
HAZARD the embed and release gate, and CI cold-installs a pinned binary that knows only
the old layout. So the re-homing must be **100% tool-driven**: a host-lifecycle
subcommand performs the move and the split mechanically, the binary auto-migrates on
read, and no file is hand-edited. This milestone reuses none of the prose work; it is
the deferred follow-up named in `plan/0030`.

## The settled ontology, with the 6-of-8 split resolved

The prior review flagged that two framings (everything host-lifecycle executed, versus a
concern-based split) disagree on six of the eight phases. Resolve it by one rule: a
receipt lives in `.host-receipts` only if it is a **methodology-version event**, the act
of moving the project to a template revision. `adopt` sets the baseline and `upgrade`
advances it (carrying the applied-set). Every other phase host-lifecycle runs is
**operational**, a thing done to the project or its components, and lives in
`.host-lifecycle-receipts`.

| File | Records | Written by |
|---|---|---|
| `.host` | the stamp: template, adopted revision, name, baseline | host-lifecycle |
| `.host-receipts` | `adopt` and `upgrade`, plus the applied-set (which **moves here** from `.host`): the methodology-version trail | host-lifecycle |
| `.host-lifecycle-receipts` | the operational phases: `classify`, `embed`, `remap`, `verify`, `publish`, `release` | host-lifecycle |
| `.host-prove-receipts` | cut until host-prove emits receipts (no file for an absent consumer) | none |

The uniform rule stands: `.host-<tool>-receipts` holds what that tool executed, while the
tool-less `.host-receipts` holds the project's methodology-version trail.

## 100% tool-driven, the core requirement

1. **A migration subcommand.** `host-lifecycle migrate-receipts <dir>` performs the whole
   re-homing mechanically and idempotently: it moves the applied-set out of `.host` into
   `.host-receipts`, splits the operational receipts out of `.host-receipts` into
   `.host-lifecycle-receipts`, and leaves the `adopt` and `upgrade` receipts in
   `.host-receipts`. It writes atomically, reports what moved, and a second run is a
   no-op (the project is already on the new layout). The agent runs one command; nothing
   is hand-edited. Operating the move ad hoc (editing the files) is a defect by
   construction, the same stance the lifecycle takes on every phase.

2. **Auto-migrate on read (permanent back-compat).** Every read path tolerates **both**
   layouts: `applied_ids` reads the legacy `applied =` lines in `.host` or the new
   applied-set in `.host-receipts`; the receipt gate unions `.host-receipts` and
   `.host-lifecycle-receipts`. So the gate stays green across the boundary, and an adopter
   that has not yet run `migrate-receipts` is still read correctly. The old-layout reader
   is permanent, retired only by a later decision once no supported adopter is on the old
   side, following the legacy single-`revision` `.host` stamp that the binary still
   auto-migrates on read today.

3. **Writes route by the ontology.** After this lands, `upgrade --record` appends the
   applied record to `.host-receipts`, a new operational receipt is appended to
   `.host-lifecycle-receipts`, and an `adopt` or `upgrade` receipt stays in
   `.host-receipts`. A project still on the old layout is migrated by the next
   `migrate-receipts`, never by a surprise rewrite mid-command.

## Delivery (software-first)

1. **host-lifecycle** (a feature release): the dual-format reader, the `migrate-receipts`
   subcommand, and the ontology-routed writes. Tests: a round-trip (an old-layout fixture
   migrates to the new layout, with the gate green before and after), an idempotent
   re-run, and an auto-migrate-on-read of a legacy fixture with no migration run. Released
   through `host-lifecycle release`, re-pinned, CI install revs bumped.
2. **Spine (host-template)**: update the stamp and receipts description (the applied-set
   now lives in `.host-receipts`; the per-tool `.host-<tool>-receipts` rule), and add an
   `UPGRADING` entry whose action is to bump host-lifecycle and run
   `host-lifecycle migrate-receipts .`, with a machine-checkable state-check `verify`.
3. **agentic-host**: re-pin host-lifecycle, run `migrate-receipts` (the tool-driven
   dogfood, not a hand edit), bump the host-template pointer, record the applied entry,
   verify, CI green.

## Verification

- `migrate-receipts` on an old-layout fixture yields the new three-file layout; the
  receipt gate is green before and after; a second run is a no-op.
- A legacy-layout fixture (applied-set in `.host`, a single `.host-receipts`) is read
  correctly with no migration run (auto-migrate on read), gate green.
- `software --check .` on agentic-host is green after the dogfood migration (the gate
  unions both receipt files; the applied-set is read from `.host-receipts`).
- The weak agent (Qwen-3.5-4B) reaches the single `migrate-receipts` command unaided.
- Whole-suite green (host-lifecycle CI, agentic-host Site and reproducible-build, the
  latter cold-installing the dual-format binary and reading the migrated layout).

## Risks and honesty

- **The dual-format reader ships before the move.** Every read path must tolerate both
  layouts in the same release that adds `migrate-receipts`, or the move un-applies the
  upgrades and HAZARDs the gate. agentic-host migrates only after CI installs that release.
- **CI cold-install.** The reproducible-build and Site jobs install host-lifecycle at the
  new pin, which carries the dual-format reader, so they read the migrated layout fine.
- **Ongoing, not a shim.** The old-layout reader is permanent backward compatibility, not
  a one-time migration helper, because copy-at-version lets each adopter cross the
  boundary at its own pace.
- **Value is organizational.** This is an ontology refinement, not a defect fix; the
  operator settled it in `plan/0030` and chose to execute it. It earns its risk by making
  the receipts model uniform and the applied-set live with the version trail it belongs to.

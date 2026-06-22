# A single file named `host` is the front door that owns the adoption-and-upgrade process

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-16

## Context and Problem Statement

`call/0005` defined the migration protocol and shipped it *as the template's
`MIGRATION.md`*, driven by `host-lifecycle`. But adoption has no front door: there
is no single thing an agent (or a patient human) can be pointed at to turn a repo
into a host and keep it current. The protocol prose also sits inside the template,
which overloads it: the template is pulled toward serving a capability rather
than being the versioned source of the techniques (`call/0004`).

We want: point an agent or a human at **one URL**, and out comes an agentic
project with all the techniques present and **upgradable**. The open question was
*what owns what*, because a self-contained instruction file and a revision-keyed
upgrade ledger cannot both be canonical without forking the spine.

## Considered Options

1. **Template doubles as a plugin marketplace.** One URL, but inverts the
   template's role, making a *source of techniques* into a *server of
   capabilities*, the
   overload `call/0004` exists to avoid.
2. **Standalone repo, multi-file plugin/skill.** Cleaner separation, but more to
   maintain and it buries the front door inside an engine.
3. **Standalone repo, a single instruction file named `host` that owns the
   *process*; the template keeps the *techniques* and the *ledger*.** One file,
   one URL, no overload.

## Decision Outcome

Chosen option 3.

- **`host` is a single instruction file** in its own repo
  (`https://github.com/connollydavid/host`). It is the front door: an agent or a
  human follows it to **adopt**, **migrate**, or **upgrade**, and ends with an
  agentic project carrying the methodology's techniques.
- **`host` is developed here as software, not as a tool submodule of this repo.**
  It gets a `[software "host"]` stanza in `.host-software`: a bare store with a
  worktree, pinned by SHA, gitignored, exactly like `host-lint` (`call/0010`). It
  is *consumed* downstream as a submodule; it is *developed* here as a worktree.
- **`host` owns the process; the template owns the techniques and the ledger.**
  This is the split that keeps "upgradable" true with no fork:
  - **`host`** = the adopt/migrate/upgrade **procedure** (what `MIGRATION.md`'s
    steps were). Stable; rarely edited.
  - **template** = the **techniques** (the `CLAUDE.md` spine, the room scaffold,
    the tool pins) *and* the revision-keyed **upgrade ledger** (`UPGRADING.md`,
    one `[upgrade "<revision>"]` stanza per structural migration). The ledger is
    data the template's own changes generate, so it lives with them.
- **Upgradability is automatic and lockstep-free.** A produced folder records its
  adopted template revision in `.host`. To upgrade, `host` tells the
  operator to run `host-lifecycle upgrade <dir>`, which prints every template
  ledger entry newer than the stamp; apply them; re-stamp. The procedure (`host`)
  does not change when the template adds a ledger entry; only the template does.
- **Copy-at-version, not embed.** A produced folder copies the spine in at the
  adopted revision and stamps it (`call/0004`); it does not submodule the
  template. (This forge embeds the template as a submodule for development
  convenience only; it is adopter-zero, not a produced folder.)

This **amends `call/0005`**: the protocol is no longer shipped *as the template's
`MIGRATION.md`*. Its procedural content moves to `host`; the template's
`MIGRATION.md` is reduced to a pointer at `host`. `UPGRADING.md` stays in the
template. The cased/moded protocol itself (`call/0005`) and the clean-break /
delta distinction (`call/0007`) are unchanged; only their home moves.

## Consequences

- Good: one URL, one file, dual-audience (agent or human). The template stops
  drifting toward being a capability server; `call/0004` holds.
- Good: `host` stays a stable single file because the per-revision ledger (the
  part that churns) remains in the template with the techniques that cause it. No
  lockstep between `host` and template revisions.
- Cost: the procedure and the ledger now live in two repos, so a reader must
  follow one reference (`host` to the template's ledger) instead of reading one
  document. The single-file ideal is "self-contained *procedure*", not
  "everything inline".
- Cost: a new repo to maintain and a new `.host-software` stanza in this forge.
- Migration of this decision itself: move `MIGRATION.md`'s steps into `host`,
  leave `UPGRADING.md` in the template, and replace the template `MIGRATION.md`
  with a pointer, tracked as follow-on work, not done by accepting this record.

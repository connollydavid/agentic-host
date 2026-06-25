# Rename the front-door check to `entrance`, with a deprecate-then-retire migration

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (the `entrance` and `entrance --check` subcommands, formerly
  `front-door`; the `.host-software` `entrance = true` flag, formerly `front-door =
  true`; the deprecate-then-retire migration shim). agentic-host-local. The rename is
  pulled forward from `plan/0043`, ahead of that milestone's opt-in generalization.
- Relates: `plan/0043` (the entrance milestone; the name settled by Qwen-3.5-4B data);
  `call/0026` and `plan/0040` (the front-door check this renames; its agentic-host-local
  scope stands); `plan/0039` (the deprecate-then-retire path and the fail-safe cutover,
  reused here for a config-key rename).

## Context and Problem Statement

The front-door check (`call/0026`, host-lifecycle v0.27.0) named the methodology's
single-file entry point `front-door`. `plan/0043` settled the name `entrance` by a
Qwen-3.5-4B run over the host-and-guest metaphor (a guest comes in the entrance),
chosen with no alias the way `plan/0039` fixes a name that overfits. The operator chose
to land the rename now as a standalone change, keeping the capability hardwired and
agentic-host-local, and to defer the opt-in generalization to `plan/0043`.

A rename with no alias strands any surviving old spelling. A `.host-software` that still
reads `front-door = true` is silently demoted to a component, the silent failure
`plan/0039` forbids. So the rename owes a migration.

## Decision

- Rename `front-door` to `entrance` with no alias: the subcommand, the `.host-software`
  flag, the code, and the agentic-host CI invocation. Released as host-lifecycle
  v0.28.0.
- A migration carries the transition, deprecate-then-retire (`plan/0039`). The parser
  accepts a legacy `front-door = true` as the entrance, so a pre-rename `.host-software`
  keeps working rather than dropping to a component; the `entrance` command warns and
  names the rename, so the old spelling never passes silently. The shim is slated for
  removal a release later. Released as host-lifecycle v0.28.1.
- Comments read forward-looking, naming `entrance`; the migration shim is the one place
  the old spelling lives.
- The scope stays agentic-host-local. No adopter declares an entrance, so no `UPGRADING`
  entry is owed; the generalization that would make entrances adopter-facing stays with
  `plan/0043`.

## Considered Options

1. **Rename and generalize as one atomic change (`plan/0043` as designed).** Declined by
   the operator for now: pull the rename forward, defer the generalization.
2. **Rename with a permanent alias.** Rejected: the `plan/0039` way fixes an overfit
   name, it never aliases it.
3. **Rename with no migration (the v0.28.0 cutover alone).** Rejected: a surviving
   `front-door = true` is silently demoted to a component.
4. **Rename, no alias, plus a deprecate-then-retire migration shim (chosen).**

## Consequences

- Good: the name matches the host-and-guest metaphor of the methodology; a pre-rename
  `.host-software` still resolves and is told to rename; the codebase reads
  forward-looking.
- Costs: a second release (v0.28.1) carries the migration that the v0.28.0 cutover
  omitted; the shim is debt, owed a retirement a release later (a named follow-up). The
  full plan/0039 retire step (a hard fail plus an adopter ledger entry) waits until the
  generalization makes entrances adopter-facing.

## Confirmation

`entrance --check .` is clean on agentic-host's front door. A legacy `front-door = true`
warns and still resolves the entrance, covered by a unit test. The full host-lifecycle
suite is green, the released binary gates green, and the whole-suite CI is green.

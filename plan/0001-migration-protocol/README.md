# Migration protocol

Build the protocol, tooling, and decisions for bringing an existing repo under
the host methodology, and dogfood it by migrating this host.

- Status: **done.** Protocol, tooling, and host self-migration shipped; the
  external case-(b) dogfood is satisfied by the completed `yarn-agentic` adoption
  (see "External dogfood" below).
- Decisions: `call/0004` (the template is the versioned source), `call/0005`
  (the cased, moded migration protocol).

## What shipped

- **`host-lifecycle` migrate verbs** (`adopt` / `version` / `classify`, with
  `--dry-run`): the token-free, mechanical half, scaffold `cast/ plan/ call/`,
  write and read the `.host` stamp, report the migration case.
- **`host-template/MIGRATION.md`**: the protocol payload, on two
  orthogonal axes, **case** (a none / b foreign / c ours-prior) decides how
  governance is established; **mode** (Preview / Shallow / Staged / Deep, with a
  selection rule and history-immutable-by-default) decides the blast radius.
- **This host, migrated (case c, Shallow):** stamped at the template revision in
  `.host`; the host model and copy-at-version sourcing recorded
  in `CLAUDE.md`; this `plan/` room established.

## External dogfood, closed

The goal of the follow-on was to validate the protocol on a real external repo.
That is **satisfied** by the **`yarn-agentic`** adoption (reported in `agentic-host`
issue #6): a complete case-(b) migration of a mature **131-milestone** inference
project (two embedded forks, 18 spec-bearing milestones, 153 spec files), staged as
five reviewed PRs to `main`, ending green (`validate plan/call`, `software --check`,
the spec gate, published site). That is a *larger* case-(b) stressor than the two
originally listed, and it surfaced real defects (the doc-site gaps fixed in
`plan/0003` / `call/0014`, plus four host-lifecycle tooling fixes), exactly what a
dogfood is for.

The originally-listed candidates are therefore **descoped**:

- **pgs-release** (case b): superseded by `yarn-agentic`, the larger case-(b)
  exercise. Left unmigrated.
- **Agentic-MCP-Win32s** (case c): its earlier attempt over-reached (rewrote the
  append-only record) and was rejected; the `.host-lint-allow` / exclude-don't-rewrite
  fixes it prompted (`call/0006`, `call/0009`) already landed. Left unmigrated; can be
  re-attempted later as its own milestone if a case-(c) exercise is wanted.

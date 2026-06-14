# Migration protocol

Build the protocol, tooling, and decisions for bringing an existing repo under
the agentic-host methodology — and dogfood it by migrating this host.

- Status: done (protocol, tooling, host self-migration); follow-on external
  dogfoods pending.
- Decisions: `call/0004` (the template is the versioned source), `call/0005`
  (the cased, moded migration protocol).

## What shipped

- **`host-lifecycle` migrate verbs** (`adopt` / `version` / `classify`, with
  `--dry-run`): the token-free, mechanical half — scaffold `cast/ plan/ call/`,
  write and read the `.host` stamp, report the migration case.
- **`host-template/MIGRATION.md`**: the protocol payload, on two
  orthogonal axes — **case** (a none / b foreign / c ours-prior) decides how
  governance is established; **mode** (Preview / Shallow / Staged / Deep, with a
  selection rule and history-immutable-by-default) decides the blast radius.
- **This host, migrated (case c, Shallow):** stamped at the template revision in
  `.host`; the agentic-host model and copy-at-version sourcing recorded
  in `CLAUDE.md`; this `plan/` room established.

## Follow-on (separate milestones, not in this one)

Validate the protocol on real external repos:

- **Agentic-MCP-Win32s** — case c, Shallow: re-point the renamed tool submodules,
  rename its ordinal-named milestone docs, reconcile its `AGENTS.md`.
- **pgs-release** — case b, Staged Shallow (not Deep): merge its foreign
  `CLAUDE.md`, rename its many ordinal-named milestone docs and their
  cross-references, acknowledge the legacy history (the upstream patch-series
  provenance forbids a history rewrite).

The full approved plan, with the grounded per-target audit, is the source for
these.

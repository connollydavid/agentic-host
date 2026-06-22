# Adoption remap is enforced by a dictionary applied deterministically, then removed

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-14
- Relates to: `call/0007` (clean-break tier 2 is "map-only"), `call/0006` (the allow-list), `call/0003` (tools composed as submodules), `CLAUDE.md` §6 (the append-only escape valve this enforces).

## Context and Problem Statement

`call/0007` says the owned record may be rewritten at adoption only "map-only":
substitute the documented rename tokens, invent nothing. As **prose discipline**
this failed in Agentic-MCP-Win32s PR #1: parallel sub-agents denumbered the record
independently and **drifted**: the same concept surfaced under names that were in
no map ("the network-and-transport milestone" was invented). Two needs follow: the
map-only rule must be **mechanically enforced**, not promised; and the migration
must not leave the old vocabulary behind as a permanent artifact.

## Decision Outcome

**An enforced mapping dictionary, applied token-free, used as removable scaffold.**

- **One declared dictionary**: `old-concept to canonical-new-name`, human-approved.
  It covers milestone names and any sub-codes the human chooses to denumber; the
  **new name is always supplied by the human**; the tool never coins one.
- **Deterministic applier** (in `host-lifecycle`, the token-free migrator): applies
  *only* declared substitutions, word-bounded, archives originals first, and
  **refuses to touch any unmapped token**. No LLM in the substitution loop, so
  fabrication and spatial drift (inconsistent names across files/agents) are
  *structurally impossible*, not merely discouraged.
- **Completeness check**: enumerates every token `host-lint` flags; each must be
  dispositioned as **map** (rename it), **allow** (`.host-lint-allow` vocabulary),
  or **acknowledge** (legacy residue). It fails while any flagged token is
  undispositioned, so there is no silent residue and no guessed mapping.
- **No ongoing gate; fault, policy-free.** Preventing *future* drift is already
  `host-lint`'s job; a new numbered concept is a tell the detector catches
  regardless of the dictionary. An ongoing gate that resolved every reference
  against the dictionary would also **cost tokens on every commit, forever**, for
  drift already prevented for free. So `host-lint` stays a **pure detector that
  faults on any tell and never consults the dictionary**; all dictionary logic is
  confined to the one-time `host-lifecycle` applier; the engine never learns policy.
  After a clean remap there are no tells, so a policy-free fault is exactly right:
  anything that faults later is a genuine new tell to fix, not something to resolve.
- **Removable scaffold, applied then cleaned.** Applying the map runs with the
  dictionary committed (so the diff reviews as *only* mapped substitutions, beside
  the archive). A follow-up deletes the dictionary file: the repo must not permanently
  carry an artifact whose content is the old ordinal names. The durable copy lives in
  the migration `call/` decision (documenting old-to-new is appropriate *there*) and in
  the apply commit, recoverable via `git`; the Rosetta stone sits in the same
  stratum (history/decision) as the old names it decodes; the live tree stays clean.
- **Coupling.** Removable-scaffold requires the **full** clean break: the live
  *record* is remapped too (archived), so nothing live still references an old name.
  The alternative, keep+dictionary (record left verbatim), makes the dictionary
  load-bearing and permanent; that is the non-clean-break mode and accepts the
  elephant by design.

## Consequences

- Good: "map-only" is a mechanical guarantee, not a promise; PR #1's spatial drift
  and fabrication cannot recur under the applier.
- Good: the completeness check makes the residual explicit and human-dispositioned
  (the irreducible non-mappable codes, review codes, bare version-like numbers, are surfaced and
  consciously allow-listed or acknowledged, never silently left or invented away).
- Good: no permanent old-vocabulary artifact and no redundant ongoing gate.
- Cost: more human input up front: a canonical name for every flagged concept. That
  input *is* the anti-fabrication guarantee, not overhead to optimise away.
- Builds on the trio: `host-lint` enumerates the flags (and gates new tells forever),
  `.host-lint-allow` dispositions vocabulary, the dictionary dispositions renames.

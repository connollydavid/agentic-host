# Verification lanes are mandatory when used: wire them, don't just reference

## The bug

The reference host never wired the verification tools the methodology prescribes:
`tools/` does not exist here, so the allium skills (`elicit`, `distill`, `tend`,
`weed`, `propagate`) are absent and an agent falls back to hand-authoring `.allium`
and driving the CLI, the wrong half of the lifecycle. The spine also stated the
lanes descriptively ("specs are checked by allium / specula"), so an adopter could
read them as optional decoration. They are not: **once a spec of a kind exists, its
tool, skills, and CI lane are required.** TLA+ stays optional until a `.tla`
appears; allium stays optional until a `.allium` appears, but not after.

## Order (per direction): tighten language, then test the migration

### 1. Tighten the language (decisive, RFC-2119)

Spine (`CLAUDE.md` + `STRUCTURE.md`): make the lane a conditional **MUST**.

- A component carrying a `.allium` spec **MUST** wire `tools/allium`, generate its
  skills, author/maintain the spec **with the skills** (`elicit`/`distill` to
  `tend` to `weed`), and gate it in the software's CI with `allium check` +
  `allium analyse` + `allium plan`; the `plan` obligations **MUST** be discharged
  by the software's tests (`propagate` generates them).
- A component carrying a `.tla` spec **MUST** wire `tools/specula` and TLC-check it
  in the software's CI.
- A spec present without its full lane is a **defect**, not a choice. The tools are
  referenced submodules; the skills are generated, gitignored symlinks
  (`link-skills.sh`), per worktree-absence coherence.

`UPGRADING.md` ledger entry so **every upgrader** applies it (the "upgraders must
fix this" requirement).

### 2. Test the migration (full alignment, in advance)

Apply the new ledger entry to agentic-host itself (it is an adopter and must
upgrade), so it reaches **full alignment**:

- Add `tools/allium`, `tools/specula`, `tools/host-lifecycle` as submodules
  (`host-lint` stays the *Where* software, skill wired from its worktree).
- Add `link-skills.sh`; gitignore `.claude/skills/*`; generate the skill symlinks
  (the allium skills become available next session).
- Confirm `host-lifecycle software --check` stays clean (no dangling-symlink
  HAZARD) and the generated skills resolve.

Running the migration here is the test: if the ledger entry is right, its execution
brings this host into alignment with no surprises.

## Verification

- Spine reads as a conditional MUST; `UPGRADING` carries the entry.
- `tools/{allium,specula,host-lifecycle}` materialized; `.claude/skills/` holds the
  six allium skills + host-lint; all gitignored, none tracked.
- `host-lifecycle software --check` clean (no HAZARD); a reloaded session lists the
  allium skills.

## Not done here

An enforcement *gate* in host-lifecycle (fail when a materialized component carries
a spec with no lane) is the ultimate teeth; recorded as a candidate follow-on so
the MUST is mechanically checked, not only reviewed.

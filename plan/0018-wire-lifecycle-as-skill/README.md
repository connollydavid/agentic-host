# Wire host-lifecycle as phase skills; the phases are an unconditional MUST

## Why

allium and specula ship Claude skills; an agent drives them through `elicit`,
`tend`, `weed`, … host-lifecycle (**our own** tool) ships none, so an agent
operates the methodology lifecycle ad-hoc, by recalling commands. That is exactly
the failure the skills exist to prevent. Wire host-lifecycle the same way: a skill
per lifecycle phase, generated into `.claude/skills/` by `link-skills.sh`.

And the phases are stronger than the verification lanes: a lane is **conditional**
(only when a spec of its kind exists), but the lifecycle phases have **no opt-out**:
every agentic project is scaffolded, embedded, migrated, verified, published and
upgraded through them. Ad-hoc operation is a defect.

## What ships (host-lifecycle `skills/<phase>/SKILL.md`)

One skill per content-named phase, each driving the matching host-lifecycle command
and owning the judgment around it:

- **classify**, read the repo, print the migration case (a/b/c), draft the rename
  map + merge plan. (`classify`; `host-lint --all`/`--log`)
- **adopt**, establish governance (the case-b merge judgment), scaffold
  `cast/ plan/ call/`, write the `.host` stamp. (`adopt`)
- **embed**, embed the software as a bare store with worktrees; write/maintain
  `.host-software`; materialize and check. (`software --materialize`/`--check`)
- **remap**, apply the rename via the `.host-remap` dictionary, dispositioning
  every tell. (`remap --check`/`--apply`)
- **verify**, the gate sweep: `validate plan/`+`call/`, `software --check` (pins,
  lanes, obligations), `book --check`, the throwaway-tell hook test.
- **publish**, generate the mdBook site in lifecycle order. (`book`)
- **upgrade**, apply the `UPGRADING` ledger actions newer than the `.host` stamp,
  re-stamp. (`upgrade`)

## Then

- Bump `tools/host-lifecycle`; re-run `link-skills.sh`; the phase skills appear in
  `.claude/skills/` (gitignored).
- Spine MUST (`CLAUDE.md` + `STRUCTURE.md`): the lifecycle phases are mandatory,
  driven through the skills + commands, **no opt-out**. `UPGRADING` entry.

## Verification

- `link-skills.sh` links the new phase skills; a reloaded session lists them.
- `host-lifecycle software --check` stays clean (the new skills are generated,
  untracked, so no HAZARD).

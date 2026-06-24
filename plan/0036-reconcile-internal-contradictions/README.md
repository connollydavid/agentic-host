# Reconcile internal contradictions

## Context

A deep audit (first run 2026-06-24, re-run after the deferred-item campaign) found a
set of contradictions where the host's own instance docs restate methodology the spine
has since moved: the `STRUCTURE.md` room map, the `README.md` tool list, and the
`CLAUDE.md` verification model. Each staled when a past milestone changed the spine
cleanly. `plan/0012` moved specs to live with the software; `plan/0029` moved the Where
room to the nested `software/<name>/<branch>/` layout; `plan/0023` added `host-prove`
and the six-rung ladder. Every one of those propagated correctly, yet each also staled
the host's own restatement of the same concept, and nothing prompted a re-reading.

So the contradictions are symptoms of one root cause: **migration and upgrade propagate
a spine change but never prompt a re-examination of the project's own instance docs for
the drift that change introduces.** The drift accumulates silently until a manual audit
catches it. The audit this milestone rests on was that demonstration: needing a
deep manual sweep to find this drift is itself the evidence that a reflective practice
the methodology should carry is absent.

This milestone reconciles the drift and closes the gap that produced it. Fixing the
stale docs alone would let the next spine change stale them again.

## The practice that closes the gap (the spine doctrine)

The hygiene grammar already grows by reflective practice (`plan/0034`): because an agent
seldom perceives its own register as a tell, reflection is prompted at the verify gate
and at adoption. Migration drift has the same shape one level up. An agent applying a
spine change seldom re-reads the project's own restatements of methodology against it,
so the spine gains a sibling reflective practice:

When a spine change is applied (an upgrade record, an adoption), the operator and the
agent re-examine the project's own instance docs for drift the change introduced, and
reconcile them in place. In scope are the restatements the spine does not own
verbatim: the `STRUCTURE.md` room map, the `README.md` and `CLAUDE.md` tool list and
verification model, and the recorded Where layout. The reflection is prompted at the
same moments as the grammar reflection (the upgrade record, the verify gate, adoption);
the agent assists and the operator validates; a confirmed divergence is reconciled
against the spine. Discovery is mechanizable later as a check that flags known
divergence shapes such as a spec path under `plan/` or a Where path off `software/`,
the way the gather mechanized tell-discovery after the grammar doctrine. That
mechanization is a named follow-up, not this milestone.

Authority: this is a methodology change, so it lives in the spine (`host-template`),
never a project `call/` (anti-ouroboros). It ships as a `CLAUDE.md` doctrine plus a
reflection step in the `upgrade`, `adopt`, and `verify` skills, with an `UPGRADING`
ledger entry, adopted in agentic-host like any spine change.

## The drift to reconcile now (the symptoms)

| Finding | Evidence | Fix | Authority |
|---|---|---|---|
| Root `CLAUDE.md` contradicts itself and the spine on the verification model. The "Agentic-host model" paragraph says verification runs in three lanes and lists the host-* family without `host-prove`, while the same file's overview names `host-prove` the ladder driver and the spine defines a six-rung ladder. | `CLAUDE.md:24` vs `CLAUDE.md:9` and `:11` and `host-template/CLAUDE.md` "The verification ladder". | Rewrite the paragraph to the six-rung ladder and include `host-prove`. | host-local prose |
| `STRUCTURE.md` (the room map) is a stale local copy. It places the What room at `plan/<NNNN>/spec/` (the spine forbids a spec under `plan/`, and root `CLAUDE.md:14` says specs live with the software), and the Where room at `host-lint/` (the retired root-scattered layout, now `software/<name>/<branch>/`), naming only host-lint of the five embedded components. | `STRUCTURE.md:9` and `:11` vs `host-template/STRUCTURE.md` (correct: What and Where at `<software>/`), root `CLAUDE.md`, and the live `software/` tree. | Sync the host room map to the spine and the real layout. This also removes the conceptual root of the orphan `plan/0001-foundation/spec/` directory. | host-local prose |
| Root `CLAUDE.md` points a spine change at a procedure file that is now a redirect stub. | `CLAUDE.md:26` ("re-run the migration (`host-template/MIGRATION.md`)") vs `host-template/MIGRATION.md` (a redirect to the `host` repo; routine spine changes propagate via `host-lifecycle upgrade`). | Point the sentence at the live mechanism; keep the load-bearing "do not fork the spine in isolation". | host-local prose |
| `README.md` names only three host-* tools, omitting `host-prove`. | `README.md:4` ("`host-grammar`, `host-lint`, `host-lifecycle`") vs `CLAUDE.md:9` and `.host-software` (host-prove is embedded and released). | Add `host-prove`. | host-local prose |
| `call/0017` authored a methodology rule now resident in the spine, yet remains `accepted` in the software-only Why room. | `call/0017:5` (`Scope:` includes `host-template`) and its body ("a real spine semantics change"); the rule lives in `host-template/CLAUDE.md` and is applied as `.host` rev `617e420`. | Retire `call/0017` the MADR way: `Status: superseded by the spine`, in place. Review `call/0018` under the same test (its scope is software and the spine cites it by name, so it reads softer); keep or retire with a recorded reason. `call/0021` was checked and is clean. | host-local `call/` status |
| The `host-prove` `.host-software` pin sits one CI-only commit past its release tag. | `.host-software` host-prove `pin = 5e01f58` (`git describe` = `v0.2.2-1-g5e01f58`); the `v0.2.2` tag is `3ca95fc`; the extra commit touches only `ci.yml`, so the artifact still reproduces. | Re-pin to the tag commit `3ca95fc`, or record the artifact-preserving pin-advance rationale. | host-local `.host-software` |
| Two record-tidiness defects. | An empty untracked `plan/0001-foundation/spec/` left from the host#12 live-trigger probe (a number collision with `0001-migration-protocol`); and PLAN.md's Skill-Hardening status box is unchecked while `SKILL-HARDENING.md` shows every goal done. | Remove the orphan directory; check the PLAN.md box and fold in the standing crates.io deferral. | host-local |

The session auto-memory staled the same way during the campaign (the prose lane is now
wired and clean, the applied-set moved, the tools are at v0.23.0). That is the agent's
own working memory, the same drift shape at a different layer; it is corrected directly
as memory hygiene, not tracked as a milestone finding.

## Resolved during the deferred-item campaign

- **Prose-hygiene gate** (the original headline finding): the spine documented a
  `verify` recheck that re-runs the prose audit, but `lifecycle.manifest` ran only
  `validate`. Closed in host-lifecycle v0.22.0 (`plan/0030` D4): the recheck chains
  `host-lifecycle prose .`, so `software --check` re-runs the audit and re-opens a
  regressed doc as a HAZARD.

## Verification

- The spine carries the migration-reflection doctrine, the `upgrade`/`adopt`/`verify`
  skills prompt it, an `UPGRADING` entry records it, and agentic-host adopts it.
- Root `CLAUDE.md`: the verification-model paragraph names `host-prove` and the six-rung
  ladder, with no surviving "three lanes" claim; the migration sentence resolves to a
  live mechanism.
- `STRUCTURE.md`: the What and Where rooms point at the software, never `plan/spec/` or
  the root-scattered layout; `software --check` and the doc-site build stay green.
- `README.md`: the host-* tool list includes `host-prove`.
- `call/0017`: `Status: superseded by the spine`; `host-lifecycle validate plan/ call/`
  clean; `call/0018` dispositioned with a recorded reason.
- `host-prove` pin: `git -C software/host-prove/main describe --tags` reports an exact
  `v0.2.2`, or a recorded rationale; `software --check` and `--verify-build` green.
- Tidiness: `plan/0001-foundation/` is gone; PLAN.md records Skill-Hardening complete
  with the crates.io deferral noted.

Whole-suite green across the affected repos at close.

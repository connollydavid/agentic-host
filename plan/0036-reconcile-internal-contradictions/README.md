# Reconcile internal contradictions

## Context

A cross-cutting audit of the plans, decisions, spine, and governance docs first ran
2026-06-24 and surfaced a set of internal contradictions: places where two of the
project's own assertions cannot both be true, or where a record states something the
implementation does not do. A second deep audit, after the deferred-item closure
campaign shipped host-lifecycle v0.21.0 through v0.23.0 and re-homed the receipts
family, refreshed this inventory. The campaign was expected to introduce drift, and it
did, so the table below is the current accurate set. This milestone owns the fixes.

Scope discipline: this plan holds the contradiction findings, each of which had no
prior home. Previously deferred follow-ups keep their existing homes and are not
restated here. PLAN.md remains the single index of all open work.

## Open findings and dispositions

| Finding | Evidence | Fix | Authority |
|---|---|---|---|
| Root `CLAUDE.md` contradicts itself and the spine on the verification model. The "Agentic-host model" paragraph says verification runs in three lanes and lists the host-* family without `host-prove`, while the same file's overview names `host-prove` the ladder driver and the spine defines a six-rung ladder. | `CLAUDE.md:24` vs `CLAUDE.md:9` and `:11` and `host-template/CLAUDE.md` "The verification ladder". | Rewrite the paragraph to the six-rung ladder and include `host-prove`. | host-local prose |
| `STRUCTURE.md` (the room map) is a stale local copy. It places the What room at `plan/<NNNN>/spec/` (the spine forbids a spec under `plan/`, and root `CLAUDE.md:14` says specs live with the software), and the Where room at `host-lint/` (the retired root-scattered layout, now `software/<name>/<branch>/`), naming only host-lint of the five embedded components. | `STRUCTURE.md:9` and `:11` vs `host-template/STRUCTURE.md` (correct: What/Where at `<software>/`), root `CLAUDE.md`, and the live `software/` tree. | Sync the host room map to the spine and the real layout. This also removes the conceptual root of the orphan `plan/0001-foundation/spec/` directory. | host-local prose |
| Root `CLAUDE.md` points a spine change at a procedure file that is now a redirect stub. | `CLAUDE.md:26` ("re-run the migration (`host-template/MIGRATION.md`)") vs `host-template/MIGRATION.md` (a redirect to the `host` repo; routine spine changes propagate via `host-lifecycle upgrade`). | Point the sentence at the live mechanism; keep the load-bearing "do not fork the spine in isolation". | host-local prose |
| `README.md` names only three host-* tools, omitting `host-prove`. | `README.md:4` ("`host-grammar`, `host-lint`, `host-lifecycle`") vs `CLAUDE.md:9` and `.host-software` (host-prove is embedded and released). | Add `host-prove`. | host-local prose |
| `call/0017` authored a methodology rule now resident in the spine, yet remains `accepted` in the software-only Why room. | `call/0017:5` (`Scope:` includes `host-template`) and its body ("a real spine semantics change"); the rule lives in `host-template/CLAUDE.md` and is applied as `.host` rev `617e420`. | Retire `call/0017` the MADR way: `Status: superseded by the spine`, in place. Review `call/0018` under the same test (its scope is software and the spine cites it by name, so it reads softer); keep or retire with a recorded reason. `call/0021` was checked and is clean. | host-local `call/` status |
| The `host-prove` `.host-software` pin sits one CI-only commit past its release tag. | `.host-software` host-prove `pin = 5e01f58` (`git describe` = `v0.2.2-1-g5e01f58`); the `v0.2.2` tag is `3ca95fc`; the extra commit touches only `ci.yml`, so the artifact still reproduces. | Re-pin to the tag commit `3ca95fc`, or record the artifact-preserving pin-advance rationale. | host-local `.host-software` |
| Two record-tidiness defects. | An empty untracked `plan/0001-foundation/spec/` left from the host#12 live-trigger probe (a number collision with `0001-migration-protocol`); and PLAN.md's Skill-Hardening status box is unchecked while `SKILL-HARDENING.md` shows every goal done. | Remove the orphan directory; check the PLAN.md box and fold in the standing crates.io deferral. | host-local |

## Resolved during the deferred-item campaign

- **Prose-hygiene gate** (the original headline finding): the spine documented a
  `verify` recheck that re-runs the prose audit, but `lifecycle.manifest` ran only
  `validate`. Closed in host-lifecycle v0.22.0 (plan/0030 D4): the recheck chains
  `host-lifecycle prose .`, so `software --check` re-runs the audit and re-opens a
  regressed doc as a HAZARD. The spine claim is now true and the gate enforces it.

## Related drift, handled separately as memory hygiene

The second audit also found the session auto-memory stale after the campaign (the
prose lane is now wired and clean, the applied-set moved to `.host-receipts`, the
tools are at v0.23.0). That is the agent's own working memory, not a repository
contradiction, so it is corrected directly rather than tracked as a milestone finding.

## Verification

- Root `CLAUDE.md`: the verification-model paragraph names `host-prove` and the
  six-rung ladder, with no surviving "three lanes" claim; the migration sentence
  resolves to a live mechanism.
- `STRUCTURE.md`: the What and Where rooms point at the software, never `plan/spec/`
  or the root-scattered layout; `software --check` and the doc-site build stay green.
- `README.md`: the host-* tool list includes `host-prove`.
- `call/0017`: `Status: superseded by the spine`; `host-lifecycle validate plan/ call/`
  clean; `call/0018` dispositioned with a recorded reason.
- `host-prove` pin: `git -C software/host-prove/main describe --tags` reports an exact
  `v0.2.2`, or a recorded rationale; `software --check` and `--verify-build` green.
- Tidiness: `plan/0001-foundation/` is gone; PLAN.md records Skill-Hardening complete
  with the crates.io deferral noted.

Whole-suite green across the affected repos at close.

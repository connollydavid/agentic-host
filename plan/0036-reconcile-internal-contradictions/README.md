# Reconcile internal contradictions

## Context

A cross-cutting audit of the plans, decisions, spine, and governance docs (run
2026-06-24) surfaced a set of internal contradictions and stale records: places
where two of the project's own assertions cannot both be true, or where a record
states something the implementation does not do. This milestone owns the fixes for
those findings.

Scope discipline: this plan holds **only** the newly surfaced findings, each of
which had no prior home. Previously deferred follow-ups (the plan/0029 residuals,
the plan/0030 receipts-family re-homing, the plan/0035 gather-corpus and
host-prove kani-ENOENT items, the plan/0034 project-local ban surface) keep their
existing homes and are deliberately **not** restated here; re-listing a tracked
item would duplicate its record. PLAN.md remains the single index of all open
work.

## Findings and dispositions

| Finding | Evidence | Fix | Authority |
|---|---|---|---|
| The spine asserts a prose-hygiene gate it does not implement. The `verify` receipt is documented as re-verified by re-running the prose audit, so a regressed doc re-opens as a HAZARD; the manifest the gate reads runs only `validate`. | `host-template/CLAUDE.md:226`; applied ledger entry `host-template/UPGRADING.md:165` (`950fbd6`, recorded in `.host`); contradicted by `host-template/lifecycle.manifest:61` (`recheck = host-lifecycle validate plan/ call/`, no prose term). | Reconcile the spine record with reality: either land the recheck wiring, or correct the docs and the applied ledger entry so they stop asserting an unimplemented gate. The wiring path itself is tracked separately as plan/0030 D4 and is not duplicated here; this plan owns making the **record honest**. **RESOLVED 2026-06-24** (deferred-item campaign): D4 landed in host-lifecycle v0.22.0 (the verify recheck chains `host-lifecycle prose .`, in-process), so the spine claim is now true and the gate enforces it. | spine (host-template), re-propagated |
| Root `CLAUDE.md` contradicts itself and the spine on the verification model. The "Agentic-host model" paragraph says verification runs in three lanes and lists the host-* family without `host-prove`, while the same file's overview lists `host-prove` and the spine defines a six-rung ladder it drives. | `CLAUDE.md` "Agentic-host model" paragraph vs `CLAUDE.md` overview (the four-tool family, `host-prove` as the ladder driver) and `host-template/CLAUDE.md` "The verification ladder". | Update the host paragraph to the six-rung ladder and include `host-prove`. | host-local (instance prose) |
| Root `CLAUDE.md` points spine changes at a procedure file that is now a redirect stub. | `CLAUDE.md` ("re-run the migration (`host-template/MIGRATION.md`)") vs `host-template/MIGRATION.md` (a redirect to the `host` repo; routine spine changes propagate via `host-lifecycle upgrade`). | Point the sentence at the live mechanism; keep the load-bearing "do not fork the spine in isolation". | host-local (instance prose) |
| `call/0017` authored a methodology rule now resident in the spine, yet remains `accepted` in the software-only Why room. | `call/0017:5` (`Scope:` includes `host-template`) and its body ("a real spine semantics change"); the rule lives in `host-template/lifecycle.manifest` and is applied as `.host` rev `617e420`. | Retire `call/0017` the MADR way: `Status: superseded by the spine`, in place. Review `call/0018` under the same test (software-scoped but authored a now-resident principle); keep or retire with a recorded reason. `call/0021` was checked and is clean (software-scoped, cites the spine MUST). | host-local (`call/` status) |
| The `host-prove` `.host-software` pin sits one CI-only commit past its release tag. | `.host-software` host-prove `pin = 5e01f58` (`git describe` = `v0.2.2-1-g5e01f58`); the `v0.2.2` tag is `3ca95fc`; the extra commit touches only `ci.yml`, so the artifact still reproduces. | Re-pin to the tag commit `3ca95fc` (doctrine: the pin is the released tag commit), or record the artifact-preserving pin-advance rationale if kept. | host-local (`.host-software`) |
| Two record-tidiness defects surfaced alongside the audit. | An empty untracked `plan/0001-foundation/spec/` left from the host#12 live-trigger probe (a number collision with `0001-migration-protocol`, and a `plan/*/spec/` dir is itself a methodology smell); and PLAN.md's Skill-Hardening status box is unchecked while `SKILL-HARDENING.md` shows every goal done. | Remove the orphan directory; check the PLAN.md box and fold in the standing crates.io deferral. | host-local |

## Out of scope

The prose-gate **wiring** (plan/0030 D4) has since closed during the deferred-item
campaign (host-lifecycle v0.22.0), which also resolved this plan's prose-gate finding.
Every other previously deferred follow-up stays in its existing home, untouched. This
plan does not re-track them.

## Verification

Each fix is verified concretely:

- Prose gate: `host-template/lifecycle.manifest` and the two prose copies agree
  (either the manifest re-runs the prose audit and `software --check` exercises
  it, or the docs no longer claim it does); `software --check` green.
- Root `CLAUDE.md`: the verification-model paragraph names `host-prove` and the
  six-rung ladder, with no surviving "three lanes" claim; the migration sentence
  resolves to a live mechanism.
- `call/0017`: `Status: superseded by the spine`; `host-lifecycle validate plan/
  call/` clean; `call/0018` dispositioned with a recorded reason.
- `host-prove` pin: `git -C software/host-prove/main describe --tags` reports an
  exact `v0.2.2` (no `-N-g` suffix), or a recorded rationale; `software --check`
  and `software --verify-build` green.
- Tidiness: `plan/0001-foundation/` is gone; PLAN.md line records Skill-Hardening
  complete with the crates.io deferral noted.

Whole-suite green across the affected repos at close.

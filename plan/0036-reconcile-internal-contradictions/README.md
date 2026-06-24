# Reconcile internal contradictions

## Context

A deep audit found contradictions where the host's own docs restate methodology the
spine has moved: the `STRUCTURE.md` room map, the `README.md` and `CLAUDE.md` tool list
and verification model, the recorded Where layout. Each staled when a past spine change
landed cleanly (specs-to-software in plan/0012, the nested layout in plan/0029, host-prove
and the ladder in plan/0023) and nothing re-read the restatement.

The contradictions are symptoms of one root cause: migration and upgrade propagate a spine
change but never prompt a re-examination of the project's own restatements. Needing a deep
manual audit to find this drift is itself the evidence that a reflective practice the
methodology should carry is absent. This milestone closes the gap and reconciles the drift.

A de-risk review (five lenses plus Qwen-3.5-4B, recorded in `design-review.md`) reshaped
the doctrine: the draft's scope rule was inoperable (4B could not apply an abstract
describes-versus-uses test), its blanket cadence was alarm fatigue, and its primary trigger
was wrong for a development host. The settled design follows.

## The doctrine (the root-cause fix, in the spine)

Widen the existing "grows by reflective practice" doctrine to one principle: an agent
perceives neither the register it emits nor the restatements its own change stales, so both
are re-examined on purpose, prompted at the trust boundaries, mechanical-first, and
operator-validated. Two arms under it:

- **gather** (plan/0034, plan/0035): forward, emergent tells in the corpus, a confirmed
  tell graduates upstream, cadence-driven.
- **reconcile** (new): backward, the project's own restatements of methodology, a confirmed
  drift fixed locally and never propagated, fired by a specific spine move.

Settled rules:

- **Prefer pointing over paraphrasing.** An instance doc should point at the spine, not
  restate it; a restatement that remains is a reconciliation liability reconcile maintains.
- **Scope is machine-checkable and annotation-backed, not a judgment** (the `LEXICON` and
  obligations house style): a restatement that must stay carries a declared assertion the
  tool checks against a source of truth. That is what makes it operable at the weak-agent bar.
- **Trigger is conditional and host-aware.** A new `restates =` field on the `UPGRADING`
  stanza marks a drift-capable entry, and reconcile fires on it, naming which restatement to
  re-read. For a development host that authors spine changes with no upgrade record, the
  **verify gate** is the binding trigger: it runs the check when a drift-capable change
  landed since the last reconcile receipt, and records `n-a` otherwise. Adoption runs the
  full reconcile once.
- **Disposition is three-way** (reuse tell-disposition): reword a live restatement, box a
  frozen citation, forward-correct an immutable record (`call/`, a `Status: done` doc,
  `MEMORY.md`).
- **A sibling `validate` check** HAZARDs an `accepted` `call/` decision whose `Scope:` names
  `host-template`, closing decision-status drift (the `call/0017` class) mechanically.

Authority: this is methodology, so it lives in the spine (`host-template`), never a project
`call/`. The count-versus-stanzas tool check is dropped as noise (the live family disagrees,
5 against 4 against 3); the tool check is a set-diff, and the verification-model check is a
positive assertion that every rung-driver is named.

## Build order

1. Seed the two spine truth data the checks need: an explicit host-* tool-family list and a
   verification-model datum (the manifest carries neither today).
2. host-lifecycle gains the annotation-backed reconcile check (a Where-root off `software/`,
   a spec path asserted under `plan/`, the host-* family set-diff, a verification-model
   omission), the `restates =` read, and the `validate` decision-scope check; released
   through the lifecycle and re-pinned.
3. Spine: widen the doctrine and add the `UPGRADING` entry; wire the reconcile step into the
   `upgrade`, `adopt`, and `verify` skills (gather stays where it is).
4. agentic-host adopts, then reconciles the symptom drift below as the doctrine's first
   dogfood run, through the new check rather than by hand.

## The symptom drift (the first dogfood)

| Finding | Evidence | Disposition |
|---|---|---|
| Root `CLAUDE.md` contradicts itself and the spine on the verification model (three lanes, `host-prove` omitted, against the six-rung ladder). | `CLAUDE.md:24` vs `:9`/`:11` and the spine ladder. | reword live |
| `STRUCTURE.md` is a stale room map: What at `plan/<NNNN>/spec/`, Where at `host-lint/`, only host-lint of five components named. | `STRUCTURE.md:9`/`:11` vs `host-template/STRUCTURE.md` and the live `software/` tree. | reword live; also clears the orphan `plan/0001-foundation/spec/` |
| Root `CLAUDE.md` points a spine change at a redirect stub. | `CLAUDE.md:26` vs `host-template/MIGRATION.md`. | reword live |
| `README.md` names only three host-* tools and omits `host-prove`. | `README.md:4` vs `.host-software`. | reword live |
| `call/0017` authored a now-spine-resident rule yet stays `accepted`. | `call/0017:5` (Scope names `host-template`); rule in `host-template/CLAUDE.md`, applied `617e420`. | `Status: superseded by the spine`; review `call/0018`; `call/0021` clean |
| The `host-prove` `.host-software` pin sits one CI-only commit past its `v0.2.2` tag. | `pin = 5e01f58` (`v0.2.2-1-g5e01f58`); tag `3ca95fc`; the extra commit is `ci.yml` only. | re-pin to the tag, or record the rationale |
| Two record-tidiness defects. | the empty orphan `plan/0001-foundation/spec/`; PLAN.md's Skill-Hardening box unchecked while `SKILL-HARDENING.md` is done. | remove the dir; check the box with the crates.io deferral noted |

Resolved already in the campaign: the prose-hygiene gate the spine asserted but
`lifecycle.manifest` did not implement (plan/0030 D4, host-lifecycle v0.22.0). The session
auto-memory staled the same way and is corrected directly as memory hygiene, not tracked here.

## Verification

- The spine carries the widened doctrine; an `UPGRADING` entry records it; the
  `upgrade`/`adopt`/`verify` skills prompt reconcile; agentic-host adopts it.
- The reconcile check flags a planted drift (a Where-root off `software/`, a missing
  rung-driver) and stays silent on a clean doc; `validate` HAZARDs a `host-template`-scoped
  `accepted` decision. A Fen (Qwen-3.5-4B) run reaches the reconcile action on a concrete
  flag unaided.
- The symptom drift above reconciles to clean: root `CLAUDE.md`, `STRUCTURE.md`, `README.md`
  match the spine and the live layout; `call/0017` is superseded; the `host-prove` pin is at
  its tag or cited; the orphan dir is gone; the PLAN.md box is checked.
- `software --check`, `validate plan/ call/`, the prose gate, and the doc-site build are
  green; whole-suite green across the affected repos at close.

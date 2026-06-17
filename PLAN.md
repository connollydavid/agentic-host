# PLAN.md

## Project: host-lint

A project under agentic evolution. This plan tracks the evolution of the `host-lint` software (a bare store with worktrees; see `call/0010` and `.host-software`).

## Status

- [x] Bootstrap: initial setup and bootstrapping
- [x] CI Pipeline: build, conformance, integration tests
- [x] Formal Spec: Allium spec, proptest, release
- [ ] Skill Hardening: hook fix, bare-numeral rule, release install path (see SKILL-HARDENING.md)

## Milestone documents

Milestones are named after their content, not numbered — ordinals name positions, and positions shift when plans are re-cut; names stay attached to their content. See BOOTSTRAP.md, CI-PIPELINE.md, FORMAL-SPEC.md.

The `plan/` room holds methodology-level milestones as `NNNN-slug` folders (the template's structure, adopted when this host migrated under the methodology). The number is identity; ordering lives here in the index, not in the name.

| Milestone | Status |
|---|---|
| [plan/0001-migration-protocol](plan/0001-migration-protocol/README.md) | done (protocol + tooling + host self-migration); external case-(b) dogfood satisfied by the yarn-agentic adoption (issue #6); Win32s + pgs-release descoped |
| [plan/0002-enforced-remap-dictionary](plan/0002-enforced-remap-dictionary/README.md) | done (host-lifecycle 0.2.0 `remap --check`/`--apply`, call/0008); remap exercised by yarn-agentic (issue #6); Win32s dogfood descoped |
| [plan/0003-doc-site-publisher](plan/0003-doc-site-publisher/README.md) | built (host-lifecycle v0.6.1 `book`/`book --check`, call/0014); dogfooded on this repo's site |
| [plan/0004-anti-ouroboros](plan/0004-anti-ouroboros/README.md) | done (host-lifecycle v0.7.0 `validate` scope gate; methodology folded to the template spine; this repo's methodology decisions superseded in place); resolves issue #9 |

The earlier content-named docs above (BOOTSTRAP, CI-PIPELINE, …) predate the `plan/` room; folding them in is a possible later cleanup, not required.

Dictionary for reading history (old ordinal names in commits and MEMORY.md entries):

| Old name | Current name |
|---|---|
| Phase 1 / PHASE1.md | Bootstrap / BOOTSTRAP.md |
| Phase 2 / PHASE2.md | CI Pipeline / CI-PIPELINE.md |
| Phase 3 / PHASE3.md | Formal Spec / FORMAL-SPEC.md |

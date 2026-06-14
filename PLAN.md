# PLAN.md

## Project: host-lint

A project under agentic evolution. This plan tracks the evolution of the software in the `host-lint` submodule.

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
| [plan/0001-migration-protocol](plan/0001-migration-protocol/README.md) | done (protocol + tooling + host self-migration); external dogfoods pending |
| [plan/0002-enforced-remap-dictionary](plan/0002-enforced-remap-dictionary/README.md) | built (host-lifecycle 0.2.0 `remap --check`/`--apply`, call/0008); Win32s + pgs-release dogfoods pending |

The earlier content-named docs above (BOOTSTRAP, CI-PIPELINE, …) predate the `plan/` room; folding them in is a possible later cleanup, not required.

Dictionary for reading history (old ordinal names in commits and MEMORY.md entries):

| Old name | Current name |
|---|---|
| Phase 1 / PHASE1.md | Bootstrap / BOOTSTRAP.md |
| Phase 2 / PHASE2.md | CI Pipeline / CI-PIPELINE.md |
| Phase 3 / PHASE3.md | Formal Spec / FORMAL-SPEC.md |

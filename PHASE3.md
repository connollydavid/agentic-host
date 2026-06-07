# PHASE3.md

## Phase 3: Formal Specification & Property Testing

### Goals
- [ ] Remove checked-in binary; add `.gitignore`
- [ ] Convert to Cargo project (required for proptest)
- [ ] Write Allium spec (`.allium`) for no-phase detection behavior
- [ ] Add proptest property-based tests
- [ ] Update CI: cargo build, proptest test, GitHub release with binary artifact
- [ ] Write README.md for no-phase-skill

### Success Criteria
- Binary is no longer committed; produced only by CI
- Allium spec validates with `allium` CLI
- Proptest suite passes with 100% coverage of VOCABULARY.md rules
- CI produces a GitHub release with static binary artifact on tag
- README.md documents project, usage, building, and testing

### Notes
Cargo conversion is required for proptest. Allium spec defines formal behavior. CI builds, tests, and releases.

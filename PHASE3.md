# PHASE3.md

## Phase 3: Formal Specification & Property Testing

### Goals
- [x] Remove checked-in binary; add `.gitignore`
- [x] Convert to Cargo project (required for proptest)
- [x] Write Allium spec (`.allium`) for no-phase detection behavior
- [x] Add proptest property-based tests
- [x] Update CI: cargo build, proptest test, GitHub release with binary artifact
- [x] Write README.md for no-phase-skill

### Success Criteria
- Binary is no longer committed; produced only by CI
- Allium spec validates with `allium` CLI
- Proptest suite passes with 100% coverage of VOCABULARY.md rules
- CI produces a GitHub release with static binary artifact on tag
- README.md documents project, usage, building, and testing

### Notes
Cargo conversion is required for proptest. Allium spec defines formal behavior. CI builds, tests, and releases.

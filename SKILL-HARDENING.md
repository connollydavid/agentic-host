# SKILL-HARDENING.md

## Skill Hardening

### Goals
- [x] Fix pre-commit hook: dispatch on `$(basename "$0")` — git passes no hook name in `$1`; commit-msg receives the message file path (verified in throwaway repo)
- [x] Implement bare-numeral header rule (`## 3`, `## 5.5`) in src, proptest, Allium spec, integration tests (CI run 27243442903 green)
- [x] Verify CI-YAML/Dockerfile scoping exclusions are implemented (`is_ci_file` in src/lib.rs, applied in scan_file)
- [x] SKILL.md: install via GitHub release download; note skill-discovery location (`.claude/skills/`)
- [x] Bump CI actions off Node 20 via `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` (forced default on 2026-06-16)
- [x] Release architecture matrix: prebuilt binaries for linux/macos/windows, amd64 + arm64 (run 27243561995)
- [x] Cut v0.1.0 tag; release publishes all six matrix binaries (needed `permissions: contents: write` on the release job)
- Deferred: crates.io publish — postponed until the skill is 100% complete (note: crates.io hosts source only; prebuilds stay on GitHub Releases)

### Success Criteria
- Hook installed as `pre-commit` or `commit-msg` blocks flagged commits and passes clean ones
- All VOCABULARY.md rules (including bare-numeral headers) covered by proptest and integration tests; CI green
- v0.1.0 release exists with a static linux-amd64 binary attached
- SKILL.md install instructions work without a local Rust toolchain

### Notes
Local cargo cannot build the project (2015 pre-nightly); all verification goes through CI. Depends on CI Pipeline being green (it is, since run 27242782567).

# SKILL-HARDENING.md

## Skill Hardening

### Goals
- [ ] Fix pre-commit hook: dispatch on `$(basename "$0")` — git passes no hook name in `$1`; commit-msg receives the message file path
- [ ] Implement bare-numeral header rule (`## 3`, `## 5.5`) in src, proptest, Allium spec, integration tests
- [ ] Verify CI-YAML/Dockerfile scoping exclusions are implemented; implement if missing
- [ ] SKILL.md: install via GitHub release download; note skill-discovery location (`.claude/skills/`)
- [ ] Bump CI actions off Node 20 (forced Node 24 on 2026-06-16)
- [ ] Cut v0.1.0 tag; verify the release job publishes the static binary

### Success Criteria
- Hook installed as `pre-commit` or `commit-msg` blocks flagged commits and passes clean ones
- All VOCABULARY.md rules (including bare-numeral headers) covered by proptest and integration tests; CI green
- v0.1.0 release exists with a static linux-amd64 binary attached
- SKILL.md install instructions work without a local Rust toolchain

### Notes
Local cargo cannot build the project (2015 pre-nightly); all verification goes through CI. Depends on CI Pipeline being green (it is, since run 27242782567).

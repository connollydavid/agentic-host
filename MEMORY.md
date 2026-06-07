# MEMORY.md

## Session Log

### 2025-01-XX — Initial Setup
- Established agentic-host directory structure with CLAUDE.md, PLAN.md, PHASE1.md
- Added no-phase-skill as git submodule for software-under-development
- Imported SKILL_AUTHORING.md conformance standard for skill authoring
- Created karpathy-guidelines skill in skills/ directory

### 2025-06-07 — Linter Implementation
- Built no-phase linter in Rust: detects phase-synonym agentic tells in commits, headers, comments
- Binary is dynamically linked (no musl toolchain for static); committed to submodule
- SKILL.md created with agent skill frontmatter; pre-commit hook wrapper added
- VOCABULARY.md is source of truth for flag/allowlist/gray-zone detection rules
- CLI interface: `no-phase --stdin`, `no-phase [files...]`, `no-phase --all`, `--json` flag

### 2025-06-07 — CI Pipeline
- Added GitHub Actions workflow: three jobs (build static binary, conformance gates, integration tests)
- lint-skill.sh implements G1-G8 mechanical gates; all pass
- test-integration.sh has 26 property tests from VOCABULARY.md should/must-not-match cases; all pass
- Fixed is_numeral to reject ordinal words (e.g. "first") that contain Roman numeral chars
- Removed allowlist pre-filter that was blocking valid phase-synonym matches in conventional commit messages

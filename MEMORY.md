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

### 2025-06-07 — Formal Spec & Property Testing
- Converted to Cargo project (src/lib.rs, src/main.rs) for proptest support
- Removed checked-in binary; added .gitignore; binary produced only by CI
- Added 10 proptest property tests covering all VOCABULARY.md detection rules; all pass
- Wrote no-phase.allium Allium specification for formal behavior definition
- Updated CI: cargo build, proptest, integration tests, GitHub release on tag (v*)
- Added README.md with usage, building, testing documentation

### 2026-06-10 — Named milestones replace ordinal phases
- Renamed PHASE1/2/3.md to BOOTSTRAP.md, CI-PIPELINE.md, FORMAL-SPEC.md; PLAN.md keeps an ordinal-to-name dictionary for reading history (older commits and entries above still say "Phase N")
- Reason: ordinals name positions and positions shift when plans are re-cut; names stay attached to content. Bare numerals ("3", "5.5") are the same tell with the noun elided — not a fix
- VOCABULARY.md now leads with a constructive rewrite dictionary (internal plan code → descriptive text, never emit the code) and notes bare-numeral headers as flaggable
- GitHub pushes are blocked in this environment: keychain has no credential, no gh CLI, no SSH key. Commits queue locally; submodule must be pushed before the host pointer commit

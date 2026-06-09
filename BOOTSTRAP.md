# BOOTSTRAP.md

## Bootstrap: Initial Setup

### Goals
- [x] Establish agentic-host directory structure
- [x] Add no-phase-skill as git submodule
- [x] Define initial project scope and objectives

### Scope
- Rust CLI binary (`no-phase`) that detects phase-synonym agentic tells in commit messages, markdown headers, and code comments
- Agent skill (`SKILL.md`) for callable linting
- Pre-commit hook wrapper for integration into git workflows
- Vocabulary reference (`VOCABULARY.md`) as source of truth for flag/allowlist/gray-zone terms

### Success Criteria
- Host structure is committed and pushed
- Submodule is configured and accessible
- PLAN.md and this document are tracked and auditable

### Notes
Bootstrap establishes the scaffolding for agentic development. The software-under-development lives in the `no-phase-skill` submodule.

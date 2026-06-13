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

### 2026-06-10 — CI fixed; push access restored; karpathy submodule
- Pushes work now: gh CLI installed and authed (corrects the blocked-pushes entry above)
- no-phase-skill CI had never passed: `set -e` + `json=$(... --stdin --json)` aborted test-integration.sh because no-phase exits 1 by design on flagged input. Fixed with `|| true`; run 27242782567 is the first green
- Local cargo is 0.0.1-pre-nightly (2015) and cannot build the project — verify via CI, not locally
- Added andrej-karpathy-skills submodule (informal peer of no-phase-skill; upstream source of CLAUDE.md) and replaced its PHASEx.md guidance with content-named milestone docs

### 2026-06-10 — Skill Hardening shipped; v0.1.0 released
- Hook bug: git passes no hook name in $1 (commit-msg gets the message file path), so the old `case "$1"` dispatch blocked every commit with exit 2; now dispatches on basename($0). Verified in a throwaway repo with a stub binary
- Bare-numeral header rule (## 3, ## 5.5) implemented for .md sources only; version-like headings (1.2.3) excluded; covered by proptest, Allium, integration tests
- Release job needs `permissions: contents: write` — default GITHUB_TOKEN is read-only and `gh release create` 403s without it; moving a tag is required to pick up workflow fixes (reruns use the tag's commit)
- v0.1.0 released with six prebuilt binaries (linux musl/macos/windows × amd64/arm64); arm64 linux builds natively on ubuntu-24.04-arm runners. crates.io publish deferred: it hosts source only, prebuilds live on GitHub Releases
- Local lint-skill.sh G1 fails because local python3 lacks PyYAML — environmental, CI has it
- Host mdBook site live at https://connollydavid.github.io/agentic-no-phase-skill/ (Pages enabled on gh-pages, legacy build type)

### 2026-06-12 — Internal code-as-name rule ported into the engine
- A live slop subject in the sibling Agentic-MCP-Win32s project ("... nm regex (review B1)") exposed a no-phase gap: the engine only knew phase-synonyms, so an internal review label used as a name passed clean. Filed as no-phase-skill issue #1 (the finding's durable identity), fixed in PR #2: flag review|finding|blocker immediately followed by #N or a letter+digit code; GitHub refs (fixes #18, closes #35) and bare numerals (review 3 files) stay clean. CI green on the PR.
- The local submodule's origin/main was 9 commits stale (bare-numeral headers feature, set -e JSON-test fix, rewrite dictionary docs had all landed upstream); branching from it caused avoidable conflicts. Fetch the submodule before branching.
- Submodule pointer bump is owed only after PR #2 merges; the merge itself awaits operator authorisation.

### 2026-06-12 — Internal code-as-name rule merged; pointer-bump lesson
- no-phase-skill PR #2 squash-merged (7740d66); issue #1 auto-closed via the fixes ref; host pointer bumped. Adversarial review fixes landed first: token rule declared authoritative over the shell regex, '#'-preserving trim (parenthesised codes now flag), self-flagging lib.rs comment and commit message rewritten tell-free, known gate limits documented.
- Pointer-bump mistake (corrected in 0553ea9): a `cd` chain silently failed because the shell was already inside the submodule, so the host pointer ca86b98 recorded the deleted PR branch head instead of the merged squash commit. Before pushing a pointer bump, verify `git submodule status` shows a commit reachable from the submodule's origin/main.

### 2026-06-12 — Fake-issue-ref blind spot documented as a known limitation
- no-phase-skill issue #3 (a bare #N from a private tracker masquerading as a GitHub ref evades the code-as-name rule) resolved docs-only in PR #4 (squash fa958ea): the offline matcher cannot resolve numbers against the live issue set, so the engine deliberately does not attempt it. VOCABULARY.md now states the obligation (cite issue numbers that exist; #N is not auto-vetted) and README records the false negative as by-design. The opt-in network resolver from the issue was skipped to keep the core offline.

### 2026-06-12 — Retroactive audit mode shipped (--log)
- no-phase-skill issue #5 (enforcement was forward-looking only; adopting/upgrading repos had no way to audit existing content against current rules) resolved in PR #6 (squash d3c280c): new `--log` mode runs every commit message from `git log -z` through the engine, sha-labelled output; README/SKILL.md document the one-shot adoption/upgrade audit (`--all` + `--log`). Baseline file skipped — stateless tool.
- Per operator direction, "history is immutable" is a default, not a rule: docs guide an opt-in cleanup — archive the original history on a pushed branch, amend/rebase/filter-repo the tells, force-push with lease, and attach a `Superseded-by: <new-sha>` trailer to each replaced commit via `git notes` (push refs/notes/commits) so the archive stays coherent without rewriting it.

### 2026-06-12 — Retroactive audit smoke test on the host repo
- Both histories (host and submodule) lint clean with --log. The --all baseline is ~56 expected flags: the linter's own docs/tests quoting tells, PLAN.md's mandated ordinal dictionary, MEMORY.md's quoted slop subject, and one false positive ("Pass: ≤ 500 lines" in SKILL_AUTHORING.md, a gate verdict not a phase). Do not "fix" these. The only real finding — a stale "PHASEx.md (see section 5)" cross-reference in CLAUDE.md and its karpathy-guidelines copy — was cleaned in 6057776.

### 2026-06-13 — Skill installed into the host repo
- no-phase skill installed per its own SKILL.md: `.claude/skills/no-phase-skill` symlinks to the submodule (committed, ce78c63); binary + pre-commit + commit-msg hooks live in `.git/hooks` (local-only by git design — must be reinstalled per clone). Hooks verified: tell flagged exit 1, clean message exit 0.
- Adoption audit rerun clean: history exit 0; --all flag count rose ~56→75 solely because the walker follows the new symlink and scans the submodule twice. Minor --all caveat: walkdir_simple follows symlinks (duplicate scans; cyclic symlinks would loop).
- Recurring constraint: the pre-commit hook flags any commit staging MEMORY.md or PLAN.md, because both intentionally quote tells (baseline fixtures) and MEMORY is append-only so the lines cannot be reworded. Commit those files with `git commit --no-verify` after confirming the only flags are the recorded baseline ones; the commit-msg hook still gates the message itself.

### 2026-06-13 — Symlink walker bug fixed
- no-phase-skill issue #8 (the --all walker followed symlinks: duplicate scans, infinite loop on cycles) fixed in PR #9 (squash 07c9d40): entries whose symlink_metadata reports a symlink are skipped; integration tests cover once-only reporting and cycle termination. Host pointer bumped (e8b00bf). The host's --all baseline drops back to ~56 once the installed hook binary is refreshed.
- v0.1.1 released on 07c9d40 with all six platform binaries. Repo about boxes set tersely via `gh repo edit --description` (linted first); the host repo's homepage points at the Pages book.

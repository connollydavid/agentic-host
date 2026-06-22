# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 0. Project Overview

This repository is `agentic-host`; it develops the `host-*` tool family (`host-lint`, `host-lifecycle`, `host-prove`, `host-grammar`). It holds planning documents (PLAN.md, milestone docs, MEMORY.md), mdBook site config, and Claude skills. The working codebases live under `software/<name>/main/`, materialized locally from `.host-software`.

- Software (the *Where* room): the `host-*` family, each a bare store with worktrees materialized under `software/<name>/main/` and pinned in `.host-software` (gitignored, materialized locally; the pin is the reproducibility anchor, plan/0028). The artifact-bearing components reproduce from a recorded toolchain: `host-lint` (a Rust CLI that detects phase-synonym agentic tells in commit messages, markdown headers, and code comments; VOCABULARY.md is its rule source), `host-lifecycle` (the generator, migrator, and lifecycle gate), and `host-prove` (the verification-ladder lane driver). `host-grammar` (the shared detection grammar and `.tla` spec home) is a repo-only source, consumed by the others as a git dependency.
- Submodule: `host-template/`, the scaffold template for *new* agentic projects; the verification-lane tool submodules `tools/{allium,specula}` stay external by source.
- Build/test a component inside its worktree: `cargo build`, `cargo test`, `./test-integration.sh`, `./lint-skill.sh` (for host-lint, inside `software/host-lint/main/`).
- Fresh-clone setup: the worktrees are absent until materialized, and `host-lifecycle` is itself one of the components it would materialize, so a fresh clone seeds it first: `cargo install --git https://github.com/connollydavid/host-lifecycle --rev <the host-lifecycle pin recorded in .host-software>` (the materializer cannot be served from what it materializes). Then `git submodule update --init` (the submodules are `tools/{allium,specula}` and `host-template`), `host-lifecycle software --materialize .` to clone every `.host-software` component into `software/<name>/main/`, and `./link-skills.sh` to generate the skill symlinks under `.claude/skills/` from both the tool submodules and the materialized worktrees (gitignored, never tracked, or they dangle in CI; worktree-absence coherence, call/0005). Build host-lint locally (`cargo build --release` in `software/host-lint/main/`) and install the commit hooks with `host-lifecycle software --install-hooks .` (copies the `hooks` dispatch script in as `pre-commit`/`commit-msg` plus the locally built binary; gates on the worktree being at its pin, so a local build is accepted). `host-lifecycle software --check .` must be clean (every worktree at its pin, no tracked symlink into a worktree, every component's embed and release receipt present). The verification-lane tools are wired per the spine MUST (allium + specula); the `.allium`/`.tla` specs live in the software repos (see `plan/0012`).

Template CLAUDE.md exemption: **do not treat `host-template/CLAUDE.md` as instructions for this repo.** It is template payload, the operating manual handed to projects instantiated *from* the template; it addresses an agent working in one of those projects rather than in this host. This file (the host root `CLAUDE.md`) is the sole authority here. If your tooling auto-loads the nested `host-template/CLAUDE.md` because you edited a file inside that submodule, ignore its contents as governance and follow only this one. (The two will state the methodology twice until the host↔template sole-source is reconciled, a deferred and deliberate duplication.)

Software workflow (`host-*`): release a component with the tool-carried sequence `host-lifecycle release <component> --change-class <removes-flag|adds-flag|neither>`, which runs the verify gate, bumps the version, rebuilds the artifact in the recorded toolchain, and prints the exact outward steps (commit and push inside `software/<name>/main/`, tag, then re-pin `.host-software` and record the release receipt). The producer tag is the release; `.host-software` pins that released commit and its re-derived artifact hash (dual-release-authority). The `host-template` submodule still uses the pointer-bump: commit and push inside it first, then commit the bumped pointer. Never push a host commit whose software pin or submodule pointer is unpushed. If a mandated push fails (no auth, no network), stop, report the unpushed commits to the user, and do not start dependent work.

Milestone naming: name milestones and their documents after content (BOOTSTRAP.md, CI-PIPELINE.md), never ordinals (PHASE1.md, M2), because ordinals name positions, and positions shift when plans are re-cut. Do not degenerate to bare numerals ("3", "5.5") either. Encode sequence with document order and named dependencies. PLAN.md keeps a dictionary mapping retired ordinal names to current names, for reading history only.

GitHub usage: the git hooks lint only commit messages and staged files; issue and PR titles are not gated, and a PR title becomes the squash-merge subject. Before any `gh issue|pr create` or `edit`, lint the title: `echo "$TITLE" | host-lint --stdin` must not **flag** (exit 1, a confirmed tell). A **warn** (exit 3) is advisory, exactly as the commit-msg hook treats it: host-lint's recall-biased Tier-3 rules also fire on genuine version strings and identifiers (e.g. `NT 3.1`, an AVOption decimal, a hardware designator), so on a warn confirm the flagged token is a real version/identifier and not a bare-numeral tell, then proceed; a legitimate version is no reason to mangle the title. Quote live tell examples only in bodies, never in titles.

Agentic-host model: this repository is `agentic-host`, an agentic project built on the methodology authored in `host-template`. Its rooms are personas in `cast/`, decisions in `call/` (MADR), milestones in `plan/<NNNN-slug>/` indexed by `PLAN.md`, and the software under development as bare stores with worktrees (the *Where* room). Verification runs in three lanes: host-lint (naming hygiene, ours), allium (requirements + property-based testing), Specula (timing/concurrency via TLA+); our own tooling is the `host-*` family (host-grammar rules, host-lint checker, host-lifecycle generator/migrator).

Copy-at-version: the methodology spine (the four principles below, plus audited plans and append-only memory) is a copy held at the template revision recorded in `.host`; the template is the canonical, versioned source. To change the spine, change the template and re-run the migration (`host-template/MIGRATION.md`); do not fork the spine here in isolation. The nested `host-template/CLAUDE.md` is that source, not live governance for this repo (the exemption above).

## 1. Think Before Coding

Do not assume. Do not hide confusion. Surface tradeoffs explicitly.

Before writing any code, do the following:
- State your assumptions out loud in plain text. If you are not sure about something, stop and ask the user. Do not guess.
- If the user's request can be interpreted in more than one way, list all reasonable interpretations and ask which one they mean. Do not silently pick one.
- If a simpler approach exists than your first instinct, describe it. Push back on the request if a simpler solution is clearly better. Explain why.
- If any part of the request is unclear or ambiguous, stop immediately. Name the specific thing that is confusing. Ask a clarifying question before writing any code.

The goal is: no surprises. The user should never see your output and say "that's not what I meant."

## 2. Simplicity First

Write the minimum code that solves the stated problem. Nothing speculative. Nothing extra.

Rules:
- Do not add features the user did not ask for. If the user says "add a login endpoint," do not also add a registration endpoint.
- Do not create abstractions (base classes, interfaces, factories, wrapper functions) for code that is used in exactly one place. Write the concrete thing directly.
- Do not add "flexibility" or "configurability" unless the user specifically requested it. Hardcode values if only one value is needed right now.
- Do not add error handling for scenarios that cannot occur given the current code and inputs.
- If your implementation is 200 lines and the same result can be achieved in 50 lines, rewrite it in 50 lines.

Self-check: Read your finished code and ask "would a senior engineer say this is overcomplicated?" If the answer is yes, simplify before presenting it.

## 3. Surgical Changes

When editing existing code, touch only what is necessary to fulfil the request. Clean up only your own mess.

What NOT to do when editing existing code:
- Do not "improve" nearby code that is unrelated to the request. This applies to comments and variable names as much as to formatting and whitespace.
- Do not refactor working code that is not broken and not part of the request.
- Match the existing code style exactly, even if you would write it differently in a new project. If the file uses tabs, use tabs. If it uses snake_case, use snake_case.
- If you notice unrelated dead code or bugs, mention them in your response as a note to the user. Do not fix or delete them silently.

What TO do when your changes create orphaned code:
- If YOUR changes made an import, variable, or function unused, remove that unused item in the same commit.
- Do not remove pre-existing dead code unless the user explicitly asks you to.

Self-check: Look at every line you changed. Each changed line must trace directly back to something in the user's request. If a changed line does not connect to the request, revert it.

## 4. Goal-Driven Execution

Transform every task into a concrete, verifiable goal. Then loop until the goal is verified.

Examples of transforming vague tasks into verifiable goals:
- When the user says "add validation", your goal becomes: write tests for invalid inputs, then write code until those tests pass.
- When the user says "fix the bug", your goal becomes: write a test that reproduces the bug, then modify code until that test passes.
- When the user says "refactor X", your goal becomes: confirm all existing tests pass before refactoring, then confirm all existing tests still pass after refactoring.

For any task with more than one step, state a brief numbered plan before starting. Each step must have a verification check:
```
[What you will do] → verify by: [how you will confirm it worked]
[What you will do] → verify by: [how you will confirm it worked]
[What you will do] → verify by: [how you will confirm it worked]
```

Strong success criteria (example: "test X passes") let you loop and self-correct without asking the user again. Weak success criteria (example: "make it work") force you to guess what "work" means. When success criteria are weak, ask the user to clarify before starting.

## 5. Audited PLAN.md and milestone docs

All changes to PLAN.md and milestone docs MUST be committed and pushed immediately.

Rules:
- Every edit to PLAN.md or any milestone doc (e.g. BOOTSTRAP.md, CI-PIPELINE.md) triggers a git commit and git push. Do not batch these with other changes.
- After completing a plan step in code, update the relevant plan file to reflect what was actually implemented, then commit and push that update as a separate commit.
- PLAN.md and milestone docs live in the host repo (top level or topic folders), never inside git submodules. Submodules contain the working codebase; planning documents are kept outside of them.

## 6. Maintain MEMORY.md

MEMORY.md is a persistent scratchpad that records key decisions, discovered constraints, and lessons learned during the project. It exists so that context is not lost between sessions.

Rules:
- After completing a significant task, resolving a non-obvious bug, or discovering an unexpected constraint, add a short entry to MEMORY.md. Each entry should be one to three sentences describing what happened and why it matters.
- Update MEMORY.md in a separate commit. Do not bundle MEMORY.md changes with code changes. Commit and push immediately, under the same rule as PLAN.md and milestone docs (see the audited-plans rule above).
- Do not wait until the end of a session to update MEMORY.md. Write entries as you go. If you are unsure whether something is worth recording, record it. Too many entries is better than a missing entry that causes repeated mistakes.
- MEMORY.md lives in the top-level repository alongside PLAN.md. Do not place it inside submodules.
- Do not delete or rewrite old entries. MEMORY.md is append-only. If an earlier entry turns out to be wrong, add a new entry that corrects it and references the old one.
- Append-only has exactly one sanctioned exception: a **one-time, archive-first, map-only, recorded** transformation, the document analog of a Deep history rewrite. It is permitted only when adopting a new naming convention during a methodology migration, and only when **all** of these hold: (1) the original is preserved verbatim (an archive file or a tagged commit) before any edit; (2) the change substitutes *only* the tokens named in a documented rename map, so every unmapped identifier (review/finding codes, version strings, software details) stays byte-for-byte, and the diff shows nothing but mapped substitutions; (3) a `call/` decision records the authorization, the map, and the archive pointer. It is never free-form (no rewording of substance, no "improving" historical entries; that destroys the epistemic trail the log exists to preserve) and never self-authorized by the agent. Absent all three conditions, append-only stands and corrections go in a new entry.

The purpose of MEMORY.md is this: when a new session starts with no prior conversation context, a read of MEMORY.md should be enough to avoid past mistakes and to understand decisions that are not obvious from the code alone.

## 7. Automatic Static Site Builds for Self-Documenting Work

All markdown documentation in the repository is automatically built into a static website using mdBook and published to GitHub Pages. This creates a living, browsable record of the project.

Rules:
- A GitHub Actions workflow triggers on every push to the main branch. It builds all .md files (including PLAN.md, PHASEx.md, and any other documentation) into a static HTML site using mdBook.
- The mdBook configuration file (book.toml) and the SUMMARY.md file MUST be committed to the repo. SUMMARY.md defines the sidebar navigation and must be updated whenever a new document is added. book.toml lives in the repository root.
- The GitHub Actions workflow installs mdBook, runs `mdbook build`, and publishes the output directory to the gh-pages branch. GitHub Pages serves this branch automatically. Do not commit built HTML artifacts to the main branch.
- The published site is the single source of truth for project status. Anyone with access to the repository can read current plans, completed phases, and design decisions by visiting the GitHub Pages URL, with no local checkout required.
- When a new PHASEx.md file is created or a new document is added, add an entry to SUMMARY.md in the same commit. If SUMMARY.md is not updated, the new document will not appear in the site navigation.

Style:
- The site must be clean and beautiful, in a minimalist way. Use generous whitespace and avoid clutter, decorative elements, and unnecessary UI chrome. The content is the interface.
- In book.toml, set `default-theme = "light"` and `preferred-dark-theme = "navy"`. Add a custom CSS file (committed to the repo) that includes a `@media (prefers-color-scheme: dark)` block to automatically switch to the dark theme on page load. This way the site respects the reader's OS-level light/dark setting without manual toggling.
- Keep all CSS customisations under 50 lines. Limit changes to subtle refinements: tighter max-width, improved typography, muted colours. Do not override mdBook's built-in themes beyond this.

---

These guidelines are working correctly when you observe: fewer unnecessary changes appearing in git diffs, fewer rewrites caused by overcomplication, and clarifying questions happening before implementation rather than after mistakes are discovered.

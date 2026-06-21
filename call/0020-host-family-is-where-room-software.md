# The host-* family is software developed here, embedded as Where-room components

- Status: accepted
- Date: 2026-06-21
- Scope: host-lint, host-lifecycle, host-prove, host-grammar (the host-* software family) and agentic-host's `.host-software` composition
- Relates to: `call/0010` (the `.host-software` Where-room recipe), `call/0013` (reserve agentic-host for this repository), `call/0017` (every phase emits a receipt — the `recurring-per-component` machinery), `STRUCTURE.md` ("the Where room is the software under test — one or more components").

## Context and Problem Statement

agentic-host is the development host for the **whole** host-* family — host-lint, host-lifecycle,
host-prove, host-grammar — not just host-lint. The planning (`plan/`, `call/`, `MEMORY.md`) and the
worktrees for all of them live here, and their code is authored here.

Each host-* artifact wears two hats at once:

1. **Developed software** — its own repo (`connollydavid/host-*`), its own test suite and **CI**
   (`ci.yml`), its own co-located specs, its own version/tag/release lifecycle. The *producer*
   identity.
2. **Methodology tooling** — agentic-host (and any adopter) consumes a pinned version to operate or
   verify the methodology: host-lint as the hygiene hook, host-lifecycle as the lifecycle driver,
   host-prove as the deep-rung verifier. The *consumer* identity.

The residency was inconsistent: **host-lint** is a `.host-software` Where component (developed here,
its built binary and skill served from the worktree), while **host-lifecycle** and **host-prove**
sit under `tools/` as referenced submodules, and **host-grammar** is a git-dep library. That
asymmetry — an accident of host-lint being "first," not a principled line — led to a false
"tooling vs Where-room software" binary: a conclusion that `host-lifecycle release host-lifecycle`
"cannot resolve" and that embedding a tool as a Where component would be a category error. It is
not. The methodology already supports **more than one software-under-development per host**:
`.host-software` is explicitly "one or more components", agentic-host already carries two
(`host-lint` + `host`), and the receipt machinery's `embed`/`release` are `recurring-per-component`.

## Decision Outcome

**agentic-host is a multi-software development host.** Everything `host-*` is software *developed
here* and is embedded as a `.host-software` **Where-room component** — host-lint (already),
host-lifecycle, host-prove, host-grammar. Each is released through the lifecycle orchestration
(`host-lifecycle release <component>`) and emits its receipt in the project ledger, while keeping
its own producer CI and release in its own repo. Its tooling function is served from its Where
worktree (built binary + worktree-sourced skills), the host-lint model.

The clean line:

- **`tools/`** holds only genuinely **external** referenced verification tools — **allium** (JUXT),
  **specula**. "Reference, don't vendor" governs an *adopter* consuming tools; it does not govern
  the *development host* that builds them.
- **`.host-software`** holds the software developed here — the whole host-* family.

The split identity is honored by a **lightweight** boundary — each tool's own repo, CI, and
release/version — **not** by giving each tool its own agentic project. agentic-host stays the
*single* development host for a coupled family (host-grammar is a shared build dependency of
host-lint and host-lifecycle; the roadmap is one). Fragmenting into a project per tool would leave
agentic-host "responsible only for host-template" — over-separation that dissolves a real strength.

## Considered options

- **Each host-* tool as its own agentic project** (own `cast/`/`call/`/`plan/`/`.host`). Rejected:
  the producer identity needs only own-repo + CI + release, not full methodology ceremony per tool;
  N projects fragment one coupled roadmap and multiply operational cost for one developer.
- **Status quo** — host-* tools stay `tools/` submodules, released ad-hoc. Rejected: it rests on the
  false tools-vs-software binary, blocks dogfooding `release` on the tools, and is asymmetric with
  host-lint for no principled reason.
- **Embed the family as Where components of one multi-software development host** (chosen): uniform
  with host-lint, makes `release <component>` resolve, and reuses the `recurring-per-component`
  machinery already built.

## Consequences

- host-lifecycle, host-prove, host-grammar migrate from `tools/` submodule / git-dep to
  `.host-software` Where components (see `plan/0028`); `tools/` then holds only allium + specula.
- The skill-wiring mechanism (`link-skills.sh`, which symlinks `tools/*/skills/*`) must also wire a
  Where component's skills from its worktree — the host-lint pattern, generalized to multi-skill
  components.
- host-grammar is a library (no deployable artifact): it releases tag-only, and its dependents
  (host-lint, host-lifecycle) keep their git-rev dependency pinned to its released tag (closing the
  current unpinned-host-grammar gap in host-lifecycle's manifest).
- The general pattern — *a development host embeds the tools it develops as Where software, an
  adopter references them* — may warrant a spine clarification in `host-template`; that is a separate
  follow-up, not this project-scoped decision.

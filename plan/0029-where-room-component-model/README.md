# plan/0029 — A first-class multi-component Where room: shapes, addressing, and a nested layout

> **Generic capability — tool (`host-lifecycle`) + spine (`host-template`).** This milestone is for
> **every** adopter, not for agentic-host's host-* situation. The driving rule: **no project-specific
> names in the tool's logic or the spine's prose; branch on the *declared recipe*, never on a name.**
> agentic-host's own migration (`plan/0028`, `call/0020`) is re-cut to *depend* on this as the first
> dogfood — the stress test, not the design driver. It also resolves the `plan/0028` adversarial
> review's blocking *spine-contradiction* finding: the multi-component Where model is settled in the
> spine here, then applied locally, rather than forked in an instance.

## Context

The Where room has always been "one or more components" (`STRUCTURE.md`; `call/0010`), and the
lifecycle's `embed`/`release` already recur per component. But the tooling was only ever exercised on
one component *shape* (a single deployable binary, host-lint) materialized in a flat,
root-scattered layout. Three things were never finished generically:

1. **Component shapes.** A component may be **artifact-bearing** (a deployable binary), a **library**
   (code, released/versioned, but no deployable artifact), or **docs/text-only** (no build at all).
   The text-only case already works (any repo-only stanza; proven live by the `host` component). The
   library case — released but artifact-free — has no defined `release`/receipt shape. The tool must
   branch on **what the recipe declares** (`build`/`artifact`/`deploy`/`toolchain` present or not),
   never on a name.
2. **Addressing.** With several components, each having a canonical worktree at its pin *plus*
   optional parallel worktrees per line, every `software` operation must answer "**which item, which
   branch?**" — `software --materialize|--check|--verify-build` currently take only the project root
   and act on all components' canonical worktrees; `release` takes the item but not the branch.
3. **Layout.** Components materialize as `<name>/`, `<name>.git/`, `<name>.<line>/` scattered at the
   host root — fine for one component, noisy and unaddressable for many.

## The generic model

A Where room is a set of **components**; each component is a **store plus branches**; each component
has a **shape** declared by its recipe. The tool operates on a component's worktree addressed by
**(item, branch)**, and validates the materialized tree generically.

### Nested layout (the enabler — replaces the root-scattered scheme)

All software lives under one `software/` directory; each component is a folder; within it the bare
**store** is separated from the per-**branch** worktrees:

```
software/
  <component>/
    .git/            # the bare object store (shared); exact store-dir name is a design knob
    <branch>/        # a worktree checked out on <branch>; the pin's branch is the canonical one
    <other-branch>/  # additional parallel lines, one folder per branch
```

- **(item, branch) is now a literal path** — `software/<item>/<branch>/` — so the addressing in the
  next section maps directly to the filesystem.
- **One `.gitignore` entry** (`/software/`) replaces the per-component triplets.
- The **"worktrees live under the host root"** rule generalizes to "under `software/`"; the off-tree
  `store=<path>` escape (a foreign filesystem/platform, e.g. a Windows Dev Drive reached from WSL)
  still applies, with `software/<component>/<store-or-branch>` as the in-tree junction.
- Skill symlinks repoint to `software/<component>/<branch>/…` (generated, never tracked — `call/0005`).

### Addressing

```
host-lifecycle software --materialize|--check|--verify-build [<item>[@<branch>]] [<dir>]
host-lifecycle release <item>[@<branch>] ...
```

- **Omit the specifier → all components, canonical worktrees** (today's behavior; backward-compatible).
- `<item>` → that one component's canonical worktree (the targeted bootstrap/check/build).
- `<item>@<branch>` → a specific parallel line.

### Shapes (branch on the declared recipe, never on a name)

- **Artifact-bearing** — declares `build`/`artifact`/`deploy`/`toolchain`; `--verify-build` rebuilds
  and reproduces the hash; `release` builds, re-derives, re-pins, tags, receipts (today's path).
- **Library** — declares a version/tag but **no** `artifact`; `--verify-build` no-ops; `release` is
  **tag-only** with a defined tag-only receipt (the missing branch). Dependents consume it by pin.
- **Docs/text-only** — no `build` at all; `--check` validates the pin only (already works).

## Deliverables

1. **Tool — layout + materialize/check.** Materialize into `software/<component>/<branch>/` with the
   store separated; `software --check` understands the nested tree; the single `/software/` ignore;
   off-tree `store=` junctions under the new paths.
2. **Tool — (item, branch) addressing.** The optional specifier on `--materialize`/`--check`/
   `--verify-build`/`release`; default-all preserved; the targeted single-item path is what the
   bootstrap and per-component verify use.
3. **Tool — shapes by declared recipe.** A no-artifact stanza is valid (not a defect) for
   `--check`/`--verify-build`; `release` emits a defined **tag-only** receipt for a library;
   artifact-bearing unchanged. No name literals anywhere.
4. **Tool — component-shipped skills + link integrity.** Generalize skill wiring to read a component's
   worktree layout (root `SKILL.md` / `skills/*` / none) for *any* component; `software --check`
   verifies a materialized component's generated links resolve (closing the dangling-generated-link
   blind spot — the gate only sees *tracked* symlinks today).
5. **Spine — the methodology change.** Update `STRUCTURE.md` + `CLAUDE.md` (the Where-room, worktree,
   and reproducible-build sections) for the nested layout, the (item, branch) addressing, and the
   three shapes; reconcile `call/0010`'s status if it now restates spine; an `UPGRADING.md` entry with
   a machine-checkable `verify=` (this entry *is* the migration adopters run); update the lifecycle
   manifest if any phase command/evidence changes.
6. **Generic fixture + weak-agent test.** A throwaway synthetic project — neutral names, one binary
   component, one library component, one docs-only component, and a parallel branch — to design and
   **Fen (4B) test** against, proving the capability on a neutral case before agentic-host touches it.

## Migration / compatibility

- **One adopter exists today** (agentic-host), so a hard cut is acceptable: the `UPGRADING` entry's
  action is "re-materialize into the new layout" (`software --materialize` rebuilds the tree;
  `.gitignore` and skill links repoint). The `.host-software` recipe stays the source of truth; the
  layout is *derived* from it, so the recipe format need not change (or gains only optional fields).
- The bootstrap interplay (a project whose Where room contains the materializer itself) is handled by
  the targeted single-item materialize (Deliverable 2) seeded from the recorded pin — generic for any
  self-hosting toolchain, not special-cased.

## Verification

- The generic fixture goes green: `software --materialize <item>` (targeted), `--check`,
  `--verify-build` on the binary, `--check` clean on the library (no-artifact) and docs components,
  `release` emits an artifact receipt for the binary and a tag-only receipt for the library; the link
  integrity check fails loudly on a deliberately-broken generated link.
- The Fen (4B) ergonomics test reaches the correct targeted command unaided (the specifier is printed,
  not constructed).
- **Then** agentic-host re-materializes into the new layout as the dogfood, and `plan/0028` proceeds
  on top of it. Whole-suite green across every repo.

## Risks / honesty

- **Breaking layout change** — re-materialize, `.gitignore`, skill-link paths, the worktree-under-root
  rule, and off-tree `store=` junctions all move; mitigated by the single-adopter hard cut and the
  fixture-first proof, but every path-deriving code path in the tool must be found (not just
  materialize: `--check`, `book` stubs, symlink-hazard resolution, `verify-build`).
- **Recipe back-compat** — keep `.host-software` stable so the change is layout-only; if a field is
  needed (e.g. an explicit branch per worktree), add it optional with a sensible default.
- **Over-generalization is its own risk** — resist adding shape/addressing knobs no adopter needs;
  the three shapes and the (item, branch) pair are the whole surface. If a capability is only ever
  exercised by agentic-host, that is the signal it was overfit and belongs in `plan/0028`, not here.

## Relationship to other milestones

- **`plan/0028`** (host-* family as Where components) is re-cut to **depend on this**: its readiness
  and cutover passes assume the layout, addressing, shapes, and skill wiring delivered here.
- Resolves the `plan/0028` review's *spine-contradiction* (the capability is delivered as a spine
  change here) and most of *grammar-pin-mess*/*library-component-slot*/*new-link-loop* by giving the
  tool the generic capability those findings said was missing.

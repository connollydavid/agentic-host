# plan/0029: A first-class multi-component Where room: recipe-dispatched shapes, addressing, layout, and tool residency

> **Generic capability: tool (`host-lifecycle`) + spine (`host-template`), for every adopter.** Design
> guardrail: **no project-specific names in the tool or spine; dispatch on the *declared recipe*, never
> on a name.** This README is the **re-cut** after an adversarial review (`design-review.md`,
> proceed-with-major-revisions): the overfit is cut (no named "shapes", no tag-worktrees, no
> release-by-ref), the two false headline claims are dropped (this is a path-derivation refactor *and* a
> recipe-field change, not "layout-only"), and (by operator decision) the **tool-residency spine
> clause** is folded in here, so this milestone genuinely resolves `plan/0028`'s blocking
> *spine-contradiction*. agentic-host's own migration (`plan/0028`, `call/0020`) is re-cut to depend on
> this as the first dogfood.

## Context

The Where room has always been "one or more components" (`STRUCTURE.md`; `call/0010`, settled into the
spine), with `embed`/`release` recurring per component. But the tooling was only exercised on one
component on `main` in a flat, root-scattered layout, and two related spine gaps were never closed:
the **residency** of the tools a development host *develops* (the spine says "reference, don't vendor"
unconditionally, contradicting a host that embeds its own tools as Where software, `plan/0028`'s
spine-contradiction), and the **mechanics** of a heterogeneous, addressable, multi-component room. This
milestone closes both, generically, in the spine.

## The generic model

A Where room is a set of **components**; each component is a **bare store plus branch worktrees**; the
tool dispatches every operation on **what the recipe declares**, expressed as two booleans: **does the
stanza declare an `artifact`?** and **does it declare a `build`?** There is no "shape" enum and no
"library" concept (those were the three agentic-host components in disguise):

- **declares `artifact`** then `--verify-build` rebuilds from the pin and must reproduce the hash;
  `release` builds, re-derives, re-pins, tags, receipts. (A binary, a JS `dist/`, a wheel, a `.so`,
  all just "declares an artifact".)
- **no `artifact`** then `--verify-build` no-ops; `release` is **tag-only**. *This path already exists in
  the tool* (`builds_view` tolerates no artifact, `release` already prints a tag-only sequence); the one
  real gap is `current_version` erroring when a brand-new component has no first tag.
- **no `build`** then `--check` validates the pin only (a text/docs component; `host` proves this works).

### Layout: uniform nesting, store separated from branch worktrees

```
software/
  <component>/
    .git/         # bare object store; name LOCKED to .git (operator); verify git discovery + tree-walk treat it as the store
    <branch>/     # a branch worktree; <branch> keeps its slashes (feature/login, release/2.0)
```

- **(item, branch) is a literal path:** `software/<item>/<branch>/`. The canonical worktree is the
  pin's branch (e.g. `software/<item>/main/`).
- **Worktrees are keyed by branch only,** exactly what `call/0010` authorizes ("one per agent or live
  release branch"). A **tag is an output of `release` and the value of `pin`, never a worktree axis**;
  there is no `tags/` tree and no detached tag-worktree.
- **The on-disk path is a *view*, not git's key.** git keys worktree admin by the ref *leaf*
  (`feature/login` and `bugfix/login` both register as `login`), so the tool resolves worktrees via
  `git worktree list --porcelain` (path↔admin), never by assuming the path is the admin name.
- **Uniform for every adopter, even single-component ones** (operator decision: reduce churn over a
  proportional-nesting special case). The cost is honest and stated in the spine: a one-component,
  one-branch project sits at `software/<c>/main/` (three extra segments and a one-time re-materialize)
  for layout uniformity.
- **One `.gitignore` entry** (`/software/`) replaces the per-component triplets, **and `software/` is
  excluded from every host-root *filesystem* tree-walk** (`remap`/`collect_files`, the link check,
  `book`); otherwise a single tree holding all component source re-arms the walk hazard that reddened
  Site CI before (`call/0011`).
- The off-tree `store=` escape still applies, with the **component dir** as the in-tree junction (kept
  shallow for `MAX_PATH`); `--check`'s handle resolution re-targets to the nested path.
- The **`escapes_root` wrong-tree HAZARD** is re-targeted onto the *derived* nested path, with a
  regression test that an escaping `store=` / `..`-climbing worktree still HAZARDs.

### Addressing: a flag, not a second positional

```
host-lifecycle software --materialize|--check|--verify-build [--item <name>[@<branch>]] [<dir>]
host-lifecycle release <name>          # canonical worktree only; no @<ref>
```

- **Omit `--item` yields all components, canonical worktrees** (today's behavior; the bare `[<dir>]`
  positional stays exactly where it is). The specifier is a **flag** because the existing parser already
  takes the first positional as `<dir>`, and a second positional `<item>` would be genuinely ambiguous
  (`software --check host-lint`: item or dir?).
- `--item <name>` yields that component's canonical worktree (the targeted bootstrap/check/build).
- `--item <name>@<branch>` yields a specific branch worktree (`<branch>` keeps its slashes).
- **`@<branch>` is never propagated into `--component` for receipts,** because the receipt gate keys
  per-component; a ref-qualified component would read as "no receipt" and HAZARD.

## Tool residency (folded in, the spine clause `plan/0028` needs)

The spine states "Reference, don't vendor. Each tool is a git submodule … its code stays out of
this repository" *unconditionally*, and lists `tools/host-lint`, `tools/host-lifecycle`,
`tools/host-prove` as referenced tools in three normative places. That contradicts a **development host**
that embeds the tools it *authors* as Where-room software. Amend the spine to draw the distinction:

- An **adopter** *references* the host-* tools, as pinned submodules, "reference, don't vendor".
- A **development host** *develops* the tools it authors and embeds them as **Where-room components**
  (materialized as bare-store-with-worktrees, released through the lifecycle), exactly like any other
  software it develops. The tool's *consumed* form (the built binary + worktree-sourced skills) is
  served from that Where component.

This is the spine change that genuinely resolves `plan/0028`'s spine-contradiction; `call/0020` (the
agentic-host-local decision to embed the host-* family) then *applies* this clause instead of forking
the spine. Update the five-rooms framing, the verification-ladder/STRUCTURE.md tool listings, and the
"Reference, don't vendor" rule accordingly.

## Deliverables

1. **Tool: layout.** Materialize/check the uniform `software/<component>/<branch>/` tree; resolve
   worktrees via `git worktree list --porcelain`; re-materialize must `git worktree prune` stale admin
   entries; detect and HAZARD a case-insensitive ref collision; re-target `escapes_root`; exclude
   `software/` from the filesystem tree-walks.
2. **Tool: addressing.** The flag-based `--item <name>[@<branch>]` on the operate verbs; default-all
   preserved; `release <name>` canonical-only; `@<branch>` kept out of receipts.
3. **Tool: recipe dispatch.** Branch on `artifact?`/`build?` with no name literals; scope the
   no-artifact work to the *one* real gap (`current_version` first-tag bootstrapping); the rest of the
   tag-only path already exists.
4. **Tool: link integrity (net-new).** A `software --check` resolver that walks `.claude/skills`,
   resolves each *generated* (untracked) link, and HAZARDs an unresolved one, distinct from the
   existing tracked-symlink hazard, worktree-absence-tolerant, and `software/`-excluded; shipped as a
   host-lifecycle patch + tag. Plus the component-shipped-skill wiring port (the `link-skills.sh`
   dir-shape logic, generalized to a Where component's worktree).
5. **Spine.** `STRUCTURE.md` + `CLAUDE.md`: the nested layout (with the honest single-component overhead
   note), the addressing, the **recipe-dispatch** wording (drop "shapes"/"library"), the artifact-path
   resolution under nesting, **and the residency clause**; the lifecycle manifest if any field changes;
   an `UPGRADING.md` entry whose `verify=` is a **state check** (`software --check` clean on the new
   layout), delivered through the copy-at-version flow.
6. **Recipe: the field change (stated, not hidden).** The `worktrees =` / `worktree = <dir> …` fields
   encode the flat scheme (the `<dir>`/`.line` token *is* the old path; the branch is recovered by
   stripping the `<name>.` prefix). Under nesting the branch is the path key, so the `<dir>`/`<line>`
   token retires; the migration rewrites or drops it.
7. **Generic fixtures + weak-agent test.** A **median-adopter fixture** (one artifact-bearing component
   on `main`, no parallel lines) proving the uniform layout and default-all addressing are unobtrusive
   for the common case; **and** a **stress fixture** (multiple components, including an
   *artifact-bearing* library and a no-`build` docs component, plus a parallel branch). Fen (4B) reaches
   the targeted `--item` command unaided (printed, not constructed). Neutral names throughout.

## Migration (copy-at-version, ordered, tool-run)

The five-step apply sequence, stated explicitly: commit the spine change in `host-template`, then add the
`[upgrade "<rev>"]` entry with the state-check `verify=`, then bump agentic-host's `.host` to that revision,
then `host-lifecycle upgrade --record <id>` (runs the `verify=`), then re-materialize. The re-materialize is
itself an ordered tool-run sequence, **never by hand**: a clean-worktree precondition (refuse a *dirty*
parallel worktree, so uncommitted work is never lost), then update `.gitignore` to `/software/`, then materialize
(pruning stale admin first), then an explicit **teardown** of the old `<name>/`, `<name>.git/`,
`<name>.<line>/` dirs (a tool step), then drop the old ignore triplets. Note the field-change migration
(Deliverable 6) rewrites `.host-software`'s parallel-worktree lines.

## Verification

- **Both fixtures green**: median-adopter (the nesting is invisible to default-all) and stress (multiple
  components, an artifact-bearing library, a docs component, a parallel branch).
- `--verify-build` reproduces an artifact-bearing component's hash under nesting; `escapes_root` still
  HAZARDs an escaping worktree; `remap`/`book` run clean with `software/` fully materialized (no
  descent); the link-integrity check fails loudly on a broken link and **skips** an un-materialized
  component; `software --check` clean; the `.git` store-dir passes git discovery + the tree-walk.
- Fen reaches the targeted `--item` command unaided.
- **Then** agentic-host migrates as the dogfood, and `plan/0028` proceeds on top.

## Risks / honesty

- **Uniform nesting taxes single-component adopters** (decided: reduce churn; stated in the spine, not
  presented as a pure win).
- **The real surface is large**: the ~14-site path-derivation refactor, the `escapes_root` re-target,
  the recipe field change, and the net-new generated-link walk, *not* "layout-only".
- **Filesystem edges**: case-insensitive collapse (this WSL2 `/mnt/c`), `MAX_PATH` at depth, the
  worktree-admin-leaf-keying, and the `.git` store-dir discovery caveat, all must be tested, not
  assumed.
- **Folding the residency clause enlarges the spine change**, but it is the clause `plan/0028` needs;
  coupling them avoids landing a half-resolved spine.

## Relationship to other milestones

- **`plan/0028`** depends on this for the layout, addressing, recipe-dispatch, skill wiring, **and** the
  residency clause that resolves its spine-contradiction.
- Resolves `plan/0028`'s *spine-contradiction* (residency clause here), *library-component-slot* (recipe
  dispatch), and *new-link-loop* (the link-integrity check).

## Residuals closed (host-lifecycle v0.21.0)

The deferred refinements landed in host-lifecycle v0.21.0 (`bf23391`, artifact
`a3364020`): a `software --teardown [--item <name>[@<branch>]] [--force]` subcommand
that removes a component's worktrees and bare store and **refuses to destroy a
worktree holding uncommitted or unpushed work** unless `--force`; a branch-collision
HAZARD in `software --check` for branches that collide as a path (case-folding, the
`/mnt/c` edge) or in git's worktree admin (a shared ref leaf); and a Fen (Qwen-3.5-4B)
ergonomics pass, where the weak agent reached the targeted `--teardown --item` command
unaided. The "resolve worktrees via porcelain" risk is closed defensively: a colliding
leaf or case is HAZARDed at check time rather than silently mis-resolved.

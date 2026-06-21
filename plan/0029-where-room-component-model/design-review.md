# plan/0029 — adversarial design review

Five independent adversarial reviewers, distinct lenses: git/filesystem mechanics; migration and
backward-compatibility; generality vs overfit; tool-implementation feasibility (against the source);
spine coherence. Findings named for content, deduplicated, cross-confirmation noted.

**Verdict: proceed only with major revisions.** The plan is *both* overfit and oversold. It overfits
three things to agentic-host's own components, and it asserts two headline properties that are false
against the `host-lifecycle` source. The sound core is real: the nested store/worktree layout for a
multi-component room is genuinely generic, and the no-artifact path already works in the tool.

## Sound kernel — attacks that failed

- **Multi-component rooms and per-agent / per-release-branch worktrees are already spine-authorized**
  (`STRUCTURE.md` "one or more components"; `call/0010` is `superseded by the spine`, i.e. settled
  methodology). The branch-keyed nested layout faithfully *finishes* an already-generic model.
- **The no-artifact (library/docs) path already works in code** — `builds_view` tolerates a stanza with
  no `artifact`; `--verify-build` no-ops it; `release` already prints a tag-only sequence; `host`
  passes `--check` today. So most of "Deliverable 3" exists.
- **`call/0010`/`0011`/`0005` are already `superseded by the spine`** — no inherited ouroboros tangle.
- **Default-all addressing preserves today's behavior** (omit the specifier → all components).

## Overfit — cut these (the operator's instinct, confirmed)

- **The three named "shapes" are `{host-lint, host-grammar, host}`. [HIGH]** "Library = no artifact" is
  false for a JS/Python/C library (they build a `dist/`/wheel/`.so`). The real discriminator is two
  booleans the tool *already* keys on — `artifact?` and `build?` — not a binary/library/docs enum.
  **Drop the named shapes and the word "library"** from the tool and spine prose; branch on the
  declared recipe alone.
- **`tags/<tag>/` worktrees are exercised by no one. [HIGH]** A worktree at a tag is detached-HEAD:
  `release` would commit onto no branch, and `--check`'s branch-equality assertion false-DRIFTs on
  `HEAD`. The tag axis exists only to solve a collision the tag axis itself introduces. **Key worktrees
  by branch only** (exactly what `call/0010` authorizes); a tag is an *output* of `release` and a value
  of `pin`, never a worktree axis.
- **`release <item>@<ref>` is unmotivated. [MED]** `release` always cuts from the canonical worktree;
  releasing arbitrary refs contradicts the audit model. Keep `@<ref>` only on
  `--materialize`/`--check`/`--verify-build`; `release` takes `<item>` only.
- **The fixture's "parallel branch" smuggles the overfit back in. [HIGH]** It exists to justify the
  nested layout. **Add a median-adopter fixture** (one component, one branch, zero parallel lines) and
  prove the nesting is *invisible* there (the default-all path); label the multi-component +
  parallel-branch fixture as the explicit stress case. And the fixture's "library" must be an
  *artifact-bearing* library (a builds-a-dist component), or it only proves the host-grammar sub-case.
- **The nesting taxes every single-component adopter. [MED]** A one-component, one-branch project now
  materializes at `software/<c>/heads/main/` — three extra segments and a breaking re-materialize for
  indirection it never uses. Either **collapse the nesting for the trivial case** (nest only when a
  second component or a parallel line exists) or **state the overhead honestly** in the spine prose.

## Oversold — two headline claims are false against the source

- **"Recipe format need not change" — false. [HIGH, three reviewers]** The `worktrees =` /
  `worktree = <dir> <branch> <pin>` fields encode the *flat* scheme: the `<dir>`/`.line` token IS the
  old path, and the branch is recovered by stripping the `{name}.` prefix; `deploy` keys on the flat
  name. Under nesting the `<dir>`/`<line>` token is dead/contradictory and the branch becomes the path
  key — **the recipe changes** (a field retires or its meaning shifts). agentic-host's own empty
  `worktrees =` fields hide this; any adopter with a parallel line breaks.
- **"Layout-only / derived" — false. [HIGH, file:line]** The flat layout is hardcoded at ~14 sites
  across 8 functions (`root.join(&s.name)`, `{name}.git`, the `.host-verify-<name>` temp worktree, the
  `{name}.{line}` prefix heuristic, `--install-hooks`, the artifact-path join, `current_version`,
  `run_release`). It is a path-derivation **refactor**, not an edit. And the **`escapes_root`
  wrong-tree HAZARD** must be re-targeted onto the *derived* nested path (with a regression test that
  an escaping `store=` / `..`-climbing worktree still HAZARDs).
- **"Resolves plan/0028's spine-contradiction" — false. [HIGH]** That finding was *host-lint-as-Where
  contradicting "Reference, don't vendor" + the `tools/host-*` listings*, not the multi-component
  model. plan/0029 does not touch the residency clause. **Either scope 0029 to layout/addressing/shapes
  only and stop claiming the resolution, or fold the residency clause in here** (the `call/0020`
  "development host embeds its tools" spine clause).

## git / filesystem mechanics

- **Worktree admin is keyed by ref LEAF, not ref-path. [HIGH]** `feature/login` and `bugfix/login`
  produce admin entries `login`/`login1`; the path-as-unique-key assumption is divorced from git's own
  bookkeeping. The tool must resolve worktrees via `git worktree list --porcelain`, never assume
  `worktrees/<ref-path>`.
- **Re-materialize fails on stale worktree admin entries. [HIGH]** Materialize skips by path-existence
  only; a deleted-but-registered worktree makes `worktree add` hard-exit. The migration must
  `git worktree prune`/`remove` first; make materialize idempotent against stale admin state.
- **A case-insensitive filesystem (this WSL2 `/mnt/c`, confirmed) collapses distinct refs and can
  corrupt the bare ref store. [HIGH]** `Feature/Login` vs `feature/login`. Detect a case-collision in
  the materialized ref set and HAZARD it.
- **Orphaned worktrees on ref delete/rename are never pruned. [MED]** `--check` should reconcile the
  materialized `software/` tree against the recipe and HAZARD extras.
- **Off-tree `store=` junction at nested depth: `MAX_PATH`, case-folded `canonicalize`. [MED]** The
  in-tree handle is now deep; specify where the junction sits and keep it shallow.

## CLI / tool feasibility (file:line grounded)

- **`software --check [<item>] [<dir>]` two-positional ambiguity. [HIGH]** The current parser takes the
  first positional as the **dir** (`pos.first()`), so `software --check host-lint` canonicalizes
  `host-lint` as a directory and errors. The "backward-compatible bare positional" claim is false — the
  specifier **must be a flag** (`--item`). Note `software` (first positional = dir) and `release`
  (first positional = component) have *opposite* conventions, so no uniform parse helper works.
- **The generated-link integrity check cannot reuse `dangling_symlink_hazards`. [HIGH]** That function
  inspects only *tracked* symlinks (`git ls-files`); generated skill links are deliberately untracked.
  This is net-new code (a filesystem walk of `.claude/skills` resolving each link) plus a `link-skills.sh`
  shell→Rust port — not a "generalization," and it must itself skip the `software/` subtree and tolerate
  worktree-absence (`call/0011`).
- **The library/no-artifact branch is ~90% already implemented. [MED, de-risking]** `--verify-build`
  no-ops, `release` is tag-only, the receipt emits `--evidence v{new}` — all present. The real gap is
  narrow: `current_version` errors with no first tag (a brand-new library can't be released). Scope
  Deliverable 3 to that, not a re-implementation of working code.
- **Keep `@<ref>` out of receipts. [LOW trap]** The receipt gate keys on component name only; a
  ref-qualified `--component` would read as "no receipt" → HAZARD. State the invariant.

## Migration

- **No teardown of the old layout. [MED]** `--materialize` is additive and never removes the old
  `<name>/`/`<name>.git/`/`<name>.<line>/` dirs; the order vs `.gitignore` is undefined, risking a
  `git add -A` of the whole materialized store (the worktree-absence footgun) or a half-migrated tree.
  Specify an ordered, tool-run sequence with an explicit teardown step (not by hand).
- **Uncommitted work in a parallel worktree is lost on re-materialize. [MED]** `worktree remove`
  refuses/discards a dirty tree. Require a clean-worktree precondition; `verify=` should check it.
- **The `UPGRADING` `verify=` can't be a doc-grep for a tree migration. [MED]** Its real post-condition
  is adopter-tree state (`software --check` clean on the new layout, old dirs gone), not a spine-prose
  grep — the first ledger entry whose post-condition is tree state.
- **"One adopter / hard cut" is too narrow. [MED]** A versioned spine means future adopters apply the
  entry later → two layouts in the field; the tool must gate on the `.host` baseline or read both. And
  agentic-host already has **two** components (host-lint + host). The five-step apply sequence (commit
  template → UPGRADING entry → bump `.host` revision → `upgrade --record` → re-materialize) is omitted.

## Spine coherence

- **A single `/software/` tree reintroduces a tree-walk hazard. [HIGH]** `remap`/`collect_files` walks
  the host root and skips only `.git`/`target`/`node_modules`/`vendor`; a single `software/` dir holding
  every component's full source would be descended into — the `call/0011` Site-CI-red class. **Exclude
  `software/` from every host-root tree-walk** (`remap`, the link check, `book`), and verify.
- **Reproducible-build artifact-path resolution + the `--verify-build` throwaway-worktree path move.
  [HIGH]** Decide and document whether `artifact = <path>` is relative to `software/<c>/heads/<branch>/`,
  and ensure the temp verify tree is excluded from the `software/` walk and does not escape-HAZARD.
- **"Reconcile `call/0010`'s status" is a no-op misreading. [factual]** It is already superseded; the
  real check is that `call/0020`'s tag-only / multi-component dependencies are satisfied by the branches
  delivered here.

## Recommended re-cut

1. **Cut the overfit:** named shapes → two recipe booleans (`artifact?`/`build?`); `tags/<tag>/`
   worktrees → branch-keyed only; `release <item>@<ref>` → `release <item>`.
2. **Drop the false framing:** reframe as a path-derivation refactor (~14 sites) + a recipe-field change
   (retire the `<dir>`/`<line>` token); drop "layout-only / recipe-unchanged"; drop or substantiate the
   "resolves spine-contradiction" claim.
3. **Flag-based `--item` specifier** (not a second positional); `@<ref>` only on the operate verbs.
4. **Exclude `software/` from tree-walks; re-target `escapes_root`** onto the derived path with a test.
5. **Median-adopter fixture** + an explicit stress fixture; the fixture library is artifact-bearing.
6. **Migration:** ordered tool-run teardown + clean-tree guard + a state-check `verify=` + the five-step
   copy-at-version apply sequence.
7. **Scope Deliverable 3** to the `current_version` first-tag gap; the rest of the no-artifact path
   exists.

## Store-dir name (operator decision)

Operator keeps **`.git`** as the per-component bare-store dir name. Locked. The one caveat the reviewers
raised: a bare store at `software/<component>/.git/` sitting beside the branch worktrees risks git's
repository-discovery treating `software/<component>/` as a repo (the `.git` name is conventionally
non-bare metadata), and a tree-walker that special-cases `.git` must treat this as the object store. A
branch literally named `.git` cannot collide (git rejects it). Verify discovery + the tree-walk behave
under this name before it ships.

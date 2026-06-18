# Install commit hooks from the software recipe

A host-lifecycle point release (**v0.8.1**) closing the fresh-clone gap surfaced
in `plan/0008`: `software --materialize` and the skill symlink were automated,
but the commit hooks were not — so a fresh clone (or a stale checkout) ran an
old host-lint, or none, on its own commits.

## What shipped

`host-lifecycle software --install-hooks <dir>`: for each `.host-software`
component that declares a `hooks` script, copy that dispatch script into the
repo's hooks directory as both `pre-commit` and `commit-msg`, alongside the
deploy artifact (the binary the script invokes). The hooks directory is resolved
via `git rev-parse --git-path hooks`, so worktrees and a custom `core.hooksPath`
resolve correctly.

- New optional `hooks = <script>` field on the software stanza (relative to the
  canonical worktree). Absent → the component is skipped.
- **Gate: worktree-at-pin, not byte hash.** The worktree must be at its recorded
  `pin` (the audited source) and the artifact must exist. The recorded artifact
  hash is the *pinned container's* output; a local toolchain legitimately
  produces different bytes, and requiring a match would force a Docker build just
  to install the gating hook. The canonical-hash match is reported as an
  informational note (`verified` vs `local build`), never a blocker.

## Wiring

`.host-software` `[software "host-lint"]` gains `hooks = pre-commit`. The
fresh-clone setup in the root `CLAUDE.md` now ends with `software --install-hooks .`
after materialize + the skill symlink.

## Verification

- host-lifecycle unit tests (33): `hooks` parses; `install_hooks` copies the
  script (as both hook names) and the binary when the worktree is at its pin, and
  blocks when it is off-pin.
- Dogfooded on this repo: `software --install-hooks .` installed `pre-commit`,
  `commit-msg`, and the `host-lint` binary, noting the local build differs from
  the canonical hash. Our own commit-msg hook now runs the v0.3.0 prose-capable
  tool.

## Not done here

host-lifecycle is installed in CI by rev (`reproducible-build.yml`,
`mdbook.yml`); those jobs do not use `--install-hooks`, so their pins are
unchanged. Bumping them is a separate, optional follow-up.

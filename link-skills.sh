#!/bin/sh
# Recreate .claude/skills/* symlinks for every *materialized* skill-bearing component.
#
# Two sources, both materialized-locally and gitignored:
#   - external tool submodules under tools/ (allium, specula)
#   - Where-room software components under software/<name>/main (the .host-software
#     recipe — host-lint, host-lifecycle, host-prove; plan/0028)
#
# These symlinks are NOT tracked: a tracked symlink into an absent worktree/submodule
# dangles wherever it is not materialized (a fresh clone, CI, a partial init) —
# worktree-absence coherence, call/0005 — and any tree-walking tool (mdBook, a linter,
# find/grep) then trips over the broken link. So we generate them instead, for what is
# present. Run after `git submodule update --init` and `software --materialize`.
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p .claude/skills
# Clear prior generated links so a moved/removed component leaves no dangling symlink.
find .claude/skills -maxdepth 1 -type l -delete
n=0

# Link every skill under each component root matched by the glob $1. A component either
# exposes one dir per skill under skills/, or ships a single skill as a root SKILL.md.
# The link target is always ../../<path-from-repo-root> (.claude/skills is two deep).
link_from() {
  for comp in $1; do
    [ -d "$comp" ] || continue
    if [ -d "$comp/skills" ]; then
      for s in "$comp"/skills/*/; do
        [ -d "$s" ] || continue
        ln -sfn "../../${s%/}" ".claude/skills/$(basename "$s")"
        n=$((n + 1))
      done
    elif [ -f "$comp/SKILL.md" ]; then
      # Name the link after the component, not the worktree branch: a Where-room root is
      # software/<name>/main, so strip a trailing /main before taking the basename
      # (a tools/<name> root has no /main suffix and is left unchanged).
      base=${comp%/main}
      ln -sfn "../../$comp" ".claude/skills/$(basename "$base")"
      n=$((n + 1))
    fi
  done
}

# External tools: tools/<tool>/skills/<skill> (host-template carries no skills — skipped).
link_from "tools/*"
# Where-room software: the canonical worktree software/<name>/main, with skills/<skill>
# (host-lifecycle, host-prove) or a single root SKILL.md (host-lint). A component with
# neither (host-grammar, host) is silently skipped.
link_from "software/*/main"

echo "link-skills: linked $n skill(s) from materialized components"

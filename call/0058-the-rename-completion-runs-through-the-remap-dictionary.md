# call/0058: the rename completion runs through the remap dictionary

- Status: accepted
- Scope: agentic-host (the same map applied mechanically to the template's tracked copies)
- Date: 2026-09-05
- Relates: plan/0085, call/0053, connollydavid/host#19

## Context and problem

The manual's rename to `AGENTS.md` (plan/0085, `ACTIVE-corpus-and-agents-manual`) was applied partially: both manuals kept `# CLAUDE.md` as their title, the template's room table and spine-definition still named the old file, and the host's copy-at-version paragraph and calx-knap note cited it. A rename completed by hand-editing stragglers is not a migration; the methodology owns a mechanism for exactly this, the remap dictionary, map-only by construction.

## Decision

The completion runs through `.host-remap`, committed before the apply so the prior commit archives the originals, applied per repository (the host's tracked corpus and the template's, the submodule's files being tracked there), and retired after, this decision being the durable copy of the map:

```
# CLAUDE.md: operating manual for an agentic project => # AGENTS.md: operating manual for an agentic project
# CLAUDE.md => # AGENTS.md
| How  | `CLAUDE.md` + `tools/` | this manual, and the verification tools | => | How  | `AGENTS.md` + `tools/` | this manual, and the verification tools |
The nested `host-template/CLAUDE.md` is that source => The nested `host-template/AGENTS.md` is that source
root CLAUDE.md belongs to plan/0079's render => the root manual belongs to plan/0079's render
methodology is settled in this spine (`CLAUDE.md` + `STRUCTURE.md`) => methodology is settled in this spine (`AGENTS.md` + `STRUCTURE.md`, with the `CLAUDE.md` pointer)
the project-specific parts of its `CLAUDE.md` => the project-specific parts of its `AGENTS.md`
```

The mappings are deliberately precise strings rather than a bare `CLAUDE.md => AGENTS.md`: a bare token substitution would corrupt the records that describe the rename itself (plan/0084, plan/0085, the 2026-09-05 MEMORY entries), which must continue to say what happened. The two intentional `CLAUDE.md` mentions that remain in the manuals are the pointer's own name in live prose.

## Consequences

- The dictionary's comment syntax (`# ` prefixes a comment) cannot express a mapping whose old string starts with a markdown H1, so both title lines were hand-edited beside the apply. Recorded as a host-lifecycle tool note: an escaped or quoted form for mapping lines beginning with `#` would make H1 renames expressible.
- The specula and allium submodules' `claude`-named scripts and agent docs are upstream vendor vocabulary (the Claude Code adapter), not this methodology's manual name, and are untouched.
- The records that cite `CLAUDE.md` before this call are history and stand as written; citations in forward documents follow the renamed file.
- The ledger's old `verify` greps are handled by the evaluator's pointer-following (shipped in v0.52.1), not by this map.

- Addendum (2026-09-05, same day): the template README's own room table carried the same stale How row and was fixed by the same substitution after the dictionary retired; the census over both manuals and the front-door documents now holds only the pointer's own name.

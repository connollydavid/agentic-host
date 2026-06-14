# A migrated project excludes its append-only record from the audit

- Status: accepted
- Date: 2026-06-14
- Refines: `call/0007` (the record tier). Builds on `host-lint` `.host-lintignore`.

## Context and Problem Statement

`call/0007` left the record (append-only `MEMORY.md`, closed milestone bodies)
either rewritten (governed, map-only) or kept. Applying it to a real target
(Agentic-MCP-Win32s) showed rewriting the record is the wrong trade: the record is
a dense lab-notebook where token-substitution produces awkward prose
(`"the bridge core bridge first-green"`) and ~25 review/tracking codes
(`finding #7`, `weed #1`, `R1`/`F1`/`G1`) resist content-naming. So a "full clean
break" of the record is expensive and degrades it.

The decisive fact, **verified on the target**: nothing re-scans the historical
tree. The commit hooks lint only the commit subject and the *staged diff*; CI runs
no linter (`mdbook` only). `host-lint --all` is a manual one-shot for migration
events. So old names sitting in the record cost **zero** on an ongoing basis — they
are read by no automated gate, ever.

## Decision Outcome

**A migrated project excludes its append-only record from the `--all` audit via a
`.host-lintignore`, rather than rewriting it or acknowledging-modulo.** The
migration writes, e.g.:

```
MEMORY.md
plan/*/README.md
```

- The **live layer** (indexes, governance, skills, cross-refs) is clean-broken to
  content names (via the `remap` dictionary, `call/0008`) and stays in audit scope.
- The **record** is left verbatim and excluded, so `--all` is genuinely `0` without
  a rewrite and without abusing the token allow-list. Old milestone names survive
  only where history lives; the renamed `plan/<NNNN-slug>/` folders are the implicit
  old→new map (a reader hitting `Phase 4` in the record finds
  `plan/0004-command-execution/`).
- `host-lint` stays general/policy-free — it honours an ignore file the way
  `git`/`ripgrep` do; the *methodology* supplies the policy by writing the file.

**Token rationale (the deciding lens):** rewriting the record is one-time cost with
**no** recurring payback (nothing re-scans it), and risks negative value (degraded
prose costs future readers). Excluding it is near-zero one-time and zero recurring.
So exclusion is the token-optimal record handling. The live-layer clean break keeps
its recurring payback and stays.

## Consequences

- Good: `--all` means "no live tells," cleanly, with no record rewrite, no lossy
  prose, no allow-list abuse.
- Good: this is the concrete resolution of the deferred baseline question
  (`call/0006`) for the record class — a path exclusion, not a per-finding baseline.
- Cost: a reader auditing *history* must run `host-lint` against the excluded paths
  deliberately; that is the rare, correct time to look. The exclusion is explicit
  and reviewable in `.host-lintignore`.

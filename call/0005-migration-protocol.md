# Adopt and upgrade existing repos by a cased, moded migration protocol

- Status: accepted
- Date: 2026-06-14

## Context and Problem Statement

Decision 0004 makes the template a versioned source and says projects adopt a
revision — but nothing defined *how* an existing repo becomes a host, or how one
that adopted an earlier revision upgrades. Real targets show the shapes vary: a
repo with no `CLAUDE.md`, a repo with a foreign `CLAUDE.md` predating the
methodology (with deep ordinal-naming debt in files and history), and our own
repos at an earlier revision. They also vary in appetite for disruption: some can
absorb a single forward-only change; rewriting history is sometimes warranted and
sometimes forbidden (when the history carries provenance others depend on).

## Considered Options

1. **Ad hoc** — migrate each repo by hand, deciding everything case by case.
2. **A defined protocol** — one skeleton with a small set of explicit choices.

## Decision Outcome

Chosen option 2: **a single protocol, parameterised by two orthogonal axes,
shipped as the template's `MIGRATION.md` and driven by `host-lifecycle`.**

- **Case = starting state** (decides how governance is established): **(a)** no
  `CLAUDE.md` → drop in the manual and elicit the repo's own conventions; **(b)**
  foreign `CLAUDE.md` → merge each rule (subsumed / project-specific / conflict →
  human); **(c)** carries a `.host` stamp → upgrade by diffing the
  recorded revision against the current one. `host-lifecycle classify` reports the
  case.
- **Mode = blast radius** (decides how the audit is applied): **Preview**
  (report only, always first), **Shallow PR** (default; live files only; history
  untouched), **Staged** (Shallow across several PRs, for volume), **Deep
  rewrite** (opt-in; archive-first, then rewrite history).
- **Selection rule.** Default Shallow; escalate to Staged on volume; choose Deep
  only when history-coherence value exceeds provenance/disruption cost, and never
  on history carrying provenance you do not control. **History is immutable by
  default** — outside Deep, legacy tells are acknowledged, not rewritten.
- **The stamp keys upgrades.** `host-lifecycle adopt` scaffolds the rooms and
  writes `.host` (template + revision + date); `version` reads it. The
  recorded revision is what a case-(c) upgrade diffs from.
- **Mechanical work is token-free.** `host-lifecycle` does the classify /
  scaffold / stamp; `host-lint --all`/`--log` does the audit. Model effort is
  spent only on the case-(b) merge, case-(a) elicitation, and audit triage.

## Consequences

- Good: adoption and upgrade are repeatable and auditable; a fresh session can
  read `MIGRATION.md` and the stamp and continue.
- Good: the dangerous operation (history rewrite) is gated behind an explicit
  mode with an archive-first rule, not reached by default.
- Cost: the protocol adds two new artifacts to maintain (the `MIGRATION.md`
  payload and the `host-lifecycle` verbs) and a stamp file per repo.
- Validated by dogfood: the host migrates itself (case c) under this decision;
  external repos follow as their own milestones.

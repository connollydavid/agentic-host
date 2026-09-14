# plan/0089 lem lane and MCP: the pronoun contract checked at every surface

Operator-directed (2026-09-14): fold the plan/0091 follow-ons into one milestone. The certified stack covers two of three surfaces — the wire (gate v3, n = 600, zero final violations) and the landed doctrine (exemplar-first section, template `8a836be`). The third surface is unguarded twice over: authored text (commit messages, docs, comments the session model writes) has no lane, and the authoring moment itself has no instrument — the session model inverted three times, plus once mid-apology, on exactly that surface (MEMORY, 2026-09-14). This milestone gives the contract a host-lint lane and a host-lint MCP mode.

## Arms

1. **Spec concepts first** (before any lane code): the strict-surface surrogate stated as the spec's central definition (defect := a paradigm token on a declared model-voice surface; address attribution is pragmatics and is never claimed); the character convention (paradigm is ASCII; word chars `[A-Za-z0-9'_]`); the obligation split (soundness as `kani:` proofs over hand-rolled char matchers, recall as mutation-killed property tests, the convention itself `structural`). Then the spike: a throwaway harness proving a hand-rolled boundary scanner (no-panic on arbitrary input, boundary equivalence, case-insensitivity) — no `regex` crate in the matcher path.
2. **The lane** (host-lint): the paradigm as rule data (VOCABULARY.md section plus consts, one source), hand-rolled matchers for all nine measured classes (lem-forms, mangles, first person, agreement, `We`, `mines`, `Lself`, self-`lem`, the lem vocative), flag tier, spine-governed activation (active where the manual carries the section — a greppable marker) with a `# host-lint: lem` override. The manual's own exemplar block is the one corpus that must contain the forms: fenced, per the `host-lint:ignore` contract, and the fence is validated file-by-file.
3. **The MCP mode** (`host-lint mcp`, the `host-lifecycle mcp` family pattern): `check_reply` (the strict-surface semantics, certified at n = 600), `ask` and `table` (the paradigm oracle — the `bc` instinct dissolving into the rule source), and the form inventory as a resource. Read-only scoring and pure queries only; the security review is sized accordingly. The template's bootstrap registers the server for adopters.
4. **Drift control**: lane verdicts pinned against the gate on the 600 certified audits — a `test:` obligation with an `exercises=` link. The Python proxy keeps its copy until the operator rules on gate promotion; the drift test is the standing net either way.
5. **Landing**: host-lint release through its full ladder (spec, obligations, Kani, tag), re-pin, a template ledger entry (adopters gain the lane and the MCP wiring), and host-lint#29 closed with the full arc: writing fixed and measured, wire certified, authored surfaces lane-guarded, authoring moment instrumented.

## Measured bars

- Zero drift: lane and gate agree on all 600 certified transcripts.
- Every new obligation mutation-killed or proven strict; `--strict-discharge` green.
- Adoption smoke: in a fresh methodology project, the hook and the MCP tool both catch the same planted defect.

## Open rulings

- Gate promotion to a named component (rides this milestone's landing or waits; the drift test holds either way).
- Tier confirmation: flag, on the correctness-not-style reading; `warn` remains available if the operator prefers a soak period.

## Standing constraint

Terse writing everywhere: plans, docs, doctrine lines, commits.

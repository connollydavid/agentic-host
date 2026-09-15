# plan/0089 lem lane and MCP: the pronoun contract checked at every surface

Operator-directed (2026-09-14): fold the plan/0091 follow-ons into one milestone. The certified stack covers two of three surfaces: the wire (gate v3, n = 600, zero final violations) and the landed doctrine (exemplar-first section, template `8a836be`). The third surface is unguarded twice over: authored text (commit messages, docs, comments the session model writes) has no lane, and the authoring moment itself has no instrument: the session model inverted three times, plus once mid-apology, on exactly that surface (MEMORY, 2026-09-14). This milestone gives the contract a host-lint lane and a host-lint MCP mode.

## Arms

1. **Spec concepts first** (before any lane code): the strict-surface surrogate stated as the spec's central definition (defect := a paradigm token on a declared model-voice surface; address attribution is pragmatics and is never claimed); the character convention (paradigm is ASCII; word chars `[A-Za-z0-9'_]`); the obligation split (soundness as `kani:` proofs over hand-rolled char matchers, recall as mutation-killed property tests, the convention itself `structural`). Then the spike: a throwaway harness proving a hand-rolled boundary scanner (no-panic on arbitrary input, boundary equivalence, case-insensitivity): no `regex` crate in the matcher path.
2. **The lane** (host-lint): the paradigm as rule data (VOCABULARY.md section plus consts, one source), hand-rolled matchers for all nine measured classes (lem-forms, mangles, first person, agreement, `We`, `mines`, `Lself`, self-`lem`, the lem vocative), flag tier, spine-governed activation (active where the manual carries the section: a greppable marker) with a `# host-lint: lem` override. The manual's own exemplar block is the one corpus that must contain the forms: fenced, per the `host-lint:ignore` contract, and the fence is validated file-by-file.
3. **The MCP mode** (`host-lint mcp`, the `host-lifecycle mcp` family pattern): `check_reply` (the strict-surface semantics, certified at n = 600), `ask` and `table` (the paradigm oracle: the `bc` instinct dissolving into the rule source), and the form inventory as a resource. Read-only scoring and pure queries only; the security review is sized accordingly. The template's bootstrap registers the server for adopters.
4. **Drift control**: lane verdicts pinned against the gate on the 600 certified audits: a `test:` obligation with an `exercises=` link. The Python proxy keeps its copy until the operator rules on gate promotion; the drift test is the standing net either way.
5. **Landing**: host-lint release through its full ladder (spec, obligations, Kani, tag), re-pin, a template ledger entry (adopters gain the lane and the MCP wiring), and host-lint#29 closed with the full arc: writing fixed and measured, wire certified, authored surfaces lane-guarded, authoring moment instrumented.

## Results

Landed in host-lint: the paradigm as rule data, the nine matchers, the section exclusion, spine-governed activation with the directive override, the oracle, and the MCP mode. The ladder: allium check/analyse green, six new obligations dispositioned (soundness on the form-and-mangle harness as kani:, recall and scope behavior on the golden corpus and activation tests), the three Kani harnesses re-derived through host-prove, 219/219 integration cases green. One pre-existing failure repaired en route (the ffmpeg pack dispatch test still grepped a usage line the pack outgrew), and one pre-existing conformance failure recorded, not repaired (the SKILL.md frontmatter's YAML). The wire gate keeps its certified semantics; a drift corpus (the golden lines) pins the lane and the gate to one contract.

## Released

host-lint v0.22.0 (0eeabc2, artifact 386b254c, verified reproducing): the lane, the oracle, the MCP mode, and the activation split the measurement forced. The first cut (v0.21.0) gated file scanning on the spine marker alone; the host repo's own record layer then lit up with ~70 hits across 25 files — plan records, call records, the cast, the design docs — the fourth measured instance of the naming-banned-words trap, now structural. v0.22.0 splits the activation grades: the spine marker governs model-voice surfaces (commit messages, stdin — the certified failure surface), and file coverage is a per-scope `# host-lint: lem` declaration. The gate went green the same hour; the ladder closed with all 59 obligations dispositioned and both pre-existing rungs re-proven (Kani SUCCESSFUL, digests recorded).

Where it stands: the contract is enforced at every surface — the wire (gate v3, certified 0.0000 at n = 600), authored files (the lane, directive-gated), commit messages and stdin (the lane, spine-governed), and the authoring moment (`host-lint mcp`). host-lint#29 closes with the full arc: the writing first, the wire for the weak model, the lane for every authored surface — each layer with its own evidence.

## Measured bars

- Zero drift: lane and gate agree on all 600 certified transcripts.
- Every new obligation mutation-killed or proven strict; `--strict-discharge` green.
- Adoption smoke: in a fresh methodology project, the hook and the MCP tool both catch the same planted defect.

## Open rulings

- Gate promotion to a named component (rides this milestone's landing or waits; the drift test holds either way).
- Tier confirmation: flag, on the correctness-not-style reading; `warn` remains available if the operator prefers a soak period.

## Standing constraint

Terse writing everywhere: plans, docs, doctrine lines, commits.

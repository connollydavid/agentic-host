# Emergent-tell discovery is a mechanical gather that the operator triages

- Status: accepted
- Date: 2026-06-24
- Scope: host-lint (the `gather` subcommand) and host-lifecycle (the `verify` and
  `adopt` skill reflect steps). The software implementation of the spine's reflective
  grammar-growth doctrine.
- Relates: the spine doctrine in `host-template` (`27d815b`, "the hygiene grammar grows
  by reflective practice"); `plan/0034` (which authored the doctrine and deferred this
  software decision); `plan/0035` (the milestone that built it); host-lint's `LEXICON`
  allowlist (the per-project legitimacy declaration the gather complements).

## Context and Problem Statement

`plan/0034` authored the doctrine: the shared tell corpus is incomplete and grows by
reflective practice, with discovery mechanical-first (sweep history and recent work for a
recurring shape the lane misses) and operator-validated. It deferred the software decision
for the discovery tooling until that tooling existed. `plan/0035` built it. This records
how the discovery is implemented and where its limits are.

## Decision

Discovery is a `gather` subcommand on host-lint. It runs `git log` over the repository and
scans the tracked markdown headers itself (one command, parse-free for a weak agent),
extracts the word-then-numeral shape, drops what the grammar already catches (`FLAG_TERMS`)
and what the legitimacy allowlists name (`PREV_SKIP`, `UNITS`, a small stop set, a `#`
reference, a year or hash), and reports the recurring residue ranked by count with example
lines.

The gather is **advisory** and exits zero; it never gates. It **never auto-graduates** a
candidate into the shared grammar, and it **never auto-bans** one. The operator triages
each candidate: propose it upstream to the shared grammar, declare it in the `LEXICON`, or
leave it. The `verify` and `adopt` skills prompt the gather, at the verify gate and at the
migration moment.

## Considered Options

1. **Auto-graduate a frequently-recurring shape.** Rejected: the universality call (a tell
   or this project's own domain vocabulary?) needs operator judgment, and an
   auto-graduation would flag an adopter's legitimate vocabulary.
2. **A gating gather that blocks the commit or the gate.** Rejected: discovery is
   recall-biased and surfaces some noise, so blocking on it would be a false gate. The
   gates stay the green sweep; the gather informs.
3. **An advisory surface that the operator triages (chosen).** Keeps the human in the loop
   for the call the tool cannot make.

## Consequences

- Good: mechanizes the doctrine's discovery; one weak-agent command, git and parse in one
  process; reuses host-lint's own grammar and allowlists to separate a candidate from
  noise; keeps the operator's judgment where the universality call lives; surfaced a real
  candidate (`lens`) on the first dogfood.
- Costs: recall-biased, so it surfaces some residue the operator dismisses; the first
  corpus is commit subjects and markdown headers, with prose and code comments a later
  extension; no project-local ban surface (YAGNI, every tell seen so far is universal).

## Confirmation

gather unit and integration tests pass; a dogfood run on this repository surfaces a
sensible candidate set; the `verify` and `adopt` skills name the gather step; the
weak-agent (Qwen-3.5-4B) triages a candidate correctly.

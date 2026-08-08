# call/0054: one commit-message fault earns a detector

- Status: accepted
- Scope: host-lint's commit-time checks; which of the four reported message faults gets a detector, at what tier and with what inputs; where unenforced guidance lives; how the work is packaged and released
- Date: 2026-08-07

## Context and problem

[connollydavid/host-lint#28](https://github.com/connollydavid/host-lint/issues/28) (operator-filed) names four faults that recur in commit messages and pass `--prose`: a message that restates comments its diff adds, advocacy in place of description, answers to points nobody raised, and precedent offered as defence. [call/0037](0037-advisory-ordinal-nouns-warn-not-flag.md) and the plan/0070 review priced the warn tier: an advisory that fires on legitimate text trains its reader to dismiss the tier. [call/0046](0046-vocabulary-states-what-the-tool-enforces.md) fixed VOCABULARY.md as enforcement-true. Any new detector has to clear both.

Five questions were put to the cast: the input surface, the tier and threshold, whether the precedent fault gets a detector, where guidance the tool cannot check lives, and packaging.

## Calibration before design

Measured over 922 accepted commits across seven repositories before anything was designed.

| measurement | result |
|---|---|
| restated comment sentences at an eight-word bar | 19 |
| the same at bars of five and twelve words | 22 and 7 |
| subject-line matches that are the record-title convention | 12 of 12 |
| precedent-as-defence patterns, widened | 0 |

The subject is therefore excluded from comparison, the eight-word bar keeps quotes and short idioms out, and the precedent detector has no corpus to earn a tier against. The caveat is recorded: the corpus is accepted history; rejected drafts and PR bodies were not sampled. A separate sweep for the [connollydavid/host-lint#24](https://github.com/connollydavid/host-lint/issues/24) remainder found zero ordinal-scaffold shapes in 2036 tracked markdown headings across ten stores.

## Convening

Five personas, ranked ballots, each required to attack its own first preference before ranking. Fen was simulated: every probe channel refused connection, the weak-agent-trap lens stood in, and the prompts are preserved with the milestone record.

| question | settled | margin |
|---|---|---|
| input surface | a `host-lint commit` verb; message and diff as named files | 4 to 1 |
| tier and threshold | warn, eight-word bar, subject excluded, commit-msg only | unanimous |
| precedent detector | not built; the shape and the measured zero recorded in guidance | unanimous |
| guidance home | skill text labeled unenforced, never VOCABULARY.md | unanimous |
| packaging | one milestone bundling the host-lint#24 carve-out; one release | 4 to 1 |

Fen's dissent on the input surface asked for one command that reproduces the verdict; it is honored in ergonomics, with the hook printing the exact re-run line beside every warn. Two floor requirements bind the implementation: a degraded path states what it did not check, never a silent clean, and a warn names the safe direction (trim the sentence from the message; keep the comment), because a printed warning is a command to a weak agent and a bare one invites deleting the durable comment instead.

## Decision

Mechanize the restatement fault exactly as calibrated: a `commit` verb with the message and the staged diff as named files, an advisory verdict, the calibrated boundaries, and a commit-msg hook that stages the diff, detects the verb from the usage banner, and falls back to `--stdin` with the unrun check disclosed. Advocacy and unraised-point answers land as skill text that says no rule enforces it. No precedent detector ships against a measured zero. The host-lint#24 remainder rides the same milestone: the whole-heading ordinal-scaffold rule demotes to the advisory tier, and a declared LEXICON designator escapes it durably, with strict escalation carrying the declaration command as its remedy.

One correction to the convening's working record: the hook dispatch script is host-lint's own file, which host-lifecycle only copies at install, so the milestone is single-component.

## Acceptance and the substitution

The real qwen3.5-4b probes were owed as the acceptance gate. Every channel stayed unreachable through 2026-08-07: the direct endpoint refused, the gateway carried no route to the model, and the MCP host sat on an unreachable subnet, with a persistent watch probing for days. The operator, with that state reported, lifted the hold and directed execution on 2026-08-07: the release ships on the labeled simulation by operator sign-off. The probe prompts and runner are preserved with the milestone record; the probes stay owed and run when a channel exists.

## Consequences

host-lint releases once for the whole milestone, change class `changes-output`, because a heading verdict that blocked yesterday is advisory today. This record is the release's authorization. The advisory tier grows by two forms, both inside the known split where the commit hook treats a warn as advisory while the release gate counts it as a regression; that split is recorded as an open operator decision, not resolved here.

## Discharge of the owed probes (2026-08-08)

The real qwen3.5-4b probes ran once a channel existed: the gateway behind TLS at api.d07yx58.net, served model confirmed in the response body, thinking on at the card's thinking-general sampling per the plan/0076 corrected protocol, by operator direction, because suppressing a small model's reasoning channel tests a weaker agent than the one the design serves. The release was not contingent on this run; what discharges is the obligation this record left owed. Transcripts and the reconciliation live with [plan/0080](../plan/0080-commit-message-faults/README.md).

Measured against the simulation: first preferences agree on three of five questions; Q2 diverges stably toward documentation-file coverage, and with that ballot standing in the convening the settled option still carries 4 to 1; Q1 yields no signal, both orders ranking by presentation position. Neither behavioral prediction reproduced in either draw: the bare warning produced the safe direction, and the revised body carries no precedent residue. Every settled decision stands, and the floor requirements remain as guards, two draws not being grounds to retire a tail risk. This measured record is the weight future convenings give a simulated Fen ballot.

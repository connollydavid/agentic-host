# plan/0087 word-choice lacuna: #27 and #24 verified-closed, the house-diction terms measured

Operator-directed (2026-09-06): "proceed to fix #27 ... consider the full lacuna and consult the cast fully." The lacuna, measured across three exploration passes the same day:

1. **[connollydavid/host-lint#27](https://github.com/connollydavid/host-lint/issues/27) does not reproduce in any form.** `harness` has matched as verbs-only since v0.17.0 (call/0051); both cited spine lines are gone from the renamed manual or survive as nouns; all four sweeps exit 0; zero verb uses exist in any corpus. It sits open only because plan/0082's closing ritual holds the close until after the session's final push.
2. **Its twin [connollydavid/host-lifecycle#24](https://github.com/connollydavid/host-lifecycle/issues/24) carries the identical "verify and close" disposition**, verified by `host-lifecycle --version` and the `.host-software` stanza, both present since v0.50.0.
3. **The substantive gap is call/0051's own deferred question**: the six `house-diction` terms were adopted **without measurement**, the wholesale-adoption anti-pattern call/0051 confesses in its own record. Their reconciliation is "now open" by that decision's words and no corpus has been read since.
4. **The held-out trio** (`framework`/`ecosystem`/`paradigm`) waits on "add one back when a corpus shows the grandiose sense": an invitation with no owner and no corpus read.
5. **The SKILL.md silence**: host-lint's agent-facing SKILL.md never mentions the LEXICON mechanism, while the strict directive's own block message names `host-lint lexicon add` as the remedy, so an agent loading only the skill gets no doctrine and no sanctioned-vocabulary path.

(#25's `.host-lint-allow` ghost is resolved, closed in v0.50.0 with the alias kept inside remap only. #26 was verified and closed by plan/0086.)

## Decision

The cast convenes **fully**, on the call/0050 and plan/0080 pattern: a written briefing; five ranked ballots (Mara, Wren, Bly, Orin, and Fen, the real qwen3.5-4b driven as acceptance test on the plan/0076 corrected protocol, or simulated with the substitution labeled and the real probe owed); each ballot attacks its own first preference before ranking it; the operator breaks ties. The convening settles the dispositions; implementation rides the cascade (host-grammar, then host-lint, then host-lifecycle) only if the ballots settle a grammar change, and the closures follow plan/0082's held-close ritual: nothing closes until every repository the work touched is pushed.

## Build sequence

### The settled conditionals {#gather-data}
- verify: the six `house-diction` terms measured over the swept corpora (occurrence counts and classification each, the call/0051 method); #27's repro re-run as a transcript (`host-lifecycle prose host-template` at exit 0, quoted); #24's verification as a transcript (`--version` and the stanza); the trio's corpus reading taken; the SKILL.md gap documented as the delta to close
- depends: none

### The briefing and the convening {#convening}
- verify: briefing.md written (the issue condensed, the calibration tables, standing constraints, the questions); five ranked ballots with self-objections; Fen's probes run or simulated-labeled; the tally table and settled design recorded in convening.md
- depends: #gather-data

### The settled changes {#implement}
- verify: whatever the ballots settle. A grammar narrowing or retirement rides the cascade with tests and the release discipline; the SKILL.md section lands in host-lint if Q3 settles so; a settled no-change records the measurement as the rule's evidence base, which is itself the deliverable call/0051 deferred
- depends: #convening

### The doctrine {#doctrine}
- verify: VOCABULARY.md's rule entries cite the measurement; call/0051's deferred question is answered on the record; MEMORY.md carries the convening and the measurement
- depends: #implement

### Verify and close {#verify-and-close}
- verify: #27 and #24 closed with their transcripts quoted, after the final push, on plan/0082's ruling; plan/0082's census rows marked done
- depends: #doctrine

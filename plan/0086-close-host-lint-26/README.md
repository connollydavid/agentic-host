# plan/0086 close host-lint#26: the shipped masking fix, verified and closed

Operator-directed (2026-09-06). The defect is already fixed and shipped; what never happened is the verification and closure. This milestone is that closure, on the plan/0082 `close-resolved` pattern: re-run the issue's own repro under the current toolchain, quote the transcript, close after the final push.

## Why

[connollydavid/host-lint#26](https://github.com/connollydavid/host-lint/issues/26) reported that `mask_allowed` blanks a declared LEXICON phrase with spaces, so a phrase at column one left four or more leading spaces, the markdown extractor read them as an indented code block, and every tell on the line was dropped silently. The fix landed through the plan/0082 `lexicon-line-masking` work: the grammar decides markdown block structure before the mask (`e5ac04cb`, "decide markdown block structure before the mask, not after"), released in host-lint v0.19.0 (`ff0516a`, canonical `359b0367`, this host's pinned binary).

The issue is still open because the node's verification step never ran: the session that shipped the fix ended first. Measured 2026-09-06 against the pinned binary, both shapes of the defect are fixed:

- a declared phrase at column one masks **itself alone**; the standalone tells on the same line warn at their own columns;
- the indented shape (a column-one phrase, then a bullet carrying a tell) leaves the bullet's tell standing.

The transcript is recorded at [repro-transcript.txt](repro-transcript.txt), binary identity established by the canonical sha256.

The node's test demand is met in the released source: `prose_lexicon_at_column_one_masks_the_phrase_not_the_line` and its plain-text sibling (`tests/property_tests.rs`), the former citing this issue by name, both green in the suite.

## Decision

No code change. The milestone's work is evidence and closure: close the issue with the transcript quoted, mark plan/0082's census row and `lexicon-line-masking` node done, and record the closure in MEMORY.md. The closing rule from plan/0082 applies unchanged: **the issue is not closed until the session's final push has landed**, because closure is a claim made to everyone with access to the repository.

## Build sequence

### The verification {#verify}
- verify: the repro transcript recorded against the pinned binary with its hash; the two regression tests identified in the released source and green in the suite; the issue's state and comment count noted (open, none)
- depends: none

### The closure {#close}
- verify: connollydavid/host-lint#26 closed with the transcript quoted in the closing comment; plan/0082's census row and `lexicon-line-masking` node updated to done; MEMORY.md records the verification; all of it after the final push
- depends: #verify

# The kani lane concludes (host-lint#32)

**Status: cut 2026-10-20, in build**

## Why

Every host-lint tag run since v0.22.1 died at GitHub's six-hour runner ceiling.
The sharding (`fc580ad`, v0.22.4) bounded each proof to its own job and did not
save the lane: each of the three lem harnesses alone eats the whole ceiling
(`scan_line_never_panics`, `form_and_mangle_hits_are_classified_by_the_table`,
`hits_are_word_bounded`), while the three `verify_*` rungs conclude in moments.
plan/0101's close parks on this lane; the day it greens at a pin, that goal
unparks and completes.

## The measured diagnosis (2026-10-20, stage zero)

One verification condition spans the whole matcher: the tokenizer loop (with
quote state) times the per-word classification times a thirteen-entry canonical
table of string equalities over symbolically-derived words, times the agreement
lookahead: and the harness asserts re-run the same tables on the hit words,
which doubles the surface. The input domains are already tiny (8 to 12 symbolic
bytes); the bound is not the problem. The composition is. Two defects of
coverage also stand: at `n <= 8` the proof never reaches `lemuselves` (ten
bytes), the longest table entry, so the longest forms sit outside today's
stated domain; and no harness declares an unwind bound (the small rungs do).

## The fix design

The properties do not change; their decomposition does.

- Extract the per-word classifier and the word-run tokenizer step from
  `scan_lem_line` into pure functions. Behavior-identical; the conformance
  corpus and the test suite prove it.
- Prove the classification invariants at word level with `n <= 10` (full table
  coverage, one word, no tokenizer, no lookahead): a Form hit is canonical; a
  Mangle hit starts with lem and is neither canonical nor whitelisted; a
  FirstPerson hit is a first-person word.
- Prove word-boundedness against the word-run step alone.
- Prove the line framing (quote state, index arithmetic, the slices) with the
  classifier behind a kani function contract if the pinned kani carries them cleanly;
  otherwise with per-property splits at reduced length. Either way every
  harness carries `#[kani::unwind(K)]`.
- The CI matrix grows one row per harness; each job must conclude with margin
  (minutes locally, not hours).

A proof that never finishes discharges nothing (the kani-conformance doctrine);
the fallback of last resort is a property reformulation, and that is a ruling
this room asks for, never one it takes.

## Release shape

Change-class `neither` (v0.23.1): the restructure moves no flag semantics.
Authorized by this room. The moment of truth is the tag run itself concluding
inside the ceiling.

The `upstream-drift` job is `continue-on-error` and never gated the lane; the
ffmpeg corpus acknowledgment it names stays a follow-on, not this room's work.

## Build sequence

### Diagnose {#diagnose}

- verify: the three heavy harnesses timed locally under a cap, the timings and the fix-class diagnosis recorded in bench/
- inputs: software/host-lint/main/src/lib.rs

### Decompose the proofs {#decompose}

- verify: every harness SUCCESSFUL through host-prove with a stated unwind bound, each in minutes locally; cargo test green; the conformance lane green; the property set unchanged
- depends: #diagnose
- inputs: software/host-lint/main/src/lib.rs, software/host-lint/main/.github/workflows/ci.yml, software/host-lint/main/host-lint.obligations

### Release v0.23.1 {#release}

- verify: the tool-carried sequence green at the tag, and the tag run concludes inside the ceiling
- depends: #decompose

### Re-pin and receipt {#re-pin}

- verify: software --check green with the lint lane discharged at the new pin
- depends: #release

### Unpark and close plan/0101 {#close-0101}

- verify: goal complete banks the closure receipt, GOAL.md returns to the no-goal state, and the operator's accept rides the record
- depends: #re-pin

### Records {#records}

- verify: the PLAN.md row complete, a MEMORY.md entry, host-lint#32 closed with the fix comment, the tree pushed
- depends: #close-0101

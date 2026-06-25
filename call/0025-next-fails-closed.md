# next fails closed on a directory with no numbered entries

- Status: accepted
- Date: 2026-06-25
- Scope: host-lifecycle (the `next` subcommand: the fail-closed exit and the
  did-you-mean room suggestion). The software change of `plan/0041`.
- Relates: `plan/0041` (which carries the operator ruling and the Qwen-3.5-4B
  ergonomics data); `connollydavid/host-lifecycle#1` (the footgun this closes);
  `plan/0039` (whose migration surfaced it).

## Context and Problem Statement

`host-lifecycle next <dir>` printed the next free `NNNN` number as the maximum of a
directory's numbered entries plus one, and fell back to `0000` when a directory had
none. So `next .` (the host root), a typo'd path, or any non-room path returned a
plausible `0000`, and an agent could go on to create a colliding `0000-slug` in the
wrong place. At the weak-agent bar a garbled argument returned a wrong answer rather
than an error.

## Decision

`next` fails closed. A path that is not a directory, and a directory with no
`NNNN-slug` entries (the host root, a typo, a non-room path, or a freshly created
empty room), exit non-zero (code `2`, the code the tool already returns for its
sibling path and argument errors) rather than printing `0000`. The error names the
likely fix. When the parent holds a known room with entries, the message carries a
did-you-mean line with the exact command (`host-lifecycle next plan`); otherwise it
points at a room and states that a room's first entry is `0000`. The suggestion is
drawn only from the known rooms, so a generated or build directory is never
suggested.

The fresh-empty-room case folds into fail-closed rather than a special case, because
a room gains a first entry quickly and fail-safe beats fail-unsafe. The Qwen-3.5-4B
ergonomics check confirmed the form: the weak agent recovered the intended room from
the diagnostic, and recognized the empty room as a first-entry case without a
dedicated affordance (`plan/0041`).

## Considered Options

1. **Keep the `0000` fallback.** Rejected: it is the footgun.
2. **Add a `--first` flag for the empty-room case.** Deferred: the ergonomics data
   showed the agent recovers unaided, so the affordance is unwarranted now.
3. **Fail closed with a did-you-mean drawn from the known rooms (chosen).**
   Fail-safe, and the suggestion is the form the weak agent recovered from most
   reliably.

## Consequences

- Good: a garbled or misdirected `next` is a loud error rather than a silent wrong
  number, so a colliding `0000-slug` cannot be created by mistake; the suggestion
  names a real room only.
- Costs: a freshly scaffolded empty room now errors on its first `next`; the blast
  radius is small (the change is local to `next`), and the message states the
  first-entry number.

## Confirmation

A unit test covers a populated room (the maximum plus one, unchanged), an empty
directory, a missing path, and the host root (each non-zero). `cargo test` is green
(`101` tests) and `cargo clippy` is clean. The released binary gates green, and
`software --check` and `software --verify-build` reproduce the artifact.

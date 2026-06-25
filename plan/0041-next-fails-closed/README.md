# plan/0041: next fails closed

Make `host-lifecycle next <dir>` fail closed when it is pointed at a directory
with no numbered entries, instead of silently yielding `0000`. Closes
connollydavid/host-lifecycle#1, the footgun surfaced during plan/0039.

## Problem

`host-lifecycle next <dir>` prints the next free `NNNN-slug` number as the maximum
of the directory's numbered entries plus one, and falls back to `0000` when there
are no numbered entries. So `next .` (the host root), a typo'd path, or any
non-room path silently yields a valid-looking `0000`, and an agent can go on to
create a colliding `0000-slug` in the wrong place. The repro is exact:

```
host-lifecycle next plan  ->  0040   # correct
host-lifecycle next call  ->  0024   # correct
host-lifecycle next .     ->  0000   # the host root has no numbered entries
```

At the weak-agent bar this is fail-unsafe: a garbled argument returns a plausible
wrong answer rather than an error.

## Decision (operator, this session)

`next` **fails closed**. A directory with no `NNNN-slug` entries (the host root, a
typo, a non-room path, or a freshly-scaffolded empty room) exits non-zero rather
than printing `0000`. The fresh-empty-room case is folded into fail-closed rather
than special-cased, because rooms gain a first entry quickly (the worked-example
`call/0000`, the first milestone) and fail-safe beats fail-unsafe.

The exact failure form (a usage message versus a distinct error message, the exit
code, and whether a did-you-mean hint helps) is settled by a **Qwen-3.5-4B
ergonomics check**: the form the weak agent recovers from correctly (re-points at
a real room, or recognizes the first-entry case and proceeds with an explicit
number) is the one shipped. If the data shows the empty-room path needs a hand, an
explicit affordance is added then, not pre-emptively.

## The change (host-lifecycle)

- `next` distinguishes a missing or non-directory path from an existing directory
  with no numbered entries, and exits non-zero in both, with a message that names
  the likely fix (point at a room such as `plan/` or `call/`). The precise wording
  and exit code follow the 4B check.
- A unit test covers: a populated room returns the maximum plus one (unchanged);
  an empty existing directory exits non-zero; a missing path exits non-zero; the
  host root exits non-zero.

## Build sequence

1. Gather Qwen-3.5-4B data on the failure UX. Show the 4B the footgun and the
   candidate failure forms (usage to stderr with a non-zero exit; a distinct error
   message; with and without the did-you-mean hint), and record which form it
   recovers from. Verify: a recorded data note naming the chosen form.
2. Implement the fail-closed `next` with the chosen form and the unit test.
   Verify: the test passes; `next .` exits non-zero; `next plan` still prints the
   correct next number.
3. Record a small `call/` decision (fail-closed `next`, the 4B-validated form).
   Verify: `host-lifecycle validate call/` reports ok.
4. Release host-lifecycle (`--change-class neither`, a patch bump), re-pin
   `.host-software`, record the receipt, and bump the CI install pins. Verify: the
   released binary gates green; `software --check` and `--verify-build` clean;
   whole-suite CI green.
5. Close connollydavid/host-lifecycle#1. Verify: the issue is closed with the
   release reference.

## Risks

- A freshly-scaffolded empty room now errors. If that path is more common than
  assumed, the 4B data surfaces it and an explicit affordance (a clear
  create-the-first-entry message, or a `--first` flag) is added. The blast radius
  is low: the change is localized to the `next` function.

## Status

Open, ready to build. Operator ruling recorded (fail closed; the form by 4B data).
Independent of plan/0040.

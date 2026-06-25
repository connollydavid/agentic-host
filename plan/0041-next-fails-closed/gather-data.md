# plan/0041 gather: the next failure form, set by Qwen-3.5-4B

The fail-closed `next` error form is the one a weak agent recovers from. A recorded
Qwen-3.5-4B (Fen) run settled it, the bar the methodology applies to ergonomics.

## How the run was reached

The rope HTTPS front-end rejected the host-only bearer (the token had rotated), so
the run went through the pal front-end to the same `qwen3.5-4b` backend. pal frames
a scenario as user content rather than a true system message, a weaker framing than
rope. The result held on a clean re-run, so the weaker framing did not change it.

## What Fen was shown

Two recovery scenarios. The first ran `next .` (the repository root) meaning to run
`next plan`, and saw each candidate form:

```host-lint:ignore
Form A — terse usage, exit 2, stderr:
    host-lifecycle next <dir>

Form B — diagnostic error, exit 1, stderr:
    host-lifecycle: '.' has no numbered (NNNN-slug) entries; point `next` at a room such as plan/ or call/

Form C — diagnostic error and a suggestion, exit 1, stderr:
    host-lifecycle: '.' has no numbered (NNNN-slug) entries
    did you mean a room? try: host-lifecycle next plan
```

The second ran `next call` against a freshly created, empty `call/` room, to test
whether the error blocks an agent on a genuine first entry.

## What Fen did

For the wrong-path scenario, Fen produced the correct recovery command for every
form. It judged the form with a suggestion line the most reliable, because the line
carries the exact command and removes the step of constructing it; the terse usage
form was the weakest. The exit value did not gate recovery: Fen recovered at every
code shown, and its stated preference for a `1` rested on reading a `2` as
non-standard, which a usage error does not warrant.

For the empty-room scenario, Fen recognized `call/` as the intended room and the
case as its first entry, and named the first filename `call/0000-...` rather than
treating the empty room as a dead end. So the fresh-empty-room case needs no special
affordance.

## The chosen form

A distinct diagnostic error that names the likely fix and carries a did-you-mean
line with an exact command:

```host-lint:ignore
host-lifecycle: '.' has no numbered (NNNN-slug) entries
did you mean a room? try: host-lifecycle next plan
```

It exits non-zero with `2`, the code the tool already returns for its sibling path
and argument errors (a missing argument, a non-directory), so one convention holds
across the tool. The empty-room path stays folded into fail-closed, with no `--first`
flag, because the agent recovers from it unaided.

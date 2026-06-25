# plan/0043 code review: the `[entrance]` stanza implementation

Three independent adversarial reviewers read the uncommitted `#implement-entrance` diff (the
`[entrance]` stanza in `parse_project_facts`, the routed `entrance` check, the document
resolution, the legacy shim) against the milestone, the design review, and `call/0027`. One
read for parser correctness and edge cases, one for the reconcile coupling and regressions,
one for fail-safe behavior and the exit codes. They converged on two blocking defects and a
cluster of parser holes, all of which shipped green because no test exercised them. The
verdict was fix-first; the fixes are below, and the suite now covers each.

## The blocking defects

### The `problems` guard reached only one consumer

The `[entrance]` value form is parsed once, and the same parse sets the entrance member apart
from `components`, the set reconcile holds `STRUCTURE.md` to. A malformed stanza (a typo in
`member`) recorded a `problems` entry but still computed `components` by excluding the typo'd
name, so the real front door stayed in `components`. The `entrance` command surfaced
`problems`; reconcile did not, so it took the corrupted set and would demand `STRUCTURE.md`
name the front door a component, the exact `call/0027` silent demotion, relocated to a
different consumer. The integrity reviewer proved it from a one-character typo; the correctness
and fail-safe reviewers reached the same seam.

Fix: reconcile now surfaces `facts.problems` and exits before it trusts `components`, so a
malformed stanza is loud in every consumer. (`software --check` was confirmed never to read
`ProjectFacts`, so the seam was reconcile alone.)

### An empty `restates` value checked nothing and reported clean

`restates =` with an empty value missed the `true` sentinel arm and parsed to an empty concept
set, which `checks` answers false for every concept. The entrance check then ran nothing and
printed clean, a fail-open inversion of the milestone's fail-safe stance. All three reviewers
found it.

Fix: an empty `restates` value is now a problem (exit `2`), the same as an unknown concept.

## The parser holes

- **A sub-named `[entrance "x"]` was silently ignored.** The match was on the literal
  `[entrance]`, so the self-documenting form the Fen runs leaned toward dropped to no entrance
  with no problem. Now it parses and flags the wrong form.
- **`document` could escape the worktree.** A `..` or absolute `document` resolved outside the
  member's worktree, and write mode could rewrite an external file. Now an escaping `document`
  is a problem.
- **The `true` sentinel was case-sensitive.** A legacy `entrance = True` did not match, so the
  member silently lost its entrance status and fell into `components`, a `call/0027`-class
  demotion over a capital letter. The legacy marker and the `restates` sentinel are both
  case-insensitive now.
- **A duplicate `member` key last-wrote silently.** A repeated `member` in one stanza is now a
  problem.

## The exit-code framing

The review found that the exit-code comment this milestone folds in contradicted the code it
sits beside: it claimed an expected logic error exits `2`, while a `--check` drift, the most
expected logic outcome, exits `1`, as it does across the tool's many check sites. The codebase
convention is the standard one and was kept: `0` clean, `1` the red outcome a command surfaces
(a drift, a HAZARD, a failed gate), `2` a command that cannot proceed on its input (a missing,
unreadable, or malformed input the user named; `next` on a numberless directory). The comment,
`gather-data.md`, and the build-sequence task are corrected to that wording rather than the
code changed across the tool.

## A noted boundary, not a defect

A reviewer observed that a partial entrance (a `restates` subset) declared on a real component
member would exclude that member from `components`. The entrance is the single set-apart entry
point by design (a non-component member: the front door, or a standalone document with its own
member), so this is a misuse outside the model rather than a code defect. The boundary is
recorded; a document inside a tool component is not the singleton entrance.

## Verdict

Ship, after the fixes. The two blocking defects are closed and covered by tests, the parser
holes are loud rather than silent, and the exit-code wording matches the tool. `cargo test` is
green and `cargo clippy` is clean; reconcile exits `2` on a typo'd member and the entrance
exits `2` on an empty `restates`, both verified on the built binary.

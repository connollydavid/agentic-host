# call/0056: a tool dependency is a floor, checked in the lane

- Status: accepted
- Scope: how a skill or a reference workflow declares its dependency on a `host-*` binary; where that binary is resolved from; when and against what the declared floor is verified; the version policy while the tools are pre-1.0
- Date: 2026-08-10

## Context and problem

Three observations arrived together, and they are one problem.

**The declaration already exists; nothing enforces it.** `host-template/UPGRADING.md` carries a
`requires = host-lifecycle vX.Y.Z` field on its ledger entries, and states repeatedly that an
adopter should bump the pinned tool before moving the pointer. The `RENAME-repro-waiver` entry was
applied with the lane running v0.35.1, which parses only `repro-exempt`, so it read an exempt
component as DRIFT. `upgrade --record` ran the entry's verify and it passed, because the verify ran
under a different binary than the lane did. A floor that is never checked against the binary
actually in the lane is not a floor; it is a comment.

**The template acquires the tool three ways.** `site.yml` and `reproducible-build.yml` build the
`tools/host-lifecycle` submodule; `prose.yml` runs `cargo install --git … --rev <inline>`. Three
mechanisms means three places a version can be stated, so skew is available by construction.
[call/0038](0038-releasing-a-tool-updates-the-template-pin.md) and the `software --check` gate do catch the
resulting drift for the template itself, and did so in this session. An **adopter** is left
uncovered: a project instantiated from the template has no `.host-software` stanza over `tools/`,
so nothing gates its wired-once tool pointer. The protection stops exactly where the population is
largest.

**Skills currently declare nothing.** A sweep of `.claude/skills/` finds no version string, no rev,
no requires clause. So this is a choice about what to build rather than a migration away from
something, and the cheap wrong answer is available: let each skill pin what it was written against.
That would re-mint the anchor once per skill and reproduce the workflow skew at greater scale.

## Decision

A skill declares a **floor**, not a pin, and the floor is verified **in the lane, at invocation,
against the binary about to run**.

1. **One anchor.** Which binary runs is resolved from `.host-software` and nowhere else. A skill
   does not pin a revision, and neither does a reference workflow; the three acquisition
   mechanisms collapse to one resolution.
2. **A floor is a capability claim.** A skill declares `requires: host-lifecycle >= X.Y.Z`, where
   the version named is the one the capability it uses first appeared in. It is a floor because a
   consumer needs a behaviour to be present, not to be exact.
3. **Checked where it is used.** The lane probes the resolved binary's version immediately before
   invoking it and compares it to the declared floor. A floor established at record time by one
   binary and relied on at run time by another is not established at all, which is the whole
   lesson of the `RENAME-repro-waiver` misread.
4. **Floor only, while the tools are 0.x.** Semver permits a 0.x minor to break, so the strict
   reading would demand `>=0.50, <0.51`. It is refused: a speculative upper bound forces churn at
   every minor and produces false failures far more often than it prevents a real incompatibility.
   The floor rises when something actually breaks. An upper bound is added only for a **known and
   recorded** incompatibility, and adding one requires a `call/`.
5. **An undeterminable version refuses.** When the lane cannot read a version, it says so and does
   not run the dependent checks. It never assumes the floor holds. This is the same floor
   [call/0055](0055-upstream-artefacts-are-referenced-not-embedded.md) sets for an unresolvable
   artefact and [call/0054](0054-one-commit-message-fault-earns-a-detector.md) sets for a degraded
   path: a silent pass on something that was not verified is the failure mode, not the safe default.

## Consequences

Every lane gains a version probe it did not have, which is the cost, and it is small next to the
failure it removes. The failure is specific and was observed: a check reporting green while running
a binary that could not evaluate what it claimed to have checked.

Adopters gain coverage they never had. Because the floor travels with the skill rather than with
the host's recipe, a project instantiated from the template carries its own requirement and can
verify it without a `.host-software` stanza naming the tool. That is the gap this decision exists
to close, and it is why the rule is written for skills and workflows generally rather than for this
repository's Where room.

This does not retire call/0038 or the `software --check` tool-pin HAZARDs. Those answer whether the
*recorded* pins agree, and they keep answering it. The floor answers whether the binary *in hand*
can do the job. A clean pin check still says nothing about the binary a lane
actually loaded, which is the distinction the four Where-room commands already draw and which this
decision extends to the tools themselves.

The `requires` field in `UPGRADING.md` is not new syntax to invent; it is an existing declaration
that becomes enforced. Its ledger entries keep their current wording.

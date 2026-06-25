# plan/0043: the entrance check (a reusable standalone-document check)

The front-door check (plan/0040, host-lifecycle v0.27.0) holds the one published
entrance of agentic-host to the spine. The same problem recurs wherever a project keeps a
self-contained document that restates the methodology and cannot link to it: an
adopter-authored standalone `SKILL.md`, or any project's operator-and-agent landing
page. This milestone is the whole effort: it generalizes the check into an opt-in,
reusable capability, builds the declaration and concept machinery the generalization
needs, and reconciles the spine flag the standalone rename left diverged. It supersedes
the agentic-host-local scope set in plan/0040.

## Problem

A self-contained document is read out of context (a single-file entry point, a skill
loaded on its own), so it cannot point at a canonical definition with a link the way an
in-host doc does (the reconcile arm). It restates, and the restatement stales silently
when the spine moves. plan/0040 solved this for one document, hardwired: the tool finds
the `.host-software` member marked `entrance = true` and checks its README against the
manifest phases, the `.host-software` tools, and the `.host` stamp format. Nothing lets
another project, or another document, opt in.

Two facts the pre-generalization audit and the design review surfaced shape the work:

- **The marker is a spine concept.** host-template (`CLAUDE.md`, `UPGRADING.md`) documents
  the marker as the adopter-facing way reconcile sets a single-file front door apart from
  `components`. The standalone rename (`call/0027`) moved the tool to `entrance = true`
  and left the spine on `front-door = true`, a divergence the deprecation shim absorbs.
  The generalization owes the spine reconciliation.
- **The marker is shared by two checks through one predicate.** `parse_project_facts`
  marks a member the entrance only when the value is exactly `true`, and the complement
  (members minus the entrance) is the `components` set reconcile holds `STRUCTURE.md` to.
  So a richer value form has to be designed carefully, or it un-marks the front door and
  re-demotes it into `components`. The design below closes that seam by construction.

## Decision (operator)

plan/0043 expands to encompass every aspect of the entrance work, rather than narrowing
to the spine reconciliation the design review recommended. The review's blocking findings
become requirements the design meets, not reasons to defer. In particular the
marker-break is designed out at the parse layer, so it is an implementation concern the
good design closes, never a milestone the work waits on. The standalone sibling framing
(reconcile holds linkable docs honest with pointers; entrance holds self-contained docs
honest with coverage and generation, because they cannot link) stands. The name `entrance`
stands, settled by the Qwen-3.5-4B run in `gather-data.md`.

## The design

### The entrance marker, one parsed primitive

A member is the entrance when the `entrance` key is present with a non-empty value. The
value is parsed once into a concept set: `true` (the full set, the front-door case) or a
list of concept names (a subset). The legacy `front-door = true` is accepted as the full
set by the deprecation shim until the shim retires. A member stays set apart whatever its
value form, so `parse_project_facts` keys on presence, never on `== "true"`, and the value
can never demote the front door into reconcile's `components`. `facts.entrance` and
`facts.components` are derived from the same single primitive, and a regression test pins
both for the value form so the seam cannot reopen silently.

### The declaration form

The marker and the concepts ride one member-level value: `entrance = phases tools` on the
existing `[software]` member, or `entrance = true` for a document that restates every
concept. The Qwen-3.5-4B runs (`gather-data.md`) chose a member-level value over a boolean
plus a separate restates line (read as ambiguous and redundant) and over a dedicated
stanza (which splits the declaration off the member that already carries `url` and `pin`).
The runs also flagged that a bare single value reads cryptic, so the form carries two
guards: `true` is the sentinel for the restates-everything case, so a full front door
never types an enumeration, and the concept names are a closed vocabulary the tool
validates at parse time, so an unknown concept is a loud error rather than a silently
ignored word.

### The concept set, checked against its homes

The declared concepts select what the check holds, each against the structured home it
already reads: the lifecycle phases against the manifest, the wired tools against the
`.host-software` drivers, the `.host` stamp against the tool's canonical format, and the
other `.host-software` concepts reconcile already names (`components`, `verifiers`,
`software-root`, `spec-home`). The check holds the document complete against the declared
set only, so a front door declaring `true` is held to every concept and a partial entrance
is held to its subset. The concept vocabulary is the reconcile vocabulary plus the phases
and the stamp, named once, so an adopter learns one set of words, not a second overlapping
one.

### The honest scope

The entrance check holds any document that restates a concept with a structured home. A
document that restates only home-less teaching doctrine (a disposition rule, the
conditional-lane MUST) declares no checkable concept, and the per-document declaration says
so plainly. This is plan/0040's settled principle carried forward: a fact is drift-proof
through the tool only when the tool reads its home, and the milestone says so rather than
claiming a coverage it cannot deliver. The generality earns itself as real entrances that
restate home-backed concepts appear; the machinery is built now so they can opt in.

### The routing rule

Generate what is naturally a format or data block (the `.host` stamp), coverage-check what
is naturally prose (a phase name, a tool name), and never put a generation marker in
teaching prose (plan/0039). The declaration stays out of the document, in the
`.host-software` value, so the document reads clean.

### The reconcile relationship

`entrance` stays a separate subcommand, the sibling of `reconcile`, settled by plan/0040
and confirmed by the review. reconcile resolves links and checks anchors over tracked
markdown; entrance reads a materialized README, covers the manifest phases, and generates
the stamp byte-exact. They share only the parsed marker primitive, kept a single tested
source so a change to the marker serves both consumers at once.

### The spine reconciliation

The spine moves to the new spelling before the shim retires, so the spine never teaches a
spelling the tool rejects. host-template renames `front-door = true` to `entrance = true`
in `CLAUDE.md` and `UPGRADING.md` and documents the value form, and ships an adopter
`UPGRADING` ledger entry for the rename whose verify post-condition holds `entrance --check`
and `reconcile` and `software --check` green, so a misapplied rename shows loudly at apply
time. The deprecation shim then retires with a hard fail on a surviving `front-door = true`,
gated on a clean `front-door` grep over host-template. The exit-code convention comment
(exit `1` an unexpected fault, exit `2` an expected logic error), validated in
`gather-data.md`, folds into the same release.

## Build sequence

The build sequence as a task graph (plan/0042), each entry an anchored task carrying a
receipt. The chain is mostly linear; the spine rename precedes the shim retirement so no
state is half-renamed.

### Settle the open decisions by review {#settle-open-decisions}

Settle the declaration form, the concept-set model, the reconcile relationship, and the
spine reconciliation by adversarial review, recorded in `design-review.md` with the
operator re-cut that expands the milestone and designs out the marker-break.

- verify: attested operator

### Rename the spine flag and add the doctrine {#spine-rename-and-doctrine}

Rename `front-door = true` to `entrance = true` in `host-template/CLAUDE.md` and
`host-template/UPGRADING.md`, document the concept-list value form, add the entrance
doctrine (an entrance is a declared self-contained document held to the spine, the
standalone sibling of reconcile), and add the adopter `UPGRADING` ledger entry for the
rename whose verify post-condition holds `entrance --check`, `reconcile`, and
`software --check`. host-template prose stays clean.

- depends: #settle-open-decisions
- verify: attested operator

### Implement the entrance generalization {#implement-entrance}

Implement the presence-keyed marker primitive with the `true` sentinel and the closed
concept vocabulary, parse the value into the concept set, route the declared set through
the check (each concept against its home), retire the deprecation shim with a hard fail on
a surviving `front-door = true` gated on a clean host-template `front-door` grep, and fold
in the exit-code convention comment. Regression tests pin `facts.entrance` and
`facts.components` for the value form, the unknown-concept parse error, and the routed
subset.

- depends: #spine-rename-and-doctrine
- verify: cd software/host-lifecycle/main && cargo test

### Validate at the weak-agent bar {#validate-4b}

Validate the declaration ergonomics and an entrance use case (a member that declares a
concept subset) with a recorded Qwen-3.5-4B run that confirms the `gather-data.md` leaning
and the sentinel-and-vocabulary guards.

- depends: #implement-entrance
- verify: attested operator

### Release, adopt, and re-pin {#release-and-re-pin}

Release host-lifecycle, bump the host-template pointer and adopt the revision, re-pin
`.host-software`, record the receipts and a `call/` decision that supersedes the scope of
`call/0026` and `call/0027`, and bump the CI install pins. The released binary gates green
and the whole suite is green.

- depends: #validate-4b
- verify: attested operator

## Risks

- The milestone touches the spine, the tool, and the agentic-host adoption at once. The
  spine rename precedes the shim retirement, and the marker primitive lands with its
  regression test, so no state is half-renamed and the value form cannot reopen the
  demotion seam.
- The declaration adds a surface every adopter could meet, so its form stays simple: one
  member-level value, a `true` sentinel, a closed vocabulary, validated loudly.
- The generality is built ahead of a second real entrance. The honest scope keeps the
  claim true to what the tool reads, so the machinery is ready without over-claiming a
  coverage it cannot yet exercise.

## Status

Open, in build. The adversarial review (three independent reviewers, `design-review.md`)
returned a re-scope verdict; the operator re-cut it to expand the milestone to encompass
every aspect, with the review's blocking findings folded in as design requirements (the
marker-break designed out at the parse layer, the concept set wired, the scope stated
honestly, the spine reconciliation landed inside the milestone). Operator decisions
recorded: opt-in and reusable; the name `entrance` by Qwen-3.5-4B data; the standalone
sibling of reconcile; the member-level declaration form with a `true` sentinel and a closed
vocabulary. Supersedes the agentic-host-local scope of plan/0040 and the scope half of
`call/0026`, and carries the rename and migration of `call/0027` to completion.

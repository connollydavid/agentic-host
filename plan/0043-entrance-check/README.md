# plan/0043: the entrance check (a reusable standalone-document check)

The front-door check (plan/0040, host-lifecycle v0.27.0) holds the one published
entrance of agentic-host to the spine. The same problem recurs wherever a project keeps a
self-contained document that restates the methodology and cannot link to it: an
adopter-authored standalone `SKILL.md`, or any project's operator-and-agent landing
page. This milestone is the whole effort: it generalizes the check into an opt-in,
reusable capability declared by a single `[entrance]` stanza, builds the document and
concept machinery the generalization needs, and reconciles the spine flag the standalone
rename left diverged. It supersedes the agentic-host-local scope set in plan/0040.

## Problem

A self-contained document is read out of context (a single-file entry point, a skill
loaded on its own), so it cannot point at a canonical definition with a link the way an
in-host doc does (the reconcile arm). It restates, and the restatement stales silently
when the spine moves. plan/0040 solved this for one document, hardwired: the tool finds
the `.host-software` member marked `entrance = true` and checks its `README.md` against the
manifest phases, the `.host-software` tools, and the `.host` stamp format. Nothing lets
another document, or another project, opt in, and the marker is wired to a member's
`README.md` by filename, so a differently-named document cannot be pointed at.

Two facts the pre-generalization audit and the design review surfaced shape the work:

- **The marker is a spine concept.** host-template (`CLAUDE.md`, `UPGRADING.md`) documents
  the marker as the adopter-facing way reconcile sets a single-file front door apart from
  `components`. The standalone rename (`call/0027`) moved the tool to `entrance = true`
  and left the spine on `front-door = true`, a divergence the deprecation shim absorbs.
  The generalization owes the spine reconciliation.
- **The per-member marker was overloaded.** When the marker was a per-member value, the
  same predicate set the entrance and defined `components` (members minus the entrance), so
  a richer value form could un-mark the front door and re-demote it into `components`. The
  declaration below moves the marker to its own stanza, which names the member outright, so
  that overload dissolves by construction.

## Decision (operator)

plan/0043 expands to encompass every aspect of the entrance work, rather than narrowing to
the spine reconciliation the design review recommended. The review's blocking findings
become requirements the design meets, not reasons to defer. The declaration is a single
`[entrance]` stanza, a global singleton among the `.host-software` members, so one entrance
reaches any document by path while the marker-break is designed out at the parse layer. The
standalone sibling framing (reconcile holds linkable docs honest with pointers; entrance
holds self-contained docs honest with coverage and generation, because they cannot link)
stands. The name `entrance` stands, settled by the Qwen-3.5-4B run in `gather-data.md`.

## The design

### The declaration: a singleton `[entrance]` stanza

A project declares its entrance in one `[entrance]` stanza in `.host-software`, a global
singleton among the member stanzas (a second stanza is a loud error). It names the member
the entrance belongs to, the document within that member's worktree, and the concepts the
document keeps complete:

```
[entrance]
    member   = host
    document = README.md
    restates = phases tools
```

`document` defaults to `README.md` and reaches any file in the member's worktree, so a
`SKILL.md` or a landing page is declared by path rather than excluded by a hardwired
filename. `restates = true` keeps the document complete against every concept (the
front-door case), so a full front door never types an enumeration; a concept list keeps it
complete against that subset. The concept names are a closed vocabulary the tool validates
at parse time, so an unknown concept is a loud error rather than a silently ignored word.

The named `member` is set apart from `components`, the one member singled out among the
rest, exactly as the front door is today, so reconcile holds the component set to the
others. Because the stanza names the member outright, there is no per-member value to
misparse, and no value form can demote the entrance into the component set: the marker-break
the review found dissolves. The Qwen-3.5-4B runs (`gather-data.md`) leaned to a member-level
value for the member-and-README case and to a self-documenting `[entrance "…"]` stanza for
clarity; the full-reach requirement (a document path the member flag cannot carry) and the
singleton constraint settle the form on the dedicated stanza.

### The migration

The legacy per-member marker, both `front-door = true` and the `entrance = true` that
agentic-host adopted in `call/0027`, is accepted by the deprecation shim as the front-door
entrance during the transition, mapped to the equivalent stanza. The shim warns and names
the stanza form. Its retirement (a hard fail on a surviving per-member marker) stays the
named follow-up the deprecate-then-retire path already owes, a release after the spine and
agentic-host move to the stanza.

### The concept set, checked against its homes

The `restates` concepts select what the check holds, each against the structured home it
already reads: the lifecycle phases against the manifest, the wired tools against the
`.host-software` drivers, the `.host` stamp against the tool's canonical format, and the
other `.host-software` concepts reconcile already names (`components`, `verifiers`,
`software-root`, `spec-home`). The check holds the document complete against the declared
set only, so a front door declaring `true` is held to every concept and a partial entrance
is held to its subset. The concept vocabulary is the reconcile vocabulary plus the phases
and the stamp, named once, so an adopter learns one set of words.

### The honest scope

The entrance check holds any document that restates a concept with a structured home. A
document that restates only home-less teaching doctrine (a disposition rule, the
conditional-lane MUST) declares no checkable concept, and its `restates` set says so plainly.
This is plan/0040's settled principle carried forward: a fact is drift-proof through the
tool only when the tool reads its home, and the milestone says so rather than claiming a
coverage it cannot deliver. The generality earns itself as real entrances that restate
home-backed concepts appear; the machinery is built now so they can opt in.

### The routing rule

Generate what is naturally a format or data block (the `.host` stamp), coverage-check what
is naturally prose (a phase name, a tool name), and never put a generation marker in
teaching prose (plan/0039). The declaration stays out of the document, in the `[entrance]`
stanza, so the document reads clean.

### The reconcile relationship

`entrance` stays a separate subcommand, the sibling of `reconcile`, settled by plan/0040
and confirmed by the review. reconcile resolves links and checks anchors over tracked
markdown; entrance reads a materialized document, covers the manifest phases, and generates
the stamp byte-exact. They share only the parsed `[entrance]` stanza (the entrance and the
set-apart member), kept a single tested source so a change serves both consumers at once.

### The spine reconciliation

host-template replaces the `front-door = true` prose with the `[entrance]` stanza in
`CLAUDE.md` and `UPGRADING.md`, documents the stanza and its `document` and `restates`
fields, and ships an adopter `UPGRADING` ledger entry that migrates a legacy per-member
marker to the stanza, whose verify post-condition holds `entrance --check`, `reconcile`, and
`software --check` green so a misapplied migration shows loudly at apply time. The exit-code
convention comment (exit `1` for the issues a command finds, exit `2` when it cannot proceed
on its input), refined by the code review in `code-review.md`, folds into the same release.

## Build sequence

The build sequence as a task graph (plan/0042), each entry an anchored task carrying a
receipt. The tool gains the stanza first, then the spine documents it, then agentic-host
moves to it, so no state is half-migrated.

### Settle the open decisions by review {#settle-open-decisions}

Settle the declaration form, the concept-set model, the reconcile relationship, and the
spine reconciliation by adversarial review, recorded in `design-review.md` with the operator
re-cut that expands the milestone, designs out the marker-break with the `[entrance]` stanza,
and reaches any document by path under a global-singleton constraint.

- verify: attested operator

### Implement the entrance generalization {#implement-entrance}

Parse the singleton `[entrance]` stanza (one per project, the member, the `document` path
defaulting to `README.md`, the `restates` concept set with a `true` sentinel and a closed
vocabulary), resolve the document within the member's worktree, route the declared concepts
through the check against their homes, set the named member apart from `components`, accept
the legacy per-member marker by the shim, and fold in the exit-code convention comment.
Regression tests pin the new parse: the stanza yields the entrance member and keeps it out
of `components`, the document path resolves within the worktree, and a declared subset checks
only its concepts. A second `[entrance]` stanza fails loudly, and so does an unknown concept
name.

- depends: #settle-open-decisions
- verify: cd software/host-lifecycle/main && cargo test

### Add the spine doctrine and the ledger entry {#spine-doctrine}

Replace the `front-door = true` prose in host-template (`CLAUDE.md` and `UPGRADING.md`) with
the `[entrance]` stanza, document its `document` and `restates` fields, add the entrance
doctrine (an entrance is a declared self-contained document held to the spine, the standalone
sibling of reconcile), and add the adopter `UPGRADING` ledger entry that migrates a legacy
per-member marker to the stanza, whose verify post-condition holds `entrance --check`,
`reconcile`, and `software --check`. host-template prose stays clean.

- depends: #implement-entrance
- verify: attested operator

### Move agentic-host to the stanza {#migrate-agentic-host}

Migrate agentic-host's `.host-software` from `entrance = true` to the `[entrance]` stanza,
adopt the host-template revision, and confirm `entrance --check`, `reconcile`, and
`software --check` stay green on the new declaration.

- depends: #spine-doctrine
- verify: attested operator

### Validate at the weak-agent bar {#validate-4b}

Validate the stanza ergonomics and an entrance use case (a member that declares a concept
subset and a non-README document) with a recorded Qwen-3.5-4B run that confirms the
singleton, the `document` path, and the sentinel-and-vocabulary guards.

- depends: #migrate-agentic-host
- verify: attested operator

### Release, re-pin, and record {#release-and-re-pin}

Release host-lifecycle, bump the host-template pointer, re-pin `.host-software`, record the
receipts and a `call/` decision that supersedes the scope of `call/0026` and carries
`call/0027` to completion, and bump the CI install pins. The released binary gates green and
the whole suite is green.

- depends: #validate-4b
- verify: attested operator

## Risks

- The milestone touches the spine, the tool, and the agentic-host declaration at once. The
  tool gains the stanza before the spine documents it and agentic-host moves to it, and the
  shim accepts the legacy marker throughout, so no state is half-migrated.
- The declaration adds a surface every adopter could meet, so it stays one stanza: a member,
  a document path, a closed concept set with a `true` sentinel, validated loudly, a single
  entrance per project.
- The generality is built ahead of a second real entrance. The honest scope keeps the claim
  true to what the tool reads, so the machinery is ready without over-claiming a coverage it
  cannot yet exercise.

## Status

Open, in build. The adversarial review (three independent reviewers, `design-review.md`)
returned a re-scope verdict; the operator re-cut it to expand the milestone to encompass
every aspect, with the review's blocking findings folded in as design requirements. Operator
decisions recorded: opt-in and reusable; the name `entrance` by Qwen-3.5-4B data; the
standalone sibling of reconcile; the declaration is a single `[entrance]` stanza, a global
singleton among the components, reaching any document by path, with the named member set
apart from `components` as the front door is today. Supersedes the agentic-host-local scope
of plan/0040 and the scope half of `call/0026`, and carries the rename and migration of
`call/0027` toward completion.

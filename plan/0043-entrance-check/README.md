# plan/0043: the entrance check (a reusable standalone-document check)

The entrance check (plan/0040, host-lifecycle v0.27.0) holds the one published
entrance of agentic-host to the spine. The same problem recurs wherever a project keeps a
self-contained document that restates the methodology and cannot link to it: an
adopter-authored standalone `SKILL.md`, or any project's operator-and-agent landing
page. This milestone generalizes the check into an opt-in, reusable capability and
renames it for the general case. It supersedes the agentic-host-local scope set in
plan/0040.

## Problem

A self-contained document is read out of context (a single-file entry point, a skill
loaded on its own), so it cannot point at a canonical definition with a link the way an
in-host doc does (the reconcile arm). It restates, and the restatement stales silently
when the spine moves. plan/0040 solved this for one document, hardwired: the tool finds
the `.host-software` member marked `entrance = true` and checks its README against the
manifest phases, the `.host-software` tools, and the `.host` stamp format. Nothing lets
another project, or another document, opt in.

## Decision (operator, this review)

- **Opt-in and reusable, not agentic-host-only.** Any project may declare a
  self-contained document as an entrance and have it held to the spine. The capability
  stays inert until declared, the way the deeper verification rungs do. This supersedes
  the decision in plan/0040 that the capability is agentic-host-local, and the scope
  half of `call/0026`.
- **The name is `entrance`.** Settled by a Qwen-3.5-4B run over the host-and-rooms-and-guest
  metaphor (a guest comes in the entrance). `landing`, `threshold`, and `welcome`
  mis-cued (a deployment step, a numeric limit, a greeting); `foyer` was the model's
  metaphor-first pick but reads as too domestic for software, so the operator chose
  `entrance` for its software resonance. `front-door` is renamed to `entrance` with no
  alias, the plan/0039 way (a name that overfits is fixed, never aliased).
- **The standalone sibling of `reconcile`.** reconcile holds a linkable document honest
  with pointers and coverage; `entrance` holds a self-contained document honest with
  coverage and generation, because it cannot link.
- **The rename landed standalone, ahead of this milestone.** The operator pulled the
  rename forward: `front-door` became `entrance` with no alias, carried by a
  deprecate-then-retire migration (the parser accepts a legacy `front-door = true` with a
  deprecation warning, slated for removal a release later). Released as host-lifecycle
  v0.28.0 and the v0.28.1 migration; `call/0027` records it. The remaining work of this
  milestone is the opt-in generalization.

## The design (proposed, for adversarial review)

- **Declared out of the prose.** A project declares which documents are entrances, and
  which spine concepts each restates, in configuration (the natural home is
  `.host-software`, generalizing the `entrance = true` flag), never a marker inside the
  document. A marker in the prose is the machinery the methodology already rejected
  (plan/0039), and the routing rule below keeps the document clean.
- **The routing rule, settled in the plan/0040 review and now general:** generate what
  is naturally a format or data block (the `.host` stamp), coverage-check what is
  naturally prose (a phase name, a tool name), and never put a generation marker in
  teaching prose. An entrance restating the phases is held complete against the manifest;
  one restating the tools is held complete against `.host-software`.
- **Adopter-facing.** The capability carries spine doctrine and an `UPGRADING` entry,
  unlike plan/0040, which was agentic-host-local with neither.

## Open decisions (settle by review before building)

- **The declaration form.** How a project names an entrance and the concepts it restates:
  a per-document `.host-software` stanza, a flag plus a concept list, or a small
  dedicated file. The form must read at the weak-agent bar.
- **One concept set or many.** A published entrance restates every concept; a skill may restate
  only the phases. So an entrance declares which concepts it must keep complete, rather
  than the check requiring all of them everywhere.
- **Refactor or extend `reconcile`.** Whether `entrance` is a separate subcommand or a
  mode that shares the coverage core with reconcile.
- **The rename blast radius (resolved).** The rename landed standalone in `call/0027`:
  the subcommand, the `.host-software` flag, the tests, and the agentic-host CI
  invocation, with a deprecate-then-retire migration for a legacy `front-door = true`.
  The first instance is migrated; the general declaration form stays the open decision
  above.

## Build sequence

The build sequence as a task graph (plan/0042), to run after the review settles the
design. Each entry is an anchored task, the chain is linear, and each task carries a
receipt.

### Settle the open decisions by review {#settle-open-decisions}

Settle the declaration form, the concept-set model, the reconcile relationship, and the
rename blast radius by adversarial review, recorded in a design-review subdoc with a
proceed verdict.

- verify: attested operator

### Implement the entrance check {#implement-entrance}

Generalize the entrance check to a declared, opt-in capability, and keep the routing rule
(generate format blocks, coverage prose). The rename itself landed standalone (`call/0027`),
so this task is the opt-in generalization on top of it. The unit tests pass.

- depends: #settle-open-decisions
- verify: cd software/host-lifecycle/main && cargo test

### Add the spine doctrine {#add-doctrine}

Add the spine doctrine (an entrance is a declared self-contained document held to the
spine, the standalone sibling of reconcile) and an `UPGRADING` entry. host-template prose
clean; the entry's verify post-condition holds.

- depends: #implement-entrance
- verify: attested operator

### Validate at the weak-agent bar {#validate-4b}

Validate the declaration ergonomics and a skill-author use case with a recorded
Qwen-3.5-4B run.

- depends: #add-doctrine
- verify: attested operator

### Migrate agentic-host and release {#release-and-re-pin}

Migrate the agentic-host entrance declaration to the general opt-in form (the first instance),
release host-lifecycle, re-pin `.host-software`, record the receipt and a `call/`
decision that supersedes the scope of `call/0026`, and bump the CI install pins. The
released binary gates green; the whole suite is green.

- depends: #validate-4b
- verify: attested operator

## Risks

- The rename touches the subcommand, a `.host-software` flag, and the agentic-host front
  door at once; the migration lands as one atomic change so no state is half-renamed.
- The declaration adds a surface every adopter could meet, so its form must stay simple,
  or the opt-in capability becomes a burden.
- Generalizing for a use case that is still mostly the own concern of agentic-host is a
  real risk; the skill-author use case is the test of whether the generality earns
  itself.

## Status

Open, design phase. Operator decisions recorded (opt-in and reusable; the name `entrance`
by Qwen-3.5-4B data; the standalone sibling of reconcile). The rename landed standalone
ahead of the milestone (host-lifecycle v0.28.0 plus a v0.28.1 deprecate-then-retire
migration, `call/0027`); the remaining work is the opt-in generalization, awaiting
adversarial review of the remaining decisions (declaration form, concept-set model,
reconcile relationship). Supersedes the agentic-host-local scope of plan/0040
and the scope half of `call/0026`.

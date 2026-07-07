# call/0041: the adopt command splits into scaffold (primitive) and adopt (onboarding)

- Status: accepted
- Scope: host-lifecycle
- Date: 2026-07-07

## Context and problem

`host-lifecycle adopt <dir> <revision>` is the scaffold-and-stamp primitive: it creates the rooms and
writes the `.host` stamp for a repository being brought under the methodology. The lifecycle adopt phase
and its skill invoke it by that name. plan/0065 introduces a human-facing three-route onboarding as
`host-adopt`, described there as a shim over the `adopt` verb, with the bare `adopt` name retiring. The
two operations are different: one scaffolds into a named directory at a revision; the other elicits a
name, decides among three routes (refuse a software repository, adopt an empty `agentic-<name>` in place,
or create the host elsewhere from an arbitrary folder), and never touches the source. A single verb cannot
carry both without overloading on argument shape.

## Decision

Split the verb. The primitive is renamed `host-lifecycle scaffold <dir> <revision>`, its behaviour
unchanged. The `adopt` verb becomes the three-route onboarding, invoked by a human through the `host-adopt`
shim. The bare `adopt <dir> <revision>` form gets a deprecate-then-retire shim: it prints a deprecation
line naming `scaffold` and forwards, and it retires a release later, the same shape as the
front-door-to-entrance rename (call/0027). The adopt skill and the lifecycle manifest's adopt phase migrate
their command to `scaffold`, and a UPGRADING ledger entry carries the migration to adopters.

The migration map, the one place the old name lives:

- `host-lifecycle adopt <dir> <revision>` becomes `host-lifecycle scaffold <dir> <revision>` (the primitive).
- `host-lifecycle adopt` with no revision becomes the three-route onboarding (the `host-adopt` shim).

## Consequences

Good: the human entry (`host-adopt`) and the primitive (`scaffold`) have distinct, honest names, and the
deprecate-then-retire shim means no adopter breaks on the release that ships the split. Bad: this is a
spine migration touching the adopt skill, the lifecycle manifest, and every adopter that scripts the old
command, so it owes a revision-keyed ledger entry; the old name lives on transiently in the shim and the
migration record. Sunset: retire the bare-`adopt`-to-`scaffold` shim one release after adopters have moved.

## Relates

plan/0065 (the onboarding layer this serves); call/0027 (the front-door-to-entrance rename, the same
deprecate-then-retire precedent); the migration ledger entry keyed to the doctrine commit in host-template.

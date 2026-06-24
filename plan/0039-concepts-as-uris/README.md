# plan/0039: Concepts as URIs (reconcile by pointing, not annotating)

**Status: designed and validated, not yet built (2026-06-24).** The design is settled; the build is the next milestone of work. The `family` to `components` rename and the removal of agentic-host's inline annotations are uncommitted in the working tree, held for the build.

## Context

The reconcile arm (plan/0036) guards a project's own restatements of methodology against drift after a spine change, using an inline annotation: a doc line carries `<!-- host-reconcile: KIND -->` and the tool checks that line against a single source of truth (the component set, the verifiers, the layout). The operator rejected every inline-annotation form on aesthetic grounds: a comment trailing a sentence, a comment pair wrapping a span, a markdown link carrying the directive, and an out-of-line metadata block. The objection is structural rather than cosmetic: any inline annotation is checker machinery sitting in the prose, and prose that reads clean is the whole point.

A replacement was explored and validated. Each methodology concept becomes a URI: one canonical definition at a stable address, and every mention points to it with a plain link rather than restating it. This is the single-source-of-truth principle (DRY, Hunt and Thomas) made concrete, and the reflection-on-action lineage the doctrine already borrows (Schon); the addressing is the first Linked Data principle (Berners-Lee), names for things made dereferenceable. The decision records carry these as outward citations, kind to predecessors and peers; the project holds itself to the same rule with rigor, which is the inward face of the one principle.

## The design (refined-B)

Each concept (the project's `components`, the `verifiers`, the `software-root`, the `spec-home`) has one canonical definition at a stable `{#id}` anchor in an authored doc, `STRUCTURE.md`. Everywhere else points to it with a relative-path link (`STRUCTURE.md#components`), which renders and resolves under stock mdBook with no custom generator pass. There is **no generated `concepts.md`**: with all four definitions in one doc, a page of links back to them is pure redundancy (see "Refinements this session"). Drift is caught not by generating the definition but by the coverage check, which holds each project-local home to its full `.host-software` set; the tool carries the concept vocabulary, so no file enumerates it.

reconcile stops scanning inline annotations and runs three checks instead:

- **link-integrity**: every concept link resolves to a declared concept anchor.
- **declared-anchor**: a link target must be a known concept id, not any resolving fragment, so a link cannot point at the wrong concept and pass.
- **coverage**: every component and verifier the source of truth names must be referenced somewhere, so dropping a tool fails by absence. This restores the bite the inline check had and link-integrity alone loses.

The concept formerly named `family` is renamed `components`: the methodology's own word for the set recorded in `.host-software`. "Family" was an agentic-host overfit, since the host-* tools happen to share a prefix while an adopter's components need not be related.

## Scaling by URI authority

The split the inline mechanism muddled is resolved by who owns each definition. Spine-universal concepts (`software-root`, `spec-home`) live at URIs in the spine's namespace, one shared vocabulary every adopter links to. Project concepts (`components`, `verifiers`) live in the project's own namespace, sourced from that project's `.host-software` and wired lanes, never a spine constant. An adopter without a book or `.host-software` skips the project-scoped checks rather than dangling or silently passing.

## Two cast reviews

The design was reviewed twice through the cast, recorded here for the build.

The first reviewed the markdown forms. Verdict: reject every inline form. The published prose must read clean (Mara); one link syntax for three meanings invites confident drift, and a stray bracket breaks it silently so the gate passes falsely (Wren). The pointer link survived as the one place a link reads naturally.

The second reviewed the fork (retire inline reconcile for concept-as-URI, or keep it renamed). Verdict: unanimous hybrid. The direction is right, but link-integrity alone is looser than the inline check, because a dropped tool is never linked so nothing catches the absence; hence the coverage and declared-anchor checks are required. The cutover must fail safe: a retired checker hard-fails on a surviving annotation rather than ignoring it silently (Bly). Retiring a mechanism shipped days earlier is its own churn, so the path is deprecate-then-retire (Orin).

## The transition: deprecate-then-retire

1. Rename `family` to `components` across the binary, its tests, and the spine manifest (done in the working tree, the suite green).
2. Mark inline reconcile deprecated, naming the concept-as-URI successor, and keep it checking under the new name so the bite holds during the transition.
3. Add the concept homes (`{#id}` anchors) to `STRUCTURE.md`, and build the coverage, declared-anchor, and link-integrity checks.
4. Convert the host's restatements to pointers.
5. Retire the inline mechanism one spine revision later, via an `UPGRADING` entry that over-reports the owed migration and hard-fails any surviving annotation.

agentic-host accepts running in the gap as the first mover: its inline annotations are already removed, so its restatements are briefly unguarded until the coverage check ships. The operator accepted this as a calculated risk; an adopter is not asked to take it, since the deprecate-then-retire path and the fail-safe cutover protect the adopter.

## Validation already in hand

- The concept-as-URI scheme renders and resolves under stock mdBook v0.5.2: the `{#id}` heading anchors are honored, a relative `STRUCTURE.md#id` link rewrites to `STRUCTURE.html#id`, and every link resolves.
- The real weak agent (Qwen-3.5-4B) authored concept pointer links unaided and correct, three of three, the `verifiers` route among them, which the inline scheme's classification step had failed. The reason is structural: pointing carries no judgment of whether a span is a restatement, the step that exhausted the model before.
- The `family` to `components` rename builds clean with the whole suite green.

## Verification (for the build)

- Each project-local concept's home in `STRUCTURE.md` names its full `.host-software` set (coverage), with no generated `concepts.md`.
- reconcile flags a dropped component (coverage), a link to an undeclared concept (declared-anchor), and a broken link (link-integrity), and stays silent on a clean set.
- A surviving inline annotation hard-fails once the mechanism is deprecated, and never silently passes.
- A weak-agent run reaches the right pointer on a concrete case unaided.
- An adopter without a book or `.host-software` skips the project-scoped checks rather than dangling.
- The host's verify gate (validate, reconcile, prose, book) is green, and the whole-suite CI is green across the affected repos.

## Refinements this session (the design as it now stands)

Settled in discussion, checked against the cast and the real Qwen-3.5-4B, and kept in plain words for the weak agent — **spine, copy-at-version, point, front-door**:

- **Project-local facts, enforced.** `components` and `verifiers` come from the project's own `.host-software`, never the spine manifest. The manifest is hardened to **phases only** — `manifest --check` rejects any other stanza — so an overfit cannot creep back into the shared spine. `components` are the `.host-software` members; `verifiers` are a `[verification] drivers` stanza (absent → skipped, fail-safe). The cast and a real 4B run backed the move; the 4B's reliable failure is exact-format emission, not the judgment, so the edit is tool-carried and the prose only points.
- **`host` is the front door, not a component.** Of the members, the four tools (host-lint, host-lifecycle, host-prove, host-grammar) are the `components`; the single-file `host` is the **front door**, the methodology's entry point, set apart by `front-door = true`. This corrects a stale comment that called it "repo-self": agentic-host, the dev environment, is not a member at all and stays invisible to adopters.
- **The principle reaches the front door.** One **spine**; everything else is a **copy-at-version** of it or **points** at it — never a restatement. The front-door `host` and every adopter are both copies-at-version of the spine, so "an adopter becomes host" is just *a copy of the one source*. Seeding the front door from the spine, so it cannot drift, is the named next application; the doctrine states the rule here, the build follows.

## Records

This document, a MEMORY entry, and a software `call/` for the concept-as-URI decision authored at build time. The `host-lifecycle next` footgun surfaced while allocating this number is filed as connollydavid/host-lifecycle#1.

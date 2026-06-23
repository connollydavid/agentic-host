# plan/0034: the hygiene grammar grows by reflective practice (fixes host#16)

Resolves connollydavid/host#16 (positional checklist-item references evade the ordinal lane).

## Context

host#16 reports that host-lint does not catch positional references to milestone
checklist items. The shapes, quoted as the lane would receive them:

```host-lint:ignore
box 7        boxes 4-8        box-1        steps 3-5
```

The meeting that produced this milestone established, against the adopter where the
shape emerged (reviewed in a scratch checkout only, never referenced in tracked files):

- **The guard is blind to the shape.** None of the positional references in that
  adopter's history or its two milestone READMEs were caught on the noun token; the
  only non-clean verdicts fired on an em-dash. Plural and range forms also evade,
  because `check_line` splits on whitespace and tests one token against a singular
  noun set.
- **Not a migration artifact.** The shape first appears in milestones authored fresh,
  whose items already carried content titles. It is an emergent authoring habit, and
  it is not in our spine (host-template never defined a checklist convention).
- **The available content name was bypassed.** A reference cited a sibling item by
  position even where a content name was at hand, so adding content anchors at the
  source would not have prevented it. The fix is detection plus doctrine, not a
  convention.
- **The deeper gap is methodological.** The spine already forbade positional naming;
  an agent ignored a rule it had, and the lane stayed silent. We had detection as a
  refusal with no sanctioned positive path, and no stated account of how the shared
  grammar grows when a tell emerges in practice. That account is the real subject here.

## Where the rule lives

The naming noun set (`FLAG_TERMS`) and `VOCABULARY.md` are host-lint's own. host-lint
consumes host-grammar only for the numeral helper and the prose-trope engine. A
positional reference is a **naming** tell, so it graduates into host-lint, not
host-grammar.

## Decision

Two coupled moves: fix the bug in host-lint, and author the growth doctrine in the
spine. The operator practice the doctrine describes is runnable today, without new
tooling.

### The doctrine (authored in host-template)

The hygiene grammar is a living, shared source that grows by reflective practice:

1. **Two authorities, named distinctly.** A project's local operator validates its
   `LEXICON` and decides what is worth proposing. The shared-grammar maintainer
   validates universality and releases the change. An adopter proposes a candidate
   upstream rather than editing software it consumes.
2. **Discovery is mechanical-first, operator-judged, agent-assisted.** The reliable
   path is a sweep of history and recent work for recurring shapes the lane misses,
   triaged by the operator. An agent rarely perceives its own register as a tell, so
   its reflection is the assist, prompted at the verify gate and at adoption, never
   the mechanism.
3. **The asymmetry that routes a shape.** Legitimacy is local, so it is declared in
   the per-project `LEXICON`. A tell recurs across projects and models, so a confirmed
   tell graduates into the shared grammar the lane enforces: a naming tell into
   host-lint, a prose trope into host-grammar.
4. **The universality test.** The operator asks whether the shape is a property of how
   models segment work, or of this domain's vocabulary. A candidate that fails the
   test is reworded, not graduated.
5. **Disposition order is never inverted.** Reword into content by default, because a
   name is almost always available. Box or declare an irreducible citation. Declare
   the legitimate contextual phrase when a shape is a genuine quantity rather than a
   position. Reserve a graduation for the residue that recurs once rewording is
   genuinely impossible.
6. **Reflection has a concrete trigger.** It is prompted at the verify gate before a
   milestone closes, and at adoption.
7. **Growth looks forward and has a correction path.** Harvesting proposes what to
   catch from now on, and does not retro-flag the immutable past, which migration
   disposes of by renaming live files, boxing frozen records, and path-excluding
   append-only logs. A grammar bump that newly flags existing live docs follows the
   disposition order: reword the live ones, box the frozen ones. A graduation that
   proves to over-flag is narrowed by a later grammar release.

A software `call/` for harvest tooling is deferred until that tooling is built (see
Follow-ups).

### Detection (host-lint)

A1. Add `box`, `boxes`, and `steps` to `FLAG_TERMS`, and accept a numeric range
    (`N-M`) and a glued hyphen-digit form (the noun joined to a numeral by a hyphen)
    after the noun, in `src/lib.rs`. Severity stays a flag, like the existing
    ordinal nouns. Verify by: synthetic fixtures for the four shapes above all flag.
A2. Preserve the boundaries. The literal checklist mark stays clean (it carries no
    noun-plus-numeral), a content-named reference stays clean, and the `box`
    disposition verb stays clean (no trailing numeral). Verify by: the mark, a
    content reference, and the verb all clean; `phase`/`stage`/`step` behaviour
    unchanged (existing tests green).
A3. `VOCABULARY.md`: document the shape, its rationale, the literal-mark boundary, the
    noun-versus-verb note, and the LEXICON resolution for a genuine quantity. Declare
    the **numeral-free contextual prefix** (the phrase without the number), because the
    numbered phrase is refused by the flag-tier guard by design. Verify by: host-lint
    self-lint clean on `VOCABULARY.md`.
A4. Update `host-lint.allium` and `.obligations` for the rule; add unit and
    integration fixtures (synthetic, never adopter-derived). Verify by: `cargo test`,
    `./test-integration.sh`, clippy clean; allium lane green.
A5. Gather weak-agent data. Drive Qwen-3.5-4B through the clear cases (a positional
    reference flags, a literal mark is clean, a genuine quantity is declared by its
    prefix) and confirm it reaches the correct verdict unaided.
A6. Release host-lint through the lifecycle, re-pin `.host-software` with the
    re-derived artifact hash, and run `software --verify-build` and `software --check`.
    Verify by: release gate green, tag pushed, both checks clean, CI green.

### Doctrine (host-template spine)

B1. Author the doctrine in `CLAUDE.md` as the continuation of the Hygiene lane item,
    prose-clean, with no promise of an unbuilt local-ban surface. Verify by: host-lint
    prose mode clean on the edit; the existing UPGRADING verify phrases unchanged.
B2. Add the `UPGRADING.md` ledger entry, `requires` pinned to the Part A host-lint
    version. Verify by: the entry parses and its verify-grep passes after the edit.
B3. Push inside the submodule, bump the pointer, re-record `.host`, and run the
    migration so this repo applies its own new doctrine. Verify by: baseline advanced,
    zero pending; any of this repo's live docs that now flag are reworded or boxed.

### Records and close

C1. Update the `PLAN.md` row and this doc to reflect what landed; commit and push
    immediately as audited docs.
C2. `MEMORY.md` entry: the routing fact (a naming tell lives in host-lint), the
    bypassed-content-name finding, the two-authority model, the verify-gate reflection
    trigger. Separate commit, pushed.
C3. Close host#16 with the before-and-after numbers.

## Scope boundaries

- Out: a project-local ban surface. Every tell seen so far is universal; building it
  is speculative.
- Out: mechanizing the harvest and the verify-gate reflection prompt in the skills.
  The doctrine is runnable today by the operator's manual sweep and an upstream
  proposal. Mechanizing it is a named follow-up.
- Out: host-grammar. The shape is a naming tell, owned by host-lint.
- Out: the adopter's residue. Their cleanup; immutable commits; never referenced in
  tracked files here.

## Verification

host-lint flags every synthetic positional shape and stays clean on the literal mark,
content names, and the disposition verb; the existing ordinal nouns are unchanged; the
weak-agent clear cases classify correctly; `software --check` and `--verify-build` are
clean; the spine prose mode is clean with the existing verify phrases intact;
`validate plan/ call/` passes; the book builds; a tell-commit is blocked by the hook;
all repos are green; host#16 is closed.

## Risks and honesty

- host-lint is a context-free shape matcher. It flags the positional shape; it does
  not, and cannot, spare an algorithmic phrase of the same shape on its own. The
  sanctioned escape is a `LEXICON` declaration of the numeral-free contextual prefix,
  human-validated, verified to mask the quantity while leaving genuine positional
  references flagged.
- That escape is correct but not frictionless for a weak agent, which must notice a
  blocking flag and declare the prefix rather than the numbered phrase. This is an
  honest cost of widening the noun set, and the reason the prefix pattern is
  documented in `VOCABULARY.md`.
- The detection move independently fixes the bug; the doctrine is the deliberate spine
  evolution. They are sequenced software-first, so a stall in the doctrine never blocks
  the shipped fix.

## Follow-ups

- Mechanize the harvest and the verify-gate reflection prompt in the skills (a
  software milestone that would carry the deferred software `call/`).
- A constrained local-ban surface only if a genuinely non-universal tell is found.

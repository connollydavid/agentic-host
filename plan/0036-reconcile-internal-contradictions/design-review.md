# Design review: the migration reflective-practice doctrine (2026-06-24)

De-risk pass before authoring the doctrine into the spine, per the established loop
(adversarially review + weak-agent test, then implement). Five independent review lenses
over the candidate doctrine plus Qwen-3.5-4B operability data. Verdict:
**proceed with major revisions**; the candidate's intent is right and the observed drift
is real, but its scope rule, its cadence, and its primary trigger are wrong, and two of
its four mechanization shapes are unbuildable as drafted.

## Method

Candidate doctrine: a prompted reflection that, after a spine change, re-examines the
project's own restatements of methodology for drift and reconciles them, sibling to the
plan/0034 grammar reflection. Reviewed through five lenses (scope-boundary operability,
prompt cadence, redundancy vs the grammar reflection, mechanization feasibility,
effectiveness against the real drift) and tested against Qwen-3.5-4B.

## Qwen-3.5-4B data

- Pick the in-scope doc: correct (re-check the project's own STRUCTURE.md; skip the
  upstream spine copy and a persona).
- Spot a specific drift and reach the reconcile action: correct.
- Apply the abstract "describes vs uses" scope rule: **inconsistent**. The model treated
  the STRUCTURE.md room map as in-scope in one prompt and as an out-of-scope "use doc" in
  another, and garbled the describe-vs-use classification. Conclusion: a weak agent
  performs the reflection when handed a **concrete** target, but cannot reliably apply the
  **abstract** scope rule. The scope must be mechanical, not a judgment.

## Convergent findings

1. **The scope rule is inoperable** (lens 1, lens 4, 4B). "Describes vs uses" is a false
   dichotomy (most governance docs do both in one line), and "the project paraphrases /
   the spine owns a copy" is unstable here: the root `CLAUDE.md` and `STRUCTURE.md` are
   simultaneously spine-derived and instance prose, and the host-to-template sole-source is
   a deliberately deferred seam. Replace the judgment with a machine-checkable set.

2. **The disposition is two-way but the docs need three** (lens 1). "Reconcile in place"
   collides with the immutable rooms: a `call/` body, a `Status: done` milestone doc, and
   `MEMORY.md` cannot be edited. Reuse the settled tell-disposition: reword a live doc, box
   a frozen citation, exclude the append-only record.

3. **Blanket cadence is alarm fatigue** (lens 2). Of 30 ledger entries, only about 6 are
   drift-capable (they move a room/tool/layout/verification concept a restatement mirrors).
   A per-upgrade prompt is noise four times in five, which trains the operator to dismiss
   the prompt on the entry that matters. The trigger must be conditional.

4. **The primary trigger is wrong for a development host** (lens 5). agentic-host authors
   its spine changes as its own milestones, so `upgrade --record` never fired for the three
   structural drifts (plan/0012, plan/0023, plan/0029). The only trigger present at those
   moments was the **verify gate**. For a development host the verify gate is the binding
   trigger; the upgrade-record and adoption triggers serve a consuming adopter.

5. **Two mechanization shapes are unbuildable as drafted** (lens 4). The host-* tool count
   against `.host-software` is noise (5 stanzas vs the README's 3 vs CLAUDE's 4, all partly
   legitimate). The "N lanes" phrase has no truth source: the manifest is a phase journal
   with no rung count. The general restatement-vs-spine diff is an unsolved language
   problem, not deferred engineering, so the doctrine must not frame it as a follow-up tool.

6. **It is one principle with the grammar reflection, two arms** (lens 3). The shared root
   is self-blindness: an agent perceives neither the register it emits nor the restatements
   its own change stales. Widen the existing doctrine rather than add a parallel one. Keep
   the arms distinct in mechanics: a tell graduates **upstream** and rides a cadence; a
   reconcile fix stays **local** and is fired by a specific spine move.

7. **The reconcile arm belongs in the upgrade skill** (lens 3, lens 5), which has no
   Reflect step today, plus adoption, plus a conditional re-check at the verify gate.
   Stapling it to the gather cadence in the verify step over-fires it.

8. **A sibling gap: decision-status drift** (lens 5). `call/0017` left `accepted` after its
   rule moved into the spine is not a doc restatement; it is a MADR status drift, governed
   by anti-ouroboros. Nothing prompts the `Status: superseded by the spine` transition. A
   `validate` check that HAZARDs an `accepted` decision whose `Scope:` names `host-template`
   closes it mechanically.

9. **Anti-ouroboros grain** (lens 1). A doctrine that institutionalizes keeping paraphrases
   in sync blesses the duplication the methodology is trying to remove. Invert the default:
   an instance doc should point at the spine, not paraphrase it; a paraphrase that exists
   is a reconciliation liability. Reflection is the fallback for the paraphrase that cannot
   be eliminated.

## The revised doctrine (settled design)

**One reflective-practice principle, two named arms.** Widen the spine's existing
"grows by reflective practice" doctrine so its root is self-blindness in general: an agent
perceives neither the register it emits nor the restatements its own change stales, so both
are re-examined on purpose, prompted at the trust boundaries, mechanical-first, and operator
-validated. Two arms under it:
- **gather** (unchanged, plan/0034 and plan/0035): forward, emergent tells in the corpus, a
  confirmed tell graduates upstream, cadence-driven (every verify, adoption).
- **reconcile** (new): backward, the project's own restatements of methodology, a confirmed
  drift is fixed locally and never propagates, fired by a specific spine move.

**Prefer pointing over paraphrasing.** The primary prescription: an instance doc should
point at the spine rather than restate it; a restatement that remains is a reconciliation
liability the project chooses to carry. Reconcile maintains the unavoidable residue.

**Scope is a machine-checkable, annotation-backed set, not a judgment.** A restatement that
must stay carries a declared assertion the tool checks against a source of truth, the way
the `LEXICON`, the obligations manifest, and `.host-software` already work. Seed the spine
with the two missing truth data first: an explicit host-* tool-family list and a
verification-model datum (the manifest has neither today). The checks:
- a spec path asserted under `plan/` (the existing `plan_spec_problems` covers the file
  case; add the prose-cell case),
- a Where-root asserted off `software/`,
- a host-* family **set-diff** against the declared family list (catches the README
  host-prove omission and the STRUCTURE.md "only host-lint of five" completeness drift in
  one shape; the raw stanza count is dropped as noise),
- a verification-model paragraph that omits a rung-driver the declared datum names (a
  positive-assertion check, replacing the unbuildable "N lanes" count).
Drop the "general prose diff as a follow-up tool" framing: the annotated set is the whole
mechanizable surface, and the residue is a prompted human reflection, not a deferred tool.

**Three-way disposition** (reuse tell-disposition): reword a live restatement to match the
spine; box a frozen citation; for an immutable record (a `call/` body, a `Status: done`
doc, `MEMORY.md`) record a forward-pointing correction rather than edit it.

**Conditional, host-aware trigger.** Add an optional `restates =` field to the `UPGRADING`
`[upgrade ...]` stanza, set by the spine author when an entry moves a mirrorable concept
(room map, tool set, Where layout, verification model). Reconcile fires when a recorded
upgrade carries a non-empty `restates`, naming which restatement to re-read. For a
**development host** that authors spine changes with no upgrade record, the **verify gate**
is the binding trigger: it runs the reconcile check whenever a drift-capable spine change
landed since the last reconcile receipt, and records `n-a` otherwise. Adoption runs the
full reconcile once. Wire the reconcile step into the `upgrade` skill (new Reflect step),
the `adopt` skill, and the `verify` skill (conditional re-check); keep gather where it is.

**Sibling validate check.** `host-lifecycle validate` HAZARDs an `accepted` `call/` decision
whose `Scope:` names `host-template`, prompting the `Status: superseded by the spine`
transition. This closes decision-status drift (`call/0017`) mechanically, the gap the
doctrine itself does not cover.

## Consequence for plan/0036

The doctrine is a larger build than the candidate: a spine doctrine widening, two new spine
truth data (the family list, the verification-model datum), the annotation-backed reconcile
check in host-lifecycle, the `restates =` ledger field, the `validate` decision-scope check,
and skill wiring across `upgrade`/`adopt`/`verify`. The symptom reconciliation (the stale
STRUCTURE.md, README, CLAUDE.md, the pin, the tidiness items) then becomes the doctrine's
first dogfood run, reconciled through the new check rather than by hand.

# call/0051: a LEXICON entry reports a grammar defect

- Status: accepted
- Scope: the hygiene lane's shared vocabulary; what a declaration in a LEXICON means, where one may be relied on, and what the published template may carry
- Date: 2026-07-29

## Context and problem

[connollydavid/host#20](https://github.com/connollydavid/host/issues/20) reported one word in the template's operating manual warning under the prose lane, in a repository that had adopted the spine and propagated it. The word was reworded and the adopter went green. Its closing note named a class the fix did not touch: the template's own documents are not held to the lane an adopter runs them under.

The class is real and it is not about where that word sat in a sentence.

The template declares its sanctioned vocabulary in a `LEXICON`, and so does this repository. Both files carry exactly one entry. It is the same word, with the same justification written out twice, reached independently. An adopter receives neither file: `scaffold` seeds a comment-only `LEXICON` with zero entries, so the spine passes its own gate here and warns in every repository it is copied into.

That is the defect. A declaration is scoped to the repository that holds it, and the spine's text is not.

## What the corpus says

The word is `harness`. Measured over the tracked markdown and source of this repository and the template:

| | count |
|---|---|
| total occurrences | 157 |
| the verb, with an abstract object | 2 |
| the noun | the remainder |

Both of the two are the `LEXICON` comments themselves, which quote the verb to explain why the noun was declared. No document in either tree uses the word as a verb at all.

The plural was measured separately after the operator asked whether it was always a verb. It occurs 46 times and is a plural noun in every one, most often naming Kani proof harnesses and the agent harnesses an operator runs.

So the rule caught nothing and charged 155 legitimate uses for it. The word is a term of art here, older than the register the lane detects: a test harness, a proof harness (Kani's own name for a `#[kani::proof]` function), an agent harness. Applying the spine's own operator test, whether a shape is a property of how models segment work or of this project's domain, the noun is domain and the verb is register.

## What the source says, and where this departs from it

The catalog was then read rather than assumed, which should have happened first. It lists the word, under the entry `"Delve" and Friends`, as one of a family of overused vocabulary. It does not qualify it by part of speech, and it does not describe a construction.

So this decision **departs from its cited source** for this entry. The departure is recorded rather than dressed up as a reading of the catalog, and it rests on two things. The corpus measurement above is the first. The second is that the catalog qualifies by part of speech where a word carries a legitimate other sense: the same entry lists `leverage` as `(as a verb)`. Narrowing a word whose noun is domain vocabulary is the method the catalog already applies; applying it here is consistent with how the catalog works while differing from what it says about this word.

Reading the catalog surfaced a larger discrepancy between it and the rule that cites it. Six of the seventeen terms this project detects (`realm`, `underscore`, `showcase`, `intricate`, `nuanced`, `multifaceted`) do not appear in the catalog at all. Two that do appear (`certainly`, `framework`) are absent here. The `(as a verb)` qualifier on `leverage` was dropped, so a financial or mechanical noun sense flags. And two separate catalog entries, the overused-vocabulary family and the grandiose-noun family, are fused into a single rule carrying one weight and one citation.

Two parts of that discrepancy are cheap enough to settle here, because a citation is a factual claim and a wrong one should not outlive the reading that caught it. The fused rule becomes three. `ai-diction` and `grandiose-noun` each cite the catalog entry they came from; `house-diction` holds the six terms the catalog does not contain, and cites this project. A verdict then names the rule it matched, and no term can borrow a source that does not carry it. What is left open is the substantive question of whether each of those six earns its place, which needs the same corpus measurement this decision applied to one word.

## The path that was not available

Rewording every site was considered first and does not work. Two occurrences sit inside `UPGRADING.md` entries, and that file's header forbids amending one: an entry is a contract with claims already recorded against it in adopters' `.host-receipts`, and editing it can convert a correctly applied upgrade into a standing hazard on a tree its owner cannot fix. Boxing is an amendment too, and the stanzas are machine-read.

The operator ruled out declaration and the ledger ruled out amendment, so the only remaining path was a narrower rule. The constraint and the evidence agreed.

## Decision

**The bare word leaves the shared grammar; the construction stays.** `ai-diction` now carries the verb with its object across four conjugations rather than the bare token. The noun clears everywhere.

**A `LEXICON` entry is a report, not a settlement.** Declaring a token records that the shared grammar over-fired on this corpus. It is provisional, and it is owed upstream.

**The same entry in two repositories is a confirmed over-fire.** Local legitimacy is local by definition, so a declaration reached independently twice is evidence about the rule rather than about either project. It is fixed in the grammar and both declarations retire. This is the existing graduation path run backwards, and it had no trigger before.

**The template carries no `LEXICON`.** Its text is copied into repositories that never receive the file, so a declaration there is unsound at the moment it is written. The published spine is held to the unexempted bar, and a tell-shaped token in it is reworded or the grammar is wrong.

## Consequences

Both `LEXICON` files retire in this change. Neither repository keeps a declaration to inherit, and neither keeps one to trust.

The template's prose is now first-class on its own terms rather than on a declaration adopters do not get, which is what [connollydavid/host#20](https://github.com/connollydavid/host/issues/20) asked for beyond its one word.

The narrowing is a behaviour change in a shared dependency, so it rides the release cascade through host-grammar, host-lint, and host-lifecycle rather than landing as a documentation edit.

Three host-lint tests used the retired token as their worked example of an over-firing term. They were first moved to `realm`, which is one of the six terms the catalog does not contain, and then to `paradigm` and `landscape`, which it does. The first move was made before the catalog was read and is the same error this decision is about, committed while recording it. The tests keep the shape they were written to prove, and that shape covers the hyphenated declared phrase that reaches the masker's word-boundary handling.

`paradigm` did not survive the session that chose it. The operator observed that `framework` is a special case with respect to software, and the observation generalises: the catalog describes prose in general, while this rule ships to software projects, where `framework`, `ecosystem` and `paradigm` each name a real thing a project builds on. All three are held out of `grandiose-noun`, which keeps `tapestry`, `landscape` and `synergy`. The evidence is the same as for the bare token, and it is stronger, because every reader of this rule is a software project by construction rather than by measurement of one corpus. The worked example the sentence above describes had used *the actor paradigm* as its instance of legitimate vocabulary while the same session held that `paradigm` had no collision to measure; the fixture was the evidence and it went unread. It now uses `tapestry`, which the catalog lists and which is also the name of a Java web framework a project may legitimately declare.

Moving that fixture surfaced a defect in the masker, filed as [connollydavid/host-lint#26](https://github.com/connollydavid/host-lint/issues/26): a declared phrase blanked at the start of a markdown line leaves four or more leading spaces, which the structural pass reads as an indented code block, so every tell on the line clears silently. The declaration's blast radius is the line rather than the phrase. The old fixture began with `The ` and never reached it. That is a second instance of this decision's own theme, a rule whose behaviour nobody had measured at its boundary, and it is scoped to host-lint rather than to the shared grammar.

The remaining sixteen terms are left detecting as they are. `showcase`, raised in the same session, occurs zero times in this corpus, so there is no collision to measure and narrowing it on a reading of the word would repeat the uncalibrated move that produced this defect. Its real defect is the attribution, which the reconciliation above covers rather than this decision.

The trigger for narrowing is a measured collision. The trigger for reconciliation is a term that cannot be traced to the source it cites. They are different questions and the second is now open.

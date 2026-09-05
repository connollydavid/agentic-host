# design-review: the cast round on the declared corpus (2026-09-05)

The design on the table: the `.host` stamp's `active-corpus = <file>` declaration (a change from the cut README's manifest-stanza lean, corrected during gather-data), the strict tier in the prose verb, the census disclosure, and the rename surfaces. Each chair attacked their own first preference before speaking.

## Mara (the operator)

Concern: what does the declaration cost to keep green? A strict corpus is a gate that reddens on every editorial slip in the manual, and the manual is edited every session.

Disposition: priced and accepted as the point. The manual sits at zero warns because the tropes pass just paid for it; the gate holds that ground at the moment of editing (the verify recheck runs `prose`, so a slipped em-dash stops the next release with the file and line named). The cost is one reword, payable immediately, on text the operator is reading anyway.

## Wren (the agentic developer)

Concern: the strict tier lives in the prose verb, but the pre-commit hook still advises warns on declared files — an author learns of the escalation only at the next release, not at commit time.

Disposition: carried, deliberately. Wiring the declaration into the hook means host-lint reads project policy, which breaks the detection/policy split this plan is built on, and the hook cannot read the stamp's list file portably. The recheck catches it before anything permanent ships. Recorded as the first candidate if the friction shows in practice.

## Bly (the downstream adopter, cold read)

Concern: the declaration is a second policy file next to `.host-lintignore`, and the two read in opposite directions (one names files held stricter, one names files held not at all). Cold, that is confusing.

Disposition: answered in the record, not the mechanics. The plan README states the difference as the design (one names the corpus held to the strict tier, one names records excluded by the append-only rule), and the ignore-list separation stays its own owed milestone. The declaration also has exactly one reader (the prose verb), so the two-lists-one-checker failure shape cannot recur here.

## Orin (the methodology maintainer)

Concern: the spine's own tree — the template — declares no corpus, so the template payload is held to advisory tiers in its own CI while every adopter's copy is held strict. The guardian is weaker than the flock.

Disposition: carried with a date. A `.host` stamp in the template would make the template pretend to be its own adopter, which the stamp's meaning forbids. The honest fix arrives with plan/0079's render, where the template's always-loaded surfaces are guarded where they are authored; noted in the plan record as a plan/0079 dependency.

## What the round changed

Nothing in the built diff. Three carries recorded (the hook gap, the two-policy-files reading, the template's own tier), all owned by named later work.

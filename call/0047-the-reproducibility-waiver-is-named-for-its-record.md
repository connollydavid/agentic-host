# call/0047: the reproducibility waiver is named for its record

- Status: accepted
- Scope: the `.host-software` recipe surface, the spine's reproducible-builds section, host-lifecycle's parser
- Date: 2026-07-23

## Context and problem

[call/0046](0046-retire-the-unimplemented-hermeticity-escape.md) retired an escape the tool never read and folded its case into the surviving key, `repro-exempt`. That left one key carrying two concepts, under a name the operator had just rejected in its sibling: a key that records something should be named for the thing recorded, and an adjective belongs to an option rather than to a field.

`repro-exempt` reads as "exempt from reproducibility", which names the state being excused rather than the record being written. What the operator actually writes on that line is the name of a decision. The key is a citation slot, and its name should say so.

Two concepts now share it, and neither is visible in the name: a migrated build that does not reproduce byte for byte yet, and a component that cannot vendor its dependencies offline. A rename that leaves the doctrine text silent about the second would be cosmetic.

## Decision

1. **The key is `repro-waiver = call/NNNN`.** Settled by the rotation-proof weak-agent probe the recent names used: `repro-waiver` was chosen from position A and again from position D against `repro-exempt`, `repro-exemption` and `build-waiver`. A second probe read both the old and the new spelling correctly, so legibility did not decide it; the naming rule did, and the probe establishes that nothing is lost.

   The migration verb's own name did **not** settle this way, and the difference is recorded rather than smoothed over: four rotations produced two position artefacts (position A twice, then position C twice), which is a preference for a slot rather than for a word. The probe was declared spoiled and `migrate-recipe` was settled on the family it joins, `migrate-receipts`. A spoiled probe is data about the protocol, exactly as plan/0076's spoiled ballot was.
2. **Both spellings parse, and the retired one reports itself.** An adopter's recipe keeps working across the rename and hears once per read that the key moved: the deprecate-then-retire discipline (plan/0039) rather than a silent swap. A test pins both spellings to the same waiver.
3. **The migration is carried by the tool.** `host-lifecycle migrate-recipe <dir>` renames the retired key, drops the one no release ever read, leaves every other line untouched, and is idempotent. Both ledger entries call it rather than instructing a hand edit, because a hand edit is where a weak agent renames the wrong line and a busy operator renames none of them. The retired keys sit in one table, so the next rename is a row rather than a verb.
4. **The doctrine names both cases the key carries**, so the second one is not inferable only from a decision record: the build that does not reproduce yet, and the component that cannot vendor offline.
5. **The retired spelling is removed at a later revision**, on its own ledger entry, once adopters have had a release to migrate. Nothing in this decision retires it today.

## Consequences

- host-lifecycle parses `repro-waiver`, keeps reading `repro-exempt` with a warning, and every line an operator reads names the surviving key. The change ships with plan/0077's release.
- The spine's reproducible-builds section and its ledger entry move to the new spelling, with an upgrade entry whose verify condition reads the adopter's own recipe rather than the template's text.
- No component here carries a waiver. This repository migrates by taking the doctrine and the parser; its `.host-software` needs no edit.
- The naming reading stays scoped as [call/0046](0046-retire-the-unimplemented-hermeticity-escape.md) left it: it binds this family of keys, and sweeping the wider recipe surface is not decided here.

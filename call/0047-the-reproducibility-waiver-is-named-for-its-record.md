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
2. **Both spellings parse, and the retired one reports itself.** An adopter's recipe keeps working across the rename and hears once per read that the key moved. This is the deprecate-then-retire discipline (plan/0039), not a silent swap, and a test pins both spellings to the same waiver.
3. **The doctrine names both cases the key carries**, so the second one is not inferable only from a decision record: the build that does not reproduce yet, and the component that cannot vendor offline.
4. **The retired spelling is removed at a later revision**, on its own ledger entry, once adopters have had a release to migrate. Nothing in this decision retires it today.

## Consequences

- host-lifecycle parses `repro-waiver`, keeps reading `repro-exempt` with a warning, and every line an operator reads names the surviving key. The change ships with plan/0077's release.
- The spine's reproducible-builds section and its ledger entry move to the new spelling, with an upgrade entry whose verify condition reads the adopter's own recipe rather than the template's text.
- This repository carries no waiver on any component, so its own migration is the doctrine and the parser, with nothing to rewrite in `.host-software`.
- The naming reading stays scoped as [call/0046](0046-retire-the-unimplemented-hermeticity-escape.md) left it: it binds this family of keys, and sweeping the wider recipe surface is not decided here.

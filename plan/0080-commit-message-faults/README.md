# plan/0080: commit-message faults

Mechanize what calibration supports. Trigger: [connollydavid/host-lint#28](https://github.com/connollydavid/host-lint/issues/28), operator-filed. Four faults recur in commit messages and pass the prose lane. Decided by [call/0054](../../call/0054-one-commit-message-fault-earns-a-detector.md); bundles the [connollydavid/host-lint#24](https://github.com/connollydavid/host-lint/issues/24) carve-out remainder, closure-queue position five. Single-component: the hook dispatch script is host-lint's own file, which host-lifecycle only copies at install.

## Calibration

Run before design, over 922 accepted commits across seven repositories ([calibrate-28.py](calibrate-28.py), raw readings in [calibration-28.txt](calibration-28.txt)).

| measurement | result |
|---|---|
| restated comment sentences, eight-word bar | 19 |
| the same at bars of five and twelve | 22 and 7 |
| subject matches that are the record-title convention | 12 of 12 |
| precedent-as-defence patterns, widened | 0 |

The heading sweep for the carve-out ([calibrate-24.py](calibrate-24.py)): 240 tracked markdown files across ten stores, 2036 headings, zero ordinal-scaffold shapes, so the tier demotion changes no current verdict.

## Landed

Two commits on host-lint main, folded to one per issue by operator direction:

- `3a6af0a`: the `commit` verb with the message and staged diff as named files, the calibrated advisory that names the safe direction, and a no-diff run that discloses the unrun check as a note; the commit-msg hook dispatch (usage-banner detection, staged-diff capture, `--stdin` fallbacks that name the unrun check); SKILL.md guidance for the unenforced faults. Mutation-proved: subject inclusion and the eight-word bar each redden exactly one test.
- `550aa87`: the ordinal-scaffold heading demoted to the advisory tier, the LEXICON carve-out for declared designators with strict escalation naming the declaration command, and the VOCABULARY entry the original rule shipped without.

## Compatibility surface

The hook detects the verb by the usage banner's `host-lint commit --message` line. Rewording that line in a later release degrades every installed hook to `--stdin` until a reinstall (disclosed, but easy to miss), so the banner's commit line is part of the hook contract. The contract is test-backed: the integration case asserting the `re-run:` line reddens if the dispatch stops reaching the verb.

## Acceptance

The convening record is [convening.md](convening.md) (input: [briefing.md](briefing.md)); ballots, tally and the settled design live there, summarized in call/0054. Fen was simulated: every probe channel refused connection. The real probes are preserved here and stay owed: [fen-p1.txt](fen-p1.txt), [fen-p1-worded.txt](fen-p1-worded.txt), [fen-p2.txt](fen-p2.txt), runner [fen-program.py](fen-program.py). Recorded untested: both probes against the real qwen3.5-4b. The operator sign-off of 2026-08-07 (call/0054) ships the release on the labeled simulation; the probes run when a channel exists.

## Release

host-lint, change class `changes-output`: a heading verdict that blocked yesterday is advisory today, and one class covers the release with the severest honest reading. Released 2026-08-07 as v0.18.0 (`ba3cf1e`, canonical hash `ab720b3e`), then 2026-08-08 as v0.18.1 (`966259f`, `fd65cad2`), a lockfile patch: the v0.18.0 tag run failed before publishing assets because `cargo install` re-resolved an unpinned transitive (allium-parser v3.5.3, incompatible with the pinned allium-cli), so every tool install now passes `--locked`. host-lifecycle v0.50.0 (`66c24d6`, `5914a633`) shipped alongside, authorized by [connollydavid/host-lifecycle#26](https://github.com/connollydavid/host-lifecycle/issues/26): its held stack plus the v0.18.1 embed via the vendor-v6 bundle, restoring the manifest-equality invariant. The entrance manifest regenerated to the released toolset. Both issues closed at the release.

# call/0046: retire the unimplemented hermeticity escape

- Status: accepted
- Scope: the spine's reproducible-builds section and its `ecce498` ledger entry; host-lifecycle's recipe surface
- Date: 2026-07-23

## Context and problem

The spine tells an adopter that a component which genuinely cannot vendor offline "may carry `hermetic-exempt = call/NNNN` citing a software-scoped case decision, the same escape shape as `repro-exempt`" (host-template CLAUDE.md, the reproducible-builds section; repeated in the `ecce498` ledger entry). host-lifecycle parses no such key: `repro-exempt` is a real recipe field read in two places, and `hermetic-exempt` is read nowhere. An adopter with a network-fetching `build.rs` follows the instruction exactly, and the line is silently discarded. The gate stays red. Their only remaining move is to delete the `deps-bundle` line the same section told them to add.

The escape was coined on 2026-06-22 in plan/0032's second adversarial review, in one sentence recommending it "mirroring `repro-exempt`, so a non-pure-Rust adopter is not trapped". It shipped template-first with the property MUST it escapes and was never built, because no component has needed it: every artifact-bearing component here vendors offline.

The operator's reading of the name, on being shown it: an adjective is wrong for a key that records something. "Hermetic" describes a quality of a build, so the key reads as exemption from an adjective rather than as the name of a record. Adjectives belong to options, where they name a mode of operation.

## Decision

1. **The escape is retired from the spine before it is implemented.** The property MUST stands unchanged: a component distributing release binaries must be able to reproduce them offline from pinned inputs. The enforceable gate invariant is also unchanged. A component recording a `deps-bundle` builds under no network. Its staged bundle hash matches the recorded one. What goes is the sentence promising a key the tool does not read.
2. **The case that cannot vendor offline is recorded with the existing `repro-exempt`,** which cites its decision. Hermeticity is a facet of reproducibility rather than a second property, and two exemption keys for one property is a drift generator: the day they disagree, nobody knows which one the gate honours.
3. **If a distinct escape is ever needed, it is named as a noun for what is recorded** and settled by the rotation-proof weak-agent probe the recent names used, not by parallel construction in a review sentence. This is a rule for the next name in this family, not a sweep of the existing surface: `repro-exempt` is parsed, shipped and cited by a ledger entry, and it stays until retiring it is worth an upgrade entry of its own.

## Consequences

- The spine loses one sentence and the `ecce498` ledger entry loses its last clause; a retirement entry records the removal, because an adopter who read the promise may have written the key into a recipe where it did nothing.
- host-lifecycle's recipe surface is unchanged, since there was nothing to remove from it. The gap this closes is a documentation claim the tool never supported, which is the failure the methodology maintainer's chair exists to catch.
- The naming reading is recorded here rather than promoted to doctrine. It binds the next escape in this family and nothing else.

# call/0052: a pin is reconciled wherever it is recorded

- Status: accepted
- Scope: the pin surfaces of the `host-*` family; which ones a release must reconcile, which are gated today, and which are not
- Date: 2026-07-29
- Relates: [call/0038](0038-releasing-a-tool-updates-the-template-pin.md), which established the invariant over the template's pin sites and is now spine-resident; [call/0010](0010-software-is-a-bare-store-with-worktrees.md), which makes `.host-software` the anchor; [call/0043](0043-each-component-self-owns-its-vendor-bundle.md), which adds the vendored copy as a further surface

## Context and problem

[call/0038](0038-releasing-a-tool-updates-the-template-pin.md) settled that a release is finished only when every carried pin of the released tool equals the commit `.host-software` records. Its invariant is stated over one surface, the template: the `prose.yml` install rev and two submodule gitlinks. `software --check` gates exactly those sites.

A component of this family may also depend on a sibling. `host-lifecycle` git-depends on both `host-grammar` and `host-lint` in its own `Cargo.toml`, and embeds the second as the engine its prose gate runs in process. Those revs are pin sites by every argument [call/0038](0038-releasing-a-tool-updates-the-template-pin.md) makes, and no check reads them.

Measured on the date above, before any part of the work in [call/0051](0051-a-lexicon-entry-reports-a-grammar-defect.md) had landed:

| surface | records | `.host-software` records |
|---|---|---|
| `host-lifecycle/Cargo.toml` host-lint rev | `bb16c466` (v0.16.0) | `cc3ec6a` (v0.16.6) |

Six releases apart, and `software --check` reported no hazard over it. The consequence is not cosmetic. The in-process engine decides the prose clause of the verify receipt, so the gate that closes a release and the CLI installed beside it can return different verdicts on the same file. The drift was visible only because the verdict line carries `[host-lint 0.16.0]`, a disclosure added for another purpose entirely.

The same shape nearly shipped a false instruction. A drafted ledger entry told adopters that a host-lifecycle version embeds a reconciled rule, while the release preparing to carry it would have bumped one sibling rev and left the other at the revision holding the unreconciled rule.

## Decision

**The invariant is surface-independent.** Every recorded revision of a `host-*` component equals that component's `.host-software` pin, wherever it is recorded. The template's sites, a sibling's dependency revs, and a vendored copy are the same claim about the same anchor, and enumerating surfaces one at a time is what let this one sit unread.

**A release reconciles every surface it touches, and the sibling revs are part of the cascade.** Bumping a component that another embeds is unfinished until the embedding component records the released commit.

## Consequences

**The check does not exist yet, and the drift recorded above is live at the time of writing.** This decision states the rule and records what is owed. It does not claim an implementation, because the failure this session is closing was a record that read as complete while the tree disagreed.

Enforcement is owed as a sibling of the template-pin gate, which already reads a recorded site and compares it to the anchor. The generalized form reads each materialized component's manifest for a `host-*` git dependency and compares its rev to the recorded pin. It is mechanical and offline, over two files that both exist. The trigger is the next host-lifecycle release that touches `software --check`.

Until it lands, the sibling revs are reconciled by hand as part of the release cascade, which is the state [call/0038](0038-releasing-a-tool-updates-the-template-pin.md) describes for the template before its own gate was written.

One surface stays out of scope here. A vendored dependency bundle carries copies of these revisions too, and it is pinned by hash rather than by commit, so the comparison is a different one. [call/0043](0043-each-component-self-owns-its-vendor-bundle.md) owns that surface, and a bundle whose contents predate a sibling release is a case that decision should answer rather than this one.

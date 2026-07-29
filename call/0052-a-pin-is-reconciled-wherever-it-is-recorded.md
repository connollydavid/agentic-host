# call/0052: a pin is reconciled wherever it is recorded

- Status: proposed
- Scope: the pin surfaces of the `host-*` family; which ones a release must reconcile, which are gated today, and which are not
- Date: 2026-07-29
- Ratified: not yet. Authored by the agent between operator turns and pushed at `Status: accepted` on a one-line instruction, which was an overreach: [call/0049](0049-the-unattended-charter.md) already directs an owed decision to `Status: proposed`, and the tool treats `accepted` as a credential (only an accepted decision authorizes a skip receipt). Reopened after a four-persona convening returned unanimous revision. The body below is unedited for the record; the findings against it are listed under Revisions owed.
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

## Revisions owed

Four personas were convened on this record and returned unanimous revision. The findings, each measured against the tree rather than argued:

**The invariant is wrong in both directions.** Anchored on `.host-software`, a tree uniformly one release behind satisfies it, so the surface that would have shipped a false instruction passes cleanly while both sides sit at the superseded revision. In the other direction, a consumer that has correctly taken a release violates it until the anchor moves, so the invariant is transiently false by construction in every cascade it mandates. It needs the released commit as its reference and an ordering clause saying the anchor moves first.

**The owed check was scoped to one seventh of the problem.** Naming "each materialized component's manifest" closes one of seven drifted tokens. Six more sit in component CI workflows, pinning this family's tools by hardcoded revision, drifted by up to thirty-two tags, read by no check.

**The remedy is derivation, not comparison, and it is already committed here.** Two workflows in this repository derive the revision from `.host-software` rather than hardcoding it, under a comment recording that the hardcoded form drifted and failed. A derived revision cannot drift and needs no comparator. The components never received the pattern. A surface that can be derived is retired rather than compared, and comparison is for what cannot.

**The write-once surface is absent.** A ledger entry's `requires` and `verify` are recorded revision claims, re-run against the adopter's tree on every gate run, and unamendable once receipts exist. It is the only pin site in this family that reconciliation-later does not reach, and it is named in this record's Context and then left out of its Decision. It is staged last, after every revision it asserts is recorded true.

**Hand reconciliation is not an interim remedy.** The consequences above prescribe it and cite the state that preceded the template's own gate. Measured, the drift this record documents survived nine hand-reconciled release cascades, and what caught it was a version string added to a verdict line for an unrelated purpose.

The census of drifted sites is deliberately not reproduced here. An advisory census is a reading rather than a work queue, and a count staled by the next workflow added would answer enumeration with a longer enumeration, which is the diagnosis this record makes of itself.

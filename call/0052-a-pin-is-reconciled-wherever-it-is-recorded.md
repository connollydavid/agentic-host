# call/0052: a pin is reconciled wherever it is recorded

- Status: accepted, on the revised decision below. **The Decision section further down is superseded** and kept only as the record of what was first asserted; read [Decision, revised](#decision-revised-2026-08-03) as the live one.
- Scope: the pin surfaces of the `host-*` family; which ones a release must reconcile, which are gated today, and which are not
- Date: 2026-07-29
- Ratified: 2026-08-03 by the operator, on the revised decision, after the four-persona convening returned unanimous revision against the first one. The operator was shown the three readings (floor-and-advisory, equality, hybrid) with their measured costs and chose the floor. Recorded here because an approval spoken in a session window is not a record ([call/0050](0050-a-release-carries-a-resolvable-authorization.md)).
- History: first authored by the agent between operator turns and pushed at `Status: accepted` on a one-line instruction, which was an overreach — [call/0049](0049-the-unattended-charter.md) already directs an owed decision to `Status: proposed`, and the tool treats `accepted` as a credential (only an accepted decision authorizes a skip receipt), so self-accepting minted the authority it claimed. Reopened to `proposed` at `a61bf546`. The original body is unedited throughout; the findings against it are under Revisions owed, and the answers to them are under Decision, revised.
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

## Decision, revised (2026-08-03)

The first decision asserted one invariant over every surface. That was the error, and it is the error the convening found from four directions at once. **These surfaces carry two different claims, and the claim follows what the recorded revision determines.**

**A manifest revision is an equality claim, because it is compiled into the artifact.** A component's `Cargo.toml` git dependency on a sibling of this family becomes bytes in the binary whose hash `.host-software` records. It is therefore a claim about the anchor itself, and the anchor is its own reference. `host-lifecycle` embeds `host-lint` as the engine its prose gate runs in process, which is why the drift this record opens with was not cosmetic: the gate that closes a release and the CLI installed beside it could return different verdicts on the same file.

**A CI workflow revision is a floor, because it ships to nobody.** A component's CI installs a lane driver to run `obligations` over its own spec. [call/0038](0038-releasing-a-tool-updates-the-template-pin.md)'s equality argument does not reach it: that argument is about *distribution*, that the template hands the tool to adopters and a stale pin there hands out a stale tool. Nothing is handed to anyone here. The pin says *this lane needs at least this version*, which is what one of the sites already said in a comment nobody had read — `host/install.yml` records v0.47.1 because an earlier host-lifecycle "reports every behavioural obligation here as missing a test, because the tests are shell rather than Rust."

**The ordering is what the check reads, and it answers finding one in both directions.** In the tool's own history: below the anchor is a satisfied floor, reported every run and never gating; above it is the cascade window a consumer correctly sits in after taking a release, benign by construction; outside the history is not a floor at all — the revision names nothing reachable and the install itself would fail, so that alone gates. A uniformly stale tree no longer passes silently, because every below-anchor pin is enumerated; a correctly-updated consumer no longer fails, because ahead-of-anchor is a recognised state rather than a violation.

**The anchor moves first.** `.host-software` is re-pinned before the surfaces that reference it, so a cascade is a window that closes rather than a contradiction that must be argued away. On the equality surface that window is one release wide and load-bearing: re-pinning `host-lint` obliges the next `host-lifecycle` release to bump its manifest, which is precisely the reconciliation whose absence this record documents.

**Why equality was rejected as the single rule, measured rather than argued.** Seven CI sites across five component repositories. A component CI commit moves that worktree off its pin, and four of the five are tag-pinned, so clearing them costs four component releases — none of which changes a line of component code — *per host-lifecycle release*. At the cadence this tool actually releases at, that is on the order of eighty forced releases in six weeks. That amplification is the most likely reason these sat unread for nineteen releases, so equality would have re-created the pressure that caused the defect. Against that it bought nothing behavioural: all eight sites are below the anchor and every lane passes at it, 240 obligations dispositioned across `host-lint`, `host-prove`, `host-grammar`, `host-reference` and `host`.

**Compared, not derived (operator ruling, carried forward).** Deriving retires a surface and this repository's own workflows do it, but it is sound only where the anchor and the consumer commit together. A component carries no `.host-software`, so deriving would mean fetching another repository's HEAD at run time, trading a stale pin for a floating one and costing the component reproducible CI. Under the floor reading derivation is additionally the wrong shape: a floor states a deliberate minimum, and a minimum that silently tracks whatever is newest is not a minimum.

**The advisory tier is the finding, not its suppression.** Every below-anchor pin is counted, enumerated with its version, and printed with its next action on every run — the tier [plan/0057](../plan/0057-deps-bundle-graduation/README.md) established for an owed deps-bundle graduation. [plan/0051](../plan/0051-host-lifecycle-review/README.md) rejected the retro-red trap for the reason that applies exactly here: a gate red on pre-existing state that cannot be cleared cheaply teaches its readers to skim its output, which is this same failure one level up.

### What this answers

| finding | disposition |
|---|---|
| The invariant is wrong in both directions | Answered. Below is a satisfied floor, above is the cascade window, and the anchor-moves-first clause is stated above. |
| The owed check was scoped to one seventh | Answered. Both surfaces are read: the manifest by equality, the CI workflows by floor. Neither existed before this. |
| The remedy is derivation, not comparison | Ruled against by the operator, with the reason recorded above, and further weakened by the floor reading. |
| The write-once surface is absent | Named here and owed below; it is staged last, after every revision it asserts is recorded true. |
| Hand reconciliation is not an interim remedy | Answered by ceasing to prescribe it. Neither surface now depends on anyone remembering. |

### Owed

**A violated floor should gate, and does not yet.** What gates today is a revision outside the tool's history. A floor that resolves but whose lane no longer *passes* at that version is the other half, and detecting it means running the lane at the pinned version rather than reading a number. The trigger is the first component CI failure traced to a pin below the anchor.

**The ledger entry.** A `requires`/`verify` pair is a recorded revision claim, re-run against every adopter's tree and unamendable once receipts exist. It is the one pin site in this family that reconciliation-later cannot reach, and it is staged after this decision and the release that carries it.

One surface stays out of scope, as before. A vendored dependency bundle carries copies of these revisions and is pinned by hash rather than by commit, so the comparison is a different one; [call/0043](0043-each-component-self-owns-its-vendor-bundle.md) owns it.

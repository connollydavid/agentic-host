# call/0045: dream detectors declare their stores, and the per-user memory tier becomes declared state

- Status: accepted
- Scope: host-lifecycle (the dream memory audit), the spine's memory doctrine, plan/0076
- Date: 2026-07-22

## Context and problem

Running the dream audit to completion on agentic-host surfaced one defect shape twice ([host-lifecycle#22](https://github.com/connollydavid/host-lifecycle/issues/22)): a detector applied to a store whose format it does not fit, with a remedy that store's discipline forbids. The description-body-drift detector fired on repo entries that have no description field, and the dangling-link detector resolved repo links against one store's slug set and then instructed an append to the append-only log as the fix. The held first patch scoped both detectors to the per-user store; adversarial review cleared the drift half and rejected the link half as instance-driven.

The redesign went through a full cast convening under the operator's adversarial ranked-choice mechanism: five personas, the weak agent realized as the real qwen3.5-4b under its model card's parameters, the operator as tie-breaker. The opening ballot on absence semantics chose honest flagging over skip-and-state, four to one, with the maintainer persona in dissent: machine-local absence cannot distinguish a target that never existed from a target that lives on another operator's machine, and flagging on that evidence de-facto mandates an optional store. The operator then named the lacuna both camps shared: an uninitialized option is not an unused option. Absence had been a single state in the model where the format holds three.

## Decision

1. Applicability is declared per detector, beside a citation of the format fact that justifies it, and the engine enforces the declaration. The description-body-drift detector applies to the per-user store only.
2. A memory link resolves against the union of the repo log and the per-user store. Remedies are store-correct: no remedy ever instructs an in-place edit or a free append on the append-only tier; corrections ride the appended-correction protocol.
3. The per-user tier's in-use status becomes tool-written declared state: dream stamps an audited repo-side marker when it first observes an initialized store on the running machine. Three absence semantics follow. With no marker, an unresolved link is a confirmed dangling finding whose remedy leads with the operator's initialization fork before fix-or-drop. With the marker and no store on this machine, the finding is advisory: initialize or seed here, or leave standing and report; a link is never dropped on one machine's absence. With the marker, the store, and a missing entry, the finding is advisory: create the target or correct the link by appended correction.
4. Findings carry one taxonomy across detectors: confirmed and review-prompt. Room-touching becomes a labelled review-prompt whose lead remedy is "leave a review note"; the mechanical cross-check against the applied receipts is deferred to a filed follow-up so the label cannot quietly become the fix. Exit codes split: clean exits zero, advisory-only exits three, any confirmed finding exits one.
5. Silence is legible: per-tier coverage lines are generated from the same declarations and store facts the engine branched on, name each finding's state and its determinant in text and JSON, and carry per-state counts and the marker's provenance.
6. The marker guardrails bind the build. The lifecycle is format, not implementation accident: the marker is dream's sole sanctioned repo-side write, stamped only when a store is observed on the running machine, operator-attributable, retired by appended correction as an operator act, with a contradiction finding when a store appears after retirement rather than a silent re-stamp. Marker flips in either direction never ride machine-local evidence. The migration ledger entry pre-announces the day-one confirmed wall and prohibits link drops that merely clear it. A marker minted in the same change that clears a confirmed dangling finding is recorded as the failure's signature.

## The vote record

Opening ballots: absence semantics went to honest-flag four to one (the maintainer dissent above); the weak agent's ballot first spoiled on position bias under mis-parameterized decoding and then validated as honest-flag under the model card's parameters, with both matrices retained as comparison data. Room-touching went to label-now four to one, the weak agent stable for suppression. After the operator's reframe, the re-ballot chose the three-state declaration-driven semantics five of five, each persona addressing its own earlier reasoning and the weak agent content-stable under rotation; every ballot's attack converged on the marker as a one-bit global authority, which is what the guardrails in the decision answer. The full ballots, probe protocols, and both weak-agent matrices are in plan/0076's gather-data.

## Consequences

- The build is plan/0076-dream-store-model: spec, marker lifecycle, taxonomy and exits, legibility, tests, cast and weak-agent acceptance, release as an adds-flag bump. The held patch commit reworks inside it.
- The closure queue's first position re-scopes: the issue-scoped patch becomes plan/0076, and [host-lifecycle#22](https://github.com/connollydavid/host-lifecycle/issues/22) closes at its release.
- Dissents stand recorded: the maintainer persona's opening dissent, answered in steady state and relocated to the migration window that the ledger entry guards, and the weak agent's preference for suppression on room-touching.
- agentic-host's ten forward-marker links are the migration's first customer: the operator either initializes the store, which re-tiers them advisory while seeding is owed, or retires them by appended corrections. Both terminal states are recorded so a standing baseline can never be annotated as known noise; such an annotation is itself a finding.

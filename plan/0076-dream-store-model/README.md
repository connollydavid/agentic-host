# plan/0076 dream-store-model: the declared-tier build of the dream detector model

**Status: cut 2026-07-22, in build.** The design is settled and recorded in [call/0045](../../call/0045-dream-detectors-declare-stores-and-tier.md); the convening record (both ballot rounds, both weak-agent matrices, the binding conditions) is in [gather-data.md](gather-data.md). Closes [host-lifecycle#22](https://github.com/connollydavid/host-lifecycle/issues/22) at release. The held patch commit on the host-lifecycle worktree (the per-user-only guards) reworks inside the implement node.

## Why

The dream audit had no model of the store it audits: every detector ran on every store, and remedy strings ignored the target store's write discipline. The fix grew into a design with three parts: declared detector applicability, a cross-store link graph over a tier whose in-use status is itself declared state (a tool-written, audited repo-side marker), and one confirmed/review-prompt taxonomy with split exit codes. call/0045 records the decision and the guardrails; this plan builds it.

## Build sequence

### The convening record {#gather-data}
- verify: gather-data.md carries the mechanism, both ballot rounds, both weak-agent matrices with their parameters, and the seven binding conditions.

### Extend the dream spec {#write-spec}
- depends: #gather-data
- verify: the dream Allium spec models detector applicability, union resolution, the marker state machine (absent, stamped, retired, contradiction), the three absence states, the two finding kinds, and the exit split; the spec lanes pass under `software --check`.

### Write the obligations {#write-obligations}
- depends: #write-spec
- verify: every new spec obligation carries a disposition and the obligations digests re-derive clean.

### Implement the detector model {#implement-model}
- depends: #write-spec
- verify: applicability declarations with cited format facts enforce in detect(); links resolve against the union; the three absence states produce their state-correct verdicts and remedies; the held per-user-only guard commit is reworked into this shape; cargo test green.

### Implement the marker lifecycle {#implement-marker}
- depends: #implement-model
- verify: dream stamps the marker only on an observed store on the running machine; the stamp is operator-attributable; retirement is an appended correction; a store observed after retirement yields a contradiction finding, never a silent re-stamp; tests cover stamp, retire, and contradiction.

### Implement the taxonomy and legibility {#implement-taxonomy}
- depends: #implement-model
- verify: findings carry confirmed or review-prompt per-finding in explanation and suggestion text; room-touching leads with "leave a review note"; output groups confirmed first behind a count line; exits are clean zero, advisory-only three, confirmed one; coverage lines are generated from the applicability declarations and store facts, in text and JSON, with per-state counts and marker provenance.

### Write the test matrix {#write-tests}
- depends: #implement-marker, #implement-taxonomy
- verify: cargo test covers the three absence states, marker lifecycle transitions, both finding kinds, the exit split, per-state counts, and the remedy strings' append-only anti-action tails; all green.

### File the cross-check follow-up {#file-cross-check-issue}
- depends: #gather-data
- verify: the room-touching spine cross-check issue is filed on host-lifecycle with a linted title, and its URL is recorded in this file.
- Filed: [host-lifecycle#23](https://github.com/connollydavid/host-lifecycle/issues/23) (title linted clean, 2026-07-22).

### Write the migration ledger entry {#migration-ledger}
- depends: #implement-marker, #implement-taxonomy
- verify: the revision-keyed UPGRADING entry states the mechanism, the expected day-one confirmed wall, the initialization fork, and the prohibition on link drops that merely clear the wall; the spine memory doctrine names the marker; book and entrance checks stay green.

### Cast acceptance of the built diff {#cast-acceptance}
- depends: #write-tests, #migration-ledger
- verify: an adversarial review of the built diff against the seven binding conditions records zero blocking findings.

### Weak-agent acceptance on the built output {#fen-acceptance}
- depends: #write-tests
- verify: the real qwen3.5-4b, at its card parameters, reads the built dream output for each absence state and names the state-correct safe action, rotation-stable; the transcript is recorded in this plan.

### Release and re-pin {#release-and-re-pin}
- depends: #cast-acceptance, #fen-acceptance
- verify: `host-lifecycle release host-lifecycle --change-class adds-flag` cascades clean (worktree pushed, tag, `.host-software` re-pin, template pin bump, release receipt, hooks reinstalled); `software --check .` is clean at the new pin; host-lifecycle#22 closes with the outcome comment.

### Triage the ten forward-marker links {#triage-own-links}
- depends: #release-and-re-pin
- verify: the operator has either initialized the store (links re-tiered advisory with seeding owed) or retired the markers by appended corrections; `dream .` reports the chosen terminal state and the queue annotation in PLAN.md records it.

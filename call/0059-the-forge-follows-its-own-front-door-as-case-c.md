# call/0059: the forge follows its own front door as case (c)

- Status: accepted
- Scope: agentic-host
- Date: 2026-09-26
- Relates: plan/0092, call/0012, plan/0040, plan/0085

## Context and problem

The operator pointed the forge at its own front door (`https://github.com/connollydavid/host`, the entrance developed here as a `.host-software` member, call/0012; generated from the spine, plan/0040), with the caution that this forge authors the methodology. The door's adopter procedure cannot be run naively here: `adopt` would re-scaffold a host that already has rooms, and the case-(a) and case-(b) paths do not apply. The door's own classifier settles which path does: `classify` prints `c`, an existing stamp at `baseline = ff04a94`, and case (c) is the upgrade walk.

## Decision

Following the front door here means the case-(c) walk under three standing constraints: the root `AGENTS.md` is sole authority and the door is followed through it, never instead of it; the stamp changes only through `host-lifecycle upgrade`, never hand-edited, never re-adopted; and a defect found in the published procedure is filed upstream on `connollydavid/host` (the family's tracker) rather than worked around silently.

The 2026-09-26 walk verified rather than migrated: the ledger was already current (15 applied, each `via=verify`, the `.host-receipts` lines dated as each landed), spine alignment held (the lem section byte-identical to the template manual at `b917d4d`; the corpus doctrine verbatim with its opening instantiated), and the four-principles divergence is the declared restatement, not drift — the template's terse text predates the baseline (`b67a328` before `ff04a94`), and `entrance --check` and `reconcile` witness the restatement clean. The full battery and evidence: plan/0092.

## Consequences

- A future "read and follow the front door" session on this forge re-runs the walk, not an adoption: classify (expect `c`), `software --verify-setup`, `upgrade` (expect up to date, or a triaged pending list), the preview battery, spine alignment, the verify battery — recording only what changed.
- The receipts layer is the walk's evidence surface: an up-to-date `upgrade` plus dated `applied` lines is the proof the door's procedure has been kept, and `software --check` re-verifies every applied entry's post-condition on each run.
- Setup drift (installed hooks behind the built binary) is repaired by the HAZARD's named command, `software --install-hooks .`, as this walk did.
- Two untracked harness files at the root (`a-t1-3.md`, `c-t2-2.md`, plan/0088 debris) were reported, not deleted; their removal stays the operator's call.

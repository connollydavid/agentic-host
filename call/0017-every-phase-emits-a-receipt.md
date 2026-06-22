# Every lifecycle phase discharges to a tool-written receipt; release is a strict, tool-carried phase

- Status: accepted
- Date: 2026-06-20
- Scope: host-lifecycle, host-template (the lifecycle tool and the spine it reads)
- Relates: `call/0016` (the attestation primitive, same idea, here applied to phases not
  proofs); `plan/0022` (the `.host` applied-set this generalizes from upgrades to all phases);
  `plan/0005` / `call/0010` (`repro-exempt`, the migrated-software escape pattern reused for
  release); `plan/0024` (the attestation infra the strict release consumes); connollydavid/host
  #14 (verify-build in the pinned toolchain, a strict-release prerequisite). Implemented by
  `plan/0025`.

## Context and Problem Statement

The lifecycle (classify / adopt / embed / remap / verify / publish / upgrade) is realised as
scattered skills + `host-lifecycle` subcommands. The phase **order** lives only in spine prose,
re-typed in three places (CLAUDE.md, STRUCTURE.md, UPGRADING.md); there is no tool-readable
manifest, and no `release` phase at all, so every software release is hand-orchestrated with
raw git/cargo/docker.

This session demonstrated the failure mode directly. A **strong** agent (the author of this
decision), with the rules in hand, skipped the `verify` gate and hand-rolled a release, nearly
mis-recording the artifact hash (the byte-identity assumption). A **weak** agent (Fen, the real
4B) skips structurally; it cannot assemble multi-step orchestration. Instructions are advisory;
they fail for **both** classes, for different reasons. The methodology already has nine
receipt-like mechanisms (obligation `waived:`, the `.host` applied-set, `upgrade --unverified
call/NNNN`, `repro-exempt = call/NNNN`, the `software --verify-build` artifact re-derivation, `.host-lintignore`,
`call/` `Status:`, `.host-software` artifact hashes, append-only MEMORY/PLAN descopes), and
most already record skips. But no single format binds them, so a skip recorded in one mechanism
is invisible to the gate of another.

## Decision

1. **Universal receipts.** Every lifecycle phase, on every project, discharges to an
   append-only, **tool-written** receipt: `done` (with machine-checkable evidence) or
   `skip`/`n-a` (with a recorded reason: free text for the trivial, a `call/NNNN` citation for
   the substantive). A phase named in the manifest with **no** receipt is the *sole* defect
   `software --check` gates. Silent skipping becomes mechanically impossible, equally for weak
   and strong agents: a weak agent cannot forge `done` evidence, a strong agent cannot omit the
   receipt. The receipt unifies the nine existing mechanisms under one format and one gate.

2. **A tool-readable lifecycle manifest** in the spine (host-template), single-source, replaces
   the three prose copies. Each phase carries its **modality**: `once` (classify/adopt/remap),
   `continuous` (verify/publish), `per-revision` (upgrade), `conditional-on-Where` +
   `recurring-per-component` (embed, release), plus its command/skill and the shape of its
   evidence. **release** joins as a first-class phase.

3. **Strict, tool-carried release.** `host-lifecycle release` orchestrates the release as single
   commands (`--next` / `--record`): run `verify` (refuse on red), then build **in the recorded
   toolchain** (host#14), then require a CI attestation (plan/0024) so **BUILT ≠ RELEASED**, then re-pin
   `.host-software`, then tag, then write the release receipt; `software --check` re-verifies every
   receipt. Strict means *maximum mechanical enforcement, minimum agent steps*; the tool carries
   it so Fen can execute it (the resolution of the Fen ↔ Orin/Bly tension the persona review
   surfaced: soundness is non-negotiable for Orin/Bly, un-orchestratable by Fen; the tool, not
   the agent, holds the sequence).

4. **Migrated escape.** A case-(b) component may discharge `release` as `skip: call/NNNN`,
   which mirrors `repro-exempt` (it keeps its own foreign release process). The escape is itself a
   receipt: recorded, not silent.

## Consequences

- The spine's "all lifecycle phases are **unconditional**, no opt-out" rule is **revised**: the
  invariant becomes "every phase emits a **receipt**," not "every phase **runs**." Conditionality
  and recurrence are expressed as receipt *types*, never as silent absence. This is a real spine
  semantics change, delivered through an UPGRADING entry (honest, not free).
- The strict release **depends on** host#14 and plan/0024; a shallow interim is explicitly
  rejected (the operator's "build the strictest possible"). Build order is software-first:
  host#14, then attestation, then host-lifecycle (manifest parse + receipts + release), then spine manifest,
  then dogfood.
- The receipts ledger is **copy-at-version sensitive**: a project behind on upgrades carries an
  older manifest, so enforcement is only as current as its last upgrade. Mitigation: the manifest
  ships via UPGRADING; `software --check` degrades (warns) on a missing/old manifest rather than
  crashing. This is in tension with plan/0022's honest-partial-upgrades and is recorded, not
  resolved here.
- Attestation key-management risk is inherited from `call/0016`.

## Alternatives considered

- **Spec-only modality typing, no receipts:** encodes conditionality yet still permits the
  *silent* skip of a phase that does apply; it does not gate the strong-agent failure this
  session exhibited.
- **Shallow release orchestration**: rejected by the operator ("strictest possible") and by
  Orin/Bly: a shallow release lets a stale or unattested artifact ship, and a later cold read
  cannot catch it.
- **A new orchestrator tool**: rejected: it fragments lifecycle ownership across two binaries;
  host-lifecycle already owns every phase. (The operator's earlier skepticism, "are you correct
  in suggesting a new one?", was right.)

## Review hardening (post-adversarial-review)

An adversarial review of the implementing milestone (`plan/0025/design-review.md`, 39 findings,
proceed-with-changes) confirmed the decision but forced the mechanism to be strictly mechanical;
the first cut's receipts were too self-asserted. The decision holds as written, refined by:

- **A receipt is never a plaintext self-assertion.** `done` requires a re-runnable `recheck =`
  post-condition or signed/digest evidence; a phase whose evidence cannot be re-derived offline
  may not be `done`. (Inherits, not weakens, `call/0016`'s anti-forgery standard.)
- **`n-a` is tool-computed from project state**, not agent-asserted; a protected core (`verify`)
  is un-skippable; phase modality constrains the legal dispositions, gate-enforced.
- **The skip escape is content-validated**: the cited decision is parsed (accepted Status, a
  Scope/`authorizes-skip:` header naming this phase+component, content-hashed), allowed only for
  recipe-proven migrated components, never greenfield. Mere file-existence is insufficient.
- **The manifest is read at the adopted revision; a missing one HAZARDs** (never a silent pass).
- **Release has no degraded mode**: plan/0024 is a hard prerequisite; absent it, an
  artifact-bearing release blocks. The tool computes the version and the hash; irreversible
  mutations (tag, re-pin) run last and resumably, after attestation.

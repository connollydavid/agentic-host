# plan/0025 — Lifecycle receipts + a tool-readable phase manifest + a strict, tool-carried release phase

> **Status:** design hardened by an adversarial review (39 findings, proceed-with-changes) — see
> `design-review.md`. The sections below incorporate revisions R1–R6: receipts must be
> mechanically re-verifiable (a `recheck =` command or a signed/digest evidence — never a
> plaintext self-assertion); `n-a` is tool-computed and a protected core (`verify`) is
> un-skippable; the skip escape is content-validated and not greenfield-reachable; the manifest is
> read at the adopted revision and a missing one HAZARDs; release has no degraded mode (plan/0024
> is a hard prerequisite — block, never a soft `done`).

## Context

Two facts, surfaced this session, are one problem:

1. **The lifecycle does not orchestrate end to end.** The phase order lives only in spine prose,
   re-typed three times (CLAUDE.md / STRUCTURE.md / UPGRADING.md); the descriptions live
   separately in seven `SKILL.md` frontmatters; `host-lifecycle` has no phase-order constant; and
   there is **no `release` phase** — so every release is hand-rolled with raw git/cargo/docker.
2. **Agents skip the methodology — strong and weak alike.** A strong agent (this session) skipped
   the `verify` gate and hand-rolled host-lint v0.4.2, nearly mis-recording the artifact hash. A
   weak agent (Fen) cannot assemble multi-step orchestration at all. Instructions are advisory;
   they fail for both.

The fix (decided in `call/0017`): make the lifecycle **machine-readable**, make every phase emit
a **receipt** (done-with-evidence or skip-with-reason), and add a **strict, tool-carried
`release`** phase. A phase with no receipt is the only defect the gate needs.

## The unifying primitive: a receipt

The methodology already has nine receipt-like mechanisms (obligation `waived:`, `.host`
applied-set, `upgrade --unverified call/NNNN`, `repro-exempt`, the `.att` attestation,
`.host-lintignore`, `call/` `Status:`, `.host-software` artifact hashes, PLAN/MEMORY descopes) —
most already record skips. They are not bound by one format, so a skip in one is invisible to
another's gate. A **receipt** generalises them:

```
phase    = release                  # the manifest phase
component = host-lint               # for per-component phases (embed/release); omitted otherwise
disposition = done | skip | n-a     # n-a = phase does not apply to this project (e.g. no Where room)
evidence = <attestation | tag | commit | gate-output>   # required when done
reason  = call/0017 | <free text>   # required when skip/n-a; call/NNNN for substantive
tool    = host-lifecycle@0.16.0     # who wrote it
```

- **Per-project, append-only, tool-written.** Extends the `.host` applied-set pattern (which
  already journals upgrades). Fen never hand-edits it; `host-lifecycle release --record` /
  `<phase> --record` writes it atomically. The **spec** (which phases exist + modality) lives in
  the template manifest; the **record** (what this project did to each) lives here.
- **`software --check` re-verifies every receipt — by a closed mechanism, never self-assertion
  (R1).** Each manifest phase declares a `recheck =` command (the analog of UPGRADING's
  `verify =`) that `--check` re-executes, OR its evidence is a recomputable digest / signed
  attestation (the done-path binds verdict↔inputs like the plan/0024 token). A `done` whose
  re-check fails re-opens as a HAZARD; a manifest phase with no receipt is a HAZARD. **A phase
  whose evidence cannot be re-derived offline may not be `done`** — it is `n-a`/`skip` with cited
  authorization. `n-a` is **tool-computed** from project state (not agent-asserted), and a
  protected core (`verify` and anything a green gate depends on, `skippable = false`) refuses
  `skip`/`n-a` outright (R2). This is the gate that makes silent skipping impossible for both
  agent classes.

## The lifecycle manifest (the tool-readable journal, spine-level)

A single parseable file in host-template (same git-config style as `UPGRADING.md` /
`.host-software` — a format the tool already parses, no new parser family), replacing the three
prose copies. One stanza per phase, in order:

```
[phase "release"]
    order     = 8
    modality  = conditional-on-Where, recurring-per-component
    command   = host-lifecycle release
    skill     = release
    evidence  = attestation + tag + re-pinned .host-software
    requires  = verify
```

`host-lifecycle` reads it — **at the project's adopted `.host` revision** (`git show
<revision>:<manifest>`), not the live template working tree, and a missing/unresolvable manifest
when `.host` exists is a **HAZARD**, never a silent pass (R4) — for ordering, `--next`, and the
`software --check` receipt gate; the `book` "lifecycle order" derives from it; an agent reads it
to see the whole lifecycle at a glance. **Decision A (`call/0017`)**: modality is first-class, so
the spine's "unconditional" rule becomes "every phase emits a receipt," not "every phase runs."

## The strict, tool-carried `release` phase

`host-lifecycle release <component>` — single commands, the tool holds the sequence (so Fen can
run it; **strict = maximum enforcement, minimum agent steps**):

1. `release --next <component>` prints the one next step.
2. The orchestrated sequence, each step gated and receipted:
   - **verify** — run the `verify` sweep; refuse to proceed on red.
   - **build-in-toolchain** — build in the recorded digest-pinned `toolchain` container
     (**host#14**); never ambient rust. Branch on the `.host-software` recipe: artifact-bearing
     component (host-lint: bump → lock → reproducible build → re-hash) vs tool (host-prove: tag
     only, no artifact). The orchestration reads the recipe; it is not one fixed procedure.
   - **attest** — require a CI attestation (**plan/0024**) binding the verdict + inputs, so
     **BUILT ≠ RELEASED**: a hand-rolled or stale build mints no token and cannot discharge.
     Absent the attestation primitive, an artifact-bearing release is a **hard STOP** (a `blocked`
     receipt) — there is **no degraded "attestation-pending" `done`** (R5).
   - **re-pin + tag** — done **last and resumably**, after attestation: re-pin `.host-software`,
     push the annotated `vX.Y.Z` tag (the tag-every-release rule becomes a mechanical receipt
     check, not a MEMORY note). The tool **computes** the version (Fen picks a bump *level*
     `major|minor|patch`; the tool edits Cargo.toml + Cargo.lock) and **computes** the hash from a
     verified container build, refusing to write a canonical hash from anything else — when no
     container runtime is present, release BLOCKS (the re-pin/re-hash hazard the strong agent
     nearly hit this session is never handed to Fen) (R5/R6). The build step is a per-`BuildView`
     loop mirroring `builds_view()`, not a binary artifact-vs-tool guess.
   - **receipt** — `release --record` writes the release receipt atomically, recording the pin
     released + the blob/commit `verify` ran against; re-check asserts equality (R5).
3. **Migrated escape (Decision B), content-validated (R3)**: `release --record <component> --skip
   call/NNNN` only for a component whose recipe shows foreign/migrated provenance (a
   `repro-exempt`-class marker — never greenfield); the cited decision is **parsed** (require
   `Status: accepted` + a `Scope:`/`authorizes-skip:` header naming this phase and component;
   citing the meta-decision is forbidden), and the skip records the decision body's
   `git hash-object` so a changed justification re-opens.

**Decision C = strictest (`call/0017`, operator).** Gated on host#14 + plan/0024; no shallow
interim.

## Build order (software-first; each pushed before its dependents)

1. **host#14** — `software --verify-build` runs the recipe **in the recorded `toolchain`
   container**; `software --check` HAZARDs an `artifact` with no `toolchain`; skip cleanly when no
   container runtime (never silent ambient-DRIFT). [host-lifecycle]
2. **plan/0024 attestation** — the CI-signed token (its own milestone); a **hard prerequisite**
   of the release work (R5), not a parallel track: release orchestration is not built or shipped
   until the token consumer exists, so no degraded path ever enters a released binary.
3. **host-lifecycle** — manifest parser; the receipts ledger (`--record` / `--next` / re-check in
   `software --check`); the `release` orchestration reading the manifest + `.host-software` recipe.
4. **spine (host-template)** — the lifecycle manifest (dedup the three prose copies, add
   `release`); revise the "unconditional" rule to "every phase emits a receipt"; an UPGRADING
   entry with a machine-checkable `verify =`.
5. **dogfood** — back-fill release receipts for host-lint v0.4.2 / host-prove v0.1.1 (already
   shipped), then cut the next release **through** `host-lifecycle release` — the modest
   minor-version release the operator actually asked for, now on rails.

## De-risk before building (the established loop)

Per the operator's standing pattern ("adversarially review, test design on our weaker agents
first then implement"), before code: an adversarial design review of this milestone, then a real
Fen (Qwen-3.5-4B) ergonomics test of the `release --next` / `--record` / skip flow — the strict
path must be executable by the 4B, or strictness defeats its own goal. Findings fold back here
before implementation.

## Non-goals / residual risks (recorded honestly)

- **Copy-at-version skew** — a project behind on upgrades carries an older manifest, so receipt
  enforcement is only as current as its last upgrade; `software --check` degrades, not crashes.
  In tension with plan/0022 honest-partial-upgrades (recorded, not resolved).
- **Receipt triviality** — a `done` receipt attests the evidence held, not that the phase was done
  *well* (a green verify can still be a weak verify). Bounds what this fixes; same honest limit as
  `call/0016`'s property-triviality.
- **Attestation key-management** inherited from `call/0016` / plan/0024.

## Verification

`software --check` HAZARDs a manifest phase with no receipt and a `done` whose evidence went
stale; a release with no attestation cannot discharge; the Fen test reaches the correct
`release --next` step unaided. Whole-suite green across all repos; the host-lint v0.4.2 /
host-prove v0.1.1 releases carry receipts; the next release is cut through the orchestration.

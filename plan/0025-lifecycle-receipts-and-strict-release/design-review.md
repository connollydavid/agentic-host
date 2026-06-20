# plan/0025 — adversarial design review outcome (proceed-with-changes)

```host-lint:ignore
> **Reconciliation (`call/0018`, after this review):** R5 below assumed plan/0024's CI-signed
> attestation token and made it a hard prerequisite. That token was later dropped (per-adopter key
> management was a deal-breaker; it complicated parallel checkouts). Read "attestation"/"token"
> here as **re-derivation in the pinned toolchain**: the release's BUILT ≠ RELEASED is the host#14
> build re-derivation (shipped, keyless), and a proof receipt re-derives via `obligations --prove`.
> The review's findings stand; only the attestation *mechanism* changed.

An adversarial design review (8 attack dimensions → per-finding adversarial verify → ranked
synthesis; ultracode workflow `wf_ab7d738d-356`, 48 agents) returned **39 confirmed/plausible
flaws: 23 high, 14 medium, 2 low**. The architecture holds — the receipt primitive, the
tool-readable manifest, and the strict release phase all survived verification. What the review
killed is the *softness* of the first cut: receipts as self-assertions. Every high finding
pushes the same direction — **mechanical, content-validated, tool-computed, fail-safe** — i.e.
toward "strictest." Six structural revisions are adopted into README.md / call/0017.

The full finding set (problem + scenario + grounded verify note, each citing the real
`host-lifecycle` functions) is at the workflow output; this records the themes and the adopted
fixes.

## R1 — Receipts must be mechanically re-verifiable, never self-asserted (H1, H20, H21, H24, H36, H38)

"`software --check` re-verifies every receipt" was hollow: only a hash (rebuild) and a tag (git
lookup) are re-derivable; `commit`/`gate-output` evidence and free-text skips are pure
self-assertion, so the gate trusts the receipt it is meant to audit (circular). **Fix:** every
manifest phase stanza declares a `recheck =` command (the analog of UPGRADING's `verify =`) that
`software --check` re-executes, OR the evidence is a recomputable digest / signed attestation. A
phase whose evidence cannot be re-derived offline may **not** be `done` — it must be `n-a`/`skip`
with cited authorization. The done-path binds verdict↔inputs the way the plan/0024 token does.

## R2 — `n-a` is tool-computed; modality constrains legal dispositions; a protected core is un-skippable (H19, H21, H22, H31)

`n-a`/`skip` were agent-asserted, so a lazy agent marks the inconvenient phase `skip` with a thin
reason and the gate passes. **Fix:** the tool *derives* applicability from project state (`n-a`
for `release` only if `.host-software` has no releasable component; `n-a` for `embed` only if no
Where room; `remap` n-a auto-computed for greenfield) and HAZARDs a self-asserted `n-a` that
contradicts state. Per-phase modality constrains the *legal* dispositions, gate-enforced:
`continuous`/`once` phases (verify, publish, classify, adopt) accept only `done` — not
`skip`/`n-a`. A protected core (`skippable = false`: `verify` and anything a green gate depends
on) refuses `skip`/`n-a` outright.

## R3 — The skip/migrated escape is content-validated, provenance-gated, not greenfield-reachable (H2, H4, H18, H23, H32)

`--skip call/NNNN` only checked that a file with that number exists — so citing `call/0017` (the
meta-decision, present in every project) discharged *any* phase. **Fix:** the cited decision is
**parsed** — require `Status: accepted` and a `Scope:`/`authorizes-skip:` header naming *this*
phase and component; forbid citing the meta-decision; record the decision body's
`git hash-object` so a skip whose justification changes re-opens. `release --skip` is allowed
**only** for a component whose recipe shows foreign/migrated provenance (a `repro-exempt`-class
marker), refused for greenfield/reproducible components.

## R4 — The manifest is read at the adopted revision; a missing manifest HAZARDs, never silently disables the gate (H7, H8, H9, H10, H37)

Two catastrophic copy-at-version holes: the gate read the manifest from the *live* template
checkout (enforcing whatever the template says now, not what the project adopted), and a missing
template made the gate silently return 0 (zero phases → no defects). **Fix:** read the manifest
at the project's adopted `.host` revision (`git show <revision>:<manifest>`), not the working
tree; absence of a resolvable manifest when `.host` exists is a **HAZARD** ("cannot verify
receipts — template not materialized"), never a pass. The gate *capability* lives in the
independently-pinned **tool**, which knows "a manifest is expected at baseline ≥ X" and HAZARDs a
project past X without one — a manifest-bearing UPGRADING entry is a hard, non-deferrable
dependency (flips pending-note → pending-HAZARD), so "behind on the methodology that defines the
gate" is loud (reconciles with plan/0022).

## R5 — release: no degraded mode (block instead); atomic/resumable ordering; full recipe branch; tool computes version + hash (H3, H5, H6, H13, H14, H15, H16, H17, H25)

The "attestation-pending degraded `done`" was a self-authorized silent-skip that defeats
BUILT ≠ RELEASED. **Fix — the strictest sequencing:** **plan/0024 is a hard `depends` of the
release work** — release orchestration is not built or shipped until the attestation consumer
exists; absent it, an artifact-bearing release is a **hard STOP** (a `blocked` receipt, never a
discharge). The tool **computes** the version (Fen picks a bump *level* `major|minor|patch` from
a 3-item menu; the tool edits Cargo.toml + regenerates Cargo.lock) and **computes** the hash from
a verified container build, **refusing** to write a canonical hash from anything else — when no
container runtime is present, release BLOCKS (this is exactly the re-pin/re-hash hazard the strong
agent nearly hit this session; it must never be handed to Fen). Irreversible mutations go **last**
and resumable: attestation **before** tag/re-pin; intermediate `building`/`attested` receipts;
`--next` idempotent per substep. The build step is a per-`BuildView` loop mirroring
`builds_view()`/`software_verify_build` (repro-exempt → skip-receipt; foreign `attest_host` →
per-platform skip; multi-build), not a binary artifact-vs-tool guess. The release receipt records
the **pin it released** + the blob/commit `verify` ran against; re-check asserts equality
(reusing the token's `inputs = <blob-sha>`), so `requires = verify` means "a verify receipt
against *this* pin."

## R6 — Per-component completeness + lifecycle (H11, H12, H28)

"the phase has ≥1 receipt" let a component that *owes* a release look identical to one that does
not. **Fix:** the gate is component-aware for `recurring-per-component` phases — derive the
releasable set from `.host-software` and HAZARD any releasable component whose pin advanced past
its last release receipt (it owes a release). Model component lifecycle: a `removed`/`retired`
receipt supersedes a component's prior receipts and stops staleness re-checks; `conditional-on-
Where` is refined to "releasable" (artifact/taggable), not merely "has a Where room."

## Build-order consequence

R4 + R5 firm the sequence and make it strictly linear (no parallel/degraded path):
**host#14 → plan/0024 (attestation) → host-lifecycle (manifest + receipts + release) → spine
manifest → dogfood.** plan/0024 is now a hard prerequisite of the release phase, not a parallel
track.

## Still open after this pass (carried, not closed)

- Tamper-evidence of the *whole* per-project receipt ledger (H20 mitigated per-skip via the
  decision content-hash; a signed-ledger option is a future call/ if the threat model warrants).
- `continuous`-phase receipt semantics (verify/publish go stale on the next commit) — R1's
  `recheck =` makes staleness *detectable*; whether a continuous phase wants a per-checkpoint
  receipt vs a standing one is settled during host-lifecycle implementation.
```

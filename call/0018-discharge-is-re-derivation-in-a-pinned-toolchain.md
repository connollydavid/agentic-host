# Discharge is re-derivation in a pinned toolchain, not a signed attestation; enforcement is project-pluggable

- Status: accepted
- Date: 2026-06-20
- Scope: host-prove, host-lifecycle (the verification toolchain)
- Supersedes: `call/0016` (the CI-signed ed25519 attestation token).
- Relates: `call/0002` (verification lanes by property type); `plan/0023` (the
  verification ladder + host-prove's version+SHA256-pinned proof toolchains); `plan/0024`
  (the milestone, now shrunk to this); connollydavid/host #8 (discharge is name-presence),
  #9 (bound dropped). Generalizes the reproducible-build mechanism already shipping
  (`.host-software`'s `artifact = … <sha256>` + `toolchain = …@sha256`, re-derived by
  `software --verify-build` **in the recorded container**, host#14) so it also covers proofs,
  not only builds.

## Context and Problem Statement

`call/0016` fixed #8 (discharge was `src.contains(name)`, name-presence, not a real PASS)
with a CI-signed ed25519 attestation token, verified offline. Two fatal problems surfaced:

- **Key management is a deal-breaker for adopters.** host-lifecycle is one shared binary, so
  a baked-in public key can't serve every adopter, and a shared keypair would let any adopter
  forge any other's tokens. Each adopter would need its own keypair, an operator-managed CI
  secret, and an integrity anchor (branch protection) for the public key: a fragile,
  human-rooted burden the methodology cannot make mechanical.
- **It complicates parallel checkouts.** Per-project secrets and committed `.att` files in
  every worktree do not compose with the bare-store/parallel-worktree model.

And the fallback "CI-green is the discharge" **overfits GitHub** (required status checks). The
methodology must not depend on GitHub, or any specific CI.

The principle `AVAILABLE ≠ DISCHARGED` (a rung discharges only on a real PASS) is right. Only
the mechanism for carrying "a real PASS happened" into a later check needs replacing.

## Decision

**An obligation discharges only by RE-DERIVING in its recorded pinned toolchain (checkable by
anyone, anywhere), not by a signed token and not by any specific CI being green.**

- **Builds** re-derive in the recorded `toolchain` container and must reproduce the recorded
  `artifact` sha256 (host#14, `software --verify-build`). A stub source yields a different hash.
- **Proofs** re-run in host-prove's **version+SHA256-pinned proof toolchain** (apalache / kani /
  tlaps, plan/0023) via `obligations --prove`, and must PASS at the declared bound. A stub /
  failing / `THEOREM X == TRUE` proof fails the re-run.
- **Re-derivation runs anywhere**: a developer's machine, any CI, a pre-push hook, a cron. The
  authority is the *pinned re-derivation*, never the platform that runs it.
- **The offline hook does only cheap structural checks**: a name-presence **lint** (the named
  target exists, honest about being a lint, not the discharge) + **input-digest staleness**
  (`git hash-object` of the consumed inputs; a change since the recorded discharge ⇒ HAZARD).
- **Enforcement is project-pluggable.** That re-derivation *ran and passed* before "done" /
  release is enforced by whatever a project has: a required status check (GitHub), a pipeline
  (any CI), a pre-push hook, or operator discipline via the `verify` lifecycle phase. The
  methodology prescribes the **act** (run `verify` before declaring done / releasing) and ships
  the **re-deriver** (`host-lifecycle`); the enforcement **mechanism** is the project's choice.

## What hash artifacts a local build gives us (and their limits)

- **Artifact sha256** (`.host-software`) discharges *build reproducibility*, unforgeable in the
  useful sense (any written hash is checked by rebuilding in the pinned toolchain).
- **Input digests** (`git hash-object`) give offline *staleness*, a cheap honest-drift catcher
  (a determined agent can re-record the hash, but still faces the re-run). Not a forgery gate.
- **A proof's PASS is a boolean from running the verifier, not a blob to hash**, so proofs
  re-run (cheaply, in the pinned proof toolchain); they are not hashed. (Proof certificates
  exist but are out of scope, over-engineering.)

## Consequences

- **No keys, no secrets, no `.att`, no signer, no per-project key management, no parallel-
  checkout friction, no CI overfit.** plan/0024 collapses to: reframe #8 (discharge =
  re-derivation), `obligations --prove` re-runs in the pinned toolchain checking PASS + bound
  (#9), input-digest staleness, and the small #10/#11/#12/#13 fixes. host-prove keeps its
  pinned toolchains + verdict/bound parser (an agent-UX aid); **no crypto on any path**.
- **`AVAILABLE ≠ DISCHARGED` / `BUILT ≠ RELEASED` survive**, discharge is still a real PASS,
  now proven by re-derivation rather than a signature.
- **Honest irreducible limit:** a project with *no* enforcement (no CI, no hook, no discipline)
  can still self-assert locally; the methodology can ship the re-deriver but cannot force a
  project to run it (the same limit as "you can skip your own tests"). The `verify` phase + a
  receipt (`plan/0025`) make *not* running it visible, not impossible.
- **Property-triviality stays out of scope** (a vacuous proof re-derives as PASS), a review
  concern, not mechanizable, exactly as `call/0016` already noted.

## Alternatives considered

- **CI-signed ed25519 token** (`call/0016`, superseded): per-adopter key management is a
  deal-breaker; complicates parallel checkouts.
- **CI-green as the authority**: overfits GitHub / a specific CI; the methodology must stay
  platform-agnostic.
- **A committed plaintext result marker**: forgeable by the agent (it edits the file); relocates
  #8, does not fix it.
- **Re-run the heavy verifier in the commit hook**: breaks the fast/offline hook; re-derivation
  belongs in the heavy `verify` lane, not the hook.

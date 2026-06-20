# Rung discharge requires a signed verifier-pass attestation, not name-presence

- Status: accepted
- Date: 2026-06-20
- Scope: host-prove, host-lifecycle, host-lint (the verification toolchain)
- Relates: `call/0002` (verification lanes by property type — the rungs extend it);
  `plan/0023` (the verification ladder this hardens); `plan/0024` (the milestone that
  implements this); connollydavid/host #8 (discharge is name-presence), #9 (bound
  dropped), #10–#12, #13 (LEXICON provenance). Generalizes the reproducible-build
  attestation already shipping in `.host-software` (`artifact = … <sha256>` +
  `toolchain = …@sha256`, recomputed offline by `software --verify-build`).

## Context and Problem Statement

`plan/0023` added deep-verification rungs (Apalache, TLAPS, Kani) discharging obligations
dispositioned `apalache:`/`tlaps:`/`kani:`. The tool validated a disposition with
`obligation_gaps` → `src.contains(name)`: it checked the proof was **present by name**, never
that it **passed**. So a stub, a failing harness, or a vacuous `THEOREM X == TRUE` satisfied
`obligations` and `software --check` — the rung sold as "stronger than a test" became weaker
than one (#8). Compounding it, the soundness **bound** of the bounded tools (Apalache
`--length=N`, Kani `--unwind=K`) was unrepresentable, dropped from `verdict.py`, and a bounded
check was presented as a complete proof (#9).

`AVAILABLE ≠ DISCHARGED`: availability of a proof is not discharge of an obligation. The audience
includes a weak (4B) agent who will forge or shortcut anything not mechanically enforced, and the
hook path must stay network-free and fast. A committed plaintext attestation is forgeable (the 4B
hand-types `{PASS, bound, sha}`); running the verifier in the hook breaks network-free.

## Decision

**An obligation discharges only against a CI-signed attestation token that binds the verifier's
PASS verdict, its bound, and the digests of the proven inputs — verified offline at check time.**

- **Token** — one `.att` per obligation / per cited reference, co-located with the spec in the
  software repo (`call/0010`, plan/0012). Fields: `claim` (the disposition verbatim), `verdict`
  (`verdict.py`'s exact PASS line), `bound` (required for bounded tools; `unbounded` only for
  TLAPS; absent ⇒ HAZARD), `inputs` (`git hash-object` of each consumed source; for LEXICON,
  `content-sha` of the fetched URL body), `tool` (from `tools.lock`), `sig` (ed25519 over the
  canonical concatenation).
- **Minter** — the CI verification lane (the one `call/0002`/plan/0023 already require) signs with
  an ed25519 private key held only in CI secrets, after the verifier exits 0. The agent commits the
  `.att`; CI fails if it does not match a fresh run (no write-back).
- **Consumer** — `host-lifecycle obligations`/`software --check` verify the signature against a
  public key shipped in the binary, recompute the input digests (mismatch ⇒ stale ⇒ HAZARD), and
  require `verdict` be a PASS word and `bound` ≥ the declared bound. This replaces `src.contains`.

The same token grounds LEXICON (#13) reference provenance: a network-having lane binds and signs
the cited URL's `content-sha`, which the offline gate verifies — the weak agent cannot fabricate a
URL whose CI-fetched body-hash matches a token it never obtained.

## Consequences

- **Weak agents are hard-gated; strong agents keep authoring latitude.** No shortcut mints a token
  without a real CI pass; a strong agent authors the proof/bound freely, but the output is verified,
  not trusted, and a later silent weakening re-stales the token via the input digest.
- **Bound becomes first-class** — `verdict.py` must emit it from the real invocation before it can
  be signed (the #9 fix is a prerequisite, not an add-on).
- **Property triviality is explicitly NOT closed.** The token attests that the verifier ran and
  passed at bound N, not that the property is meaningful — a vacuous proof still passes. Whether a
  proof proves the *right* thing stays a human/strong-agent review concern; it is not mechanizable,
  and this decision does not claim to gate it.
- **Key management is now soundness-critical** (a leaked CI key forges tokens); key rotation is a
  future `call/` decision. A new crypto dependency (ed25519 verify) enters host-lifecycle.

## Alternatives considered

- **Plaintext committed attestation** — forgeable by a 4B (hand-typed); relocates #8, does not fix it.
- **Run the verifier in the hook / on `--check`** — sound but breaks the network-free, fast hook
  constraint (Kani/Apalache/TLAPS are heavy); CI-only, it is just "the lanes already run it."
- **Query live CI status** — network + platform coupling, unavailable offline / fresh-clone /
  non-GitHub, carries no bound, forgeable via workflow YAML.

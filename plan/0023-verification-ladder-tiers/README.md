# plan/0023 — Verification-ladder tiers: solver (#3) + code-conformance (#4)

Resolves connollydavid/host#3 (no solver tier — parametric/unbounded invariants could
only be bounded-checked or tested) and #4 (no lane to verify the *implementation*
against the spec, beyond tests + trace validation). Both surfaced while applying the
methodology; both are domain-independent gaps in the verification toolchain.

The ladder gains three opt-in deeper rungs above the bounded lanes (allium PBT,
specula/TLC), each driven by an idiomatic agentic skill built to run **down to a small
model** (Qwen-3.5-4B / the Fen persona): the tool's output is parsed into one
machine-readable verdict, so the agent matches a word rather than interpreting raw output.

## What shipped

**New tool — `host-prove` (connollydavid/host-prove, Unlicense, v0.1.0).** The
deep-verification lane driver: three skills + verdict-parsing wrappers + provenance-pinned
installers (official prebuilt binaries, version + SHA256 in `tools.lock`; no Docker).
- `apalache-symbolic` → Apalache (TLA+ → SMT/Z3): parametric/unbounded `.tla` invariants.
- `tlaps-proof` → TLAPS (`tlapm`): unbounded proof. Authoring needs a strong model; the
  skill scopes a weak model to running/maintaining existing proofs.
- `kani-conformance` → Kani: Rust code↔spec conformance.
- `scripts/verdict.py` is the single fixture-tested parser all wrappers pipe through.

**host-lifecycle v0.15.0.** Ties the rungs into the existing obligation + lane machinery,
not a parallel lane:
- `obligation_gaps` accepts `kani:<harness>` / `apalache:<inv>` / `tlaps:<theorem>`
  dispositions beside `test:`/`structural`/`waived:`; `obligations … --prove <dir>`
  validates the proof name exists.
- `spec_lane_problems` raises a **conditional** HAZARD — fires only when a `.obligations`
  manifest *declares* a rung but its CI lane (`cargo kani` / `apalache-mc` / `tlapm`) is
  absent. Opt-in and inert: bare `.tla`/crate presence never activates a rung.

**Spine.** host-template `CLAUDE.md` reframes the three lanes as a ladder with the rungs
(`4a98d92`); `UPGRADING.md` adds the ledger entry (with a machine-checkable `verify`); the
host front-door `README.md` mirrors it.

## Dogfood (real, software-first; verified locally and CI-wired)

- **Kani in host-lint** (`a7ae5e9`): three `#[cfg(kani)]` proofs — `is_review_code`
  (#digit is a code; two letters are not → discharge `rule-{success,failure}.Detect
  InternalCodeAsName`) and `seg_glob` (`*` matches any segment, panic-free). All verify
  SUCCESSFUL in seconds. **Lesson:** an initial `is_dotted_code`/`check_bare_numeral_header`
  attempt did not terminate — `str::split` pulls in `memchr` + heap, which blows CBMC up;
  the fix is to target char/byte-level functions (now a rule in the skill). `#[cfg(kani)]`
  + a `check-cfg` lint keep `cargo build`/`test` and the reproducible artifact
  byte-identical (Cargo.lock unchanged; `software --check` note confirms).
- **Apalache + TLAPS in host-grammar** (`fbd2e6c`): `ParallelScanSymbolic.tla` — Apalache
  **PROVEN** the chunked tiling reconstructs the input for all (N,K), 1≤K≤N≤8 (positions +
  finite sets; no `RECURSIVE`, which Apalache rejects). `ChunkBounds.tla` — TLAPS
  **ALL-PROVED** (14 obligations) that every worker index is in-bounds for all (N,K).
  `spec/ParallelScan.obligations` declares both rungs; `.github/workflows/host-prove.yml`
  runs them on a CI OS matrix.

## Weak-agent (Fen) validation

Drove the `kani-conformance` skill with the real Qwen-3.5-4B @ Q8_0
(`unsloth/Qwen3.5-4B-MTP-GGUF`). The decision-table routing and STOP/hard-rules **held
down to the 4B** — it routed a `SUCCESSFUL` verdict correctly and *refused to weaken a
failing proof even when the user pushed for it*. Where it slipped was free-form harness
authoring (`kani::any::<&str>()`); fixed by adding a ready-to-fill bounded-byte template.
Unsloth tool-calling: 3/3 well-formed. The design lesson — route through one CLI wrapper +
a fixed verdict vocabulary — makes the rung robust regardless of the serving layer.

## Verification

`software --check` clean (incl. the new "Kani lane present (declares kani:)" line);
`validate plan/`/`call/` ok; `upgrade .` up to date at baseline `4a98d92`. Whole suite
green across host-prove, host-lifecycle, host-lint, host-grammar, and this host.

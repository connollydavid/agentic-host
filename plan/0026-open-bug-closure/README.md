# plan/0026, Open-bug closure: the full sequenced plan for every open issue

> **STATUS: COMPLETE (2026-06-20).** All 8 tracked bugs closed, whole-suite green. Standalone
> fixes: host-lint#7 (v0.4.3), host#14 (host-lifecycle v0.16.0). plan/0024: host#8, #9, #10,
> #11, #12, #13, closed together after a completeness review that caught and fixed one residual
> (#11's tools.lock header still overstated uniform SHA256; host-prove f0852e5). connollydavid/host
> has zero open issues. The plan/0025 release-orchestration track is separate, future work.

The single plan that closes **every** open bug across the project, in dependency order. It does
not re-specify the mechanisms (those live in plan/0024 and plan/0025); it is the coverage map +
the critical path + the per-stage closure criteria, so no open bug is orphaned and the build
order is unambiguous.

## Every open bug (8), and what closes it

| Bug | One line | Closed by | Mechanism |
|---|---|---|---|
| **host-lint#7** | `--all` ignores `.gitignore`, walks `build/`, vendored deps, `.git/`; slow + noisy; contradicts the "scan tracked files" docs | **Standalone** (host-lint fix) | `--all` scans actually-tracked files (`git ls-files`) / a gitignore-aware walk; doc matches behaviour |
| **host#14** | `software --verify-build` builds with ambient rust, ignoring the recorded `toolchain` pin | **Standalone** (host-lifecycle fix) | build the recipe inside the recorded digest-pinned `toolchain` container; `--check` HAZARDs `artifact` with no `toolchain`; skip cleanly when no runtime |
| **host#8** | rung discharge is name-presence (`src.contains`), not a real PASS | **plan/0024** | discharge = re-run the verifier in the pinned toolchain (`obligations --prove`); `src.contains` removed |
| **host#9** | bounded rungs' soundness bound (`--length`/`--unwind`) unrepresentable + dropped | **plan/0024** | `bound` is a required signed field; extend `verdict.py` to emit it **first** |
| **host#10** | host-prove rung CI lanes un-wireable in a separate repo (host-relative paths, wrapper HAZARD, broken `references/`) | **plan/0024** | wireable CI snippets, expose the literal tool name, create `references/` |
| **host#11** | host-prove README/`tools.lock` overstate uniform SHA256 (Kani is a cargo-locked source build) | **plan/0024** | honest wording: `git hash-object` inputs + tool from `tools.lock`; Kani ≠ SHA256 binary |
| **host#12** | specs under `plan/*/spec/` evade the mandatory lanes | **plan/0024** | `spec_lane_problems` HAZARDs a `plan/*/spec/` spec + a declared rung with no re-derivable lane |
| **host#13** | LEXICON: tell-shaped tokens have no provenance, so can only warn | **plan/0024** | line-based LEXICON; URL liveness checked by a network-having lane; warn becomes error |
| **host#14** *(orchestration home)* | the strict release that consumes the pinned-toolchain build | **plan/0025** | host#14's fix is standalone; its *use* (release builds in the pinned toolchain) lands with the release work |

**Coverage: 8/8 mapped, no orphans.** host-lint#7 and host#14 were the only open bugs without a
milestone; both are standalone fixes. #8 to #13 are plan/0024. The orchestration/receipts
meta-gap (not a GitHub bug, but the root of this session's findings) is plan/0025.

## Dependency DAG / critical path

```
Standalone fixes (independent, no deps):
   host-lint#7  ──▶ host-lint patch release
   host#14      ──▶ host-lifecycle release  (its build is re-derived in the pinned
                    toolchain — that re-derivation IS host#14, already done)

plan/0024 (the big milestone, independent of the standalone fixes):
   host-prove(#9,#10,#11) ▶ host-lifecycle(#8,#12) ▶ host-lint LEXICON(#13) ▶ seed ▶ spine

plan/0025 (consumes the standalone host#14 build + plan/0024):
   host-lifecycle(manifest+receipts+release) ▶ spine manifest ▶ dogfood releases
```

Critical path = plan/0024 to plan/0025 (the longest chain). host-lint#7 and host#14 are off the
critical path and can land immediately.

## The sequence

### Standalone quick wins (close host-lint#7 + host#14)

- **host-lint#7**: replace the naive `walkdir_simple` in the `--all` path with a tracked-file
  scan (`git ls-files`, honest to the docs) or a `.gitignore`-aware walk; verify on a repo with a
  populated `build/` + vendored tree (finishes fast, flags only authored source). host-lint patch
  release (v0.4.3, re-hash + re-pin per the version-bump-moves-the-hash rule), tag, CI green.
  **Closes host-lint#7.**
- **host#14**: `software_verify_build` runs the recipe **inside** the recorded `toolchain`
  container (not ambient rust); `software_check` HAZARDs an `artifact` with no `toolchain`; both
  skip cleanly (clear message) when no container runtime is present, never silent ambient-DRIFT.
  host-lifecycle minor release, tag, re-pin CI. **Closes host#14.** (Also: plan/0025 build-step-1.)

### plan/0024: sound discharge by re-derivation + LEXICON (closes host#8 to #13)

Re-scoped by **`call/0018`** (the CI-signed token was a deal-breaker, per-adopter key management,
and "CI-green" overfits GitHub): discharge = **re-derivation in the recorded pinned toolchain**, no
keys, portable to any CI or none. Build chain is software-first:
1. **host-prove**: a small **Rust** binary (retiring `verdict.py`, off the trust path) emits the
   `bound` (**#9**); keep the pinned proof toolchains; wireable CI snippets +
   `kani-conformance/references/` (**#10**); honest `tools.lock`/README (**#11**). No signer, no crypto.
2. **host-lifecycle**: `obligations --prove` re-runs each declared rung in its pinned toolchain and
   gates on PASS-at-bound, replacing `src.contains` (**#8**); input-digest staleness; add the
   `plan/*/spec/` lane gate (**#12**).
3. **host-lint**: LEXICON loader + the three mechanical guards + named citation-gated shapes +
   `lexicon` CRUD + the committed strict switch (**#13**).
4. **adopt/upgrade**: seed LEXICON + the strict default at adoption.
5. **spine**: `call/0018` (discharge = pinned re-derivation; enforcement project-pluggable) + the
   `AVAILABLE ≠ DISCHARGED` / LEXICON principles + an UPGRADING entry; agentic-host re-records.

### plan/0025: orchestration + receipts + strict release (the meta-gap, finalizes host#14)

Depends on the standalone host#14 (the build re-derivation) + plan/0024 (sound discharge). Build per
plan/0025 (hardened R1 to R6): host-lifecycle manifest parser + receipts ledger + release
orchestration, then spine lifecycle manifest + the "every phase emits a receipt" rule + UPGRADING, then
dogfood by re-cutting host-lint / host-prove releases **through** `host-lifecycle release`.

## Definition of done (complete = whole-suite green + every issue closed)

- Every open issue closed by a **referencing commit** (`closes connollydavid/host#N` once the fix
  lands and CI is green), title lint-clean.
- `host-lifecycle verify .` clean (validate + `software --check` + `book --check` + tell test) on
  agentic-host; whole-suite green across host-lint, host-lifecycle, host-prove, host-grammar, and
  this host (complete-means-whole-suite-green, mind main-only triggers and the release jobs).
- The strict release phase is dogfooded: at least one component re-released **through**
  `host-lifecycle release`, and it leaves a re-verifiable release receipt.

## De-risk status

Mechanisms are already de-risked: plan/0024 by the LEXICON adversarial review (24 flaws) + the
real-4B test (the attestation design panel's CI-signed token was later dropped, `call/0018`
re-derivation needs no keys); plan/0025 by the 39-finding adversarial review
(`plan/0025/design-review.md`). The remaining live de-risk is the Fen (4B) ergonomics test of the
`host-lifecycle release` UX, run **after** its prototype exists (the UX is tool-computed; a live
test beats a mock). The standalone fixes need no design de-risk (they are bounded corrections).

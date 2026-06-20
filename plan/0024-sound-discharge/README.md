# plan/0024 — Sound discharge by re-derivation in a pinned toolchain (no keys, no CI overfit)

> Was "attestation tokens." Superseded in design by `call/0018`: the CI-signed ed25519 token
> was a deal-breaker (per-adopter key management) and complicated parallel checkouts. The
> principle `AVAILABLE ≠ DISCHARGED` survives; the mechanism is now **re-derivation in a pinned
> toolchain** — no keys, no signer, no `.att`, portable to any CI or none.

## Context

A post-plan/0023 audit filed five soundness defects in the verification ladder (connollydavid/host
#8–#12) plus the LEXICON enhancement (#13). They are one problem: **the tooling under-enforces
what the prose claims.**

- **#8** — discharge is *name-presence*: `obligation_gaps` does `src.contains(name)`, so a stub /
  failing / `THEOREM X == TRUE` proof passes `obligations` and `software --check`. The rung sold
  as "stronger than a test" is *weaker* than one. `AVAILABLE ≠ DISCHARGED`, unenforced.
- **#9** — the soundness **bound** (Apalache `--length=N`, Kani `--unwind=K`) is unrepresentable,
  dropped from the verdict, and a bounded check is presented as a complete proof.
- **#10** — rung CI lanes are un-wireable in a *separate* software repo (`./tools/host-prove`
  paths absent; a wrapper hides the literal `apalache-mc` the HAZARD detector greps; kani guide →
  non-existent `references/`).
- **#11** — README/`tools.lock` overstate uniform SHA256 pinning (Kani is a cargo-locked source
  build, `sha256=n/a`).
- **#12** — a spec under `plan/*/spec/` evades the mandatory lanes; the spine calls it a defect but
  no gate enforces it.
- **#13 (LEXICON)** — tell-shaped tokens (versions, dotted codes, tracker refs) have no provenance,
  so the identifier/reference class can only *warn*; a phantom `#999` passes. Validated this cycle:
  24-flaw design review + a real Qwen-3.5-4B test that **launders a tell** and **fabricates a URL**.

## The mechanism: re-derivation in a pinned toolchain (`call/0018`)

Discharge is **re-running the real verifier in its recorded pinned toolchain and checking it
passes** — checkable by anyone, anywhere, with no keys and no dependence on a specific CI. It
generalizes the build mechanism already shipping: `software --verify-build` re-derives the
`artifact` sha256 **in the recorded `toolchain` container** (host#14) — extended from builds to
proofs.

- **Builds** re-derive in the recorded container, reproducing the recorded `artifact` hash (done —
  host#14). A stub source yields a different hash.
- **Proofs** re-run in host-prove's **version+SHA256-pinned proof toolchain** (apalache / kani /
  tlaps, plan/0023) via `obligations --prove`, and must PASS at the declared bound.
- **The offline hook** does only cheap checks: a name-presence **lint** (the named harness exists)
  + **input-digest staleness** (`git hash-object` of the consumed inputs — changed ⇒ HAZARD).
- **Enforcement is project-pluggable**: that `verify` (which re-derives) ran and passed before
  done/release is enforced by a required check (GitHub), a pipeline (any CI), a pre-push hook, or
  the operator running the `verify` phase. The methodology prescribes the act, ships the
  re-deriver (`host-lifecycle`), and never bakes in a CI.

## How it closes each issue

| Issue | Closed by |
|---|---|
| #8 | discharge = `obligations --prove` re-runs the verifier and gates on PASS, not `src.contains`; the offline check is renamed an honest *lint* |
| #9 | the `bound` lives in the lane/disposition; `obligations --prove` re-runs at it and checks PASS-at-bound; host-prove emits the bound from the real invocation |
| #10 | the running lane is the one plan/0023 already requires; fix the skill CI snippets to be wireable in a separate repo (no `./tools/host-prove` paths; expose the literal tool name); create the missing `references/` |
| #11 | honest wording: `inputs` are `git hash-object` shas + `tool` from `tools.lock` (Kani = cargo-locked, not a SHA256 binary) |
| #12 | `spec_lane_problems` additionally HAZARDs a spec under `plan/*/spec/` and a declared rung obligation with no re-derivable lane |
| #13 | LEXICON (below); URL provenance is checked by a network-having lane (re-derivation), the offline part is masking |

## LEXICON (#13) — folded in, keyless

A line-based **`LEXICON`** file (absorbs `.host-lint-allow`), the **sole** truth (no runtime
auto-context). Each entry is the **full contextual phrase** (`Windows 3.1`, never bare `3.1`); a
tracker ref carries its URL. host-lint masks the *phrase* before detection; the identifier/reference
tier escalates **warn → error**. Locked: **broad-strict + seed at adoption/upgrade**; **fixed named
citation-gated reference shapes** (hash-number, jira-key, gh-cross-repo); **URL = required provenance
metadata** (the phrase masks; URL liveness is checked by a network-having lane, not the offline
hook). Three **mechanical guards** the 4B test forced: reject a bare master-key entry; **reject
laundering a real tell** (an entry that is *itself* a tell → forces rename); **CI URL-liveness**.
A `lexicon add/rm/list` CRUD **computes** the phrase so the weak agent never authors it.

## Non-goals / residual (recorded honestly)

- **Property triviality is NOT closed** — a vacuous proof re-derives as PASS; meaningfulness is a
  review concern, not mechanizable.
- **Input-digest staleness defeats honest drift, not a determined forger** — the forger still
  faces the re-run; that is the gate.
- **A project with no enforcement can self-assert locally** — the methodology ships the re-deriver
  but cannot force a project to run it (same limit as skipping your tests); the `verify` phase +
  the `plan/0025` receipt make *not* running it visible.

## Build chain (software-first)

1. **host-prove** ✓ (v0.2.0, `91719aa`) — a small **Rust** binary that **runs the verifier itself**
   (`cargo kani` / `apalache-mc` / `tlapm` via `std::process`) and parses in one process: one
   command for a weak agent, no shell wrappers, no unpinned `python3` (`verdict.py` retired). Emits
   the `bound` (#9); wireable CI snippets + the created `kani-conformance/references/` (#10); honest
   `tools.lock`/README — Kani is a cargo-locked source build (#11). Off the trust path; no crypto.
2. **host-lifecycle** ✓ (v0.17.0, `5708dd8`) — `obligations --rederive <dir>` re-runs each declared
   rung via host-prove and gates on **PASS-at-bound**, replacing `src.contains`-as-discharge (#8/#9;
   the offline `src.contains` stays, honestly a presence *lint*). The verdict-interpretation
   (`verdict_discharges`) is a pure, unit-tested function; the runner shells host-prove. `software
   --check` HAZARDs a `.allium`/`.tla`/`.cfg` under `plan/*/spec/` (#12). Remaining: record/recompute
   `inputs` digests for the offline staleness signal.
3. **host-lint** ✓ (v0.5.0, `ed00abc`) — the `LEXICON` file (replacing `.host-lint-allow`) +
   parser (phrase/URL split, `#`+non-digit comment carve-out) + the three guards reusing
   `classify_line` (master-key, no-laundering = the phrase is itself a flag-tell, citation gate =
   `#N`/`owner/repo#N` needs a URL) + the `lexicon add/rm/list/--check/--check-urls` CRUD + the
   committed `# host-lint: strict` warn->flag escalation (#13). Spec: `config.strict` + the
   `EscalateUnderStrict` rule, allium check/analyse clean, obligations dispositioned. host-lint
   does **not** enable strict on itself — its own source carries warn-tier rule examples, which
   strict would escalate to blocking flags. 90/90 integration green; `--verify-build` reproduces
   the re-pinned artifact `dd0a111` in the recorded container.
4. **adopt/upgrade** — seed LEXICON + the strict default at adoption (host-lifecycle).
5. **spine** — `call/0018` principle (discharge = pinned re-derivation; enforcement
   project-pluggable) + the LEXICON principles in host-template `CLAUDE.md` + an UPGRADING entry;
   then agentic-host re-records.

## Verification

`obligations --prove` (in the `verify` lane, runnable anywhere) rejects a stub proof (re-run
fails) and a boundless/stale disposition; a vacuous proof is out of scope (documented). LEXICON:
the 4B re-tested against the **built** `lexicon` tool. Whole-suite green across all repos; #8–#13
closed. No keys, no `.att`, no CI overfit, no parallel-checkout friction.

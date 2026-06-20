# plan/0024 — Attestation tokens: sound rung discharge + LEXICON provenance

## Context

A post-plan/0023 adversarial audit filed five soundness defects in the verification ladder
(connollydavid/host #8–#12) plus the LEXICON enhancement (#13). They are one problem twice:
**the tooling under-enforces what the prose claims.**

- **#8** — discharge is *name-presence*: `obligation_gaps` does `src.contains(name)`, so a stub /
  failing / `THEOREM X == TRUE` proof passes `obligations` and `software --check`. The rung sold as
  "stronger than a test" is *weaker* than one (a test at least runs). The `AVAILABLE ≠ DISCHARGED`
  principle, unenforced.
- **#9** — the soundness **bound** (Apalache `--length=N`, Kani `--unwind=K`) is unrepresentable in
  the disposition, dropped from `verdict.py`'s `PROVEN` line, and the docs present a *bounded* check
  as a *complete* proof.
- **#10** — rung CI lanes are un-wireable in a *separate* software repo (`./tools/host-prove` paths
  absent; a wrapper hides the literal `apalache-mc` the HAZARD detector greps → spurious HAZARD;
  kani guide → non-existent `references/`).
- **#11** — README/`tools.lock` overstate uniform SHA256 pinning (Kani is a cargo-locked source
  build, `sha256=n/a`).
- **#12** — a spec under `plan/*/spec/` evades the mandatory lanes; the spine calls it a defect but
  no gate enforces it.
- **#13 (LEXICON)** — tell-shaped tokens (versions, dotted codes, tracker refs) have no provenance,
  so the identifier/reference class can only *warn*; a phantom `#999` passes. Validated this cycle:
  24-flaw design review (proceed-with-changes) + a real Qwen-3.5-4B test that **launders a tell**
  and **fabricates a URL** — proving the guards must be mechanical, not prompt-level.

## The unifying primitive: a CI-signed attestation token

Selected by a design panel over four candidates. A committed *plaintext* token is forgeable by the
4B (it hand-types `{PASS, bound, sha}` — relocating #8, not fixing it); running the verifier *in the
hook* breaks network-free. The answer is the **generalization of the reproducible-build attestation
already shipping here** — `.host-software`'s `artifact = … <sha256>` + `toolchain = …@sha256`, which
`software --verify-build` recomputes offline/read-only — from build artifacts to **proof verdicts**.

**Token** — one `.att` file per discharged obligation / per cited reference, co-located **with the
spec in the software repo** (respects specs-co-locate, plan/0012). Newline-keyed, `.host-software`
style:

```
claim    = apalache:Reconstructs          # the disposition verbatim (or url:<cited-url> for LEXICON)
verdict  = PROVEN Reconstructs            # host-prove's exact PASS line — the word the weak model matches
bound    = length=12                      # REQUIRED for bounded tools; `unbounded` only for tlaps; absent => HAZARD
inputs   = <blob-sha> spec/Reconstructs.tla   # one per consumed input, via `git hash-object` (LEXICON: content-sha = sha256(body))
tool     = apalache-mc@0.58.0             # resolved from tools.lock
sig      = ed25519:<base64>               # CI-only signature over the canonical concatenation of all fields
```

- **Minter** = the CI lane that already runs the verifier (plan/0023's kani/apalache/tlaps lanes;
  LEXICON minted by a network-having lane that fetches the URL once). After exit 0 it runs
  `host-prove` (the Rust binary — see the build chain), `git hash-object`es the inputs, signs with an
  **ed25519 private key held only in CI secrets**. The **agent commits** the `.att` (no CI write-back / push-loop); CI fails if a committed
  token does not match a fresh run.
- **Consumer** = `host-lifecycle obligations` / `software --check`, **offline** in the hook path:
  ed25519-verify `sig` against the **public key shipped in the binary**, recompute the input digests
  (mismatch ⇒ stale ⇒ HAZARD — the *breaks-tomorrow* detector), check `verdict` is a PASS word and
  `bound` ≥ any bound declared in the `.obligations` disposition. **Discharge iff all four hold** —
  this replaces `src.contains(name)` (main.rs ~2186/2196).

## Weak agents vs strong agents (the asked-for split)

Same token, opposite affordances. **Weak (4B):** every shortcut is mechanically dead — cannot forge
the sig (no CI key), stub the verifier (a stubbed run mints no signature), fabricate a URL (no
matching CI-fetched content-hash), or drop the bound (absent ⇒ HAZARD). **Strong:** trusted to
*author* — the property/theorem, the harness, and the **declared bound** — with full creative
latitude up front, but the output only mints a token by *passing CI*, the bound is recorded and
re-checked, and any later silent weakening re-stales the token via the input digest. *Authority to
author is granted; correctness is still earned through the verifier.*

## How it closes each issue

| Issue | Closed by |
|---|---|
| #8 | discharge = a signed PASS verdict, not a name; `src.contains` removed |
| #9 | `bound` is a required signed field; **first** extend `verdict.py` to emit it from the real invocation |
| #10 | the minting lane is the one plan/0023 already requires; fix the skill CI snippets to be wireable in a separate repo (no `./tools/host-prove` paths; expose/detect the literal tool name); create the missing `references/` |
| #11 | honest wording: `inputs` are `git hash-object` shas + `tool` from tools.lock (Kani = cargo-locked, not SHA256 binary) |
| #12 | `spec_lane_problems` additionally HAZARDs a spec under `plan/*/spec/` and a declared rung obligation with no valid token |
| #13 | LEXICON (below); its URL provenance is the same token over `content-sha` |

## LEXICON (#13) — folded in, same primitive

A line-based **`LEXICON`** file (absorbs the `.host-lint-allow` mechanism), the **sole** truth (no
runtime auto-context). Each entry is the **full contextual phrase** (`Windows 3.1`, never bare
`3.1`); a tracker ref carries its URL. host-lint masks the *phrase* before detection; the
identifier/reference tier escalates **warn → error**. Locked decisions: **broad-strict + seed at
adoption/upgrade**; **fixed named citation-gated reference shapes** (hash-number, jira-key,
gh-cross-repo — not raw regex); **URL = required provenance metadata** (the phrase masks; URL
liveness is a CI attestation). Three **mechanical guards** the 4B test forced: reject a bare
master-key entry; **reject laundering a real tell** (an entry that is *itself* a tell → forces
rename); **CI URL-liveness** via the signed `content-sha`. A `lexicon add/rm/list` CRUD **computes**
the phrase so the weak agent never authors it.

## Non-goals / residual risks (recorded honestly)

- **Property triviality is NOT closed.** The token proves *the verifier ran and passed at bound N*,
  not that the property is meaningful — a vacuous `== TRUE` still passes. Whether a proof proves the
  *right* thing stays a review concern, not a gate (it is not mechanizable). This bounds what #8 fixes.
- **CI key management becomes soundness-critical** (a leaked private key forges tokens) — rotation is
  a `call/` decision; restrict the secret to protected branches.
- **Input-digest completeness** — `inputs` must capture transitive spec deps or a break there won't
  re-stale.

## Build chain (software-first)

1. **host-prove** — **rewrite the Python `verdict.py` as a Rust binary** (no unpinned interpreter on
   the trust path — the host#14 discipline; host-prove joins host-lint/host-lifecycle/host-grammar as
   Rust, retiring the project's lone `.py`). The binary parses the verifier output into the fixed
   verdict vocabulary, emits the `bound` (#9), and ed25519-`sign`s the token (the lanes run it after
   exit 0). Keep the thin `*_check.sh` wrappers (invoke the tool, pipe to the binary). Fix the skill
   CI snippets (#10) + create `kani-conformance/references/`; honest `tools.lock`/README (#11).
2. **host-lifecycle** — consume + ed25519-verify the token, replace `src.contains`, check the bound,
   add the `plan/*/spec/` gate (#12), ship the public key, add the ed25519 dep (keep it lean).
3. **host-lint** — LEXICON loader + the three guards + named citation-gated shapes + `lexicon` CRUD
   + the committed `strict` switch.
4. **adopt/upgrade** — seed LEXICON + the strict default at adoption (host-lifecycle).
5. **spine** — `call/0016` (this mechanism) + the `AVAILABLE ≠ DISCHARGED` and LEXICON principles in
   host-template `CLAUDE.md` + an UPGRADING entry; then agentic-host re-pins/records.

## Verification

`obligations`/`software --check` reject a stub proof (no signed PASS) and a boundless/stale token;
a vacuous proof is *out of scope* (documented). LEXICON: the 4B re-tested against the **built**
`lexicon` tool (the guards refuse the laundering it tried). Whole-suite green across all repos;
#8–#13 closed.

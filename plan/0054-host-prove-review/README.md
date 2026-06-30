# plan/0054 host-prove review: findings, and the on-demand verifier-plugin design

This milestone records a maximum-effort review of `host-prove`, the verification-ladder lane driver
(the re-deriver the ladder trusts), and the design decided for its remediation. It is the next review
in the campaign after `host-grammar` (plan/0053). It is treated as doctrine-grade (operator ruling)
because host-prove is the no-hollow-green enforcement tool, and the review found that host-prove can
itself report a hollow green: it has several paths that settle a PASS over a real failure.

## What was reviewed

- Component: `host-prove` at its pinned release (`3d1bba79`, v0.2.3): the single `src/main.rs`
  (333 lines), the `host-prove.allium` spec and its `host-prove.obligations` manifest, `tools.lock`,
  the `install/*.sh` scripts, the three skill guides, the `tests/` fixtures and runner, and the CI.
- Method: five independent reviewers, one per surface (verdict-parsing soundness; the fail-closed
  CLI, subprocess, and exit-code path; the allium spec and obligation discharge under the
  no-hollow-green lens; the `install/*.sh` and `tools.lock` provenance; CI, the reproducible build,
  tests, and the weak-model skill guides). Each probed its claims empirically against the built
  binary; the load-bearing false-passes were independently reproduced before write-up.
- Result: 23 findings, deduped. Two critical false-passes, six high, eleven medium, four low. No
  function panics, and the reproducible-build recipe matches `.host-software` byte for byte.

## The contract the findings test against

- **Verdict soundness (the cardinal rule).** host-prove is the re-deriver the ladder trusts
  (`call/0018`: discharge is the verifier passing on re-derivation). A PASS verdict (`SUCCESSFUL` /
  `PROVEN` / `ALL-PROVED` / `TYPECHECK-OK`, exit 0) must never be reported over a real failure, a
  refutation, a crash, or an incomplete run. Ambiguity must fail closed (exit 2). A false PASS
  silently defeats the whole ladder; a false FAIL or false ERROR is far less dangerous.
- **No hollow green (plan/0052).** A lane that cannot perform its check must not report clean, and an
  obligation must be discharged by a test that exercises the rule. host-prove must hold itself to the
  doctrine it drives for others.
- **Provenance.** Each verifier is pinned by version and SHA256 in `tools.lock` and verified before
  use; the host-prove binary builds offline and re-derives byte-identically.

## Findings

Critical (false-pass):

1. **Kani prefers SUCCESSFUL over FAILED** and ignores the `Complete - <n> failures` summary, so a
   refuted `harness` is reported as a clean proof when both verdict tokens appear.
2. **TLAPS treats every status except exactly `failed` as proved**, so an `omitted` leaf, a
   `missing` or `interrupted` obligation, and even a decorated `failed (smt: timeout)` all settle to
   `ALL-PROVED` at the top, unbounded rung.

High:

3. **TLAPS never checks the expected obligation count or theorem**, so a truncated or killed run
   reports `ALL-PROVED` on whatever subset it emitted.
4. **TLAPS matches `status:` and `loc:` as a bare substring on any line**, so echoed spec content
   (`ASSUME msg.status: proved`) fabricates a proved obligation.
5. **The verifier process exit code is discarded.** The verdict rests only on output text, so a tool
   that prints a clean line then exits non-zero is reported as a pass.
6. **A malformed `--bound`** (with no `unwind=` or `length=` prefix) is dropped at the verifier yet
   stamped verbatim into the PASS verdict, so the recorded bound can over-claim the coverage the run
   explored; the `unspecified` safety net catches only an absent bound, not a malformed one.
7. **`kani_failed` discharges the `NonPassHasNoBound` invariant without asserting** that the FAILED
   line carries no bound; the property the invariant exists to enforce is asserted by no test.
8. **host-prove's own discharge gate cannot catch that.** Its CI pins a host-lifecycle predating
   plan/0052, runs the discharge check advisory-only (no `--strict-discharge`), and the manifest
   declares no `exercises=` link, so host-prove has not adopted the discharge strengthening it drives
   for others. Its tests are white-box (they call the parsers directly), so the links fit.

Medium:

9. **Apalache prefers `NoError` over `Error`**, so a co-occurrence reports PROVEN.
10. **Apalache `Deadlock` and `RuntimeError`** fall through to ERROR (exit 2), mislabeling a real
    negative result as could-not-run.
11. **An unrecognized `--mode` value silently means `check`** rather than a rejection.
12. **The spec models a `Verdict.bound` field the code does not represent**, and the three `Bound`
    values use two incompatible verdict-line encodings (`[bound=<x>]` versus a separate `[unbounded]`).
13. **`BoundedToolsNeverUnbounded` is discharged by a presence-only assertion** that never checks the
    unbounded form is absent, and only for the with-bound case.
14. **`NonPassHasNoBound` and the unusable transition are tested for one representative each**; the
    apalache check-mode ERROR path and the tlaps zero-status ERROR path have no test at all.
15. **The Apalache fixtures were captured from version 0.47.2** while `tools.lock` pins 0.58.0, so the
    parser contract is validated against a version that is never shipped.
16. **The `run_*` command-builders** (flag assembly, bound-prefix stripping, the live dispatch) are
    exercised by no test.
17. **The kani skill guide calls the soundness `--bound` optional** and never tells the model that a
    `[bound=unspecified]` PASS must be flagged. The omission contradicts the bound design.
18. **`cargo kani setup` fetches an unverified, undocumented backend.** The lockfile pins the crate,
    not the backend binary the setup step downloads.
19. **CI never runs the installers or the SHA-verification path** (only a syntax check), and the
    README advertises a CI matrix that does not exist, so the provenance anchor is asserted but never
    machine-verified.

Low:

20. **The apalache PROVEN label trusts `--inv`** rather than confirming the checked invariant from
    output (sound in direct-run, where the flag and the run share a source).
21. **`get(flag)` returns the next token unconditionally**, so a value-flag placed before another
    flag swallows it (fail-closed in practice, but a misleading verdict).
22. **The release job publishes the asset without re-deriving and comparing its hash** in the same
    run, so a reproducibility regression would publish silently.
23. **`verify_sha`'s `[0-9a-f]*` guard is a weak validator** (it rejects a valid uppercase digest and
    admits a hex-prefixed non-digest); the exact comparison is the real gate, so there is no bypass.

## What was checked and cleared

No function panics, on any surface. The reproducible-build recipe (the image digest, the build line,
`strip = true`, and the linux-scoped `--build-id=none`) matches `.host-software` byte for byte.
`verify_sha` is fail-closed: it refuses an empty or `n/a` expected hash, and the exact `sha256sum`
comparison admits no wrong value, so no bypass exists. The verdict vocabulary is consistent across the
spec, the source, and the three guides, and the guides are procedural for a weak model (one wrapper
command per step, a fixed verdict word matched, explicit STOP conditions, authoring handed to a strong
model). `TlapsPassIsUnbounded`, `PassCarriesBound`, the three transition edges, and the `StartRun`
waiver are genuinely discharged. The `--stdin` parse path runs no subprocess and touches no network.

## The operator decision

- **Fix everything.** The verdict-parsing, bound, and discharge findings are clear fail-closed
  soundness fixes, not recall or precision tradeoffs.
- **The verifiers become on-demand, tool-carried plugins**, modeled on host-reference's out-of-process
  helpers (`call/0033`, `call/0034`). The `install/*.sh` scripts fold into a `host-prove install
  <tool>` Rust subcommand that reads `tools.lock`, verifies the SHA256 before use, and exposes the
  binary, orchestrated in one process (shelling only `curl`, `sha256sum`, and `tar`, so host-prove
  keeps its zero-dependency offline-reproducible build). A verifier that is absent at run time is
  auto-installed (SHA-verified) and then run, so a weak agent issues one command. A `call/` decision
  will record the architecture when the work lands.
- **Doctrine-grade.** The design is cast-reviewed and gated on a real qwen3.5-4b probe, as plan/0052
  was, because host-prove is the no-hollow-green tool and the guide and auto-install changes are
  weak-agent-facing.
- **One milestone** carries the soundness fixes, the plugin rework, the decision record, the cast
  review, and the probe gate.

## Network aspects

host-prove's network behaviour splits into contexts. The on-demand auto-install decision adds one new
context, recorded here before it is built so its terms are explicit.

1. **Build time stays offline.** The binary has zero third-party dependencies and builds with
   `--network none` in the pinned muslrust container; the artifact `.host-software` records is produced
   with no network. Auto-install changes nothing here: the binary fetches nothing at build time, and
   the build stays hermetic.

2. **The `--stdin` parse path touches no network and spawns no subprocess.** The parser, its unit
   tests, and `tests/run.sh` validate the verdict mapping fully offline, so the discharge-trust logic
   is testable with no network and no verifier installed.

3. **Running a verifier is a local subprocess.** Once a verifier is installed, host-prove runs it as a
   local process and parses its output; host-prove itself opens no socket. apalache and tlaps are local
   provers (a JVM tool and a prebuilt installer); kani runs locally once set up. The one residual
   exception is `cargo kani setup`, which fetches a backend on first use (finding 18).

4. **Auto-install on demand is the single place host-prove reaches the network, under pinned,
   verified, fail-closed terms.**
   - When a declared verifier is absent at run time, host-prove fetches the pinned asset named in
     `tools.lock` (a github release asset for apalache and tlaps; the crates.io crate plus `cargo kani
     setup` for kani), verifies its SHA256 against `tools.lock` before the artifact is extracted or
     executed, and only then runs it. A mismatch fails closed (exit 2). The fetch is of a pinned,
     hash-verified tool, never of untrusted input, so it is consistent with the spirit of the
     no-reach-out rule (`call/0031`): that rule forbids fetching untrusted content while processing
     untrusted data, whereas here the fetched artifact is the verifier itself, pinned and verified, and
     the trigger is an explicit verifier invocation.
   - The fetch happens once per host, at first activation; later runs use the installed binary and
     touch no network. The network cost is a one-time activation, not a per-run dependency.
   - The verdict is reproducible from the pinned tool version, but the auto-install fetch is not part of
     the reproducible-build attestation, which covers only the host-prove binary. Tool provenance (the
     `tools.lock` pin plus its SHA) is a runtime concern, separate from the build provenance
     `.host-software` records.

5. **Offline and air-gapped operation degrades closed.** Because auto-install needs the network,
   host-prove in an offline or `--network none` environment cannot install an absent verifier. The
   design requires this to fail closed: an absent verifier that cannot be fetched yields a could-not-run
   verdict (exit 2) with a precise message, never a silent pass; a verifier already on PATH is used with
   no fetch. An air-gapped operator pre-installs the pinned verifiers (the same `host-prove install`
   path against a local mirror, or a pre-seeded PATH), so auto-install is a convenience for the
   connected case, not a hard dependency for a run whose verifier is already present.

6. **CI keeps the two contexts apart.** The hermetic build and the parser tests run offline
   (`--network none`); they need no verifier and no network. The provenance check the review asks for
   (finding 19) is a distinct, network-enabled lane that runs `host-prove install <tool>`, confirms the
   SHA against `tools.lock`, and runs a smoke verdict; a periodic re-fetch detects an upstream asset
   re-published under the same name with a different hash (a supply-chain drift alarm). That lane is the
   machine-verification the current syntax-only CI lacks.

7. **Supply-chain posture.** Every fetch is pinned by exact version and asset and verified by SHA256
   before use, so the untrusted transport (the network, the github CDN, crates.io) cannot substitute a
   different artifact without detection. The open edge is the `cargo kani setup` backend (finding 18),
   which the lockfile does not cover; the milestone will pin it or, failing a clean pin, document the
   residual on the kani plugin. The reachable hosts are the github release CDN and crates.io, and the
   underlying `curl` honours a standard proxy environment.

## Cast consultation, and the revised install design (supersedes the auto-install plan above)

The operator flagged three worries about auto-install-on-demand (silent failures, updates, sandbox
restrictions) and asked the cast to weigh in. All five personas were consulted. The result reversed
the auto-install-on-demand default and surfaced the true defect.

- **Unanimous (all five): per-run pin-binding is the real fix.** Every run must bind the verifier to
  the embedded `tools.lock` pin by version and hash before executing it; an absent, wrong-version, or
  unverifiable verifier yields exit 2 and no verdict, never folded into a pass or a fail. A verdict
  comes from the exact pinned tool or it does not come. The first sketch reused whatever was installed
  or on PATH with no version check, the silent-staleness defect the operator sensed: after a pin bump a
  host keeps using the old verifier and still reports a clean pass.
- **Majority (Mara, Orin, Fen, Wren): fail closed by default, install as a separate explicit verb.**
  Fen reframed the weak-agent case: its rule is one tool-driven command at a time with the tool naming
  the next move, not collapsing an install side effect into a run, so a fail-closed verdict that prints
  `run: host-prove install <tool>` is the tool carrying the process. Wren required a hard split: the
  run path is pure-local and structurally cannot install, so a sandbox or air-gapped host is never
  surprised, and `host-prove install` is the only verb that touches the network or filesystem. Orin
  required the resolver to bind to the embedded pin (a version-stamped install dir keyed to the pin, so
  a bump moves the lookup path and the old version is never glanced at) and that re-install always be
  an explicit operator act, because the host may be air-gapped and the operator must learn the pin
  moved. Mara required that no verdict ever issue from a tool not verified against the pin, with a cheap
  check (`host-prove doctor`).

**The decided design (operator-confirmed, to be recorded in `call/0036`):**

1. **Per-run pin-binding.** The run path resolves the verifier only from a version-stamped install
   keyed to the embedded pin, with an install-time SHA marker that must match the embedded pin; absent,
   mismatched, or unverifiable resolves to a distinct **BLOCKED** verdict at exit 2 that names
   `host-prove install <tool>`. No pass or fail issues from an unbound verifier. A PATH binary of
   unverifiable provenance counts as not-pinned.
2. **Hard split, fail closed.** The run and parse path is pure-local (it works under `--network none`
   and air-gapped) and never installs. `host-prove install <tool>` is the sole verb that fetches,
   SHA-verifies, and installs, into a version-stamped directory; a CI provisioning lane runs it.
3. **Update-safe.** The version-stamped directory is keyed to the embedded pinned version, so a pin
   bump cannot be silently ignored: the next run resolves to a path that does not exist and reports
   BLOCKED, so the operator runs install and learns the pin moved.
4. **Provenance and doctor.** A PASS verdict carries the resolved tool version and its pin-bound
   marker, so a glance or a cold read confirms the pinned tool produced it; `host-prove doctor` prints
   each declared verifier's installed version and pin status without running a proof.

This updates the network-aspects section above: auto-install is not a run-path side effect.
Installation is a separate, explicit, network-touching verb, and the run path is pure-local and fail
closed, so a sandbox cannot be surprised and an air-gapped host degrades to BLOCKED rather than a
silent or surprising failure.

## Status

In progress. The soundness fixes (the false-passes and the bound integrity) and the discharge dogfood
(`NonPassHasNoBound` asserts bound-absence, `exercises=` links, `--strict-discharge` in CI) are landed
at host-prove `f4736e9`: 19 unit tests, 9 fixtures, clippy, and strict discharge of 27 obligations all
green. The cast consultation is complete and the install design is decided and
recorded above. The remaining work (the fail-closed resolver and the `host-prove install` and
`host-prove doctor` verbs, retiring `install/*.sh`, re-capturing the apalache fixtures from the pinned
version, the kani skill-guide fix, `call/0036`, the broader cast review and the qwen3.5-4b probe, and
the release) is the next step.

# plan/0048: a declared rung's re-deriver must be runnable, and its digest earned

A host-lint `src/lib.rs` change stales the kani obligation digests, and the tag is born red on the
obligations staleness lint while the proof itself is fine. This kept recurring, and the standing
workaround was to hand-edit the digest ledger. This milestone traces that to its root, which is not
a release-tooling decision at all, and fixes it as a methodology migration rather than a patch to one
host.

## How the scope arrived here

The milestone opened as a release-time guard: should `host-lifecycle release` block, auto-record, or
attest when it finds a stale digest. Driving the real qwen3.5-4b cold (no leading framing) showed the
weak agent cannot reason about the underlying soundness, conflating "recompute the fingerprint" with
"re-run the proof," so a preference poll on that guard was the wrong instrument. Consulting the cast
reframed it: the fingerprint is a proxy for "is the proof current," and the born-red exists because
the proxy is refreshed by hand, no longer tied to the proof it claims to track. The principle the cast
settled on: a cheap proxy may stand in for an expensive check only while it stays mechanically
coupled to it, refreshed by the thing that runs the real proof and by nothing else.

Asking why the coupled path was abandoned uncovered the actual defect. The sanctioned
`host-lifecycle obligations <spec> --rederive --record-digests` re-runs the proof through host-prove
and records the digest only on a pass. It had been recorded in memory as failing with `ENOENT` on
the `/mnt/c` WSL mount, a host-prove invocation gap blamed on the filesystem. That diagnosis was
wrong. The proof runs fine on `/mnt/c`. The real causes were that **host-prove was never installed on
PATH** by the local setup (host-lint's CI installs it; the fresh-clone discipline never did), and that
it was handed `src/` rather than the crate root. Once host-prove is installed and pointed at the
crate root, the full chain re-derives both rungs and exits clean, locally, on `/mnt/c`.

So the re-deriver was referenced and materialized, its CI lane present, and yet not runnable on the
box that needed it. It was available but never discharged, the very `call/0018` distinction, turned
on the re-deriver itself. Nobody noticed for two weeks because the kani proof is verified by another
path (CI runs `cargo kani` directly and re-derives there), so the local re-derivation's brokenness was
invisible, and a `command not found` reads as a filesystem fault, so it was filed as a WSL problem and
never re-opened.

## The decision: express it as a migration, not a host fix

A one-off `cargo install host-prove` in this host's setup would re-bury the gap for the next adopter.
The fix generalizes an invariant the spine already has. The spine enforces "declare a deeper rung,
oblige its lane": `software --check` HAZARDs a `kani:`/`apalache:`/`tlaps:` obligation with no matching
CI workflow. But "the workflow is present in CI config" is weaker than "the re-derivation actually
runs," and the gap between them is exactly where this hid. The migration is one clause longer:

> A declared rung obliges its lane to be runnable, not merely present. Re-derivation that cannot run
> is not discharged. Available is not present-in-CI is not runnable is not discharged.

## The validated design (Fen, hard evidence, non-leading)

Two questions were put to the real qwen3.5-4b with neutral framing, after an earlier leading round was
discarded.

A check that the re-deriver resolves on PATH falls short on its own. Asked cold whether a gate
that confirms the tool is on PATH could still pass while the verification does not work, six of eight
runs said yes, naming version mismatch, wrong arguments, missing dependencies, and a stand-in
executable that returns success. So a PATH probe alone is recognized as too weak even at the
weak-agent bar.

Asked which check best ensures the claim is real, given the gate must stay cheap, eight of eight runs
chose a recorded result showing the proof was run on the current code and passed, over both an
on-PATH check and a one-off smoke run. That recorded-pass-on-current-code is the digest ledger earned
by a passing re-derivation, with the staleness check guaranteeing it is current. The weak agent
reconstructed `call/0018` from first principles.

So the gate does not gain a PATH probe. It gains two coupled things:
- A **runnability** check that the re-deriver **executes** (a cheap version probe), not merely
  resolves, since on-PATH is not works.
- The digest stays **earned**: recorded only by `--rederive --record-digests` (now runnable), never
  hand-edited, so the existing staleness check soundly means a passing re-derivation on the current
  code.

## The fix

### host-lifecycle

`software --check`, for a materialized component that declares a deeper rung, probes that the rung's
re-deriver executes (host-prove runs, the verifier is reachable) and HAZARDs when it cannot, beside
the existing "no CI lane" HAZARD. The probe is cheap and never runs the proof; the real re-derivation
stays the pluggable `call/0018` enforcement.

### host-template doctrine and the ledger

The "Mandatory when used" and `call/0018` text widens the "obliges its CI lane" rule into "obliges a
runnable lane driver," with the available-is-not-runnable-is-not-discharged line and the
earn-the-digest rule (discharge through `--rederive --record-digests`, never a hand edit). One
independent, version-gated `UPGRADING` entry carries it; every adopter who upgrades gets the
runnability gate, so the first time their own declared rung is not runnable, the gate says so.

### agentic-host adopts it

Like any adopter: record the ledger entry, install host-prove in the fresh-clone setup and in the CI
that runs `software --check`, and the gate goes green by being runnable. The CLAUDE.md setup line is
the project-local instance of the spine rule, not the fix.

### the record is corrected

The WSL-ENOENT entries in MEMORY were a misdiagnosis and are struck with a correcting entry: the
re-derivation runs on `/mnt/c`; the causes were host-prove not on PATH and the wrong directory. This
stays local, since it is this host's own record, not methodology.

## Build sequence

### Diagnose, audit, and decide {#diagnose-audit}

Reproduce the false ENOENT, prove the local re-derivation runs once host-prove is on PATH and pointed
at the crate root, audit the missed install step and the misdiagnosis, and settle the migration shape
with the cast.

- verify: attested operator

### Validate the gate strictness with Fen {#validate-strictness}

Put the gate check to the real qwen3.5-4b with neutral framing: a PATH probe is insufficient (six of
eight), a recorded pass on the current code is best (eight of eight). The gate checks runnability that
executes plus an earned, current digest.

- depends: #diagnose-audit
- verify: attested operator

### The runnability gate in host-lifecycle {#runnability-gate}

`software --check` probes that a declared rung's re-deriver executes and HAZARDs when it cannot. Unit
tests cover a declared rung with a runnable driver, with a missing driver, and with no declared rung.

- depends: #validate-strictness
- verify: cd software/host-lifecycle/main && cargo test

### Spine doctrine, ledger, and release {#spine-and-release}

Generalize the host-template doctrine and add the independent, version-gated `UPGRADING` entry. Release
host-lifecycle, re-pin `.host-software`, advance the host-template pointer so the entry is PENDING, and
correct the memory. The migration is now built and published; adopting it on this host is its own step.

- depends: #runnability-gate
- verify: attested operator

### agentic-host adopts the entry {#adopt}

On the operator's trigger, "Read and follow https://github.com/connollydavid/host to keep this
repository an agentic project," adopt like any project: record the ledger entry, install host-prove in
the fresh-clone setup and the CI that runs `software --check`, bump the CI host-lifecycle pins, and
confirm the whole suite is green. The gate goes green by being runnable.

- depends: #spine-and-release
- verify: attested operator

## Risks

- The runnability probe runs in every `software --check`, including CI, so the CI that runs the gate
  must install the re-deriver. That install is part of the adoption, and its absence is precisely the
  HAZARD the migration adds.
- A probe that the re-deriver executes is stronger than on-PATH but still not a proof that the rung
  passes; the earned digest and the pluggable re-derivation carry that, as `call/0018` intends.

## Status

migration built and released; adoption awaits the operator trigger. The runnability gate ships in
host-lifecycle v0.31.0 (`software --check` HAZARDs a declared rung whose re-deriver does not execute).
The spine doctrine and the version-gated `UPGRADING` entry `6174996` ("a re-deriver that runs") are
pushed; `.host-software` is re-pinned to v0.31.0 and the host-template pointer is advanced, so the
entry reads PENDING here. The memory misdiagnosis is corrected. The remaining `#adopt` step (record
the entry, install host-prove in setup and CI, bump the CI pins) runs on the operator's trigger,
"Read and follow https://github.com/connollydavid/host to keep this repository an agentic project."

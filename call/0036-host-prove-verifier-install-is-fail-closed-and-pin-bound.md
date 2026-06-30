# host-prove installs verifiers as a separate fail-closed verb, and binds every verdict to the embedded pin

- Status: accepted
- Date: 2026-06-30
- Scope: the `host-prove` lane driver (plan/0054). Instance software, binds no adopter, no spine
  change. Decides how the deep-verification verifiers (Kani, Apalache, TLAPS) are installed and how a
  run binds to them. Supersedes the earlier within-plan choice of auto-install on demand.
- Relates: `call/0018` (discharge is the verifier passing on re-derivation, so a verdict must come
  from the pinned verifier); `call/0033` and `call/0034` (host-reference's out-of-process plugins, the
  prior art for an arms-length, install-on-enable helper); `call/0031` (the no-reach-out rule);
  `plan/0052` and `[[no-hollow-green-doctrine]]` (a lane that cannot perform its check must not report
  clean).

## Context and Problem Statement

host-prove runs one verifier and settles to one machine-matchable verdict that maps to an exit code;
downstream the verdict is trusted as the discharge of a deep-verification obligation. The verifiers are
heavy third-party tools pinned by version and SHA256 in `tools.lock`. plan/0054 set out to make them
on-demand, tool-carried plugins modeled on the host-reference helpers, and an earlier within-plan
choice was auto-install on demand: an absent verifier would be fetched, verified, installed, and run in
one command.

The operator raised three worries about that choice: silent failures, updates, and sandbox
restrictions. A cast consultation (all five personas) found the auto-install default unsafe and located
the true defect. The first resolver reused whatever verifier was installed or on PATH without checking
its version against the embedded pin, so after a pin bump a host would keep using the old verifier and
still emit a clean pass: a wrong-version verdict with no signal, exactly the hollow green host-prove
exists to prevent, in host-prove itself. Auto-install also made a run reach the network and write to
the filesystem as a side effect, which a sandbox, a hermetic build, or an air-gapped host blocks, so a
routine run would surprise those environments and fail at run time.

## Decision

- **A verdict binds to the embedded pin, every run.** The run path resolves a verifier only from a
  version-stamped install keyed to the pin embedded in the host-prove binary, with an install-time
  SHA256 marker that must equal the embedded pin. An absent, wrong-version, or unverifiable verifier
  resolves to a distinct `BLOCKED` verdict at exit 2 that names the next command, `host-prove install
  <tool>`. A verifier not bound to the pin issues neither a pass nor a fail. A binary found on PATH
  whose provenance cannot be bound to the pin counts as not-pinned. This is the no-hollow-green doctrine
  applied to the re-deriver: a lane that cannot prove it ran the pinned verifier reports a precondition
  failure, never a result.
- **Installation is a separate, explicit, fail-closed verb.** `host-prove install <tool>` is the only
  path that touches the network or the filesystem: it fetches the pinned asset, verifies its SHA256
  before extracting or executing it, and installs into a version-stamped directory. The run and parse
  path is pure-local and never installs, so it works under a hermetic build, a sandbox, or an
  air-gapped host. A CI provisioning lane runs the install verb deliberately, ahead of the prove step.
  Auto-install on demand is dropped: re-install is always an explicit operator act, because the host
  may be air-gapped and the operator must learn that the pin moved.
- **Updates are safe by construction.** The version-stamped directory is keyed to the embedded pinned
  version, so a pin bump moves the lookup path. The old version is never glanced at; the next run
  resolves to a path that does not exist, reports `BLOCKED`, and the operator runs install.
- **A verdict carries its provenance, and `host-prove doctor` reports it.** A PASS verdict carries the
  resolved tool version and its pin-bound marker, so a single glance or a later cold read confirms the
  pinned tool produced it. `host-prove doctor` prints each declared verifier's installed version and
  pin status without running a proof, the cheap check the human operator needs.

## Consequences

- The shell installers (`install/*.sh`, `_common.sh`) retire in favour of the in-process `host-prove
  install` verb, so the orchestration lives in one fail-closed process rather than a shell wrapper.
- A run is reproducible in its verdict and pure-local; the network reach is confined to the explicit
  install verb. The `cargo kani setup` backend remains an unpinned fetch (a documented residual on the
  kani plugin), the one provenance edge the SHA pin does not cover.
- The weak agent gets one tool-driven command at a time: a run that names `host-prove install <tool>`
  when blocked is the tool carrying the process, not a hidden side effect. The design is gated on a
  real qwen3.5-4b probe before release, as a doctrine-grade change requires.

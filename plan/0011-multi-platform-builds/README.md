# Per-platform builds in the software recipe

`connollydavid/host#1`: a single component, built from one source `pin`, can
ship on several platforms — e.g. a CUDA server built once for `linux-cuda` and
once for `windows-msvc-cuda` from the same commit. The flat `.host-software`
build fields (`build`/`toolchain`/`artifact`/`deploy`/`repro-exempt`) recorded
exactly **one** build per component, so a second platform had nowhere to live.
The workarounds — a fake second component, or overloading `worktree =` — both
break the one-pin audit anchor.

## What shipped (host-lifecycle v0.9.0)

A per-platform build subsection, nested under the component stanza:

```
[software "ik"]
	url = https://example.test/ik.git
	pin = abc123…
[build "ik" "linux-cuda"]
	toolchain   = nvidia/cuda:12.4@sha256:…
	build       = cmake --preset cuda
	artifact    = build/bin/srv <sha256>
	deploy      = ik
	attest-host = linux
[build "ik" "windows-msvc-cuda"]
	toolchain   = …
	build       = cmake --preset msvc
	artifact    = build/bin/srv.exe <sha256>
	attest-host = windows
	repro-exempt = call/NNNN
```

- Each `[build "<name>" "<platform>"]` shares the component's `url`+`pin` and
  carries its own `build`/`toolchain`/`artifact`/`deploy`/`repro-exempt`.
- **`attest-host`** names the OS (`std::env::consts::OS`: `linux`/`windows`/
  `macos`) that reproduces this build. `software --check` and `--verify-build`
  iterate the builds and attest each only on its `attest-host`; a build whose
  host is not the current one is **skipped, not failed** — the way an exempt
  build is skipped. A Linux runner cannot reproduce the Windows artifact and is
  not asked to.
- **`repro-exempt` is per-build**, not per-component: one platform may be proven
  reproducible while another carries a case-decision exemption.
- The flat single-build form is preserved as the default build (it becomes one
  `builds_view` entry with no `attest-host`, attesting on any host — the
  pre-issue-#1 behaviour). Single-platform components need no change.
- The Where stub (`host-lifecycle book`) lists a component's platforms.

## Spine change

The `.host-software` schema is methodology, so the design is recorded in the
template spine, not as an agentic-host `call/` (an accepted methodology-scoped
decision fails the anti-ouroboros `validate` gate — see `call/0004`). The
template carries it as prose in `STRUCTURE.md` + `CLAUDE.md` and as an
`UPGRADING.md` ledger entry keyed to template `c137567`, requiring
host-lifecycle v0.9.0. This mirrors how `plan/0005` (the reproducible-build
anchor) recorded its spine change.

## Deferred

Automated cross-OS worktree **materialization** (checking out a Windows tree
from a bare store on an ext4 host, and vice versa) is out of scope for this cut.
The recipe records each platform build; a human materializes the foreign-OS
worktree and runs `--verify-build` there. The skip-on-foreign-host behaviour is
exactly what lets each host attest only what it can build.

## Verification

- host-lifecycle unit tests (35, +2): `parses_platform_builds` (two subsections
  parse, flat fields stay empty, `builds_view` yields both);
  `foreign_platform_build_is_skipped_not_failed` (a build pinned to a non-runner
  OS with a wrong hash and absent artifact yields **0** provenance failures).
- Back-compat: the existing flat-form tests (`parses_build_provenance`,
  `provenance_attestation_and_exemption`, `install_hooks…`) pass unchanged.

## Not done here

agentic-host's own `.host-software` ships only single-platform `host-lint`, so
it gains no `[build …]` section and is not re-pinned. CI installs host-lifecycle
by rev; the change is back-compatible, so those pins are unchanged (bumping them
is an optional follow-up).
